# ClaudeCode Class

The `ClaudeCode` class is the main entry point for interacting with Claude Code CLI from Python.

## Initialization

```python
from claude_code import ClaudeCode, AuthType

# With Anthropic API
claude = ClaudeCode(
    auth_type=AuthType.ANTHROPIC_API,
    api_key="your-api-key",
    allowed_tools=["Bash", "Glob"],
    max_turns=5,
    timeout=60
)

# With AWS Bedrock
claude = ClaudeCode(
    auth_type=AuthType.AWS_BEDROCK,
    region="us-west-2",
    model="anthropic.claude-3-7-sonnet-20250219-v1:0"
)

# With Google Vertex AI
claude = ClaudeCode(
    auth_type=AuthType.GOOGLE_VERTEX,
    region="us-central1",
    project_id="your-project-id",
    model="claude-3-7-sonnet@20250219"
)
```

## Constructor Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `auth_type` | `AuthType` | Authentication type to use | `AuthType.ANTHROPIC_API` |
| `api_key` | `str` | Anthropic API key (required for `ANTHROPIC_API` auth type) | `None` |
| `region` | `str` | AWS region or Cloud ML region (required for `AWS_BEDROCK` and `GOOGLE_VERTEX`) | `None` |
| `project_id` | `str` | Google Cloud project ID (required for `GOOGLE_VERTEX`) | `None` |
| `model` | `str` | Model ID in provider-specific format | `None` |
| `allowed_tools` | `List[str]` | List of tools to allow | `None` |
| `disallowed_tools` | `List[str]` | List of tools to disallow | `None` |
| `max_turns` | `int` | Maximum number of turns in a conversation | `None` |
| `mcp_config` | `str` | Path to MCP configuration JSON file | `None` |
| `timeout` | `int` | Timeout in seconds | `None` |

## Methods

### `configure`

Updates the configuration of the Claude Code client.

```python
claude.configure(
    allowed_tools=["Bash", "Glob"],
    max_turns=5,
    timeout=60,
    model="new-model"
)
```

#### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `allowed_tools` | `List[str]` | List of tools to allow | `None` |
| `disallowed_tools` | `List[str]` | List of tools to disallow | `None` |
| `max_turns` | `int` | Maximum number of turns in a conversation | `None` |
| `mcp_config` | `str` | Path to MCP configuration JSON file | `None` |
| `timeout` | `int` | Timeout in seconds | `None` |
| `model` | `str` | Model ID in provider-specific format | `None` |

#### Returns

None

### `load_mcp_config`

Loads MCP configuration from a JSON file.

```python
claude.load_mcp_config("/path/to/mcp-config.json")
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `config_path` | `str` | Path to the MCP configuration JSON file |

#### Returns

None

#### Raises

- `ValidationError`: If the file doesn't exist, contains invalid JSON, or has an invalid structure

### `run_prompt`

Runs a one-shot prompt with Claude Code.

```python
# With text output
result = claude.run_prompt("Explain how git works")

# With JSON output
json_result = claude.run_prompt(
    "Analyze this code",
    output_format=OutputFormat.JSON
)
```

#### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `prompt` | `str` | The prompt to send to Claude Code | (required) |
| `output_format` | `OutputFormat` | Output format for the response | `OutputFormat.TEXT` |

#### Returns

- `str`: When `output_format` is `OutputFormat.TEXT`
- `Dict`: When `output_format` is `OutputFormat.JSON`

#### Raises

- `ValidationError`: If input validation fails
- `ExecutionError`: If there's an error running Claude Code
- `TimeoutError`: If Claude Code times out

### `stream_prompt`

Streams a one-shot prompt with Claude Code.

```python
# Stream text
for chunk in claude.stream_prompt("Create a function"):
    print(chunk, end="")

# Stream JSON
for json_chunk in claude.stream_prompt(
    "Analyze this code",
    output_format=OutputFormat.STREAM_JSON
):
    print(json_chunk["content"], end="")
```

#### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `prompt` | `str` | The prompt to send to Claude Code | (required) |
| `output_format` | `OutputFormat` | Output format for the response | `OutputFormat.TEXT` |

#### Returns

- `Iterator[str]`: When `output_format` is `OutputFormat.TEXT`
- `Iterator[Dict]`: When `output_format` is `OutputFormat.STREAM_JSON`

#### Raises

- `ValidationError`: If input validation fails
- `ExecutionError`: If there's an error running Claude Code
- `TimeoutError`: If Claude Code times out

### `start_conversation`

Starts a new conversation with Claude Code.

```python
conversation = claude.start_conversation(
    allowed_tools=["Bash", "Glob"],
    max_turns=5,
    timeout=60
)

response1 = conversation.send("Create a function")
response2 = conversation.send("Add error handling")
```

#### Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `conversation_id` | `str` | ID for the conversation | auto-generated |
| `allowed_tools` | `List[str]` | List of tools to allow (overrides client config) | `None` |
| `disallowed_tools` | `List[str]` | List of tools to disallow (overrides client config) | `None` |
| `max_turns` | `int` | Maximum number of turns (overrides client config) | `None` |
| `mcp_config` | `str` | Path to MCP configuration JSON file (overrides client config) | `None` |
| `model` | `str` | Model ID in provider-specific format (overrides client config) | `None` |
| `timeout` | `int` | Timeout in seconds (overrides client config) | `None` |
| `output_format` | `OutputFormat` | Output format for responses | `OutputFormat.TEXT` |

#### Returns

- `Conversation`: A new Conversation instance