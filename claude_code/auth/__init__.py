"""
Authentication module for Claude Code.
"""

from .types import AuthType
from .provider import AuthProvider

__all__ = [
    "AuthType",
    "AuthProvider",
]