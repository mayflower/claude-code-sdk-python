# Claude Code SDK Tutorial

This tutorial will guide you through using the Claude Code SDK in your Python applications. The SDK provides a convenient way to interact with Anthropic's Claude Code CLI directly from your Python code.

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#basic-usage)
- [Authentication Methods](#authentication-methods)
- [Working with Conversations](#working-with-conversations)
- [Streaming Responses](#streaming-responses)
- [JSON Responses](#json-responses)
- [Tool Configuration](#tool-configuration)
- [Error Handling](#error-handling)
- [Advanced Examples](#advanced-examples)

## Installation

First, ensure you have the Claude Code CLI installed:

```bash
npm install -g @anthropic-ai/claude-code
```

Then install the Python SDK:

```bash
pip install git+https://github.com/mayflower/claude-code-sdk-python.git
```

## Basic Usage

The simplest way to use the SDK is to create a client and send a one-shot prompt:

```python
from claude_code import ClaudeCode, AuthType

# Create a client using your Anthropic API key
claude = ClaudeCode(
    auth_type=AuthType.ANTHROPIC_API,
    api_key="your-api-key"  # Or use environment variable ANTHROPIC_API_KEY
)

# Send a prompt and get the response
response = claude.run_prompt("Explain how git branching works")
print(response)
```

If you're already logged in via the Claude Code CLI, you can also use the default authentication:

```python
from claude_code import ClaudeCode

# Use default authentication from CLI
claude = ClaudeCode()

response = claude.run_prompt("Write a Python function to parse JSON")
print(response)
```

## Authentication Methods

The SDK supports three authentication methods:

### 1. Direct Anthropic API

```python
from claude_code import ClaudeCode, AuthType

claude = ClaudeCode(
    auth_type=AuthType.ANTHROPIC_API,
    api_key="your-api-key"
)
```

### 2. AWS Bedrock

```python
from claude_code import ClaudeCode, AuthType

claude = ClaudeCode(
    auth_type=AuthType.AWS_BEDROCK,
    region="us-west-2",  # AWS region
    model="anthropic.claude-3-7-sonnet-20250219-v1:0"  # Bedrock model ID
)
```

### 3. Google Vertex AI

```python
from claude_code import ClaudeCode, AuthType

claude = ClaudeCode(
    auth_type=AuthType.GOOGLE_VERTEX,
    project_id="your-gcp-project-id",
    region="us-central1",
    model="claude-3-7-sonnet@20250219"  # Vertex AI model ID
)
```

## Working with Conversations

For multi-turn conversations, use the conversation API:

```python
from claude_code import ClaudeCode

claude = ClaudeCode()

# Start a conversation
conversation = claude.start_conversation()

# First message
response1 = conversation.send("Create a Python class for a blog post")
print(f"First response:\n{response1}\n")

# Follow-up message - Claude remembers the previous context
response2 = conversation.send("Add methods for managing comments")
print(f"Second response:\n{response2}\n")

# Continue the conversation
response3 = conversation.send("Now add a method to publish the post")
print(f"Third response:\n{response3}\n")
```

You can also limit the number of turns:

```python
conversation = claude.start_conversation(max_turns=5)
```

## Streaming Responses

For long responses or real-time interactions, use streaming:

```python
from claude_code import ClaudeCode

claude = ClaudeCode()

# Stream the response
print("Generating response...")
for chunk in claude.stream_prompt("Write a detailed explanation of how HTTPS works"):
    print(chunk, end="")  # Process each chunk as it arrives
print("\nDone!")
```

## JSON Responses

For structured output, use JSON format:

```python
from claude_code import ClaudeCode, OutputFormat
import json

claude = ClaudeCode()

# Get a JSON response
result = claude.run_prompt(
    "Generate a list of 5 programming book recommendations with title, author, and year",
    output_format=OutputFormat.JSON
)

# Process the JSON response
print(f"JSON response:\n{json.dumps(result, indent=2)}")

# Access specific fields
if "recommendations" in result:
    for book in result["recommendations"]:
        print(f"- {book['title']} by {book['author']} ({book['year']})")
```

You can also stream JSON responses:

```python
from claude_code import ClaudeCode, OutputFormat

claude = ClaudeCode()

# Stream JSON response
for chunk in claude.stream_prompt(
    "Generate a real-time report on CPU usage",
    output_format=OutputFormat.STREAM_JSON
):
    # Each chunk is a parsed JSON object
    print(f"Timestamp: {chunk['timestamp']}, CPU: {chunk['cpu_percent']}%")
```

## Tool Configuration

Configure which tools Claude has access to:

```python
from claude_code import ClaudeCode

# Create a client with specific tool access
claude = ClaudeCode(
    allowed_tools=["Bash(ls,git)", "Glob", "Read", "Write"]
)

# Or configure an existing client
claude.configure(
    allowed_tools=["Bash(ls,cat,find)", "Glob", "Grep", "LS", "Read"],
    max_turns=10
)

# Run a prompt that uses tools
result = claude.run_prompt("Find all Python files in the current directory")
print(result)
```

You can also disallow specific tools:

```python
claude = ClaudeCode(
    disallowed_tools=["Bash(rm,mv,cp)"]  # Prevent file modifications
)
```

## Error Handling

Handle errors gracefully:

```python
from claude_code import ClaudeCode
from claude_code.exceptions import (
    ClaudeCodeError,
    AuthenticationError,
    ExecutionError,
    TimeoutError,
    ValidationError
)

claude = ClaudeCode()

try:
    response = claude.run_prompt("Some prompt")
    print(response)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except TimeoutError as e:
    print(f"Request timed out: {e}")
except ValidationError as e:
    print(f"Invalid input: {e}")
except ExecutionError as e:
    print(f"Execution failed: {e}")
    # Access additional information
    print(f"Exit code: {e.exit_code}")
    print(f"Stdout: {e.stdout}")
    print(f"Stderr: {e.stderr}")
except ClaudeCodeError as e:
    # Base exception for all SDK errors
    print(f"An error occurred: {e}")
```

## Advanced Examples

### Executing Shell Commands with Bash Tool

```python
from claude_code import ClaudeCode

claude = ClaudeCode(allowed_tools=["Bash(ls,cat,grep)"])

response = claude.run_prompt("""
Please analyze the current directory:
1. List all files
2. Count the number of Python files
3. Find the largest file
""")

print(response)
```

### Building a File Search Utility

```python
from claude_code import ClaudeCode

claude = ClaudeCode(allowed_tools=["Glob", "Grep", "Read"])

def search_code(query, file_pattern="**/*.py"):
    """Search for code matching the query in files matching the pattern."""
    prompt = f"""
    Search for code related to "{query}" in files matching pattern "{file_pattern}".
    1. Find relevant files
    2. Locate the most relevant code sections
    3. Explain what you found
    """
    return claude.run_prompt(prompt)

# Usage
results = search_code("database connection", "**/*.py")
print(results)
```

### Creating a Documentation Generator

```python
from claude_code import ClaudeCode

claude = ClaudeCode(allowed_tools=["Glob", "Read", "Write"])

def generate_docs_for_module(module_path):
    """Generate markdown documentation for a Python module."""
    prompt = f"""
    Create comprehensive markdown documentation for the Python module at {module_path}:
    1. Read the module
    2. Identify all classes and functions
    3. Document each with descriptions, parameters, and return values
    4. Include examples of usage
    5. Create a table of contents
    Return the documentation as properly formatted markdown in your response (you'll need to save it to a file manually)
    """
    return claude.run_prompt(prompt)

# Usage
docs = generate_docs_for_module("my_project/utils.py")

# Save the documentation to a file
output_path = "my_project/utils_docs.md"
with open(output_path, "w") as f:
    f.write(docs)
    
print(f"Documentation generated and saved to {output_path}")
```

### AI-powered Code Review

```python
from claude_code import ClaudeCode

claude = ClaudeCode(allowed_tools=["Glob", "Grep", "Read"])

def code_review(file_paths):
    """Perform an AI code review on the specified files."""
    files_list = "\n".join(file_paths)
    prompt = f"""
    Perform a thorough code review of the following files:
    {files_list}
    
    For each file:
    1. Identify potential bugs or issues
    2. Suggest optimizations
    3. Check for security vulnerabilities
    4. Verify error handling
    5. Assess code style and readability
    
    Format your response as a detailed code review report.
    """
    return claude.run_prompt(prompt)

# Usage
review = code_review(["src/auth.py", "src/api.py", "src/models.py"])
print(review)
```

### Interactive AI Coding Assistant

```python
from claude_code import ClaudeCode

claude = ClaudeCode(allowed_tools=["Bash", "Glob", "Grep", "Read", "Edit", "Write"])

def interactive_coding_session():
    """Interactive session with the AI coding assistant."""
    conversation = claude.start_conversation()
    
    print("AI Coding Assistant (type 'exit' to quit)")
    print("-------------------------------------------")
    
    while True:
        user_input = input("\n> ")
        if user_input.lower() in ("exit", "quit"):
            break
            
        response = conversation.send(user_input)
        print(f"\n{response}")

# Usage
interactive_coding_session()
```

This tutorial provides an overview of the key features of the Claude Code SDK. For more detailed information, refer to the full API documentation.

## Complex Workflow Examples

Here are complete examples of how the Claude Code SDK can be integrated into complex workflows:

### CI/CD Pipeline Enhancement

This example shows how to integrate Claude Code into a CI/CD pipeline to improve code quality:

```python
import os
import json
import subprocess
from claude_code import ClaudeCode, OutputFormat

class CodeQualityGate:
    def __init__(self):
        # Initialize Claude with access to code analysis tools
        self.claude = ClaudeCode(
            allowed_tools=["Bash", "Glob", "Grep", "Read"]
        )
    
    def analyze_pull_request(self, repo_url, pull_request_id):
        """Analyze a GitHub pull request and provide code quality feedback."""
        # Clone repository
        repo_dir = f"/tmp/repo_{pull_request_id}"
        subprocess.run(f"git clone {repo_url} {repo_dir}", shell=True)
        os.chdir(repo_dir)
        
        # Checkout PR branch
        subprocess.run(f"git fetch origin pull/{pull_request_id}/head:pr_{pull_request_id}", shell=True)
        subprocess.run(f"git checkout pr_{pull_request_id}", shell=True)
        
        # Get changed files
        diff_output = subprocess.check_output("git diff --name-only origin/main", shell=True).decode()
        changed_files = [f for f in diff_output.split('\n') if f.strip()]
        
        # Analyze code with Claude
        analysis = self.claude.run_prompt(
            f"""
            Analyze the following changed files in this pull request:
            {', '.join(changed_files)}
            
            Provide the following in JSON format:
            1. A list of potential bugs or issues
            2. Security concerns
            3. Performance improvement suggestions
            4. Code quality score (0-100)
            5. Whether this PR should be approved or needs revision
            """,
            output_format=OutputFormat.JSON
        )
        
        # Post results as PR comment (simplified example)
        print(f"Analysis of PR #{pull_request_id}:")
        print(json.dumps(analysis, indent=2))
        
        # Fail CI if score is too low
        if analysis.get("code_quality_score", 0) < 70:
            print("❌ Code quality check failed - see detailed analysis above")
            return False
        
        print("✅ Code quality check passed")
        return True

# Usage in CI pipeline
if __name__ == "__main__":
    gate = CodeQualityGate()
    success = gate.analyze_pull_request(
        os.environ["GITHUB_REPO_URL"],
        os.environ["PULL_REQUEST_ID"]
    )
    if not success:
        exit(1)
```

### Automated Migration Tool

This example demonstrates using Claude to help migrate code between frameworks:

```python
import os
import logging
from claude_code import ClaudeCode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migration-tool")

class FrameworkMigrator:
    def __init__(self, source_dir, target_dir, source_framework, target_framework):
        self.source_dir = source_dir
        self.target_dir = target_dir
        self.source_framework = source_framework
        self.target_framework = target_framework
        
        # Initialize Claude with file access permissions
        self.claude = ClaudeCode(
            allowed_tools=["Glob", "Grep", "Read", "Write", "Edit"]
        )
        
        # Ensure target directory exists
        os.makedirs(self.target_dir, exist_ok=True)
    
    def analyze_project(self):
        """Analyze the source project structure and dependencies."""
        logger.info(f"Analyzing {self.source_framework} project...")
        
        analysis = self.claude.run_prompt(
            f"""
            Analyze the {self.source_framework} project in {self.source_dir}.
            
            1. List all source files
            2. Identify third-party dependencies
            3. Determine the project structure
            4. Identify key components that need migration
            
            Create a migration plan for converting this to {self.target_framework}.
            """
        )
        
        logger.info("Analysis complete")
        return analysis
    
    def migrate_file(self, source_file):
        """Migrate a single file from source framework to target framework."""
        # Calculate relative path and create target path
        rel_path = os.path.relpath(source_file, self.source_dir)
        
        # Adjust file extension based on frameworks
        if self.source_framework == "React" and self.target_framework == "Vue":
            # React .jsx -> Vue .vue
            if rel_path.endswith('.jsx'):
                rel_path = rel_path[:-4] + '.vue'
        
        target_file = os.path.join(self.target_dir, rel_path)
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        
        logger.info(f"Migrating {rel_path}")
        
        # Use Claude to convert the file
        result = self.claude.run_prompt(
            f"""
            Convert this {self.source_framework} file to {self.target_framework}.
            
            Source file: {source_file}
            Target file: {target_file}
            
            1. Read the source file
            2. Understand its functionality
            3. Create a {self.target_framework} equivalent
            4. Write the converted code to the target file
            5. Return a summary of the changes made
            """
        )
        
        logger.info(f"Migrated {rel_path}")
        return result
    
    def migrate_project(self):
        """Migrate the entire project."""
        # Analyze the project first
        migration_plan = self.analyze_project()
        print(f"Migration Plan:\n{migration_plan}\n")
        
        # Find source files
        if self.source_framework == "React":
            source_files = self.claude.run_prompt(
                f"""
                Find all React component files in {self.source_dir}.
                Run appropriate glob commands to locate .js, .jsx, and .tsx files.
                Return only the list of files, one per line.
                """
            ).strip().split('\n')
        elif self.source_framework == "Angular":
            source_files = self.claude.run_prompt(
                f"""
                Find all Angular component files in {self.source_dir}.
                Run appropriate glob commands to locate .ts files that contain Components.
                Return only the list of files, one per line.
                """
            ).strip().split('\n')
        else:
            # Generic file finding
            source_files = self.claude.run_prompt(
                f"""
                Find all source code files in {self.source_dir} that need migration.
                Return only the list of files, one per line.
                """
            ).strip().split('\n')
        
        # Migrate each file
        for file in source_files:
            if not file.strip():
                continue
            try:
                summary = self.migrate_file(file.strip())
                print(f"✅ {file}: {summary.splitlines()[0]}")
            except Exception as e:
                logger.error(f"Error migrating {file}: {e}")
                print(f"❌ {file}: Failed")
        
        # Update dependencies
        self.update_dependencies()
        
        logger.info("Migration complete!")
    
    def update_dependencies(self):
        """Update the project dependencies for the target framework."""
        logger.info("Updating dependencies...")
        
        self.claude.run_prompt(
            f"""
            Create appropriate dependency files for the {self.target_framework} project.
            
            1. Examine the {self.source_framework} dependencies
            2. Determine equivalent {self.target_framework} dependencies
            3. Create package.json or equivalent file in {self.target_dir}
            4. Include all necessary dependencies
            """
        )

# Usage
if __name__ == "__main__":
    migrator = FrameworkMigrator(
        source_dir="./legacy-react-app",
        target_dir="./new-vue-app",
        source_framework="React",
        target_framework="Vue"
    )
    migrator.migrate_project()
```

### AI-Augmented Development Workflow

This example shows how to integrate Claude Code into a developer workflow with git hooks and custom commands:

```python
import os
import sys
import argparse
import subprocess
from claude_code import ClaudeCode

class AIDevAssistant:
    def __init__(self):
        self.claude = ClaudeCode(
            allowed_tools=["Bash", "Glob", "Grep", "Read", "Edit"]
        )
        self.repo_root = subprocess.check_output(
            "git rev-parse --show-toplevel", shell=True
        ).decode().strip()
    
    def setup_git_hooks(self):
        """Set up git hooks to use AI assistance."""
        # Create pre-commit hook
        hook_path = os.path.join(self.repo_root, ".git/hooks/pre-commit")
        
        with open(hook_path, "w") as f:
            f.write(f"""#!/bin/bash
            # Pre-commit hook with AI assistance
            python {os.path.abspath(__file__)} pre-commit
            """)
        
        os.chmod(hook_path, 0o755)
        print(f"✅ Installed AI pre-commit hook to {hook_path}")
        
        # Create commit-msg hook
        hook_path = os.path.join(self.repo_root, ".git/hooks/commit-msg")
        
        with open(hook_path, "w") as f:
            f.write(f"""#!/bin/bash
            # Commit message hook with AI assistance
            python {os.path.abspath(__file__)} improve-commit-msg $1
            """)
        
        os.chmod(hook_path, 0o755)
        print(f"✅ Installed AI commit-msg hook to {hook_path}")
    
    def pre_commit_review(self):
        """Review staged changes before commit."""
        print("🔍 AI pre-commit code review in progress...")
        
        # Get staged files
        staged_files = subprocess.check_output(
            "git diff --cached --name-only", shell=True
        ).decode().strip().split('\n')
        
        if not staged_files or not staged_files[0]:
            print("No files staged for commit")
            return True
        
        # Ask Claude to review the changes
        result = self.claude.run_prompt(
            f"""
            Review the staged changes in this git repository.
            Focus on:
            1. Code quality issues
            2. Potential bugs
            3. Security vulnerabilities
            4. Test coverage
            
            Files to review: {', '.join(staged_files)}
            
            If there are issues that should block the commit, clearly mark them as "BLOCKING".
            If there are only minor suggestions, mark them as "NON-BLOCKING".
            """
        )
        
        print("\n===== AI Code Review =====")
        print(result)
        print("=========================\n")
        
        if "BLOCKING" in result:
            print("❌ AI review found blocking issues. Fix them or use --no-verify to bypass.")
            return False
        
        print("✅ AI review passed with no blocking issues")
        return True
    
    def improve_commit_message(self, commit_msg_file):
        """Improve the commit message."""
        # Read the original commit message
        with open(commit_msg_file, 'r') as f:
            original_msg = f.read()
        
        if original_msg.startswith("AI:"):
            # Already AI-improved
            return True
        
        # Get the staged changes for context
        diff = subprocess.check_output(
            "git diff --cached", shell=True
        ).decode()
        
        # Ask Claude to improve the message
        improved_msg = self.claude.run_prompt(
            f"""
            Improve this git commit message based on the diff:
            
            Original message:
            {original_msg}
            
            Diff of changes:
            {diff[:10000]}  # Limit diff size
            
            Create a commit message following best practices:
            1. Start with a short, clear summary line (50 chars or less)
            2. Leave a blank line after the summary
            3. Provide a detailed explanation of what changed and why
            4. Mention any breaking changes or important notes
            5. Add "AI:" prefix to indicate AI assistance
            
            Return only the new commit message text with no additional formatting.
            """
        )
        
        # Ensure it starts with "AI:"
        if not improved_msg.startswith("AI:"):
            improved_msg = f"AI: {improved_msg}"
        
        # Write the improved message
        with open(commit_msg_file, 'w') as f:
            f.write(improved_msg)
        
        print("✅ Commit message improved by AI")
        return True
    
    def help_with_task(self, task_description):
        """Get AI help with a development task."""
        print(f"🤖 Getting AI assistance for: {task_description}")
        
        # Ask Claude for help
        response = self.claude.run_prompt(
            f"""
            Help with this development task in the current repository:
            
            Task: {task_description}
            
            1. Understand the current codebase
            2. Provide a step-by-step plan
            3. Suggest code modifications or new code to implement
            4. Consider testing and error handling
            """
        )
        
        print("\n===== AI Task Assistance =====")
        print(response)
        print("=============================\n")
    
    def generate_tests(self, file_path):
        """Generate tests for a specific file."""
        print(f"🧪 Generating tests for: {file_path}")
        
        # Determine test framework
        if os.path.exists(os.path.join(self.repo_root, "jest.config.js")):
            test_framework = "Jest"
        elif os.path.exists(os.path.join(self.repo_root, "pytest.ini")):
            test_framework = "pytest"
        else:
            test_framework = "determine automatically"
        
        # Generate tests
        test_code = self.claude.run_prompt(
            f"""
            Generate comprehensive tests for the file at {file_path}.
            
            1. Read the file
            2. Understand its functionality
            3. Create tests using the {test_framework} framework
            4. Include edge cases and error conditions
            5. Write the tests to an appropriate test file
            
            Return the path to the generated test file and a summary of the tests.
            """
        )
        
        print("\n===== Generated Tests =====")
        print(test_code)
        print("=========================\n")

# Command-line interface
if __name__ == "__main__":
    assistant = AIDevAssistant()
    
    parser = argparse.ArgumentParser(description="AI Development Assistant")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    parser.add_argument("--setup", action="store_true", help="Set up git hooks")
    
    task_parser = subparsers.add_parser("task", help="Get help with a development task")
    task_parser.add_argument("description", help="Description of the task")
    
    test_parser = subparsers.add_parser("test", help="Generate tests for a file")
    test_parser.add_argument("file", help="File to generate tests for")
    
    review_parser = subparsers.add_parser("review", help="Review current changes")
    
    commit_msg_parser = subparsers.add_parser("improve-commit-msg", help="Improve commit message")
    commit_msg_parser.add_argument("file", help="Commit message file")
    
    subparsers.add_parser("pre-commit", help="Run pre-commit checks")
    
    args = parser.parse_args()
    
    if args.setup:
        assistant.setup_git_hooks()
    elif args.command == "task":
        assistant.help_with_task(args.description)
    elif args.command == "test":
        assistant.generate_tests(args.file)
    elif args.command == "review":
        assistant.pre_commit_review()
    elif args.command == "improve-commit-msg":
        assistant.improve_commit_message(args.file)
    elif args.command == "pre-commit":
        result = assistant.pre_commit_review()
        if not result:
            sys.exit(1)
    else:
        parser.print_help()
```

### Automated Documentation System

This example demonstrates building a complete documentation system powered by Claude:

```python
import os
import re
import json
import shutil
import markdown
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from claude_code import ClaudeCode, OutputFormat

class DocumentationGenerator:
    def __init__(self, source_dir, output_dir, project_name):
        self.source_dir = os.path.abspath(source_dir)
        self.output_dir = os.path.abspath(output_dir)
        self.project_name = project_name
        self.claude = ClaudeCode(
            allowed_tools=["Glob", "Read", "Grep"]
        )
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Set up Jinja for templates
        self.templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = Environment(loader=FileSystemLoader(self.templates_dir))
    
    def create_project_structure(self):
        """Analyze the project structure."""
        print("📚 Analyzing project structure...")
        
        structure = self.claude.run_prompt(
            f"""
            Analyze the project structure in {self.source_dir}.
            
            Create a JSON representation with:
            1. Main components/modules
            2. How they relate to each other
            3. Key files in each component
            4. Dependencies between components
            
            Return the result as valid JSON.
            """,
            output_format=OutputFormat.JSON
        )
        
        return structure
    
    def document_component(self, component_path, component_name):
        """Generate documentation for a specific component."""
        print(f"📝 Documenting component: {component_name}")
        
        # Get detailed docs for the component
        component_docs = self.claude.run_prompt(
            f"""
            Create comprehensive documentation for the {component_name} component at {component_path}.
            
            Include:
            1. Overview and purpose
            2. API documentation
            3. Usage examples
            4. Internal architecture
            5. Dependencies
            
            Format the documentation in Markdown.
            """
        )
        
        # Save the docs
        output_path = os.path.join(self.output_dir, "components", f"{component_name}.md")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w") as f:
            f.write(component_docs)
        
        return {
            "name": component_name,
            "path": os.path.relpath(output_path, self.output_dir),
            "content_snippet": component_docs[:200] + "..."
        }
    
    def create_api_reference(self):
        """Generate API reference documentation."""
        print("🔍 Creating API reference...")
        
        api_docs = self.claude.run_prompt(
            f"""
            Create a comprehensive API reference for the project in {self.source_dir}.
            
            For each public API:
            1. Function/method signature
            2. Parameter descriptions
            3. Return value(s)
            4. Examples
            5. Notes and caveats
            
            Format the documentation in Markdown, organized by module/component.
            """
        )
        
        # Save the API reference
        output_path = os.path.join(self.output_dir, "api-reference.md")
        with open(output_path, "w") as f:
            f.write(api_docs)
        
        return os.path.relpath(output_path, self.output_dir)
    
    def create_getting_started(self):
        """Create a getting started guide."""
        print("🚀 Creating getting started guide...")
        
        guide = self.claude.run_prompt(
            f"""
            Create a comprehensive getting started guide for the project in {self.source_dir}.
            
            Include:
            1. Installation instructions
            2. Basic configuration
            3. Simple usage examples
            4. Common patterns
            5. Troubleshooting tips
            
            Format the documentation in Markdown.
            """
        )
        
        # Save the guide
        output_path = os.path.join(self.output_dir, "getting-started.md")
        with open(output_path, "w") as f:
            f.write(guide)
        
        return os.path.relpath(output_path, self.output_dir)
    
    def generate_complete_docs(self):
        """Generate complete documentation."""
        print(f"📖 Generating documentation for {self.project_name}...")
        
        # Create basic structure and copy assets
        os.makedirs(os.path.join(self.output_dir, "assets"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "components"), exist_ok=True)
        
        # Analyze project structure
        structure = self.create_project_structure()
        
        # Document each component
        component_docs = []
        for component in structure.get("components", []):
            component_info = self.document_component(
                os.path.join(self.source_dir, component["path"]),
                component["name"]
            )
            component_docs.append(component_info)
        
        # Create API reference
        api_reference_path = self.create_api_reference()
        
        # Create getting started guide
        getting_started_path = self.create_getting_started()
        
        # Generate index page
        template = self.jinja_env.get_template("index.html")
        index_content = template.render(
            project_name=self.project_name,
            generation_date=datetime.now().strftime("%Y-%m-%d"),
            components=component_docs,
            api_reference_path=api_reference_path,
            getting_started_path=getting_started_path,
            project_structure=json.dumps(structure, indent=2)
        )
        
        with open(os.path.join(self.output_dir, "index.html"), "w") as f:
            f.write(index_content)
        
        print(f"✅ Documentation generated successfully in {self.output_dir}")
        
        # Create a summary
        summary = self.claude.run_prompt(
            f"""
            Create a summary of the documentation generated for {self.project_name}.
            
            Include:
            1. Overview of content created
            2. Key components documented
            3. Special features or APIs highlighted
            4. Suggestions for future documentation improvements
            
            Keep it concise but informative.
            """
        )
        
        print("\n===== Documentation Summary =====")
        print(summary)
        print("===============================\n")
        
        return self.output_dir

# Usage
if __name__ == "__main__":
    generator = DocumentationGenerator(
        source_dir="./my-project",
        output_dir="./docs",
        project_name="MyAwesomeProject"
    )
    generator.generate_complete_docs()
```