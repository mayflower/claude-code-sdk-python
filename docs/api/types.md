# Types and Enums

The Claude Code SDK includes several types and enums to help with type safety and clarity.

## OutputFormat Enum

The `OutputFormat` enum defines the available output formats for Claude Code responses:

```python
from claude_code import OutputFormat

# Plain text output
output_format = OutputFormat.TEXT

# JSON output
output_format = OutputFormat.JSON

# Streaming JSON output
output_format = OutputFormat.STREAM_JSON
```

### Usage

```python
from claude_code import ClaudeCode, OutputFormat

claude = ClaudeCode(api_key="your-api-key")

# Get JSON response
json_result = claude.run_prompt(
    "Analyze this code",
    output_format=OutputFormat.JSON
)

# Stream JSON response
for json_chunk in claude.stream_prompt(
    "Analyze this code",
    output_format=OutputFormat.STREAM_JSON
):
    print(json_chunk)
```

## ToolConfig Class

The `ToolConfig` class provides utility methods for working with Claude Code tools:

```python
from claude_code.types import ToolConfig

# Format a list of tools for the Claude Code CLI
tools = ["Bash", "Glob", "Grep"]
formatted = ToolConfig.format_allowed_tools(tools)
# formatted = "Bash,Glob,Grep"

# Parse a tool string from the Claude Code CLI
tool_str = "Bash,Glob,Grep"
parsed = ToolConfig.parse_tool_string(tool_str)
# parsed = ["Bash", "Glob", "Grep"]
```

### Static Methods

#### `format_allowed_tools`

Formats a list of tools for the Claude Code CLI.

```python
@staticmethod
def format_allowed_tools(tools: List[str]) -> str:
    """Format allowed tools for Claude Code CLI."""
    return ",".join(tools)
```

#### `parse_tool_string`

Parses a tool string from the Claude Code CLI.

```python
@staticmethod
def parse_tool_string(tool_str: str) -> List[str]:
    """Parse tool string from Claude Code CLI."""
    return [t.strip() for t in tool_str.split(",") if t.strip()]
```