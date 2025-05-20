# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python SDK for interacting with Claude Code, Anthropic's AI-powered coding assistant. It provides a Python wrapper around the Claude Code CLI, allowing developers to use Claude Code directly from Python applications with features like:

- One-shot prompts
- Multi-turn conversations
- Streaming responses
- JSON formatted outputs
- Cloud provider integration (AWS Bedrock, Google Vertex AI)

## Architecture

The SDK follows a client-based architecture:

- `ClaudeCode` (in `client.py`): Main client interface with configuration options
- `Conversation` (in `conversation.py`): Manages multi-turn conversations
- `AuthProvider` (in `auth/provider.py`): Handles authentication across different providers
- `utils/subprocess.py`: Manages command execution and streaming

The main workflow runs CLI commands via subprocess and manages their execution, passing authentication details through environment variables.

## Development Commands

### Setup and Installation

```bash
# Install package in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov black ruff mypy
```

### Testing

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/unit/test_client.py

# Run a specific test function
pytest tests/unit/test_client.py::TestClient::test_run_prompt

# Run tests with coverage
pytest --cov
```

### Code Quality

```bash
# Format code with black
black claude_code tests examples

# Run linting with ruff
ruff check claude_code tests examples

# Run type checking with mypy
mypy claude_code
```

### Building and Publishing

```bash
# Build distribution packages
python -m build

# Test installation from local files
pip install dist/claude_code_sdk-*.whl
```

## Key Concepts

1. **Authentication Methods**: The SDK supports three authentication methods:
   - Direct Anthropic API key
   - AWS Bedrock
   - Google Vertex AI

2. **Conversation Management**: The SDK manages conversation state, allowing for multi-turn interactions while maintaining context.

3. **Response Formats**: Supports text, JSON, and streaming outputs.

4. **Tool Configuration**: Allows configuration of which Claude Code tools are allowed or disallowed.

## Prerequisites

- Python 3.8 or higher
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)

## Common Usage Patterns

### Basic Usage

```python
from claude_code import ClaudeCode

# Initialize with Anthropic API key
claude = ClaudeCode(api_key="your-api-key")

# Run a single prompt
result = claude.run_prompt("Explain how this project works")
print(result)
```

### Tool Configuration

```python
from claude_code import ClaudeCode

claude = ClaudeCode(api_key="your-api-key")

# Configure allowed tools
claude.configure(
    allowed_tools=["Bash(git:*)", "View", "GlobTool", "GrepTool"],
    max_turns=5
)
```

### Error Handling

```python
from claude_code import ClaudeCode
from claude_code.exceptions import (
    ClaudeCodeError,
    AuthenticationError,
    ExecutionError,
    TimeoutError,
    ValidationError
)

try:
    response = claude.run_prompt("Some prompt")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except TimeoutError as e:
    print(f"Request timed out: {e}")
except ValidationError as e:
    print(f"Invalid input: {e}")
except ExecutionError as e:
    print(f"Execution failed: {e}")
except ClaudeCodeError as e:
    print(f"An error occurred: {e}")
```