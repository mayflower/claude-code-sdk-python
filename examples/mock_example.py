"""
Example of using Claude Code SDK with mocked responses.
"""

import os
from unittest.mock import patch
from claude_code import ClaudeCode, AuthType

# Mock the subprocess.run function to return a canned response
@patch('subprocess.run')
def main(mock_run):
    # Set up the mock to return a successful response
    mock_process = type('MockProcess', (), {
        'returncode': 0,
        'stdout': b"This is a mock response from Claude Code.",
        'stderr': b""
    })
    mock_run.return_value = mock_process

    # Create a client with dummy API key
    claude = ClaudeCode(
        auth_type=AuthType.ANTHROPIC_API,
        api_key="dummy-api-key"
    )
    
    # Run a simple prompt
    print("Sending prompt to mocked Claude Code...")
    result = claude.run_prompt("Tell me about Claude Code SDK.")
    print(f"Response: {result}")

    # Create a conversation
    print("\nStarting a mock conversation...")
    conversation = claude.start_conversation()
    
    # First message
    response1 = conversation.send("What can I do with the SDK?")
    print(f"First response: {response1}")
    
    # Follow-up message
    response2 = conversation.send("How do I use streaming?")
    print(f"Second response: {response2}")

if __name__ == "__main__":
    print("Claude Code SDK Mock Example")
    print("--------------------------\n")
    main()