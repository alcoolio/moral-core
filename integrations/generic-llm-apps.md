# Integration Guide: Generic LLM Applications

## Overview

This guide covers integrating Moral Core skills into any LLM-powered application — chatbots, writing assistants, Q&A systems, content generators, or any system that takes a system prompt.

## Integration Pattern

### Step 1: Load the Shared Principles

Always include the priority ladder and conflict resolution rules from PRINCIPLES.md. This ensures consistent behavior when skills interact.

```python
from pathlib import Path

principles = Path("PRINCIPLES.md").read_text()
```

### Step 2: Select and Load Skills

Choose skills based on your deployment context. See [policy-bundles.md](policy-bundles.md) for recommended combinations.

```python
skill_names = ["general-ethics", "epistemic-humility", "human-oversight"]
skills = []
for name in skill_names:
    skill_path = Path(f"skills/{name}/SKILL.md")
    skills.append(skill_path.read_text())
```

### Step 3: Compose the System Prompt

```python
system_prompt = f"""You are a helpful assistant.

## Ethical Framework
{principles}

## Active Ethical Skills
{"---".join(skills)}
"""
```

### Step 4: Configure Your LLM Call

Pass the system prompt to your LLM API. The exact mechanism depends on your provider.

```python
# Example with a generic API
response = llm.chat(
    system=system_prompt,
    messages=[{"role": "user", "content": user_input}]
)
```

## Prompt Size Considerations

- PRINCIPLES.md is approximately 4,000 tokens.
- Each SKILL.md is approximately 1,500-2,500 tokens.
- A policy bundle of 3-5 skills plus principles typically uses 10,000-17,000 tokens.
- For context-limited models, prioritize PRINCIPLES.md and the most critical skills.
- Consider extracting only the Behavioral Rules section from each skill if token budget is tight.

## Testing

After integration, run the test cases from each loaded skill's TEST_CASES.md against your system to verify behavior.

## Recommended Minimum

For any general-purpose LLM application, load at minimum:
- `general-ethics`
- `epistemic-humility`
- `human-oversight`

This provides baseline moral reasoning, honest uncertainty handling, and escalation logic.
