# Usage Examples

This page provides various examples of using the Claude Code SDK.

## Basic Examples

### Hello World

```python
from claude_code import ClaudeCode

claude = ClaudeCode(api_key="your-api-key")
result = claude.run_prompt("Say hello world")
print(result)
```

### Streaming Response

```python
from claude_code import ClaudeCode

claude = ClaudeCode(api_key="your-api-key")

for chunk in claude.stream_prompt("Generate a Python function that calculates Fibonacci numbers"):
    print(chunk, end="")
```

### Multi-Turn Conversation

```python
from claude_code import ClaudeCode

claude = ClaudeCode(api_key="your-api-key")
conversation = claude.start_conversation()

# First turn
response1 = conversation.send("Create a Python class for user management")
print("First response:")
print(response1)

# Second turn (follows up on first)
response2 = conversation.send("Add authentication methods to that class")
print("\nSecond response:")
print(response2)
```

## Authentication Examples

### Using Anthropic API Key from Environment

```python
import os
from claude_code import ClaudeCode

# Set the API key in the environment
os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

# ClaudeCode will pick up the API key from the environment
claude = ClaudeCode()
result = claude.run_prompt("Hello!")
print(result)
```

### Using AWS Bedrock

```python
from claude_code import ClaudeCode, AuthType

claude = ClaudeCode(
    auth_type=AuthType.AWS_BEDROCK,
    region="us-west-2",
    model="anthropic.claude-3-7-sonnet-20250219-v1:0"
)

result = claude.run_prompt("What model are you using?")
print(result)
```

### Using Google Vertex AI

```python
from claude_code import ClaudeCode, AuthType

claude = ClaudeCode(
    auth_type=AuthType.GOOGLE_VERTEX,
    region="us-central1",
    project_id="your-project-id",
    model="claude-3-7-sonnet@20250219"
)

result = claude.run_prompt("What model are you using?")
print(result)
```

## Advanced Examples

### Working with JSON Output

```python
from claude_code import ClaudeCode, OutputFormat

claude = ClaudeCode(api_key="your-api-key")

# Get a structured JSON response
json_result = claude.run_prompt(
    "Analyze this code snippet and return metrics as JSON:\n\n```python\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)\n```",
    output_format=OutputFormat.JSON
)

print(f"Function name: {json_result['function_name']}")
print(f"Complexity: {json_result['complexity']}")
print(f"Issues found: {len(json_result['issues'])}")
```

### Streaming JSON

```python
from claude_code import ClaudeCode, OutputFormat

claude = ClaudeCode(api_key="your-api-key")

# Stream JSON responses
for json_chunk in claude.stream_prompt(
    "Generate a step-by-step guide to refactoring this code",
    output_format=OutputFormat.STREAM_JSON
):
    if json_chunk.get("type") == "step":
        print(f"Step {json_chunk['step_number']}: {json_chunk['description']}")
```

### Tool Configuration

```python
from claude_code import ClaudeCode

claude = ClaudeCode(
    api_key="your-api-key",
    allowed_tools=["Bash(git:*)", "GlobTool", "GrepTool"]
)

# Ask Claude to use git
result = claude.run_prompt("List all commits in this repository")
print(result)

# Reconfigure with different tools
claude.configure(
    allowed_tools=["Bash(ls,cat)", "GlobTool"],
    disallowed_tools=["GrepTool"]
)

# Ask Claude to list files but not search content
result = claude.run_prompt("List all Python files in this project")
print(result)
```

### Using MCP (Model Context Protocol)

```python
import json
import tempfile
from claude_code import ClaudeCode

# Create a temporary MCP config file
mcp_config = {
    "mcpServers": {
        "custom-tool": {
            "command": "node",
            "args": ["./tool-server.js"],
            "env": {
                "PORT": "3000"
            }
        }
    }
}

# Write the config to a temporary file
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
    json.dump(mcp_config, f)
    config_path = f.name

# Create the client with the MCP config
claude = ClaudeCode(
    api_key="your-api-key",
    mcp_config=config_path
)

# Allow the custom tool
claude.configure(allowed_tools=["mcp__custom-tool__analyze"])

# Use the custom tool
result = claude.run_prompt("Use the custom tool to analyze my project")
print(result)
```

### Handling Exceptions

```python
from claude_code import ClaudeCode
from claude_code.exceptions import (
    AuthenticationError,
    ValidationError,
    ExecutionError,
    TimeoutError
)

claude = ClaudeCode(api_key="your-api-key")

try:
    result = claude.run_prompt("Hello", timeout=5)
    print(result)
except AuthenticationError as e:
    print(f"Authentication error: {e}")
except ValidationError as e:
    print(f"Validation error: {e}")
except TimeoutError as e:
    print(f"Timeout error after {e.timeout} seconds")
    print(f"Partial output: {e.stdout}")
except ExecutionError as e:
    print(f"Execution error (code {e.exit_code}): {e}")
    print(f"Error details: {e.stderr}")
```