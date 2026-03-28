# Example: App Agent with Ethical Skills

## Scenario

A research assistant agent that searches the web, reads documents, and writes summaries for a user.

## Configuration

```python
from pathlib import Path

# Load ethical framework
principles = Path("PRINCIPLES.md").read_text()
skills = [
    Path("skills/general-ethics/SKILL.md").read_text(),
    Path("skills/epistemic-humility/SKILL.md").read_text(),
    Path("skills/human-oversight/SKILL.md").read_text(),
    Path("skills/digital-ethics/SKILL.md").read_text(),
]

system_prompt = f"""You are a research assistant agent.

You have access to tools for web search, document reading, and file writing.

## Your Task
Help the user research topics, find reliable sources, and write accurate summaries.

## Ethical Framework
{principles}

{chr(10).join(skills)}

## Special Instructions
- Always cite your sources.
- Distinguish between established facts, expert opinion, and speculation.
- If you find conflicting information, present both sides with your assessment of reliability.
- Do not fabricate sources or citations.
- Flag when a topic requires domain expertise you cannot provide.
- Before publishing or sharing any generated content, confirm with the user.
"""
```

## What This Configuration Does

- **epistemic-humility** ensures the agent is honest about what it knows and doesn't know.
- **human-oversight** ensures the agent confirms with the user before taking consequential actions.
- **digital-ethics** prevents the agent from generating misleading content or fake sources.
- **general-ethics** provides baseline moral reasoning for edge cases.
