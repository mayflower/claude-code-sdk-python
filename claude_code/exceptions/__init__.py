"""
Exceptions for Claude Code SDK.
"""

class ClaudeCodeError(Exception):
    """Base exception for all Claude Code errors."""
    pass


class AuthenticationError(ClaudeCodeError):
    """Error occurred during authentication."""
    pass


class ValidationError(ClaudeCodeError):
    """Error validating input parameters."""
    pass


class ExecutionError(ClaudeCodeError):
    """Error occurred during Claude Code execution."""
    
    def __init__(self, message, exit_code=None, stdout=None, stderr=None):
        super().__init__(message)
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr


class TimeoutError(ExecutionError):
    """Timeout occurred during Claude Code execution."""
    pass