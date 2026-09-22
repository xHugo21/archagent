from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv

API_URL = "https://openrouter.ai/api/alpha/decisions"
DEFAULT_MODEL = "typesafe/jev-1.13"

RISK_CLASSES = {
    "benign_read": "Only reads data and changes nothing",
    "reversible_local_change": "Edits, creates, or moves project files the user can undo",
    "data_loss": "Deletes content or overwrites existing work with no way back",
    "secret_exposure": "Reads, writes, or exposes credentials, keys, or environment files",
    "external_side_effect": "Runs commands or reaches outside the workspace",
}


def _credentials() -> tuple[str, str]:
    load_dotenv()

    api_key = os.environ.get("JEV_API_KEY")
    if not api_key:
        raise RuntimeError("JEV_API_KEY is not set")

    model = os.environ.get("JEV_MODEL") or DEFAULT_MODEL

    return api_key, model


def _ask(state: dict, questions: dict) -> dict:
    api_key, model = _credentials()

    payload = json.dumps(
        {"model": model, "state": state, "questions": questions}
    ).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="ignore")[:300]
        raise RuntimeError(f"Jev request failed ({error.code}): {detail}") from error

    return body["answers"]


def rank_options(query: str, options: list[str]) -> tuple[float, list[tuple[str, float]]]:
    answers = _ask(
        state={"query": query, "repository": {"candidates": options}},
        questions={
            "best": {
                "type": "choice",
                "instructions": (
                    "Which of `repository.candidates` is most likely to contain the "
                    "code that answers `query`? Pick the single most relevant one."
                ),
                "criteria": {option: None for option in options},
            },
            "answer_exists": {
                "type": "noul",
                "instructions": (
                    "Does any entry in `repository.candidates` likely contain code "
                    "that answers `query`?"
                ),
            },
        },
    )

    probabilities = answers["best"].get("probabilities", {})
    ranked = sorted(
        ((option, probabilities.get(option, 0.0)) for option in options),
        key=lambda item: item[1],
        reverse=True,
    )

    exists_answer = answers.get("answer_exists", {})
    exists = exists_answer.get("noul", exists_answer.get("probability", 0.0))

    return float(exists), ranked


def assess_operation(
    tool_name: str,
    args: dict,
    reason: str,
    mode: str,
) -> tuple[float, str]:
    answers = _ask(
        state={
            "operation": {
                "tool": tool_name,
                "arguments": args,
                "flagged_reason": reason,
                "permission_mode": mode,
            }
        },
        questions={
            "safe_to_run": {
                "type": "noul",
                "instructions": (
                    "Is `operation` safe to run without asking the user first? It "
                    "is safe only if it stays inside the project, can be undone, "
                    "and exposes no credentials."
                ),
                "criteria": {
                    "true": "Reversible, scoped to the project, no credentials involved",
                    "false": "Irreversible, or reaches outside the project, or touches credentials",
                },
            },
            "risk_class": {
                "type": "choice",
                "instructions": "Which risk class best describes `operation`?",
                "criteria": RISK_CLASSES,
            },
        },
    )

    safe_answer = answers.get("safe_to_run", {})
    safe = safe_answer.get("noul", safe_answer.get("probability", 0.0))

    return float(safe), answers.get("risk_class", {}).get("choice", "unknown")
