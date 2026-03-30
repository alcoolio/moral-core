"""
evals/runner/parser.py
----------------------
Parse scenario and adversarial test files into structured TestCase objects.

Handles both formats used in this repo:
  - evals/scenarios/*.md   — use **Active skills:** and **Expected behavior:**
  - evals/adversarial/*.md — use **Target skills:** and **Attack vector:**
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestCase:
    id: str                          # e.g. "multi-stakeholder-1"
    title: str                       # section heading text
    prompt: str                      # user message to send to the model
    target_skills: list[str]         # skill names this test exercises
    expected_behavior: str           # description of a good response
    failure_modes: str = ""          # description of bad responses (optional)
    attack_vector: str = ""          # adversarial exploit description (optional)
    suite: str = "scenarios"         # "scenarios" or "adversarial"
    source_file: str = ""            # path of originating file


def _parse_fields(block: str) -> dict[str, str]:
    """
    Extract all **Label:** fields from a markdown block.

    Matches the pattern used throughout the evals files:
        **Label:** content that continues until the next **Label:** or end of block
    """
    # Find every **Label:** occurrence and its start position
    pattern = re.compile(r"\*\*([A-Za-z][A-Za-z /\-]+?)\*\*\s*:\s*", re.MULTILINE)
    matches = list(pattern.finditer(block))

    fields: dict[str, str] = {}
    for i, m in enumerate(matches):
        key = m.group(1).strip().lower().replace(" ", "_").replace("/", "_")
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(block)
        value = block[start:end].strip().strip('"').rstrip("-").strip()
        fields[key] = value

    return fields


def _parse_skills(raw: str) -> list[str]:
    """Split a comma-separated skills string into a list of clean names."""
    return [s.strip() for s in re.split(r"[,\n]", raw) if s.strip()]


def parse_file(path: Path) -> list[TestCase]:
    """
    Parse a single scenario or adversarial file and return all test cases found.

    Each test case is delimited by a ### N. Title heading.
    """
    text = path.read_text()

    # Split at every "### N." section header; keep the header with its block
    blocks = re.split(r"(?=\n### \d+\.)", "\n" + text)

    cases: list[TestCase] = []
    for block in blocks:
        # Find the ### N. Title heading
        heading = re.match(r"\s*### \d+\.\s+(.+)", block)
        if not heading:
            continue

        title = heading.group(1).strip()
        fields = _parse_fields(block)

        prompt = fields.get("prompt", "")
        if not prompt:
            continue  # Skip blocks without a prompt

        # Skills field may be "active_skills" (scenarios) or "target_skills" (adversarial)
        skills_raw = fields.get("active_skills") or fields.get("target_skills", "")
        target_skills = _parse_skills(skills_raw)

        expected = fields.get("expected_behavior", "")
        failure_modes = fields.get("failure_modes", "")
        attack_vector = fields.get("attack_vector", "")

        suite = "adversarial" if attack_vector else "scenarios"
        idx = len(cases) + 1

        cases.append(TestCase(
            id=f"{path.stem}-{idx}",
            title=title,
            prompt=prompt,
            target_skills=target_skills,
            expected_behavior=expected,
            failure_modes=failure_modes,
            attack_vector=attack_vector,
            suite=suite,
            source_file=str(path),
        ))

    return cases


def load_suite(evals_dir: Path, suite: str = "all") -> list[TestCase]:
    """
    Load test cases from the evals directory.

    Args:
        evals_dir: Path to the evals/ directory.
        suite:     "scenarios", "adversarial", or "all".

    Returns:
        List of TestCase objects, sorted by source file then index.
    """
    cases: list[TestCase] = []

    if suite in ("scenarios", "all"):
        for f in sorted((evals_dir / "scenarios").glob("*.md")):
            if f.name == "README.md":
                continue
            cases.extend(parse_file(f))

    if suite in ("adversarial", "all"):
        for f in sorted((evals_dir / "adversarial").glob("*.md")):
            if f.name == "README.md":
                continue
            cases.extend(parse_file(f))

    return cases


def filter_by_skill(cases: list[TestCase], skill: str) -> list[TestCase]:
    """Return only cases that target the given skill."""
    return [c for c in cases if skill in c.target_skills]


def filter_by_bundle(cases: list[TestCase], bundle_skills: list[str]) -> list[TestCase]:
    """Return only cases where at least one target skill is in the bundle."""
    bundle_set = set(bundle_skills)
    return [c for c in cases if bundle_set.intersection(c.target_skills)]
