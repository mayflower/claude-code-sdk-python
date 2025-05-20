"""
Tests for the types module.
"""

import pytest

from claude_code.types import OutputFormat, ToolConfig


class TestOutputFormat:
    """Tests for the OutputFormat enum."""

    def test_values(self):
        """Test OutputFormat enum values."""
        assert OutputFormat.TEXT.value == "text"
        assert OutputFormat.JSON.value == "json"
        assert OutputFormat.STREAM_JSON.value == "stream-json"


class TestToolConfig:
    """Tests for the ToolConfig class."""

    def test_format_allowed_tools(self):
        """Test formatting allowed tools."""
        tools = ["Bash", "Glob", "Grep"]
        formatted = ToolConfig.format_allowed_tools(tools)
        assert formatted == "Bash,Glob,Grep"
        
        # Test empty list
        assert ToolConfig.format_allowed_tools([]) == ""
        
        # Test list with empty strings (should be ignored)
        assert ToolConfig.format_allowed_tools(["Bash", "", "Grep"]) == "Bash,Grep"

    def test_parse_tool_string(self):
        """Test parsing tool string."""
        tool_str = "Bash,Glob,Grep"
        parsed = ToolConfig.parse_tool_string(tool_str)
        assert parsed == ["Bash", "Glob", "Grep"]
        
        # Test with spaces
        assert ToolConfig.parse_tool_string("Bash, Glob, Grep") == ["Bash", "Glob", "Grep"]
        
        # Test empty string
        assert ToolConfig.parse_tool_string("") == []
        
        # Test string with empty items
        assert ToolConfig.parse_tool_string("Bash,,Grep") == ["Bash", "Grep"]