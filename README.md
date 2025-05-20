# Claude Code SDK for Python

A Python SDK for interacting with Claude Code, Anthropic's AI-powered coding assistant.

## Installation

```bash
pip install claude-code-sdk
```

## Requirements

- Python 3.8 or higher
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code`)

## Usage

### Basic Usage

```python
from claude_code import ClaudeCode

# Initialize with Anthropic API key
claude = ClaudeCode(api_key="your-api-key")

# Run a single prompt
result = claude.run_prompt("Explain how this project works")
print(result)

# Stream results
for chunk in claude.stream_prompt("Create a function to parse JSON"):
    print(chunk, end="")
```

### Multi-turn Conversations

```python
from claude_code import ClaudeCode

claude = ClaudeCode(api_key="your-api-key")

# Start a conversation
conversation = claude.start_conversation()

# Send multiple prompts in the same conversation
response1 = conversation.send("Create a Python class for a blog post")
print(response1)

response2 = conversation.send("Add methods for comments")
print(response2)
```

### Using with AWS Bedrock

```python
from claude_code import ClaudeCode, AuthType

# Initialize with AWS Bedrock
claude = ClaudeCode(
    auth_type=AuthType.AWS_BEDROCK,
    model="anthropic.claude-3-7-sonnet-20250219-v1:0",
    region="us-west-2"
)

# Now use it as normal
result = claude.run_prompt("Analyze this code")
```

### Using with Google Vertex AI

```python
from claude_code import ClaudeCode, AuthType

# Initialize with Google Vertex AI
claude = ClaudeCode(
    auth_type=AuthType.GOOGLE_VERTEX,
    model="claude-3-7-sonnet@20250219",
    project_id="your-project-id",
    region="us-central1"
)

# Now use it as normal
result = claude.run_prompt("Refactor this function")
```

### Configuring Tools

```python
from claude_code import ClaudeCode

claude = ClaudeCode(api_key="your-api-key")

# Configure allowed tools
claude.configure(
    allowed_tools=["Bash(git:*)", "View", "GlobTool", "GrepTool"],
    max_turns=5
)

# Run with tool access
result = claude.run_prompt("Find all Python files in this project")
```

## License

MIT

## Author

Johann-Peter Hartmann (johann-peter.hartmann@mayflower.de)