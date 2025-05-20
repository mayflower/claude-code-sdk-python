"""
Claude Code SDK - Python wrapper for Anthropic's Claude Code CLI.
"""

from .client import ClaudeCode
from .auth.types import AuthType
from .exceptions import (
    ClaudeCodeError,
    AuthenticationError,
    ExecutionError,
    TimeoutError,
    ValidationError,
)
from .types import OutputFormat

__version__ = "0.1.0"

__all__ = [
    "ClaudeCode",
    "AuthType",
    "OutputFormat",
    "ClaudeCodeError",
    "AuthenticationError",
    "ExecutionError",
    "TimeoutError",
    "ValidationError",
]