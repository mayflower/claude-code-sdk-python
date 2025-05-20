"""
Claude Code conversation management.
"""

import tempfile
import json
import uuid
from typing import Dict, Iterator, List, Optional, Union

from .auth.provider import AuthProvider
from .types import OutputFormat
from .utils import run_command, stream_command, stream_json_command
from .exceptions import ValidationError, ExecutionError


class Conversation:
    """
    Claude Code conversation.

    This class manages a conversation with Claude Code, allowing
    multiple back-and-forth messages in the same context.
    """

    def __init__(
        self,
        auth_provider: AuthProvider,
        conversation_id: Optional[str] = None,
        allowed_tools: Optional[List[str]] = None,
        disallowed_tools: Optional[List[str]] = None,
        max_turns: Optional[int] = None,
        mcp_config: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[int] = None,
        output_format: OutputFormat = OutputFormat.TEXT,
    ):
        """
        Initialize a Claude Code conversation.

        Args:
            auth_provider: Authentication provider.
            conversation_id: Conversation ID for continuing an existing conversation.
            allowed_tools: List of tools to allow.
            disallowed_tools: List of tools to disallow.
            max_turns: Maximum number of back-and-forth turns.
            mcp_config: Path to MCP configuration JSON file.
            model: Model to use.
            timeout: Timeout in seconds.
            output_format: Output format for responses.
        """
        self.auth_provider = auth_provider
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.allowed_tools = allowed_tools
        self.disallowed_tools = disallowed_tools
        self.max_turns = max_turns
        self.mcp_config = mcp_config
        self.model = model
        self.timeout = timeout
        self.output_format = output_format
        
        # Track number of turns
        self.turn_count = 0
        
        # Check for conflicting settings
        if self.allowed_tools and self.disallowed_tools:
            overlap = set(self.allowed_tools) & set(self.disallowed_tools)
            if overlap:
                raise ValidationError(
                    f"Tools cannot be both allowed and disallowed: {', '.join(overlap)}"
                )

    def _build_command(self, prompt: str) -> List[str]:
        """
        Build the command to run.

        Args:
            prompt: Prompt message.

        Returns:
            Command to run.
        """
        cmd = ["claude"]
        
        # Common flags
        cmd.extend(["-p"])
        
        # Output format
        if self.output_format != OutputFormat.TEXT:
            cmd.extend(["--output-format", self.output_format.value])
        
        # Continue conversation if not the first turn
        if self.turn_count > 0:
            cmd.extend(["-c"])
        
        # Tool configuration
        if self.allowed_tools:
            cmd.extend(["--allowedTools", ",".join(self.allowed_tools)])
        
        if self.disallowed_tools:
            cmd.extend(["--disallowedTools", ",".join(self.disallowed_tools)])
        
        # Max turns
        if self.max_turns:
            cmd.extend(["--max-turns", str(self.max_turns)])
        
        # MCP configuration
        if self.mcp_config:
            cmd.extend(["--mcp-config", self.mcp_config])
        
        # Add the prompt (will be passed through stdin)
        return cmd

    def _get_env(self) -> Dict[str, str]:
        """
        Get environment variables for the conversation.

        Returns:
            Dictionary of environment variables.
        """
        env = self.auth_provider.get_environment()
        
        # Add model override if specified for this conversation
        if self.model:
            env["ANTHROPIC_MODEL"] = self.model
            
        # Set conversation ID for continuity
        env["CLAUDE_CONVERSATION_ID"] = self.conversation_id
        
        return env

    def send(self, prompt: str) -> str:
        """
        Send a message to Claude Code.

        Args:
            prompt: Prompt message.

        Returns:
            Claude Code's response.

        Raises:
            ValidationError: If input validation fails.
            ExecutionError: If there's an error running Claude Code.
            TimeoutError: If Claude Code times out.
        """
        if not prompt or not prompt.strip():
            raise ValidationError("Prompt cannot be empty")
        
        if self.max_turns and self.turn_count >= self.max_turns:
            raise ValidationError(f"Conversation has reached the maximum number of turns: {self.max_turns}")
        
        cmd = self._build_command(prompt)
        env = self._get_env()
        
        exit_code, stdout, stderr = run_command(
            cmd, env=env, timeout=self.timeout, input_data=prompt
        )
        
        if exit_code != 0:
            raise ExecutionError(
                f"Claude Code failed with exit code {exit_code}",
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
            )
        
        self.turn_count += 1
        return stdout

    def stream(self, prompt: str) -> Iterator[str]:
        """
        Send a message to Claude Code and stream the response.

        Args:
            prompt: Prompt message.

        Yields:
            Chunks of Claude Code's response.

        Raises:
            ValidationError: If input validation fails.
            ExecutionError: If there's an error running Claude Code.
            TimeoutError: If Claude Code times out.
        """
        if not prompt or not prompt.strip():
            raise ValidationError("Prompt cannot be empty")
        
        if self.max_turns and self.turn_count >= self.max_turns:
            raise ValidationError(f"Conversation has reached the maximum number of turns: {self.max_turns}")
        
        cmd = self._build_command(prompt)
        env = self._get_env()
        
        for chunk in stream_command(cmd, env=env, timeout=self.timeout, input_data=prompt):
            yield chunk
        
        self.turn_count += 1

    def stream_json(self, prompt: str) -> Iterator[Dict]:
        """
        Send a message to Claude Code and stream the JSON response.

        Args:
            prompt: Prompt message.

        Yields:
            Parsed JSON objects from Claude Code's response.

        Raises:
            ValidationError: If input validation fails.
            ExecutionError: If there's an error running Claude Code.
            TimeoutError: If Claude Code times out.
        """
        if self.output_format != OutputFormat.STREAM_JSON:
            raise ValidationError("Output format must be STREAM_JSON for stream_json")
        
        if not prompt or not prompt.strip():
            raise ValidationError("Prompt cannot be empty")
        
        if self.max_turns and self.turn_count >= self.max_turns:
            raise ValidationError(f"Conversation has reached the maximum number of turns: {self.max_turns}")
        
        cmd = self._build_command(prompt)
        env = self._get_env()
        
        for chunk in stream_json_command(cmd, env=env, timeout=self.timeout, input_data=prompt):
            yield chunk
        
        self.turn_count += 1