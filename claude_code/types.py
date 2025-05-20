"""
Common types for Claude Code.
"""

from enum import Enum, auto
from typing import Dict, List, Optional, Union, Any


class OutputFormat(Enum):
    """Output format for Claude Code responses."""
    
    TEXT = "text"
    """Plain text output."""
    
    JSON = "json"
    """JSON output."""
    
    STREAM_JSON = "stream-json"
    """Streaming JSON output."""


class ToolConfig:
    """Configuration for Claude Code tools."""
    
    @staticmethod
    def format_allowed_tools(tools: List[str]) -> str:
        """Format allowed tools for Claude Code CLI."""
        return ",".join([t for t in tools if t])

    @staticmethod
    def parse_tool_string(tool_str: str) -> List[str]:
        """Parse tool string from Claude Code CLI."""
        return [t.strip() for t in tool_str.split(",") if t.strip()]