import types
from pathlib import Path
from typing import Union, get_origin, get_args, Any

WORKSPACE_ROOT = Path.cwd().resolve()


def resolve_user_path(path: str) -> Path:
    candidate = Path(path).expanduser().resolve()
    return candidate


def resolve_workspace_path(path: str) -> Path:
    candidate = (WORKSPACE_ROOT / path).resolve()
    if not str(candidate).startswith(str(WORKSPACE_ROOT)):
        raise ValueError("Path escapes workspace root")
    return candidate


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
