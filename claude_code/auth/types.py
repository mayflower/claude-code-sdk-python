"""
Authentication types for Claude Code.
"""

from enum import Enum, auto


class AuthType(Enum):
    """Authentication types for Claude Code."""
    
    ANTHROPIC_API = auto()
    """Authenticate using direct Anthropic API key."""
    
    AWS_BEDROCK = auto()
    """Authenticate using AWS Bedrock."""
    
    GOOGLE_VERTEX = auto()
    """Authenticate using Google Vertex AI."""