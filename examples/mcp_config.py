"""
Example using Claude Code with MCP configuration.
"""

import os
import json
import tempfile
from claude_code import ClaudeCode, AuthType


def main():
    """Run with MCP configuration."""
    # Create a temporary MCP config file
    mcp_config = {
        "mcpServers": {
            "example-server": {
                "command": "node",
                "args": ["./server.js"],
                "env": {
                    "API_KEY": "your-api-key"
                }
            }
        }
    }
    
    # Write config to temporary file
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(mcp_config, f)
        config_path = f.name
    
    try:
        # Create client with MCP config
        claude = ClaudeCode(
            auth_type=AuthType.ANTHROPIC_API,
            api_key=os.environ.get("ANTHROPIC_API_KEY"),
            mcp_config=config_path,
            allowed_tools=["mcp__example-server__custom_tool"]
        )
        
        # Run a prompt that uses the MCP server
        print("Running prompt with MCP configuration...")
        print("Note: This example requires an actual MCP server to work")
        result = claude.run_prompt("Use the custom MCP tool to do something")
        print(result)
    
    finally:
        # Clean up the temporary file
        os.unlink(config_path)


if __name__ == "__main__":
    main()