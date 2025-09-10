# __init__.py
from __future__ import annotations

import re
from typing import List, Any

# Simulated PyPI registry to avoid network calls in this offline/demo package.
# Names in this set are considered "taken" (i.e., not available).
_MOCK_PYPI_TAKEN = {"existing_name", "taken_package"}

def _sanitize_name(raw: str) -> str:
    """
    Normalize to PyPI-friendly lowercase underscore names.
    - lowercase
    - spaces/hyphens -> underscores
    - drop non [a-z0-9_]
    - collapse multiple underscores
    - trim leading/trailing underscores
    """
    s = (raw or "").strip().lower()
    s = s.replace("-", "_").replace(" ", "_")
    s = re.sub(r"[^a-z0-9_]", "", s)
    s = re.sub(r"_+", "_", s)
    return s.strip("_")


def _is_name_available(name: str) -> bool:
    """
    Simulated availability check: treat names in the mock registry as taken;
    everything else as available. No real network calls are performed.
    """
    if not name:
        return False
    return name not in _MOCK_PYPI_TAKEN  # type: ignore


def _default_candidates(custom_text: str) -> List[str]:
    """
    Deterministic fallback candidate generation from input text when LLM
   -based generation is unavailable.
    Produces up to 10 candidates: base, base_2, ..., base_10
    """
    words = re.findall(r"[A-Za-z0-9]+", custom_text or "")
    base = "_".join(words[:3]).lower() if words else "name"
    base = _sanitize_name(base) or "name"

    candidates: List[str] = []
    seen = set()
    for i in range(1, 11):
        candidate = base if i == 1 else f"{base}_{i}"
        candidate = _sanitize_name(candidate)
        if candidate and candidate not in seen:
            seen.add(candidate)
            candidates.append(candidate)
    return candidates


def _generate_candidates_from_llm(custom_text: str, llm: Any) -> List[str]:
    """
    Attempt to extract 10 <name> elements from an injected LLM (llm).
    Supported signals (in priority order):
      - llm.mock_names: list[str]
      - llm.generate_candidates(custom_text): List[str]
    Falls back to deterministic defaults if signals are unavailable.
    """
    if llm is not None:
        mock = getattr(llm, "mock_names", None)
        if isinstance(mock, list) and mock:
            seen = set()
            out: List[str] = []
            for raw in mock[:10]:
                s = _sanitize_name(str(raw))
                if s and s not in seen:
                    seen.add(s)
                    out.append(s)
            if out:
                return out

        gen = getattr(llm, "generate_candidates", None)
        if callable(gen):
            try:
                out = gen(custom_text)
                if isinstance(out, list):
                    seen = set()
                    res: List[str] = []
                    for raw in out[:10]:
                        s = _sanitize_name(str(raw))
                        if s and s not in seen:
                            seen.add(s)
                            res.append(s)
                    if res:
                        return res
            except Exception:
                pass

    return _default_candidates(custom_text)


def _collect_candidates(custom_text: str, llm: Any) -> List[str]:
    """
    Collect up to 10 candidate names using LLM signals when available,
    otherwise fall back to deterministic defaults.
    """
    cands = _generate_candidates_from_llm(custom_text, llm)
    if not cands:
        cands = _default_candidates(custom_text)
    # Ensure we return at most 10
    return cands[:10]


def generate_available_package_name(custom_text: str, llm: Any) -> str:
    """
    Public API (single function): Generate and return the first available PyPI-style
    package name based on the provided description, using an injected LLM.

    - Accepts a ChatLLM7-like object via the llm parameter for dependency injection.
    - Uses an offline, simulated PyPI registry to avoid network access in this minimal demo.
    - Produces 10 candidate names (lowercase, underscores, no special chars) and returns
      the first one not present in the simulated registry. If none are available, expands
      with simple variants derived from the first candidate.
    """
    candidates = _collect_candidates(custom_text, llm)

    # First pass: direct candidates
    for name in candidates:
        if _is_name_available(name):
            return name

    # Second pass: simple variants of the first candidate
    base = candidates[0] if candidates else "name"
    for i in range(2, 50):
        variant = _sanitize_name(f"{base}_{i}")
        if _is_name_available(variant):
            return variant

    raise RuntimeError("Exhausted variant search without finding an available name.")


__all__ = ["generate_available_package_name"]