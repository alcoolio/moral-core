"""
moral-core skill loader utility
================================
Reusable helpers for loading ethical skills into any Python-based framework.

Usage:
    from integrations.frameworks.loader import compose_system_prompt, load_bundle, load_skill

All paths resolve relative to the moral-core repo root, so this file can be
copied into your project or used in-place from a git submodule.
"""

from pathlib import Path
import re
import yaml

# Resolve the repo root two levels up from this file:
#   integrations/frameworks/loader.py -> integrations/ -> repo root
MORAL_CORE_PATH = Path(__file__).resolve().parent.parent.parent


def load_principles() -> str:
    """Load PRINCIPLES.md — always include this first when composing prompts."""
    return (MORAL_CORE_PATH / "PRINCIPLES.md").read_text()


def load_skill(name: str, rules_only: bool = False) -> str:
    """
    Load a single skill by directory name (e.g. 'general-ethics').

    Args:
        name:       The skill directory name under skills/.
        rules_only: If True, extract only the Behavioral Rules section (~300 tokens
                    vs ~2000 tokens for the full skill). Use when context is tight.

    Returns:
        Skill text as a string.
    """
    path = MORAL_CORE_PATH / f"skills/{name}/SKILL.md"
    if not path.exists():
        raise FileNotFoundError(f"Skill not found: {path}")
    text = path.read_text()
    if rules_only:
        match = re.search(r"## 6\. Behavioral Rules\n(.*?)(?=\n## )", text, re.DOTALL)
        return match.group(1).strip() if match else text
    return text


def load_bundle(bundle_name: str, rules_only: bool = False) -> str:
    """
    Load a pre-built policy bundle from skills-manifest.yaml.

    Available bundles:
        baseline-safe       — minimum viable layer for any deployment
        mediation-first     — conflict resolution and counseling
        anti-abuse          — systems with abuse victims or perpetrators
        child-safe          — systems used by or around children
        robotics-care       — physical robots in care or service roles
        eco-care            — environmental or ecological decisions
        inclusive-assistant — diverse population assistance
        civic-governance    — civic tech and participatory design

    Args:
        bundle_name: Bundle key from skills-manifest.yaml.
        rules_only:  If True, extract only Behavioral Rules from each skill.

    Returns:
        Composed string: PRINCIPLES.md + all skill texts separated by '---'.
    """
    manifest_path = MORAL_CORE_PATH / "skills-manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text())

    bundles = manifest.get("bundles", {})
    if bundle_name not in bundles:
        available = ", ".join(bundles.keys())
        raise ValueError(f"Bundle '{bundle_name}' not found. Available: {available}")

    skill_names = bundles[bundle_name]["skills"]
    principles = load_principles()
    skill_texts = [load_skill(s, rules_only=rules_only) for s in skill_names]
    return principles + "\n\n---\n\n" + "\n\n---\n\n".join(skill_texts)


def compose_system_prompt(
    role: str,
    bundle: str = None,
    skills: list = None,
    rules_only: bool = False,
) -> str:
    """
    Compose a full system prompt by combining a role description with ethical skills.

    Provide either `bundle` or `skills`, not both. If neither is provided, only
    PRINCIPLES.md is appended.

    Args:
        role:       Your base system prompt / role description.
        bundle:     Name of a pre-built bundle to load (e.g. 'baseline-safe').
        skills:     List of individual skill names to load (e.g. ['general-ethics', 'empathy']).
        rules_only: If True, extract only the Behavioral Rules section from each skill.

    Returns:
        Complete system prompt string ready for injection.

    Example:
        system = compose_system_prompt(
            role="You are a helpful customer support assistant.",
            bundle="anti-abuse",
        )
    """
    if bundle and skills:
        raise ValueError("Provide either `bundle` or `skills`, not both.")

    if bundle:
        ethics = load_bundle(bundle, rules_only=rules_only)
    elif skills:
        principles = load_principles()
        skill_texts = [load_skill(s, rules_only=rules_only) for s in skills]
        ethics = principles + "\n\n---\n\n" + "\n\n---\n\n".join(skill_texts)
    else:
        ethics = load_principles()

    return f"{role}\n\n## Ethical Framework\n\n{ethics}"


def list_bundles() -> dict:
    """Return a dict of bundle_name -> description from the manifest."""
    manifest = yaml.safe_load((MORAL_CORE_PATH / "skills-manifest.yaml").read_text())
    return {
        name: meta.get("description", "")
        for name, meta in manifest.get("bundles", {}).items()
    }


def list_skills() -> list:
    """Return a list of available skill names from the manifest."""
    manifest = yaml.safe_load((MORAL_CORE_PATH / "skills-manifest.yaml").read_text())
    return [s["name"] for s in manifest.get("skills", [])]
