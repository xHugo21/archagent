import subprocess
import types
from pathlib import Path
from typing import Union, get_origin, get_args, Any

WORKSPACE_ROOT = Path.cwd().resolve()

IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".commandcode",
}


def resolve_user_path(path: str) -> Path:
    candidate = Path(path).expanduser().resolve()
    return candidate


def resolve_workspace_path(path: str) -> Path:
    candidate = (WORKSPACE_ROOT / path).resolve()
    if not str(candidate).startswith(str(WORKSPACE_ROOT)):
        raise ValueError("Path escapes workspace root")
    return candidate


def workspace_files(base: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=WORKSPACE_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            return sorted(
                line
                for line in result.stdout.splitlines()
                if line.strip()
                and (WORKSPACE_ROOT / line).resolve().is_relative_to(base)
            )
    except Exception:
        pass

    return sorted(
        str(file_path.relative_to(WORKSPACE_ROOT))
        for file_path in base.rglob("*")
        if file_path.is_file()
        and not any(part in IGNORED_DIRS for part in file_path.relative_to(base).parts)
    )


def python_type_to_schema(annotation: Any) -> dict[str, Any]:
    origin = get_origin(annotation)

    if origin in (Union, types.UnionType):
        args = get_args(annotation)
        non_none_args = [arg for arg in args if arg is not type(None)]

        if len(non_none_args) == 1 and len(non_none_args) != len(args):
            schema = python_type_to_schema(non_none_args[0])
            schema["nullable"] = True
            return schema

        return {"anyOf": [python_type_to_schema(arg) for arg in args]}

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
