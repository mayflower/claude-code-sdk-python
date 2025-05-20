"""
Claude Code client.
"""

import json
import os
import tempfile
from typing import Dict, Iterator, List, Optional, Union

from .auth.provider import AuthProvider
from .auth.types import AuthType
from .conversation import Conversation
from .exceptions import ValidationError
from .types import OutputFormat, ToolConfig
from .utils import run_command, stream_command, stream_json_command


class ClaudeCode:
    """
    Claude Code client.

    This client provides a Python interface to the Claude Code CLI.
    """

    def __init__(
        self,
        auth_type: AuthType = AuthType.ANTHROPIC_API,
        api_key: Optional[str] = None,
        region: Optional[str] = None,
        project_id: Optional[str] = None,
        model: Optional[str] = None,
        allowed_tools: Optional[List[str]] = None,
        disallowed_tools: Optional[List[str]] = None,
        max_turns: Optional[int] = None,
        mcp_config: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        """
        Initialize the Claude Code client.

        Args:
            auth_type: Authentication type.
            api_key: Anthropic API key (required for ANTHROPIC_API auth type).
            region: AWS region or Cloud ML region (required for AWS_BEDROCK and GOOGLE_VERTEX).
            project_id: Google Cloud project ID (required for GOOGLE_VERTEX).
            model: Model ID in provider-specific format.
            allowed_tools: List of tools to allow.
            disallowed_tools: List of tools to disallow.
            max_turns: Maximum number of turns in a conversation.
            mcp_config: Path to MCP configuration JSON file.
            timeout: Timeout in seconds.
        """
        self.auth_provider = AuthProvider(
            auth_type=auth_type,
            api_key=api_key,
            region=region,
            project_id=project_id,
            model=model,
        )
        
        # Try to load authentication from environment if not provided
        self.auth_provider.update_from_environment()

        # Configuration
        self.allowed_tools = allowed_tools
        self.disallowed_tools = disallowed_tools
        self.max_turns = max_turns
        self.mcp_config = mcp_config
        self.timeout = timeout
        
        # Check for conflicting settings
        if self.allowed_tools and self.disallowed_tools:
            overlap = set(self.allowed_tools) & set(self.disallowed_tools)
            if overlap:
                raise ValidationError(
                    f"Tools cannot be both allowed and disallowed: {', '.join(overlap)}"
                )

    def configure(
        self,
        allowed_tools: Optional[List[str]] = None,
        disallowed_tools: Optional[List[str]] = None,
        max_turns: Optional[int] = None,
        mcp_config: Optional[str] = None,
        timeout: Optional[int] = None,
        model: Optional[str] = None,
    ) -> None:
        """
        Configure the Claude Code client.

        Args:
            allowed_tools: List of tools to allow.
            disallowed_tools: List of tools to disallow.
            max_turns: Maximum number of turns in a conversation.
            mcp_config: Path to MCP configuration JSON file.
            timeout: Timeout in seconds.
            model: Model ID in provider-specific format.
        """
        if allowed_tools is not None:
            self.allowed_tools = allowed_tools
        if disallowed_tools is not None:
            self.disallowed_tools = disallowed_tools
        if max_turns is not None:
            self.max_turns = max_turns
        if mcp_config is not None:
            self.mcp_config = mcp_config
        if timeout is not None:
            self.timeout = timeout
        if model is not None:
            self.auth_provider.model = model
        
        # Check for conflicting settings
        if self.allowed_tools and self.disallowed_tools:
            overlap = set(self.allowed_tools) & set(self.disallowed_tools)
            if overlap:
                raise ValidationError(
                    f"Tools cannot be both allowed and disallowed: {', '.join(overlap)}"
                )

    def load_mcp_config(self, config_path: str) -> None:
        """
        Load MCP configuration from a JSON file.

        Args:
            config_path: Path to the MCP configuration JSON file.
        """
        if not os.path.exists(config_path):
            raise ValidationError(f"MCP configuration file not found: {config_path}")
        
        # Validate that this is a valid JSON file
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            
            if not isinstance(config, dict) or "mcpServers" not in config:
                raise ValidationError(
                    f"Invalid MCP configuration file: {config_path}"
                )
        except json.JSONDecodeError:
            raise ValidationError(
                f"Invalid JSON in MCP configuration file: {config_path}"
            )
        
        self.mcp_config = config_path

    def run_prompt(
        self,
        prompt: str,
        output_format: OutputFormat = OutputFormat.TEXT,
    ) -> Union[str, Dict]:
        """
        Run a one-shot prompt with Claude Code.

        Args:
            prompt: The prompt to send to Claude Code.
            output_format: Output format for the response.

        Returns:
            Claude Code's response (text or parsed JSON depending on output_format).

        Raises:
            ValidationError: If input validation fails.
            ExecutionError: If there's an error running Claude Code.
            TimeoutError: If Claude Code times out.
        """
        conversation = self.start_conversation(output_format=output_format)
        
        response = conversation.send(prompt)
        
        # If output_format is JSON, parse the response
        if output_format == OutputFormat.JSON:
            try:
                return json.loads(response)
            except json.JSONDecodeError as e:
                raise ValidationError(f"Error parsing JSON response: {e}") from e
        
        return response

    def stream_prompt(
        self,
        prompt: str,
        output_format: OutputFormat = OutputFormat.TEXT,
    ) -> Union[Iterator[str], Iterator[Dict]]:
        """
        Stream a one-shot prompt with Claude Code.

        Args:
            prompt: The prompt to send to Claude Code.
            output_format: Output format for the response.

        Returns:
            Iterator of response chunks.

        Raises:
            ValidationError: If input validation fails.
            ExecutionError: If there's an error running Claude Code.
            TimeoutError: If Claude Code times out.
        """
        conversation = self.start_conversation(output_format=output_format)
        
        if output_format == OutputFormat.STREAM_JSON:
            return conversation.stream_json(prompt)
        else:
            return conversation.stream(prompt)

    def start_conversation(
        self,
        conversation_id: Optional[str] = None,
        allowed_tools: Optional[List[str]] = None,
        disallowed_tools: Optional[List[str]] = None,
        max_turns: Optional[int] = None,
        mcp_config: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[int] = None,
        output_format: OutputFormat = OutputFormat.TEXT,
    ) -> Conversation:
        """
        Start a new conversation with Claude Code.

        Args:
            conversation_id: ID for the conversation, auto-generated if not provided.
            allowed_tools: List of tools to allow (overrides client config).
            disallowed_tools: List of tools to disallow (overrides client config).
            max_turns: Maximum number of turns (overrides client config).
            mcp_config: Path to MCP configuration JSON file (overrides client config).
            model: Model ID in provider-specific format (overrides client config).
            timeout: Timeout in seconds (overrides client config).
            output_format: Output format for responses.

        Returns:
            A new Conversation instance.
        """
        return Conversation(
            auth_provider=self.auth_provider,
            conversation_id=conversation_id,
            allowed_tools=allowed_tools or self.allowed_tools,
            disallowed_tools=disallowed_tools or self.disallowed_tools,
            max_turns=max_turns or self.max_turns,
            mcp_config=mcp_config or self.mcp_config,
            model=model or self.auth_provider.model,
            timeout=timeout or self.timeout,
            output_format=output_format,
        )