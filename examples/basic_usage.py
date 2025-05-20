"""
Basic usage examples for Claude Code SDK.
"""

import os
from claude_code import ClaudeCode, AuthType, OutputFormat


def simple_prompt():
    """Simple prompt example."""
    # Create a client with API key from environment
    claude = ClaudeCode(
        auth_type=AuthType.ANTHROPIC_API,
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    # Run a simple prompt
    result = claude.run_prompt("Explain how git works in one paragraph")
    print(result)


def streaming_response():
    """Streaming response example."""
    claude = ClaudeCode(
        auth_type=AuthType.ANTHROPIC_API,
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    # Stream the response
    print("Streaming response:")
    for chunk in claude.stream_prompt("Write a short Python function to calculate Fibonacci numbers"):
        print(chunk, end="")


def json_response():
    """JSON response example."""
    claude = ClaudeCode(
        auth_type=AuthType.ANTHROPIC_API,
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    # Get JSON response
    result = claude.run_prompt(
        "Return a JSON object with the first 5 Fibonacci numbers",
        output_format=OutputFormat.JSON
    )
    print(f"JSON response: {result}")


def conversation_example():
    """Multi-turn conversation example."""
    claude = ClaudeCode(
        auth_type=AuthType.ANTHROPIC_API,
        api_key=os.environ.get("ANTHROPIC_API_KEY")
    )
    
    # Start a conversation
    conversation = claude.start_conversation()
    
    # First message
    response1 = conversation.send("Create a Python class for a blog post")
    print("First response:")
    print(response1)
    print("\n" + "-" * 50 + "\n")
    
    # Follow-up message
    response2 = conversation.send("Add methods for adding and viewing comments")
    print("Second response:")
    print(response2)


def tool_usage_example():
    """Example with tool configuration."""
    claude = ClaudeCode(
        auth_type=AuthType.ANTHROPIC_API,
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        allowed_tools=["Bash(ls,cat,find)", "GlobTool", "GrepTool"]
    )
    
    # Run a prompt that uses tools
    result = claude.run_prompt("List all Python files in the current directory")
    print(result)


if __name__ == "__main__":
    # Uncomment the example you want to run
    simple_prompt()
    # streaming_response()
    # json_response()
    # conversation_example()
    # tool_usage_example()