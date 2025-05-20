"""
Tests for the ClaudeCode client.
"""

import json
import pytest
from unittest.mock import patch, call, MagicMock

from claude_code import ClaudeCode, AuthType, OutputFormat
from claude_code.exceptions import ValidationError, ExecutionError


class TestClaudeCode:
    """Tests for the ClaudeCode class."""

    def test_initialization(self):
        """Test client initialization."""
        client = ClaudeCode(
            auth_type=AuthType.ANTHROPIC_API,
            api_key="test-api-key",
            allowed_tools=["Bash", "Glob"],
            max_turns=5,
            timeout=60
        )
        
        assert client.auth_provider.auth_type == AuthType.ANTHROPIC_API
        assert client.auth_provider.api_key == "test-api-key"
        assert client.allowed_tools == ["Bash", "Glob"]
        assert client.max_turns == 5
        assert client.timeout == 60

    def test_validation_conflicting_tools(self):
        """Test validation for conflicting tool configuration."""
        with pytest.raises(ValidationError):
            ClaudeCode(
                auth_type=AuthType.ANTHROPIC_API,
                api_key="test-api-key",
                allowed_tools=["Bash", "Glob"],
                disallowed_tools=["Bash"]
            )

    def test_configure(self):
        """Test configuration updates."""
        client = ClaudeCode(
            auth_type=AuthType.ANTHROPIC_API,
            api_key="test-api-key"
        )
        
        client.configure(
            allowed_tools=["Bash", "Glob"],
            max_turns=5,
            timeout=60,
            model="new-model"
        )
        
        assert client.allowed_tools == ["Bash", "Glob"]
        assert client.max_turns == 5
        assert client.timeout == 60
        assert client.auth_provider.model == "new-model"

    def test_load_mcp_config(self, tmp_path):
        """Test loading MCP configuration."""
        # Create temporary MCP config file
        config_file = tmp_path / "mcp-config.json"
        config_file.write_text(json.dumps({
            "mcpServers": {
                "test-server": {
                    "command": "node",
                    "args": ["server.js"]
                }
            }
        }))
        
        client = ClaudeCode(
            auth_type=AuthType.ANTHROPIC_API,
            api_key="test-api-key"
        )
        
        client.load_mcp_config(str(config_file))
        assert client.mcp_config == str(config_file)

    def test_load_mcp_config_invalid_path(self):
        """Test loading MCP configuration with invalid path."""
        client = ClaudeCode(
            auth_type=AuthType.ANTHROPIC_API,
            api_key="test-api-key"
        )
        
        with pytest.raises(ValidationError):
            client.load_mcp_config("/nonexistent/path.json")

    def test_load_mcp_config_invalid_json(self, tmp_path):
        """Test loading MCP configuration with invalid JSON."""
        # Create temporary file with invalid JSON
        config_file = tmp_path / "mcp-config.json"
        config_file.write_text("not valid json")
        
        client = ClaudeCode(
            auth_type=AuthType.ANTHROPIC_API,
            api_key="test-api-key"
        )
        
        with pytest.raises(ValidationError):
            client.load_mcp_config(str(config_file))

    def test_load_mcp_config_invalid_structure(self, tmp_path):
        """Test loading MCP configuration with invalid structure."""
        # Create temporary file with JSON but invalid structure
        config_file = tmp_path / "mcp-config.json"
        config_file.write_text(json.dumps({"invalid": "structure"}))
        
        client = ClaudeCode(
            auth_type=AuthType.ANTHROPIC_API,
            api_key="test-api-key"
        )
        
        with pytest.raises(ValidationError):
            client.load_mcp_config(str(config_file))

    def test_run_prompt(self, mock_successful_subprocess_run, claude_code_client):
        """Test running a prompt."""
        result = claude_code_client.run_prompt("Test prompt")
        
        # Verify subprocess.run was called with the right parameters
        mock_successful_subprocess_run.assert_called_once()
        cmd = mock_successful_subprocess_run.call_args[0][0]
        assert cmd[0] == "claude"
        assert "-p" in cmd
        
        # Check environment
        env = mock_successful_subprocess_run.call_args[1]["env"]
        assert env["ANTHROPIC_API_KEY"] == "test-api-key"
        
        # Check result
        assert result == "Mock response from Claude Code"

    def test_run_prompt_json(self, mock_json_subprocess_run, claude_code_client):
        """Test running a prompt with JSON output."""
        result = claude_code_client.run_prompt(
            "Test prompt", 
            output_format=OutputFormat.JSON
        )
        
        # Verify subprocess.run was called with the right parameters
        mock_json_subprocess_run.assert_called_once()
        cmd = mock_json_subprocess_run.call_args[0][0]
        assert cmd[0] == "claude"
        assert "-p" in cmd
        assert "--output-format" in cmd
        assert "json" in cmd
        
        # Check result
        assert result == {"result": "success", "message": "Mock JSON response"}

    def test_stream_prompt(self, mock_streaming_subprocess_popen, claude_code_client):
        """Test streaming a prompt."""
        chunks = list(claude_code_client.stream_prompt("Test prompt"))
        
        # Verify subprocess.Popen was called with the right parameters
        mock_streaming_subprocess_popen.assert_called_once()
        cmd = mock_streaming_subprocess_popen.call_args[0][0]
        assert cmd[0] == "claude"
        assert "-p" in cmd
        
        # Check streaming results
        assert len(chunks) == 3
        assert chunks[0] == "Chunk 1"
        assert chunks[1] == "Chunk 2"
        assert chunks[2] == "Chunk 3"

    def test_start_conversation(self, claude_code_client):
        """Test starting a conversation."""
        conversation = claude_code_client.start_conversation(
            allowed_tools=["Bash", "Glob"],
            max_turns=5,
            timeout=60
        )
        
        assert conversation.auth_provider == claude_code_client.auth_provider
        assert conversation.allowed_tools == ["Bash", "Glob"]
        assert conversation.max_turns == 5
        assert conversation.timeout == 60
        assert conversation.turn_count == 0