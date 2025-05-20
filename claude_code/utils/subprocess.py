"""
Subprocess utilities for Claude Code.
"""

import json
import os
import subprocess
import tempfile
from typing import Dict, Iterator, List, Optional, Tuple, Union, IO

from ..exceptions import ExecutionError, TimeoutError


def run_command(
    cmd: List[str],
    env: Optional[Dict[str, str]] = None,
    timeout: Optional[int] = None,
    input_data: Optional[str] = None,
) -> Tuple[int, str, str]:
    """
    Run a command and return its exit code, stdout, and stderr.

    Args:
        cmd: Command to run, as a list of strings.
        env: Environment variables to set for the command.
        timeout: Timeout in seconds.
        input_data: Data to pass to the command's stdin.

    Returns:
        Tuple of (exit_code, stdout, stderr).

    Raises:
        TimeoutError: If the command times out.
        ExecutionError: If there's an error running the command.
    """
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)

    stdin = subprocess.PIPE if input_data else None

    try:
        result = subprocess.run(
            cmd,
            env=merged_env,
            input=input_data.encode("utf-8") if input_data else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        return (
            result.returncode,
            result.stdout.decode("utf-8", errors="replace"),
            result.stderr.decode("utf-8", errors="replace"),
        )
    except subprocess.TimeoutExpired as e:
        stdout = e.stdout.decode("utf-8", errors="replace") if e.stdout else ""
        stderr = e.stderr.decode("utf-8", errors="replace") if e.stderr else ""
        raise TimeoutError(
            f"Command timed out after {timeout} seconds",
            exit_code=None,
            stdout=stdout,
            stderr=stderr,
        ) from e
    except subprocess.SubprocessError as e:
        raise ExecutionError(f"Error running command: {e}") from e


def stream_command(
    cmd: List[str],
    env: Optional[Dict[str, str]] = None,
    timeout: Optional[int] = None,
    input_data: Optional[str] = None,
) -> Iterator[str]:
    """
    Run a command and stream its stdout.

    Args:
        cmd: Command to run, as a list of strings.
        env: Environment variables to set for the command.
        timeout: Timeout in seconds.
        input_data: Data to pass to the command's stdin.

    Yields:
        Lines from the command's stdout.

    Raises:
        TimeoutError: If the command times out.
        ExecutionError: If there's an error running the command.
    """
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)

    # If we have input data, write it to a temporary file and redirect from it
    stdin_file: Optional[IO] = None
    if input_data:
        stdin_file = tempfile.NamedTemporaryFile(mode="w+", encoding="utf-8")
        stdin_file.write(input_data)
        stdin_file.flush()
        stdin_file.seek(0)

    try:
        process = subprocess.Popen(
            cmd,
            env=merged_env,
            stdin=stdin_file if stdin_file else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1,  # Line buffered
        )

        # Set up a timeout if requested
        if timeout:
            import threading
            
            def kill_process():
                if process.poll() is None:
                    process.kill()
            
            timer = threading.Timer(timeout, kill_process)
            timer.start()

        # Stream stdout
        for line in process.stdout:
            yield line.rstrip("\n")

        # Wait for the process to finish
        exit_code = process.wait()

        # Cancel the timeout timer if it's still active
        if timeout:
            timer.cancel()

        # If the process failed, raise an ExecutionError
        if exit_code != 0:
            stderr = process.stderr.read() if process.stderr else ""
            raise ExecutionError(
                f"Command failed with exit code {exit_code}",
                exit_code=exit_code,
                stdout="",
                stderr=stderr,
            )

    except Exception as e:
        # Make sure we kill the process if something goes wrong
        if "process" in locals() and process.poll() is None:
            process.kill()
            process.wait()
        
        if isinstance(e, TimeoutError) or isinstance(e, ExecutionError):
            raise
        raise ExecutionError(f"Error running command: {e}") from e
    
    finally:
        # Clean up the temporary file if we created one
        if stdin_file:
            stdin_file.close()


def stream_json_command(
    cmd: List[str],
    env: Optional[Dict[str, str]] = None,
    timeout: Optional[int] = None,
    input_data: Optional[str] = None,
) -> Iterator[Dict]:
    """
    Run a command and stream its stdout as JSON objects.

    Args:
        cmd: Command to run, as a list of strings.
        env: Environment variables to set for the command.
        timeout: Timeout in seconds.
        input_data: Data to pass to the command's stdin.

    Yields:
        Parsed JSON objects from the command's stdout.

    Raises:
        TimeoutError: If the command times out.
        ExecutionError: If there's an error running the command.
        ValueError: If there's an error parsing the JSON.
    """
    for line in stream_command(cmd, env, timeout, input_data):
        if not line.strip():
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON from command output: {e}") from e