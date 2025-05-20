"""
Authentication provider for Claude Code.
"""

import os
from typing import Dict, Optional

from .types import AuthType
from ..exceptions import AuthenticationError


class AuthProvider:
    """Provider for Claude Code authentication."""

    def __init__(
        self,
        auth_type: AuthType,
        api_key: Optional[str] = None,
        region: Optional[str] = None,
        project_id: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Initialize the authentication provider.

        Args:
            auth_type: The authentication type to use.
            api_key: Anthropic API key (required for ANTHROPIC_API auth type).
            region: AWS region or Cloud ML region (required for AWS_BEDROCK and GOOGLE_VERTEX).
            project_id: Google Cloud project ID (required for GOOGLE_VERTEX).
            model: Model ID in provider-specific format.
        """
        self.auth_type = auth_type
        self.api_key = api_key
        self.region = region
        self.project_id = project_id
        self.model = model
        self._validate()

    def _validate(self) -> None:
        """Validate the authentication configuration."""
        if self.auth_type == AuthType.ANTHROPIC_API:
            if not self.api_key:
                raise AuthenticationError("API key is required for Anthropic API authentication")
        elif self.auth_type == AuthType.AWS_BEDROCK:
            if not self.region:
                raise AuthenticationError("Region is required for AWS Bedrock authentication")
        elif self.auth_type == AuthType.GOOGLE_VERTEX:
            if not self.region:
                raise AuthenticationError("Region is required for Google Vertex AI authentication")
            if not self.project_id:
                raise AuthenticationError("Project ID is required for Google Vertex AI authentication")

    def get_environment(self) -> Dict[str, str]:
        """
        Get environment variables for authentication.

        Returns:
            Dictionary of environment variables.
        """
        env = {}

        if self.auth_type == AuthType.ANTHROPIC_API:
            env["ANTHROPIC_API_KEY"] = self.api_key or ""
        elif self.auth_type == AuthType.AWS_BEDROCK:
            env["CLAUDE_CODE_USE_BEDROCK"] = "1"
            if self.region:
                env["AWS_REGION"] = self.region
        elif self.auth_type == AuthType.GOOGLE_VERTEX:
            env["CLAUDE_CODE_USE_VERTEX"] = "1"
            if self.region:
                env["CLOUD_ML_REGION"] = self.region
            if self.project_id:
                env["ANTHROPIC_VERTEX_PROJECT_ID"] = self.project_id

        if self.model:
            env["ANTHROPIC_MODEL"] = self.model

        return env

    def update_from_environment(self) -> None:
        """Update authentication configuration from environment variables."""
        if self.auth_type == AuthType.ANTHROPIC_API and not self.api_key:
            self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        elif self.auth_type == AuthType.AWS_BEDROCK and not self.region:
            self.region = os.environ.get("AWS_REGION")
        elif self.auth_type == AuthType.GOOGLE_VERTEX:
            if not self.region:
                self.region = os.environ.get("CLOUD_ML_REGION")
            if not self.project_id:
                self.project_id = os.environ.get("ANTHROPIC_VERTEX_PROJECT_ID")

        if not self.model:
            self.model = os.environ.get("ANTHROPIC_MODEL", "claude-3-7-sonnet-20250219")