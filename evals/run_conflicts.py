"""
moral-core skill-conflict eval runner
======================================
Runs each scenario in `evals/scenarios/skill-conflicts.md` three times — with
skill A only, skill B only, and both skills loaded — then asks an LLM-as-judge
how much A and B disagreed on operational advice and how well the combined
response navigated the tension via the priority ladder.

Use this to surface gaps in `PRINCIPLES.md`'s priority ladder: pairs of skills
where A-only and B-only produce divergent advice **and** the combined response
fails to name and resolve the conflict are pairs the ladder hasn't tightened
enough.

Usage
-----
    # Default: Anthropic, all conflict scenarios
    python evals/run_conflicts.py

    # Filter to scenarios involving a specific skill
    python evals/run_conflicts.py --skill empathy

    # Filter to a specific pair
    python evals/run_conflicts.py --pair empathy,epistemic-humility

    # Different provider / model
    python evals/run_conflicts.py --provider openai --model gpt-4o

    # Save full JSON results
    python evals/run_conflicts.py --output evals/results/conflicts-$(date +%Y-%m-%d).json

    # Dry run: parse + print the cases without making any model calls
    python evals/run_conflicts.py --dry-run

Environment variables
---------------------
    ANTHROPIC_API_KEY   — required for --provider anthropic
    OPENAI_API_KEY      — required for --provider openai
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

# Make repo root importable
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from evals.runner.conflict import (
    ConflictCase,
    ConflictRun,
    ConflictScores,
    aggregate_by_pair,
    build_system_prompts,
    judge_conflict,
    parse_conflict_file,
)


# ---------------------------------------------------------------------------
# Provider call (mirrors evals/run.py)
# ---------------------------------------------------------------------------

def _run_model(system: str, prompt: str, provider: str, model: str) -> str:
    import os

    if provider == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        resp = client.messages.create(
            model=model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.content[0].text

    if provider == "openai":
        from openai import OpenAI
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_BASE_URL"),
        )
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1024,
        )
        return resp.choices[0].message.content

    if provider == "ollama":
        import requests
        resp = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
            },
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]

    raise ValueError(f"Unknown provider: {provider}")


DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-6",
    "openai":    "gpt-4o",
    "ollama":    "llama3",
}

DEFAULT_JUDGE_MODELS = {
    "anthropic": "claude-haiku-4-5-20251001",
    "openai":    "gpt-4o-mini",
    "ollama":    "llama3",
}


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

_RESET, _BOLD = "\033[0m", "\033[1m"
_RED, _YELLOW, _GREEN, _CYAN, _GREY = (
    "\033[91m", "\033[93m", "\033[92m", "\033[96m", "\033[90m"
)


def _c(text: str, code: str, use_color: bool) -> str:
    return f"{code}{text}{_RESET}" if use_color else text


def _status_color(status: str) -> str:
    return {"PASS": _GREEN, "WARN": _YELLOW, "FAIL": _RED, "ERROR": _RED}.get(status, _GREY)


def _print_run(idx: int, total: int, run: ConflictRun, use_color: bool) -> None:
    status = run.scores.status() if not run.error else "ERROR"
    icon = "✓" if status == "PASS" else ("~" if status == "WARN" else "✗")
    icon_c = _c(icon, _status_color(status), use_color)
    label = _c(f"{status:<5}", _status_color(status), use_color)
    counter = _c(f"[{idx}/{total}]", _GREY, use_color)

    title = run.case.title[:48].ljust(48)
    pair = f"{run.case.skill_a} ↔ {run.case.skill_b}"
    print(f"  {counter}  {icon_c} {label}  {title}  {_c(pair, _CYAN, use_color)}")

    if run.error:
        print(f"           ↳ ERROR: {run.error}")
        return

    s = run.scores
    level_str = s.priority_level_cited if s.priority_level_cited else "—"
    expected = run.case.expected_priority_level or "—"
    detail = (
        f"agree:{s.agreement}  resolve:{s.resolution}  "
        f"named:{'Y' if s.names_tension else 'N'}  "
        f"level:{level_str} (expected {expected})"
    )
    print(f"           ↳ {_c(detail, _GREY, use_color)}")
    if status != "PASS":
        print(f"             {s.reasoning}")


def _print_pair_matrix(runs: list[ConflictRun], use_color: bool) -> None:
    aggs = aggregate_by_pair(runs)
    if not aggs:
        return

    sep = _c("─" * 72, _GREY, use_color)
    print(f"\n{sep}")
    print(_c("  Per-pair aggregate", _BOLD, use_color))
    print(sep)
    print(f"  {'pair':<48}  {'n':>3}  {'agree':>6}  {'resolve':>7}  {'named':>6}")
    print(sep)
    for pair, stats in sorted(aggs.items(), key=lambda kv: kv[1]["mean_resolution"]):
        a, b = pair
        pair_str = f"{a} ↔ {b}"[:48].ljust(48)
        agree = stats["mean_agreement"]
        resolve = stats["mean_resolution"]
        named = stats["tension_named_rate"]

        resolve_color = _GREEN if resolve >= 4.0 else (_YELLOW if resolve >= 3.0 else _RED)
        agree_color = _RED if agree <= 2.5 else (_YELLOW if agree <= 3.5 else _GREEN)
        named_color = _GREEN if named >= 0.8 else (_YELLOW if named >= 0.5 else _RED)

        print(
            f"  {pair_str}  {stats['n']:>3}  "
            f"{_c(f'{agree:>6.2f}', agree_color, use_color)}  "
            f"{_c(f'{resolve:>7.2f}', resolve_color, use_color)}  "
            f"{_c(f'{named:>6.0%}', named_color, use_color)}"
        )
    print(sep)
    print(_c("  Reading: low agree + low resolve = ladder gap.", _GREY, use_color))
    print(sep + "\n")


def _print_summary(runs: list[ConflictRun], use_color: bool) -> None:
    scored = [r for r in runs if not r.error]
    n = len(scored)
    if n == 0:
        print("\nNo scored runs.\n")
        return

    passed = sum(1 for r in scored if r.scores.status() == "PASS")
    warned = sum(1 for r in scored if r.scores.status() == "WARN")
    failed = sum(1 for r in scored if r.scores.status() == "FAIL")
    errored = sum(1 for r in runs if r.error)

    mean_agreement   = sum(r.scores.agreement  for r in scored) / n
    mean_resolution  = sum(r.scores.resolution for r in scored) / n
    named_rate       = sum(1 for r in scored if r.scores.names_tension) / n
    level_cited_rate = sum(1 for r in scored if r.scores.priority_level_cited) / n

    sep = _c("─" * 56, _GREY, use_color)
    print(f"\n{sep}")
    print(_c("  Summary", _BOLD, use_color))
    print(sep)
    print(
        f"  Tests:  {len(runs)} total  |  "
        f"{_c(str(passed), _GREEN, use_color)} pass  |  "
        f"{_c(str(warned), _YELLOW, use_color)} warn  |  "
        f"{_c(str(failed), _RED, use_color)} fail  |  "
        f"{_c(str(errored), _RED, use_color)} error"
    )
    print(f"  Mean agreement (A vs B):    {mean_agreement:.2f} / 5  (lower = more conflict)")
    print(f"  Mean resolution (combined): {mean_resolution:.2f} / 5  (higher = better)")
    print(f"  Tension named rate:         {named_rate:.0%}")
    print(f"  Priority-level cited rate:  {level_cited_rate:.0%}")
    print(f"{sep}\n")


# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------

def _filter_cases(
    cases: list[ConflictCase],
    skill: str | None,
    pair: str | None,
) -> list[ConflictCase]:
    if skill:
        cases = [c for c in cases if skill in (c.skill_a, c.skill_b)]
    if pair:
        parts = [p.strip() for p in pair.split(",")]
        if len(parts) != 2:
            raise ValueError("--pair must be 'skillA,skillB'")
        wanted = tuple(sorted(parts))
        cases = [c for c in cases if c.pair == wanted]
    return cases


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="moral-core skill-conflict eval runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--scenarios", default=None,
                   help="Path to skill-conflicts.md (defaults to evals/scenarios/skill-conflicts.md)")
    p.add_argument("--skill", help="Run only scenarios involving this skill")
    p.add_argument("--pair",  help="Run only the given pair, e.g. 'empathy,epistemic-humility'")
    p.add_argument("--provider", default="anthropic",
                   choices=["anthropic", "openai", "ollama"])
    p.add_argument("--model",       help="Model under test")
    p.add_argument("--judge-model", help="Judge model")
    p.add_argument("--output",      help="Path to write JSON results")
    p.add_argument("--no-color",    action="store_true")
    p.add_argument("--dry-run",     action="store_true",
                   help="Parse cases and print plan; make no model calls")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    use_color = not args.no_color and sys.stdout.isatty()

    scenarios_path = Path(args.scenarios) if args.scenarios else (
        REPO_ROOT / "evals" / "scenarios" / "skill-conflicts.md"
    )
    if not scenarios_path.exists():
        print(f"Error: scenarios file not found: {scenarios_path}", file=sys.stderr)
        return 1

    cases = parse_conflict_file(scenarios_path)
    try:
        cases = _filter_cases(cases, args.skill, args.pair)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if not cases:
        print("No conflict scenarios match the given filters.", file=sys.stderr)
        return 1

    model       = args.model       or DEFAULT_MODELS[args.provider]
    judge_model = args.judge_model or DEFAULT_JUDGE_MODELS[args.provider]

    sep = _c("=" * 64, _BOLD, use_color)
    print(f"\n{sep}")
    print(_c("  moral-core skill-conflict eval runner", _BOLD, use_color))
    print(sep)
    print(f"  Scenarios:   {scenarios_path}")
    print(f"  Cases:       {len(cases)}")
    print(f"  Provider:    {args.provider}  /  model: {model}")
    print(f"  Judge:       {judge_model}")
    if args.dry_run:
        print(f"  Mode:        dry-run (no model calls)")
    print(f"{sep}\n")

    if args.dry_run:
        for i, c in enumerate(cases, 1):
            print(f"  [{i}/{len(cases)}]  {c.title}")
            print(f"             pair: {c.skill_a} ↔ {c.skill_b}")
            print(f"             tension: {c.tension[:80]}")
        print()
        return 0

    runs: list[ConflictRun] = []
    for idx, case in enumerate(cases, start=1):
        try:
            prompts = build_system_prompts(case)
            response_a        = _run_model(prompts["a"],        case.prompt, args.provider, model)
            response_b        = _run_model(prompts["b"],        case.prompt, args.provider, model)
            response_combined = _run_model(prompts["combined"], case.prompt, args.provider, model)

            scores = judge_conflict(
                case=case,
                response_a=response_a,
                response_b=response_b,
                response_combined=response_combined,
                provider=args.provider,
                model=judge_model,
            )
            run = ConflictRun(
                case=case,
                response_a=response_a,
                response_b=response_b,
                response_combined=response_combined,
                scores=scores,
            )
        except Exception as exc:
            run = ConflictRun(
                case=case,
                response_a="",
                response_b="",
                response_combined="",
                scores=ConflictScores(
                    agreement=1, resolution=1, names_tension=False,
                    priority_level_cited=None, reasoning="",
                ),
                error=str(exc),
            )

        runs.append(run)
        _print_run(idx, len(cases), run, use_color)

    _print_pair_matrix(runs, use_color)
    _print_summary(runs, use_color)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        aggs = aggregate_by_pair(runs)
        out_path.write_text(json.dumps({
            "meta": {
                "timestamp":   datetime.now(timezone.utc).isoformat(),
                "provider":    args.provider,
                "model":       model,
                "judge_model": judge_model,
                "scenarios":   str(scenarios_path),
            },
            "summary": {
                "n_total":  len(runs),
                "n_passed": sum(1 for r in runs if not r.error and r.scores.status() == "PASS"),
                "n_warned": sum(1 for r in runs if not r.error and r.scores.status() == "WARN"),
                "n_failed": sum(1 for r in runs if not r.error and r.scores.status() == "FAIL"),
                "n_errored": sum(1 for r in runs if r.error),
            },
            "by_pair": {
                f"{a}|{b}": stats for (a, b), stats in aggs.items()
            },
            "runs": [r.as_dict() for r in runs],
        }, indent=2))
        print(f"Results saved to {out_path}")

    any_fail = any(r.error or r.scores.status() == "FAIL" for r in runs)
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
