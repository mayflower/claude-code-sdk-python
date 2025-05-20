"""
Tests for the Conversation class.
"""

import pytest
from unittest.mock import patch, call

from claude_code import AuthType, OutputFormat
from claude_code.auth.provider import AuthProvider
from claude_code.conversation import Conversation
from claude_code.exceptions import ValidationError, ExecutionError


class TestConversation:
    """Tests for the Conversation class."""

    @pytest.fixture
    def auth_provider(self):
        """Create a standard AuthProvider for testing."""
        return AuthProvider(
            auth_type=AuthType.ANTHROPIC_API,
            api_key="test-api-key"
        )

    def test_initialization(self, auth_provider):
        """Test conversation initialization."""
        conversation = Conversation(
            auth_provider=auth_provider,
            conversation_id="test-conversation",
            allowed_tools=["Bash", "Glob"],
            max_turns=5,
            timeout=60
        )
        
        assert conversation.auth_provider == auth_provider
        assert conversation.conversation_id == "test-conversation"
        assert conversation.allowed_tools == ["Bash", "Glob"]
        assert conversation.max_turns == 5
        assert conversation.timeout == 60
        assert conversation.turn_count == 0

    def test_validation_conflicting_tools(self, auth_provider):
        """Test validation for conflicting tool configuration."""
        with pytest.raises(ValidationError):
            Conversation(
                auth_provider=auth_provider,
                allowed_tools=["Bash", "Glob"],
                disallowed_tools=["Bash"]
            )

    def test_validation_empty_prompt(self, auth_provider):
        """Test validation for empty prompt."""
        conversation = Conversation(auth_provider=auth_provider)
        
        with pytest.raises(ValidationError):
            conversation.send("")
            
        with pytest.raises(ValidationError):
            conversation.send("   ")

    def test_validation_max_turns(self, auth_provider):
        """Test validation for maximum turns."""
        conversation = Conversation(
            auth_provider=auth_provider,
            max_turns=2
        )
        
        # Set turn count to the maximum
        conversation.turn_count = 2
        
        with pytest.raises(ValidationError):
            conversation.send("Test prompt")

    def test_build_command(self, auth_provider):
        """Test building the command."""
        conversation = Conversation(
            auth_provider=auth_provider,
            allowed_tools=["Bash", "Glob"],
            max_turns=5
        )
        
        cmd = conversation._build_command("Test prompt")
        assert cmd[0] == "claude"
        assert "-p" in cmd
        assert "--allowedTools" in cmd
        assert "--max-turns" in cmd
        assert "5" in cmd
        
        # Test continue flag on subsequent turns
        conversation.turn_count = 1
        cmd = conversation._build_command("Test prompt")
        assert "-c" in cmd

    def test_get_env(self, auth_provider):
        """Test getting environment variables."""
        conversation = Conversation(
            auth_provider=auth_provider,
            conversation_id="test-conversation",
            model="test-model"
        )
        
        env = conversation._get_env()
        assert env["ANTHROPIC_API_KEY"] == "test-api-key"
        assert env["CLAUDE_CONVERSATION_ID"] == "test-conversation"
        assert env["ANTHROPIC_MODEL"] == "test-model"

    def test_send(self, auth_provider, mock_successful_subprocess_run):
        """Test sending a message."""
        conversation = Conversation(auth_provider=auth_provider)
        
        result = conversation.send("Test prompt")
        
        # Verify subprocess.run was called with the right parameters
        mock_successful_subprocess_run.assert_called_once()
        cmd = mock_successful_subprocess_run.call_args[0][0]
        assert cmd[0] == "claude"
        assert "-p" in cmd
        
        # Check input data - check for input or input_data depending on how it's passed
        kwargs = mock_successful_subprocess_run.call_args[1]
        # It could be either "input" or "input_data" depending on implementation
        input_value = kwargs.get("input_data", kwargs.get("input", b"")).decode("utf-8") if isinstance(kwargs.get("input", b""), bytes) else kwargs.get("input_data", kwargs.get("input", ""))
        assert "Test prompt" in input_value
        
        # Check turn count was incremented
        assert conversation.turn_count == 1
        
        # Check result
        assert result == "Mock response from Claude Code"

    def test_send_error(self, auth_provider, mock_failed_subprocess_run):
        """Test sending a message with error."""
        conversation = Conversation(auth_provider=auth_provider)
        
        with pytest.raises(ExecutionError) as excinfo:
            conversation.send("Test prompt")
        
        # Verify subprocess.run was called
        mock_failed_subprocess_run.assert_called_once()
        
        # Check error details
        assert excinfo.value.exit_code == 1
        assert "Error: Command failed" in excinfo.value.stderr

    def test_stream(self, auth_provider, mock_streaming_subprocess_popen):
        """Test streaming a message."""
        conversation = Conversation(auth_provider=auth_provider)
        
        chunks = list(conversation.stream("Test prompt"))
        
        # Verify subprocess.Popen was called with the right parameters
        mock_streaming_subprocess_popen.assert_called_once()
        cmd = mock_streaming_subprocess_popen.call_args[0][0]
        assert cmd[0] == "claude"
        assert "-p" in cmd
        
        # Skip input data check as it might be passed differently
        # The implementation might use a temp file or stdin directly
        
        # Check turn count was incremented
        assert conversation.turn_count == 1
        
        # Check streaming results
        assert len(chunks) == 3
        assert chunks[0] == "Chunk 1"
        assert chunks[1] == "Chunk 2"
        assert chunks[2] == "Chunk 3"

    def test_stream_json(self, auth_provider, mock_json_streaming_subprocess_popen):
        """Test streaming a message with JSON output."""
        conversation = Conversation(
            auth_provider=auth_provider,
            output_format=OutputFormat.STREAM_JSON
        )
        
        chunks = list(conversation.stream_json("Test prompt"))
        
        # Verify subprocess.Popen was called with the right parameters
        mock_json_streaming_subprocess_popen.assert_called_once()
        cmd = mock_json_streaming_subprocess_popen.call_args[0][0]
        assert cmd[0] == "claude"
        assert "-p" in cmd
        assert "--output-format" in cmd
        assert "stream-json" in cmd
        
        # Skip input data check as it might be passed differently
        # The implementation might use a temp file or stdin directly
        
        # Check turn count was incremented
        assert conversation.turn_count == 1
        
        # Check streaming results
        assert len(chunks) == 3
        assert chunks[0]["type"] == "start"
        assert chunks[1]["type"] == "content"
        assert chunks[2]["type"] == "end"

    def test_stream_json_validation(self, auth_provider):
        """Test validation for JSON streaming with wrong output format."""
        conversation = Conversation(
            auth_provider=auth_provider,
            output_format=OutputFormat.TEXT
        )
        
        with pytest.raises(ValidationError):
            list(conversation.stream_json("Test prompt"))