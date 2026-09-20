from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from dotenv import load_dotenv

API_URL = "https://openrouter.ai/api/alpha/decisions"
DEFAULT_MODEL = "typesafe/jev-1.13"


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


def rank_files(query: str, paths: list[str]) -> tuple[float, list[tuple[str, float]]]:
    answers = _ask(
        state={"query": query, "repository": {"files": paths}},
        questions={
            "best_file": {
                "type": "choice",
                "instructions": (
                    "Which of `repository.files` is most likely to contain the code "
                    "that answers `query`? Pick the single most relevant path."
                ),
                "criteria": {path: None for path in paths},
            },
            "answer_exists": {
                "type": "noul",
                "instructions": (
                    "Does any file in `repository.files` likely contain code that "
                    "answers `query`?"
                ),
            },
        },
    )

    probabilities = answers["best_file"].get("probabilities", {})
    ranked = sorted(
        ((path, probabilities.get(path, 0.0)) for path in paths),
        key=lambda item: item[1],
        reverse=True,
    )

    exists_answer = answers.get("answer_exists", {})
    exists = exists_answer.get("noul", exists_answer.get("probability", 0.0))

    return float(exists), ranked
