"""
moral-core automated evaluation runner
=======================================
Runs scenario-based and adversarial tests against a configured model,
scores responses using an LLM-as-judge, and reports pass/fail results.

Usage
-----
    # Run all tests against Anthropic Claude
    python evals/run.py --provider anthropic

    # Run only adversarial tests against OpenAI
    python evals/run.py --suite adversarial --provider openai --model gpt-4o

    # Filter to tests for a single skill
    python evals/run.py --skill general-ethics --provider anthropic

    # Filter to tests for an entire bundle
    python evals/run.py --bundle baseline-safe --provider anthropic

    # Use a different judge model than the model under test
    python evals/run.py --provider anthropic --model claude-opus-4-6 --judge-model claude-haiku-4-5-20251001

    # Save results to a JSON file
    python evals/run.py --output evals/results/run-2026-03-29.json

    # Disable colour output (for CI logs)
    python evals/run.py --no-color

Environment variables
---------------------
    ANTHROPIC_API_KEY   — required for --provider anthropic
    OPENAI_API_KEY      — required for --provider openai
    OPENAI_BASE_URL     — optional; override for OpenAI-compatible endpoints
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

# Ensure repo root is on sys.path so we can import from integrations/
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from evals.runner.parser import load_suite, filter_by_skill, filter_by_bundle, TestCase
from evals.runner.judge import score, ScoreResult, _CALLERS
from evals.runner.report import (
    EvalResult,
    print_header,
    print_result,
    print_summary,
    save_json,
)

# ---------------------------------------------------------------------------
# Skill loader  (re-uses integrations/frameworks/loader.py)
# ---------------------------------------------------------------------------

try:
    from integrations.frameworks.loader import load_bundle as _load_bundle
    from integrations.frameworks.loader import load_skill as _load_skill
    from integrations.frameworks.loader import load_principles, list_bundles
    _HAS_LOADER = True
except ImportError:
    _HAS_LOADER = False


def _system_prompt_for_case(case: TestCase, bundle: str | None) -> str:
    """
    Build the system prompt for the model under test.

    Priority:
    1. If --bundle was specified, load that bundle.
    2. If the test case has target skills, load those skills.
    3. Fall back to PRINCIPLES.md only.
    """
    if not _HAS_LOADER:
        # Graceful fallback: return empty string (model has no ethical context).
        # This is intentional for testing baseline model behaviour.
        return "You are a helpful assistant."

    if bundle:
        ethics = _load_bundle(bundle)
        return f"You are a helpful assistant.\n\n{ethics}"

    if case.target_skills:
        try:
            from integrations.frameworks.loader import load_skills
            ethics = load_principles() + "\n\n---\n\n" + "\n\n---\n\n".join(
                _load_skill(s) for s in case.target_skills
            )
            return f"You are a helpful assistant.\n\n{ethics}"
        except FileNotFoundError:
            pass  # Some skills in the test file may not exist yet

    return f"You are a helpful assistant.\n\n{load_principles()}"


# ---------------------------------------------------------------------------
# LLM call for the model under test  (mirrors agents/runner.py)
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

    elif provider == "openai":
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

    elif provider == "ollama":
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

    else:
        raise ValueError(f"Unknown provider: {provider}")


# ---------------------------------------------------------------------------
# Default models
# ---------------------------------------------------------------------------

DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-6",
    "openai":    "gpt-4o",
    "ollama":    "llama3",
}

DEFAULT_JUDGE_MODELS = {
    "anthropic": "claude-haiku-4-5-20251001",   # fast and cheap for judging
    "openai":    "gpt-4o-mini",
    "ollama":    "llama3",
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="moral-core automated evaluation runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument(
        "--suite",
        default="all",
        choices=["scenarios", "adversarial", "all"],
        help="Which test suite to run (default: all)",
    )
    p.add_argument("--skill",  help="Filter to tests targeting a specific skill")
    p.add_argument("--bundle", help="Filter to tests for skills in a bundle; also loads that bundle as system prompt")
    p.add_argument(
        "--provider",
        default="anthropic",
        choices=["anthropic", "openai", "ollama"],
        help="LLM provider for the model under test (default: anthropic)",
    )
    p.add_argument("--model",       help="Model to test (uses provider default if omitted)")
    p.add_argument("--judge-model", help="Model to use for scoring (uses cheap default if omitted)")
    p.add_argument("--output",      help="Path to save JSON results (optional)")
    p.add_argument("--no-color",    action="store_true", help="Disable coloured terminal output")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    use_color = not args.no_color and sys.stdout.isatty()

    evals_dir = Path(__file__).parent
    model       = args.model       or DEFAULT_MODELS[args.provider]
    judge_model = args.judge_model or DEFAULT_JUDGE_MODELS[args.provider]

    # Load test cases
    cases = load_suite(evals_dir, suite=args.suite)
    if args.skill:
        cases = filter_by_skill(cases, args.skill)
    elif args.bundle and _HAS_LOADER:
        bundles = list_bundles()
        if args.bundle not in bundles:
            print(f"Error: unknown bundle '{args.bundle}'. Available: {', '.join(bundles)}", file=sys.stderr)
            return 1
        import yaml
        manifest = yaml.safe_load((REPO_ROOT / "skills-manifest.yaml").read_text())
        bundle_skills = manifest["bundles"][args.bundle]["skills"]
        cases = filter_by_bundle(cases, bundle_skills)

    if not cases:
        print("No test cases found for the given filters.", file=sys.stderr)
        return 1

    print_header(
        provider=args.provider,
        model=model,
        judge_model=judge_model,
        suite=args.suite,
        n_cases=len(cases),
        use_color=use_color,
    )

    results: list[EvalResult] = []

    for idx, case in enumerate(cases, start=1):
        try:
            system_prompt = _system_prompt_for_case(case, bundle=args.bundle)
            response = _run_model(system_prompt, case.prompt, args.provider, model)
            scores = score(
                prompt=case.prompt,
                response=response,
                expected_behavior=case.expected_behavior,
                failure_modes=case.failure_modes,
                provider=args.provider,
                model=judge_model,
            )
            result = EvalResult(case=case, response=response, scores=scores)
        except Exception as exc:
            # Don't abort the whole run on a single error
            dummy_scores = ScoreResult(
                harm_avoidance=1, helpfulness=1, proportionality=1,
                clarity=1, honesty=1, reasoning=""
            )
            result = EvalResult(case=case, response="", scores=dummy_scores, error=str(exc))

        results.append(result)
        print_result(idx, len(cases), result, use_color=use_color)

    print_summary(results, use_color=use_color)

    if args.output:
        save_json(
            results=results,
            path=Path(args.output),
            provider=args.provider,
            model=model,
            judge_model=judge_model,
            suite=args.suite,
        )

    # Exit code: 0 if all pass, 1 if any fail
    any_fail = any(
        r.scores.status() == "FAIL" or r.error
        for r in results
    )
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
