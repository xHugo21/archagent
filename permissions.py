from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from utils import WORKSPACE_ROOT, resolve_workspace_path

READ_ONLY_TOOLS = {"read_file", "list_files", "search_text", "find_files"}
WRITE_TOOLS = {"edit_file", "write_file", "move_file", "apply_patch"}
DESTRUCTIVE_TOOLS = {"delete_file"}
KNOWN_TOOLS = READ_ONLY_TOOLS | WRITE_TOOLS | DESTRUCTIVE_TOOLS
VALID_MODES = {"safe", "normal", "full"}


@dataclass
class PermissionDecision:
    action: str
    reason: str


class PermissionManager:
    def check(self, tool_name: str, args: dict[str, Any], mode: str) -> PermissionDecision:
        mode = mode if mode in VALID_MODES else "normal"

        path_analysis = self._analyze_paths(args)
        if path_analysis["escapes_workspace"]:
            return PermissionDecision("deny", "Path escapes workspace root")

        sensitive_reason = path_analysis["sensitive_reason"]

        if mode == "safe":
            if tool_name in READ_ONLY_TOOLS:
                if sensitive_reason:
                    return PermissionDecision("ask", sensitive_reason)
                return PermissionDecision("allow", "Read-only tool allowed in safe mode")
            return PermissionDecision(
                "deny", "Safe mode is read-only. Switch to /mode normal or /mode full"
            )

        if mode == "normal":
            if tool_name in READ_ONLY_TOOLS:
                if sensitive_reason:
                    return PermissionDecision("ask", sensitive_reason)
                return PermissionDecision("allow", "Read-only tool allowed")

            if tool_name in DESTRUCTIVE_TOOLS:
                reason = "delete_file is destructive"
                if isinstance(args.get("recursive"), bool) and args["recursive"]:
                    reason += " (recursive=true)"
                return PermissionDecision("ask", reason)

            if tool_name in WRITE_TOOLS:
                reasons: list[str] = []
                if sensitive_reason:
                    reasons.append(sensitive_reason)

                overwrite_reason = self._overwrite_reason(tool_name, args)
                if overwrite_reason:
                    reasons.append(overwrite_reason)

                if reasons:
                    return PermissionDecision("ask", "; ".join(reasons))

                return PermissionDecision("allow", "Write tool allowed")

            return PermissionDecision("ask", "Unknown tool requires approval")

        if tool_name in KNOWN_TOOLS:
            return PermissionDecision("allow", "Full mode")

        return PermissionDecision("allow", "Full mode (unknown tool)")

    def _overwrite_reason(self, tool_name: str, args: dict[str, Any]) -> str | None:
        try:
            if tool_name == "write_file":
                path = args.get("path")
                if isinstance(path, str):
                    target = resolve_workspace_path(path)
                    if target.exists() and target.is_file():
                        return f"write_file will overwrite existing file: {path}"

            if tool_name == "move_file":
                destination = args.get("destination_path")
                if isinstance(destination, str):
                    target = resolve_workspace_path(destination)
                    if target.exists():
                        return f"move_file destination already exists: {destination}"
        except Exception:
            return None

        return None

    def _analyze_paths(self, args: dict[str, Any]) -> dict[str, Any]:
        sensitive_paths: list[str] = []

        for key, value in args.items():
            if not isinstance(value, str):
                continue
            if key != "path" and not key.endswith("_path"):
                continue

            try:
                resolved = resolve_workspace_path(value)
            except ValueError:
                return {"escapes_workspace": True, "sensitive_reason": None}
            except Exception:
                continue

            rel_path = resolved.relative_to(WORKSPACE_ROOT).as_posix()
            if self._is_sensitive_path(rel_path):
                sensitive_paths.append(rel_path)

        if sensitive_paths:
            joined = ", ".join(sorted(set(sensitive_paths)))
            return {
                "escapes_workspace": False,
                "sensitive_reason": f"Touches protected path(s): {joined}",
            }

        return {"escapes_workspace": False, "sensitive_reason": None}

    def _is_sensitive_path(self, rel_path: str) -> bool:
        if rel_path == ".git" or rel_path.startswith(".git/"):
            return True

        if rel_path in {"master.txt", "AGENTS.md"}:
            return True

        name = Path(rel_path).name
        if name == ".env" or name.startswith(".env."):
            return True

        return False
