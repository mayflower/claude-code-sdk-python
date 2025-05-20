# API Reference

This section provides detailed documentation for the Claude Code SDK API.

## Core Classes

- [ClaudeCode](client.md): Main client class for interacting with Claude Code.
- [Conversation](conversation.md): Class for managing multi-turn conversations.

## Authentication

- [Auth Types and Providers](auth.md): Documentation for authentication options.

## Types and Utilities

- [Types and Enums](types.md): Documentation for types and enums.
- [Exceptions](exceptions.md): Documentation for exception classes.

## Module Structure

The Claude Code SDK is organized into the following modules:

```
claude_code/
├── __init__.py          # Package exports
├── client.py            # ClaudeCode class
├── conversation.py      # Conversation class
├── types.py             # Common types
├── auth/                # Authentication
│   ├── __init__.py
│   ├── provider.py      # AuthProvider class
│   └── types.py         # AuthType enum
├── exceptions/          # Exception classes
│   └── __init__.py
└── utils/               # Utility functions
    ├── __init__.py
    └── subprocess.py    # Subprocess utilities
```

## Complete Import Example

```python
from claude_code import (
    # Main classes
    ClaudeCode,
    
    # Enums
    AuthType,
    OutputFormat,
    
    # Exceptions
    ClaudeCodeError,
    AuthenticationError,
    ValidationError,
    ExecutionError,
    TimeoutError,
)
```