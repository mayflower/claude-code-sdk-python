"""
Example using Claude Code with Google Vertex AI.
"""

import os
from claude_code import ClaudeCode, AuthType


def main():
    """Run a Vertex AI-authenticated prompt."""
    # Create a client with Google Vertex AI authentication
    claude = ClaudeCode(
        auth_type=AuthType.GOOGLE_VERTEX,
        region=os.environ.get("CLOUD_ML_REGION", "us-central1"),
        project_id=os.environ.get("ANTHROPIC_VERTEX_PROJECT_ID"),
        model="claude-3-7-sonnet@20250219"
    )
    
    # Run a simple prompt
    result = claude.run_prompt("What model are you using?")
    print(result)


if __name__ == "__main__":
    main()