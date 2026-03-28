# Loading a Single Skill

## Python Example

```python
from pathlib import Path

# Load the skill
skill = Path("skills/empathy/SKILL.md").read_text()

# Incorporate into system prompt
system_prompt = f"""You are a helpful assistant.

## Ethical Skill: Empathy
{skill}
"""

# Use with your LLM API
response = llm.chat(system=system_prompt, messages=messages)
```

## Claude Code Example

In a Claude Code project, reference skills from the top-level `skills/` directory in your CLAUDE.md or system prompt:

```markdown
# CLAUDE.md

When responding to users in distress, follow the empathy skill guidelines in skills/empathy/SKILL.md.
```

## Minimal Integration (Copy-Paste)

For quick integration, copy the **Behavioral Rules** section from any SKILL.md directly into your system prompt:

```
You are a customer support assistant.

When interacting with users:
- Acknowledge the user's emotional state before addressing their problem
- Use supportive but honest tone
- Do not make promises you cannot keep
- If the user appears to be in crisis, provide crisis resources
- Maintain boundaries between empathy and compliance
```

## Which Skill to Start With

If you're loading only one skill, `general-ethics` provides the broadest coverage. For specific contexts:

| Context | Recommended First Skill |
|---|---|
| Any general app | `general-ethics` |
| Support/service | `empathy` |
| Information/research | `epistemic-humility` |
| Autonomous systems | `human-oversight` |
| Content generation | `digital-ethics` |
| Children's apps | `child-safety` |
