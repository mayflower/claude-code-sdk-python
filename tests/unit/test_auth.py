"""
Tests for authentication functionality.
"""

import os
import pytest
from unittest.mock import patch

from claude_code.auth import AuthProvider, AuthType
from claude_code.exceptions import AuthenticationError


class TestAuthProvider:
    """Tests for the AuthProvider class."""

    def test_anthropic_api_auth(self):
        """Test initialization with Anthropic API."""
        provider = AuthProvider(
            auth_type=AuthType.ANTHROPIC_API,
            api_key="test-api-key"
        )
        
        env = provider.get_environment()
        assert env["ANTHROPIC_API_KEY"] == "test-api-key"
        assert "CLAUDE_CODE_USE_BEDROCK" not in env
        assert "CLAUDE_CODE_USE_VERTEX" not in env

    def test_bedrock_auth(self):
        """Test initialization with AWS Bedrock."""
        provider = AuthProvider(
            auth_type=AuthType.AWS_BEDROCK,
            region="us-west-2",
            model="anthropic.claude-3-7-sonnet-20250219-v1:0"
        )
        
        env = provider.get_environment()
        assert env["CLAUDE_CODE_USE_BEDROCK"] == "1"
        assert env["AWS_REGION"] == "us-west-2"
        assert env["ANTHROPIC_MODEL"] == "anthropic.claude-3-7-sonnet-20250219-v1:0"
        assert "ANTHROPIC_API_KEY" not in env

    def test_vertex_auth(self):
        """Test initialization with Google Vertex AI."""
        provider = AuthProvider(
            auth_type=AuthType.GOOGLE_VERTEX,
            region="us-central1",
            project_id="test-project",
            model="claude-3-7-sonnet@20250219"
        )
        
        env = provider.get_environment()
        assert env["CLAUDE_CODE_USE_VERTEX"] == "1"
        assert env["CLOUD_ML_REGION"] == "us-central1"
        assert env["ANTHROPIC_VERTEX_PROJECT_ID"] == "test-project"
        assert env["ANTHROPIC_MODEL"] == "claude-3-7-sonnet@20250219"
        assert "ANTHROPIC_API_KEY" not in env

    def test_auth_validation_anthropic(self):
        """Test validation for Anthropic API auth."""
        # Should raise an error when API key is missing
        with pytest.raises(AuthenticationError):
            AuthProvider(auth_type=AuthType.ANTHROPIC_API)

    def test_auth_validation_bedrock(self):
        """Test validation for AWS Bedrock auth."""
        # Should raise an error when region is missing
        with pytest.raises(AuthenticationError):
            AuthProvider(auth_type=AuthType.AWS_BEDROCK)

    def test_auth_validation_vertex(self):
        """Test validation for Google Vertex AI auth."""
        # Should raise an error when region is missing
        with pytest.raises(AuthenticationError):
            AuthProvider(auth_type=AuthType.GOOGLE_VERTEX, project_id="test-project")
            
        # Should raise an error when project_id is missing
        with pytest.raises(AuthenticationError):
            AuthProvider(auth_type=AuthType.GOOGLE_VERTEX, region="us-central1")

    def test_update_from_environment(self):
        """Test updating auth config from environment."""
        with patch.dict(os.environ, {
            "ANTHROPIC_API_KEY": "env-api-key",
            "AWS_REGION": "us-east-1",
            "CLOUD_ML_REGION": "us-central1",
            "ANTHROPIC_VERTEX_PROJECT_ID": "env-project",
            "ANTHROPIC_MODEL": "env-model"
        }):
            # Test Anthropic API
            provider = AuthProvider(auth_type=AuthType.ANTHROPIC_API, api_key="placeholder")
            provider.api_key = None  # Clear it so we can test environment loading
            provider.update_from_environment()
            assert provider.api_key == "env-api-key"
            
            # Test AWS Bedrock
            provider = AuthProvider(auth_type=AuthType.AWS_BEDROCK, region="placeholder")
            provider.region = None  # Clear it so we can test environment loading
            provider.update_from_environment()
            assert provider.region == "us-east-1"
            
            # Test Google Vertex AI
            provider = AuthProvider(
                auth_type=AuthType.GOOGLE_VERTEX, 
                region="placeholder",
                project_id="placeholder"
            )
            provider.region = None
            provider.project_id = None
            provider.update_from_environment()
            assert provider.region == "us-central1"
            assert provider.project_id == "env-project"
            
            # Test model
            provider = AuthProvider(auth_type=AuthType.ANTHROPIC_API, api_key="test-key")
            provider.update_from_environment()
            assert provider.model == "env-model"