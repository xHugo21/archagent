from __future__ import annotations

import inspect
import json
import shutil
import subprocess
import types
from pathlib import Path
from typing import Any, Union, get_args, get_origin, get_type_hints

WORKSPACE_ROOT = Path.cwd().resolve()
_TOOL_REGISTRY: dict[str, dict[str, Any]] = {}


def _resolve_path(path: str) -> Path:
    candidate = (WORKSPACE_ROOT / path).resolve()
    if not str(candidate).startswith(str(WORKSPACE_ROOT)):
        raise ValueError("Path escapes workspace root")
    return candidate


def _python_type_to_schema(annotation: Any) -> dict[str, Any]:
    origin = get_origin(annotation)

    if origin in (Union, types.UnionType):
        args = get_args(annotation)
        non_none_args = [arg for arg in args if arg is not type(None)]

        if len(non_none_args) == 1 and len(non_none_args) != len(args):
            schema = _python_type_to_schema(non_none_args[0])
            schema["nullable"] = True
            return schema

        return {"anyOf": [_python_type_to_schema(arg) for arg in args]}

    if origin in (list, tuple, set):
        return {"type": "array"}
    if origin is dict:
        return {"type": "object"}

    if annotation is str:
        return {"type": "string"}
    if annotation is int:
        return {"type": "integer"}
    if annotation is float:
        return {"type": "number"}
    if annotation is bool:
        return {"type": "boolean"}

    return {"type": "string"}


def tool(description: str):
    def decorator(func):
        signature = inspect.signature(func)
        type_hints = get_type_hints(func)

        properties: dict[str, Any] = {}
        required: list[str] = []

        for name, param in signature.parameters.items():
            annotation = type_hints.get(name, str)
            prop_schema = _python_type_to_schema(annotation)

            if param.default is not inspect._empty:
                default_value = param.default
                # Keep defaults JSON-safe where possible.
                try:
                    json.dumps(default_value)
                    prop_schema["default"] = default_value
                except TypeError:
                    pass
            else:
                required.append(name)

            properties[name] = prop_schema

        function_schema: dict[str, Any] = {
            "name": func.__name__,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
            },
        }

        if required:
            function_schema["parameters"]["required"] = required

        _TOOL_REGISTRY[func.__name__] = {
            "type": "function",
            "function": function_schema,
        }

        return func

    return decorator


@tool("Read a UTF-8 text file. Optionally limit by start and end line numbers.")
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


@tool("Edit a file by replacing one unique exact text block with new text.")
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


@tool("Create or overwrite a UTF-8 text file.")
def write_file(path: str, content: str) -> str:
    try:
        file_path = _resolve_path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return "OK"
    except Exception as e:
        return f"Execution Error: {str(e)}"


@tool("List files and directories under a path.")
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


@tool("Search for text in files under a path and return matching lines.")
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


@tool("Find files matching a glob pattern under a path.")
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


@tool("Move or rename a file or directory.")
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


@tool("Delete a file. Can also delete a directory if recursive=true.")
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


@tool("Patch helper: applies one exact text replacement in a file.")
def apply_patch(path: str, old_text: str, new_text: str) -> str:
    """Apply a patch-like replacement to a file via exact-match replacement."""
    return edit_file(path=path, old_text=old_text, new_text=new_text)


tools = list(_TOOL_REGISTRY.values())
