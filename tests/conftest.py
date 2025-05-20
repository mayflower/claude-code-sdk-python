"""
Common test fixtures for Claude Code SDK.
"""

import os
import json
import pytest
from unittest.mock import MagicMock, patch

from claude_code import ClaudeCode, AuthType


@pytest.fixture
def mock_successful_subprocess_run():
    """Mock for successful subprocess.run."""
    with patch("subprocess.run") as mock_run:
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = b"Mock response from Claude Code"
        mock_process.stderr = b""
        mock_run.return_value = mock_process
        yield mock_run


@pytest.fixture
def mock_failed_subprocess_run():
    """Mock for failed subprocess.run."""
    with patch("subprocess.run") as mock_run:
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_process.stdout = b""
        mock_process.stderr = b"Error: Command failed"
        mock_run.return_value = mock_process
        yield mock_run


@pytest.fixture
def mock_json_subprocess_run():
    """Mock for subprocess.run returning JSON."""
    with patch("subprocess.run") as mock_run:
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = b'{"result": "success", "message": "Mock JSON response"}'
        mock_process.stderr = b""
        mock_run.return_value = mock_process
        yield mock_run


@pytest.fixture
def mock_streaming_subprocess_popen():
    """Mock for subprocess.Popen in streaming mode."""
    with patch("subprocess.Popen") as mock_popen:
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.poll.return_value = 0
        mock_process.wait.return_value = 0
        
        # Mock stdout iterator that returns 3 lines
        mock_process.stdout.__iter__.return_value = [
            "Chunk 1\n",
            "Chunk 2\n",
            "Chunk 3\n"
        ]
        
        mock_popen.return_value = mock_process
        yield mock_popen


@pytest.fixture
def mock_json_streaming_subprocess_popen():
    """Mock for subprocess.Popen in JSON streaming mode."""
    with patch("subprocess.Popen") as mock_popen:
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.poll.return_value = 0
        mock_process.wait.return_value = 0
        
        # Mock stdout iterator that returns 3 JSON objects
        mock_process.stdout.__iter__.return_value = [
            '{"type": "start", "message": "Starting"}\n',
            '{"type": "content", "message": "Content"}\n',
            '{"type": "end", "message": "Finished"}\n'
        ]
        
        mock_popen.return_value = mock_process
        yield mock_popen


@pytest.fixture
def claude_code_client():
    """Create a standard ClaudeCode client for testing."""
    return ClaudeCode(
        auth_type=AuthType.ANTHROPIC_API,
        api_key="test-api-key"
    )


@pytest.fixture
def claude_with_tools():
    """Create a ClaudeCode client with tools configured."""
    return ClaudeCode(
        auth_type=AuthType.ANTHROPIC_API,
        api_key="test-api-key",
        allowed_tools=["Bash", "Glob", "Grep"],
        max_turns=5
    )


@pytest.fixture
def bedrock_client():
    """Create a ClaudeCode client configured for AWS Bedrock."""
    with patch.dict(os.environ, {"AWS_REGION": "us-west-2"}):
        return ClaudeCode(
            auth_type=AuthType.AWS_BEDROCK,
            region="us-west-2",
            model="anthropic.claude-3-7-sonnet-20250219-v1:0"
        )


@pytest.fixture
def vertex_client():
    """Create a ClaudeCode client configured for Google Vertex AI."""
    with patch.dict(os.environ, {
        "CLOUD_ML_REGION": "us-central1",
        "ANTHROPIC_VERTEX_PROJECT_ID": "test-project"
    }):
        return ClaudeCode(
            auth_type=AuthType.GOOGLE_VERTEX,
            region="us-central1",
            project_id="test-project",
            model="claude-3-7-sonnet@20250219"
        )