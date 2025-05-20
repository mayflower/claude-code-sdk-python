#!/usr/bin/env python3
"""
Integration test for Claude Code SDK.

This script tests multiple functionalities of the SDK:
- Basic prompts
- Streaming responses
- JSON responses
- Conversations
- Tool configuration
- Different authentication methods (if credentials are available)

Set your ANTHROPIC_API_KEY environment variable before running.
"""

import os
import time
import json
from typing import Optional

from claude_code import ClaudeCode, AuthType, OutputFormat
from claude_code.exceptions import ClaudeCodeError

def print_section(title):
    """Print a section title."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_basic_prompt(client):
    """Test basic prompt functionality."""
    print_section("Testing Basic Prompt")
    
    result = client.run_prompt("Explain what the Claude Code SDK is in one sentence.")
    print(f"Response: {result}")
    
    assert result, "Basic prompt response should not be empty"
    return True

def test_streaming(client):
    """Test streaming response functionality."""
    print_section("Testing Streaming Response")
    
    print("Streaming response:")
    stream_chunks = []
    for chunk in client.stream_prompt("Count from 1 to 5, with a brief pause between each number."):
        print(chunk, end="")
        stream_chunks.append(chunk)
        time.sleep(0.1)  # Small delay to make the streaming visible
    print("\n")
    
    assert stream_chunks, "Streaming response should not be empty"
    return True

def test_json_response(client):
    """Test JSON response functionality."""
    print_section("Testing JSON Response")
    
    result = client.run_prompt(
        "Return a JSON object with the current date and a greeting message.",
        output_format=OutputFormat.JSON
    )
    print(f"JSON response: {json.dumps(result, indent=2)}")
    
    assert isinstance(result, dict), "JSON response should be a dictionary"
    return True

def test_conversation(client):
    """Test conversation functionality."""
    print_section("Testing Conversations")
    
    conversation = client.start_conversation()
    
    # First message
    print("Sending first message...")
    response1 = conversation.send("What are three key features of the Claude Code SDK?")
    print(f"First response:\n{response1}\n")
    
    # Follow-up message
    print("Sending follow-up message...")
    response2 = conversation.send("How would you implement the streaming feature?")
    print(f"Second response:\n{response2}\n")
    
    assert response1, "First conversation response should not be empty"
    assert response2, "Second conversation response should not be empty"
    return True

def test_tool_configuration(client):
    """Test tool configuration."""
    print_section("Testing Tool Configuration")
    
    # Configure client with specific tools
    client.configure(
        allowed_tools=["Bash(ls,echo)", "Glob", "Grep"],
        max_turns=10
    )
    
    result = client.run_prompt("What tools do you have access to?")
    print(f"Response with configured tools:\n{result}\n")
    
    assert result, "Tool configuration response should not be empty"
    return True

def test_aws_bedrock(region: Optional[str] = None, model: Optional[str] = None):
    """Test AWS Bedrock integration if credentials are available."""
    print_section("Testing AWS Bedrock Integration")
    
    if not region:
        region = os.environ.get("AWS_REGION")
    
    if not region:
        print("Skipping AWS Bedrock test - AWS_REGION not set")
        return False
    
    try:
        bedrock_client = ClaudeCode(
            auth_type=AuthType.AWS_BEDROCK,
            region=region,
            model=model or "anthropic.claude-3-7-sonnet-20250219-v1:0"
        )
        
        result = bedrock_client.run_prompt("What model are you using?")
        print(f"AWS Bedrock response:\n{result}\n")
        return True
    except ClaudeCodeError as e:
        print(f"AWS Bedrock test failed: {e}")
        return False

def test_google_vertex(project_id: Optional[str] = None, region: Optional[str] = None, model: Optional[str] = None):
    """Test Google Vertex AI integration if credentials are available."""
    print_section("Testing Google Vertex AI Integration")
    
    if not project_id:
        project_id = os.environ.get("ANTHROPIC_VERTEX_PROJECT_ID")
    
    if not region:
        region = os.environ.get("CLOUD_ML_REGION")
    
    if not project_id or not region:
        print("Skipping Google Vertex AI test - required environment variables not set")
        return False
    
    try:
        vertex_client = ClaudeCode(
            auth_type=AuthType.GOOGLE_VERTEX,
            project_id=project_id,
            region=region,
            model=model or "claude-3-7-sonnet@20250219"
        )
        
        result = vertex_client.run_prompt("What model are you using?")
        print(f"Google Vertex AI response:\n{result}\n")
        return True
    except ClaudeCodeError as e:
        print(f"Google Vertex AI test failed: {e}")
        return False

def run_all_tests():
    """Run all integration tests."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set. Please set it before running this test.")
        return
    
    # Create the client
    client = ClaudeCode(
        auth_type=AuthType.ANTHROPIC_API,
        api_key=api_key
    )
    
    results = {}
    
    # Run tests with direct API auth
    try:
        results["basic_prompt"] = test_basic_prompt(client)
        results["streaming"] = test_streaming(client)
        results["json_response"] = test_json_response(client)
        results["conversation"] = test_conversation(client)
        results["tool_configuration"] = test_tool_configuration(client)
    except ClaudeCodeError as e:
        print(f"Error during testing: {e}")
    
    # Test cloud provider integrations
    results["aws_bedrock"] = test_aws_bedrock()
    results["google_vertex"] = test_google_vertex()
    
    # Print summary
    print_section("Test Summary")
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED/SKIPPED"
        print(f"{test_name.ljust(20)}: {status}")

if __name__ == "__main__":
    print("Claude Code SDK Integration Test")
    print("===============================\n")
    run_all_tests()