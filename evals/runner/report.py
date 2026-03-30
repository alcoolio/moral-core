"""
evals/runner/report.py
----------------------
Terminal and JSON reporting for evaluation runs.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .judge import DIMENSIONS, THRESHOLDS, FAILURE_RATE_THRESHOLDS, ScoreResult
from .parser import TestCase


# ---------------------------------------------------------------------------
# ANSI colour helpers
# ---------------------------------------------------------------------------

_RESET  = "\033[0m"
_BOLD   = "\033[1m"
_RED    = "\033[91m"
_YELLOW = "\033[93m"
_GREEN  = "\033[92m"
_CYAN   = "\033[96m"
_GREY   = "\033[90m"


def _c(text: str, code: str, use_color: bool) -> str:
    return f"{code}{text}{_RESET}" if use_color else text


# ---------------------------------------------------------------------------
# EvalResult  — result of one test case
# ---------------------------------------------------------------------------

@dataclass
class EvalResult:
    case: TestCase
    response: str
    scores: ScoreResult
    error: Optional[str] = None  # set if the run failed before scoring

    def as_dict(self) -> dict:
        return {
            "id":            self.case.id,
            "title":         self.case.title,
            "suite":         self.case.suite,
            "source_file":   self.case.source_file,
            "target_skills": self.case.target_skills,
            "status":        self.scores.status() if not self.error else "ERROR",
            "average":       round(self.scores.average(), 2) if not self.error else None,
            "scores":        self.scores.as_dict() if not self.error else None,
            "reasoning":     self.scores.reasoning if not self.error else None,
            "error":         self.error,
        }


# ---------------------------------------------------------------------------
# Aggregate stats
# ---------------------------------------------------------------------------

def _compute_stats(results: list[EvalResult]) -> dict:
    scored = [r for r in results if not r.error]
    if not scored:
        return {}

    total = len(results)
    errors = sum(1 for r in results if r.error)
    passed = sum(1 for r in scored if r.scores.status() == "PASS")
    warned = sum(1 for r in scored if r.scores.status() == "WARN")
    failed = sum(1 for r in scored if r.scores.status() == "FAIL")

    dim_means = {}
    for dim in DIMENSIONS:
        vals = [getattr(r.scores, dim) for r in scored]
        dim_means[dim] = sum(vals) / len(vals)

    # Failure rate = proportion of individual scores (across all dims) that are <= 2
    all_scores = [getattr(r.scores, d) for r in scored for d in DIMENSIONS]
    failure_rate = sum(1 for s in all_scores if s <= 2) / len(all_scores) if all_scores else 0

    return {
        "total":        total,
        "scored":       len(scored),
        "errors":       errors,
        "passed":       passed,
        "warned":       warned,
        "failed":       failed,
        "failure_rate": failure_rate,
        "dim_means":    dim_means,
    }


def _dim_status(dim: str, mean: float) -> str:
    t = THRESHOLDS[dim]
    if mean >= t["green"]:
        return "GREEN"
    if mean >= t["yellow"]:
        return "YELLOW"
    return "RED"


def _rate_status(rate: float) -> str:
    if rate < FAILURE_RATE_THRESHOLDS["green"]:
        return "GREEN"
    if rate < FAILURE_RATE_THRESHOLDS["yellow"]:
        return "YELLOW"
    return "RED"


# ---------------------------------------------------------------------------
# Terminal printer
# ---------------------------------------------------------------------------

def print_header(provider: str, model: str, judge_model: str,
                 suite: str, n_cases: int, use_color: bool = True) -> None:
    sep = _c("=" * 56, _BOLD, use_color)
    print(f"\n{sep}")
    print(_c("  moral-core eval runner", _BOLD, use_color))
    print(sep)
    print(f"  Suite:       {suite}")
    print(f"  Provider:    {provider}  /  model: {model}")
    print(f"  Judge:       {judge_model}")
    print(f"  Test cases:  {n_cases}")
    print(f"{sep}\n")


def print_result(idx: int, total: int, result: EvalResult, use_color: bool = True) -> None:
    status = result.scores.status() if not result.error else "ERROR"

    if result.error:
        icon = _c("✗", _RED, use_color)
        label = _c("ERROR", _RED, use_color)
        suffix = f"  {result.error}"
    elif status == "PASS":
        icon = _c("✓", _GREEN, use_color)
        label = _c("PASS ", _GREEN, use_color)
        suffix = _c(f"  avg {result.scores.average():.1f}", _GREY, use_color)
    elif status == "WARN":
        icon = _c("~", _YELLOW, use_color)
        label = _c("WARN ", _YELLOW, use_color)
        suffix = _c(f"  avg {result.scores.average():.1f}", _GREY, use_color)
    else:
        icon = _c("✗", _RED, use_color)
        label = _c("FAIL ", _RED, use_color)
        suffix = _c(f"  avg {result.scores.average():.1f}", _GREY, use_color)

    counter = _c(f"[{idx}/{total}]", _GREY, use_color)
    title = result.case.title[:52].ljust(52)
    print(f"  {counter}  {icon} {label}  {title}{suffix}")

    # Show per-dimension breakdown for non-passing results
    if status in ("WARN", "FAIL") and not result.error:
        scores = result.scores.as_dict()
        parts = []
        for dim in DIMENSIONS:
            s = scores[dim]
            short = dim[:4]
            if s <= 2:
                parts.append(_c(f"{short}:{s}", _RED, use_color))
            elif s < THRESHOLDS[dim]["green"]:
                parts.append(_c(f"{short}:{s}", _YELLOW, use_color))
            else:
                parts.append(_c(f"{short}:{s}", _GREEN, use_color))
        print(f"           ↳ {' '.join(parts)}  — {result.scores.reasoning}")


def print_summary(results: list[EvalResult], use_color: bool = True) -> None:
    stats = _compute_stats(results)
    if not stats:
        print("\nNo results to summarise.\n")
        return

    sep = _c("─" * 56, _GREY, use_color)
    print(f"\n{sep}")
    print(_c("  Summary", _BOLD, use_color))
    print(sep)

    total  = stats["total"]
    passed = stats["passed"]
    warned = stats["warned"]
    failed = stats["failed"]
    errors = stats["errors"]

    pass_str  = _c(str(passed), _GREEN,  use_color) if passed else str(passed)
    warn_str  = _c(str(warned), _YELLOW, use_color) if warned else str(warned)
    fail_str  = _c(str(failed), _RED,    use_color) if failed else str(failed)
    err_str   = _c(str(errors), _RED,    use_color) if errors else str(errors)

    print(f"  Tests:  {total} total  |  {pass_str} pass  |  {warn_str} warn  |  {fail_str} fail  |  {err_str} error")

    rate = stats["failure_rate"]
    rate_st = _rate_status(rate)
    rate_color = _GREEN if rate_st == "GREEN" else (_YELLOW if rate_st == "YELLOW" else _RED)
    print(f"  Score failure rate: {rate:.1%}  [{_c(rate_st, rate_color, use_color)}]")

    print(f"\n  Dimension means:")
    for dim in DIMENSIONS:
        mean = stats["dim_means"][dim]
        st = _dim_status(dim, mean)
        color = _GREEN if st == "GREEN" else (_YELLOW if st == "YELLOW" else _RED)
        bar_filled = int(mean)
        bar = "█" * bar_filled + "░" * (5 - bar_filled)
        threshold_label = f"(threshold {THRESHOLDS[dim]['green']:.1f})"
        print(f"  {dim.replace('_',' '):<18}  {mean:.2f}  {bar}  [{_c(st, color, use_color)}]  {_c(threshold_label, _GREY, use_color)}")

    print(f"{sep}\n")


# ---------------------------------------------------------------------------
# JSON output
# ---------------------------------------------------------------------------

def save_json(
    results: list[EvalResult],
    path: Path,
    provider: str,
    model: str,
    judge_model: str,
    suite: str,
) -> None:
    stats = _compute_stats(results)
    output = {
        "meta": {
            "timestamp":   datetime.now(timezone.utc).isoformat(),
            "provider":    provider,
            "model":       model,
            "judge_model": judge_model,
            "suite":       suite,
        },
        "summary": {
            **stats,
            "dim_status": {
                dim: _dim_status(dim, stats["dim_means"][dim])
                for dim in DIMENSIONS
            } if stats.get("dim_means") else {},
        },
        "results": [r.as_dict() for r in results],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2))
    print(f"Results saved to {path}")
