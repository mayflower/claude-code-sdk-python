"""
Tests for subprocess utilities.
"""

import json
import subprocess
import pytest
from unittest.mock import patch, MagicMock

from claude_code.utils.subprocess import (
    run_command,
    stream_command,
    stream_json_command,
)
from claude_code.exceptions import ExecutionError, TimeoutError


class TestSubprocessUtils:
    """Tests for subprocess utilities."""

    def test_run_command_success(self, mock_successful_subprocess_run):
        """Test running a command successfully."""
        exit_code, stdout, stderr = run_command(["echo", "test"])
        
        mock_successful_subprocess_run.assert_called_once()
        assert exit_code == 0
        assert stdout == "Mock response from Claude Code"
        assert stderr == ""

    def test_run_command_failure(self, mock_failed_subprocess_run):
        """Test running a command that fails."""
        exit_code, stdout, stderr = run_command(["invalid", "command"])
        
        mock_failed_subprocess_run.assert_called_once()
        assert exit_code == 1
        assert stdout == ""
        assert stderr == "Error: Command failed"

    def test_run_command_with_input(self, mock_successful_subprocess_run):
        """Test running a command with input data."""
        exit_code, stdout, stderr = run_command(
            ["cat"], input_data="test input"
        )
        
        mock_successful_subprocess_run.assert_called_once()
        # Check that input data was passed correctly
        kwargs = mock_successful_subprocess_run.call_args[1]
        assert kwargs["input"] == b"test input"
        
        assert exit_code == 0
        assert stdout == "Mock response from Claude Code"
        assert stderr == ""

    def test_run_command_timeout(self):
        """Test running a command that times out."""
        with patch("subprocess.run") as mock_run:
            # Mock subprocess.run to raise TimeoutExpired
            timeout_error = subprocess.TimeoutExpired(
                cmd=["test"],
                timeout=10
            )
            # Add stdout and stderr attributes manually
            timeout_error.stdout = b"Partial output"
            timeout_error.stderr = b"Timed out"
            mock_run.side_effect = timeout_error
            
            with pytest.raises(TimeoutError) as excinfo:
                run_command(["test"], timeout=10)
            
            assert "timed out" in str(excinfo.value)
            assert excinfo.value.stdout == "Partial output"
            assert excinfo.value.stderr == "Timed out"

    def test_stream_command(self, mock_streaming_subprocess_popen):
        """Test streaming a command output."""
        chunks = list(stream_command(["cat"]))
        
        mock_streaming_subprocess_popen.assert_called_once()
        assert len(chunks) == 3
        assert chunks[0] == "Chunk 1"
        assert chunks[1] == "Chunk 2"
        assert chunks[2] == "Chunk 3"

    def test_stream_command_with_input(self, mock_streaming_subprocess_popen):
        """Test streaming a command with input data."""
        chunks = list(stream_command(["cat"], input_data="test input"))
        
        mock_streaming_subprocess_popen.assert_called_once()
        # Check that a temporary file was used for input
        kwargs = mock_streaming_subprocess_popen.call_args[1]
        assert kwargs["stdin"] is not None
        
        assert len(chunks) == 3
        assert chunks[0] == "Chunk 1"
        assert chunks[1] == "Chunk 2"
        assert chunks[2] == "Chunk 3"

    def test_stream_command_error(self):
        """Test streaming a command that errors."""
        with patch("subprocess.Popen") as mock_popen:
            mock_process = MagicMock()
            mock_process.stdout.__iter__.return_value = ["Some output\n"]
            mock_process.wait.return_value = 1
            mock_process.stderr = MagicMock()
            mock_process.stderr.read.return_value = "Command failed"
            mock_popen.return_value = mock_process
            
            # Consume one item from the iterator
            next(stream_command(["invalid", "command"]))
            
            # The second item should raise an ExecutionError
            with pytest.raises(ExecutionError) as excinfo:
                list(stream_command(["invalid", "command"]))
            
            assert excinfo.value.exit_code == 1
            assert "Command failed" in excinfo.value.stderr

    def test_stream_json_command(self, mock_json_streaming_subprocess_popen):
        """Test streaming a command with JSON output."""
        json_chunks = list(stream_json_command(["cat"]))
        
        mock_json_streaming_subprocess_popen.assert_called_once()
        assert len(json_chunks) == 3
        assert json_chunks[0]["type"] == "start"
        assert json_chunks[1]["type"] == "content"
        assert json_chunks[2]["type"] == "end"

    def test_stream_json_command_invalid_json(self):
        """Test streaming a command with invalid JSON output."""
        with patch("subprocess.Popen") as mock_popen:
            mock_process = MagicMock()
            mock_process.stdout.__iter__.return_value = ["Not valid JSON\n"]
            mock_process.wait.return_value = 0
            mock_popen.return_value = mock_process
            
            with pytest.raises(ValueError) as excinfo:
                list(stream_json_command(["cat"]))
            
            assert "Error parsing JSON" in str(excinfo.value)