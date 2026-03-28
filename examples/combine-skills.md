# Combining Multiple Skills

## Basic Composition

Skills are designed to be concatenated. Load PRINCIPLES.md first (it contains conflict resolution rules), then add skills.

```python
from pathlib import Path

# Always load principles first
principles = Path("PRINCIPLES.md").read_text()

# Load selected skills
skill_names = ["general-ethics", "empathy", "epistemic-humility"]
skills = [Path(f"skills/{s}/SKILL.md").read_text() for s in skill_names]

system_prompt = f"""You are a helpful assistant.

## Core Principles
{principles}

## Ethical Skills
{"---".join(skills)}
"""
```

## Using a Policy Bundle

```python
BUNDLES = {
    "baseline-safe": ["general-ethics", "epistemic-humility", "human-oversight"],
    "child-safe": ["child-safety", "protect-vulnerable", "empathy", "digital-ethics", "human-oversight"],
    "inclusive-assistant": ["anti-sexism", "anti-racism", "disability-respect", "empathy", "elder-protection"],
}

def load_bundle(name):
    principles = Path("PRINCIPLES.md").read_text()
    skills = [Path(f"skills/{s}/SKILL.md").read_text() for s in BUNDLES[name]]
    return f"{principles}\n\n{'---'.join(skills)}"

system_prompt = f"You are a helpful assistant.\n\n{load_bundle('baseline-safe')}"
```

## Handling Conflicts Between Skills

When skills give conflicting guidance, the Priority Ladder in PRINCIPLES.md resolves it:

1. Prevent immediate severe harm (highest)
2. Protect vulnerable beings
3. Avoid coercion and dehumanization
4. De-escalate conflict
5. Preserve dignity and fairness
6. Tell the truth with calibrated uncertainty
7. Respect autonomy within safety bounds
8. Reduce long-term ecological and social harm (lowest)

The skill aligned with the higher-priority level wins.

## Token Budget Optimization

If you are constrained on prompt tokens, you can load only the Behavioral Rules section from each skill:

```python
import re

def extract_rules(skill_text):
    match = re.search(r'## 6\. Behavioral Rules\n(.*?)(?=\n## )', skill_text, re.DOTALL)
    return match.group(1) if match else ""
```
