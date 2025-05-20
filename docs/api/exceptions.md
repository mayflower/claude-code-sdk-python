# Exceptions

The Claude Code SDK defines several exception classes to provide clear error handling.

## Exception Hierarchy

```
ClaudeCodeError
├── AuthenticationError
├── ValidationError
├── ExecutionError
│   └── TimeoutError
```

## ClaudeCodeError

Base exception for all Claude Code errors.

```python
from claude_code.exceptions import ClaudeCodeError

try:
    # Claude Code operation
except ClaudeCodeError as e:
    print(f"Claude Code error: {e}")
```

## AuthenticationError

Error occurred during authentication.

```python
from claude_code.exceptions import AuthenticationError

try:
    # Authentication operation
except AuthenticationError as e:
    print(f"Authentication error: {e}")
```

### Common causes

- Missing API key for `ANTHROPIC_API` auth type
- Missing region for `AWS_BEDROCK` auth type
- Missing region or project ID for `GOOGLE_VERTEX` auth type

## ValidationError

Error validating input parameters.

```python
from claude_code.exceptions import ValidationError

try:
    # Validation operation
except ValidationError as e:
    print(f"Validation error: {e}")
```

### Common causes

- Empty prompt
- Conflicting tool configuration (same tool in both allowed and disallowed tools)
- Invalid MCP configuration file
- Exceeding maximum turns in a conversation
- Wrong output format for streaming JSON

## ExecutionError

Error occurred during Claude Code execution.

```python
from claude_code.exceptions import ExecutionError

try:
    # Claude Code execution
except ExecutionError as e:
    print(f"Execution error: {e}")
    print(f"Exit code: {e.exit_code}")
    print(f"Stdout: {e.stdout}")
    print(f"Stderr: {e.stderr}")
```

### Properties

| Property | Description |
|----------|-------------|
| `exit_code` | Exit code from the Claude Code CLI |
| `stdout` | Standard output from the Claude Code CLI |
| `stderr` | Standard error from the Claude Code CLI |

### Common causes

- Claude Code CLI not installed
- Claude Code CLI command failed

## TimeoutError

Timeout occurred during Claude Code execution.

```python
from claude_code.exceptions import TimeoutError

try:
    # Claude Code execution with timeout
except TimeoutError as e:
    print(f"Timeout error: {e}")
    print(f"Partial stdout: {e.stdout}")
    print(f"Partial stderr: {e.stderr}")
```

### Properties

Inherits all properties from `ExecutionError`.

### Common causes

- Claude Code CLI operation took too long to complete