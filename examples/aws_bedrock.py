"""
Example using Claude Code with AWS Bedrock.
"""

import os
from claude_code import ClaudeCode, AuthType


def main():
    """Run a Bedrock-authenticated prompt."""
    # Create a client with AWS Bedrock authentication
    claude = ClaudeCode(
        auth_type=AuthType.AWS_BEDROCK,
        region=os.environ.get("AWS_REGION", "us-west-2"),
        model="anthropic.claude-3-7-sonnet-20250219-v1:0"
    )
    
    # Run a simple prompt
    result = claude.run_prompt("What model are you using?")
    print(result)


if __name__ == "__main__":
    main()