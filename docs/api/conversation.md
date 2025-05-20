# Conversation Class

The `Conversation` class manages a multi-turn conversation with Claude Code.

## Initialization

```python
from claude_code import ClaudeCode, OutputFormat

# Create a client
claude = ClaudeCode(api_key="your-api-key")

# Start a conversation using the client
conversation = claude.start_conversation(
    allowed_tools=["Bash", "Glob"],
    max_turns=5,
    timeout=60,
    output_format=OutputFormat.TEXT
)
```

> **Note**: You typically don't initialize the `Conversation` class directly. Instead, use the `start_conversation` method from a `ClaudeCode` client.

## Methods

### `send`

Sends a message to Claude Code and returns the response.

```python
response = conversation.send("Create a Python class for a blog post")
print(response)
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | `str` | Prompt message |

#### Returns

- `str`: Claude Code's response

#### Raises

- `ValidationError`: If input validation fails
- `ExecutionError`: If there's an error running Claude Code
- `TimeoutError`: If Claude Code times out

### `stream`

Sends a message to Claude Code and streams the response.

```python
for chunk in conversation.stream("Create a Python function"):
    print(chunk, end="")
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | `str` | Prompt message |

#### Returns

- `Iterator[str]`: Chunks of Claude Code's response

#### Raises

- `ValidationError`: If input validation fails
- `ExecutionError`: If there's an error running Claude Code
- `TimeoutError`: If Claude Code times out

### `stream_json`

Sends a message to Claude Code and streams the JSON response.

```python
for json_chunk in conversation.stream_json("Analyze this code"):
    if json_chunk["type"] == "content":
        print(json_chunk["content"], end="")
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | `str` | Prompt message |

#### Returns

- `Iterator[Dict]`: Parsed JSON objects from Claude Code's response

#### Raises

- `ValidationError`: If input validation fails or output format is not `STREAM_JSON`
- `ExecutionError`: If there's an error running Claude Code
- `TimeoutError`: If Claude Code times out

## Properties

### `turn_count`

The number of turns in the conversation.

```python
print(f"Conversation has {conversation.turn_count} turns")
```

### `conversation_id`

The unique identifier for the conversation.

```python
print(f"Conversation ID: {conversation.conversation_id}")
```

### `allowed_tools`

List of tools allowed in the conversation.

```python
print(f"Allowed tools: {conversation.allowed_tools}")
```

### `disallowed_tools`

List of tools disallowed in the conversation.

```python
print(f"Disallowed tools: {conversation.disallowed_tools}")
```

### `max_turns`

Maximum number of turns allowed in the conversation.

```python
print(f"Maximum turns: {conversation.max_turns}")
```

### `output_format`

Output format for responses.

```python
print(f"Output format: {conversation.output_format}")
```