from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path.cwd().resolve()


def _resolve_path(path: str) -> Path:
    candidate = (WORKSPACE_ROOT / path).resolve()
    if not str(candidate).startswith(str(WORKSPACE_ROOT)):
        raise ValueError("Path escapes workspace root")
    return candidate


def read_file(path: str, start_line: int = 1, end_line: int | None = None) -> str:
    try:
        file_path = _resolve_path(path)
        if not file_path.exists() or not file_path.is_file():
            return f"Error: File not found: {path}"

        with file_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        if start_line < 1:
            return "Error: start_line must be >= 1"

        start_idx = start_line - 1
        end_idx = end_line if end_line is not None else len(lines)

        if start_idx >= len(lines):
            return ""

        return "".join(lines[start_idx:end_idx])
    except Exception as e:
        return f"Execution Error: {str(e)}"


def edit_file(path: str, old_text: str, new_text: str) -> str:
    try:
        file_path = _resolve_path(path)
        if not file_path.exists() or not file_path.is_file():
            return f"Error: File not found: {path}"

        content = file_path.read_text(encoding="utf-8")
        occurrences = content.count(old_text)

        if occurrences == 0:
            return "Error: old_text not found in file"
        if occurrences > 1:
            return "Error: old_text appears multiple times; provide more specific text"

        updated = content.replace(old_text, new_text, 1)
        file_path.write_text(updated, encoding="utf-8")
        return "OK"
    except Exception as e:
        return f"Execution Error: {str(e)}"


def write_file(path: str, content: str) -> str:
    try:
        file_path = _resolve_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return "OK"
    except Exception as e:
        return f"Execution Error: {str(e)}"


def list_files(path: str = ".", recursive: bool = False) -> str:
    try:
        base = _resolve_path(path)
        if not base.exists() or not base.is_dir():
            return f"Error: Directory not found: {path}"

        iterator = base.rglob("*") if recursive else base.iterdir()
        files = [str(p.relative_to(WORKSPACE_ROOT)) for p in iterator]
        files.sort()
        return "\n".join(files)
    except Exception as e:
        return f"Execution Error: {str(e)}"


def search_text(query: str, path: str = ".") -> str:
    try:
        base = _resolve_path(path)
        if not base.exists():
            return f"Error: Path not found: {path}"

        if shutil.which("rg"):
            result = subprocess.run(
                ["rg", "-n", "--no-heading", query, str(base)],
                capture_output=True,
                text=True,
                timeout=30,
            )
            output = result.stdout.strip() or result.stderr.strip()
            return output or "No matches found"

        matches: list[str] = []
        for file_path in base.rglob("*"):
            if not file_path.is_file():
                continue
            try:
                for line_no, line in enumerate(
                    file_path.read_text(encoding="utf-8", errors="ignore").splitlines(),
                    start=1,
                ):
                    if query in line:
                        rel = file_path.relative_to(WORKSPACE_ROOT)
                        matches.append(f"{rel}:{line_no}:{line}")
            except Exception:
                continue

        return "\n".join(matches) if matches else "No matches found"
    except Exception as e:
        return f"Execution Error: {str(e)}"


def find_files(pattern: str, path: str = ".") -> str:
    try:
        base = _resolve_path(path)
        if not base.exists() or not base.is_dir():
            return f"Error: Directory not found: {path}"

        matches = [
            str(p.relative_to(WORKSPACE_ROOT))
            for p in base.rglob(pattern)
            if p.exists() and p.is_file()
        ]
        matches.sort()
        return "\n".join(matches) if matches else "No matches found"
    except Exception as e:
        return f"Execution Error: {str(e)}"


def move_file(source_path: str, destination_path: str) -> str:
    try:
        source = _resolve_path(source_path)
        destination = _resolve_path(destination_path)
        if not source.exists():
            return f"Error: Source not found: {source_path}"

        destination.parent.mkdir(parents=True, exist_ok=True)
        source.rename(destination)
        return "OK"
    except Exception as e:
        return f"Execution Error: {str(e)}"


def delete_file(path: str, recursive: bool = False) -> str:
    try:
        target = _resolve_path(path)
        if not target.exists():
            return f"Error: Path not found: {path}"

        if target.is_dir():
            if not recursive:
                return "Error: Target is a directory. Set recursive=true to delete it"
            shutil.rmtree(target)
        else:
            target.unlink()

        return "OK"
    except Exception as e:
        return f"Execution Error: {str(e)}"


def apply_patch(path: str, old_text: str, new_text: str) -> str:
    """Apply a patch-like replacement to a file via exact-match replacement."""
    return edit_file(path=path, old_text=old_text, new_text=new_text)


tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a UTF-8 text file. Optionally limit by start and end line numbers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Path to the file."},
                    "start_line": {
                        "type": "integer",
                        "description": "1-based start line number.",
                        "default": 1,
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "1-based end line number (exclusive).",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": "Edit a file by replacing one unique exact text block with new text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "old_text": {"type": "string"},
                    "new_text": {"type": "string"},
                },
                "required": ["path", "old_text", "new_text"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Create or overwrite a UTF-8 text file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories under a path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "default": "."},
                    "recursive": {"type": "boolean", "default": False},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_text",
            "description": "Search for text in files under a path and return matching lines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "path": {"type": "string", "default": "."},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_files",
            "description": "Find files matching a glob pattern under a path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {"type": "string"},
                    "path": {"type": "string", "default": "."},
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "move_file",
            "description": "Move or rename a file or directory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_path": {"type": "string"},
                    "destination_path": {"type": "string"},
                },
                "required": ["source_path", "destination_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_file",
            "description": "Delete a file. Can also delete a directory if recursive=true.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "recursive": {"type": "boolean", "default": False},
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "apply_patch",
            "description": "Patch helper: applies one exact text replacement in a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "old_text": {"type": "string"},
                    "new_text": {"type": "string"},
                },
                "required": ["path", "old_text", "new_text"],
            },
        },
    },
]
