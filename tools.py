import subprocess


def run_bash_command(command: str) -> str:
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=30
        )
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Execution Error: {str(e)}"


tools = [
    {
        "type": "function",
        "function": {
            "name": "run_bash_command",
            "description": "Run a shell command in a Linux terminal to manage files or check system state.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The full bash command to execute.",
                    }
                },
                "required": ["command"],
            },
        },
    }
]
