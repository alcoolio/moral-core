# Moral Core Agents

Framework-agnostic reviewer and designer agents built on the Moral Core ethical skills library.

## What These Are

Each agent is a **plain markdown file** containing a system prompt you can paste into any LLM that accepts system prompts — Claude, GPT-4, Gemini, Mistral, or any other model. No SDK, no framework, no tooling required.

They are designed to be used interactively: you paste content into the conversation and the agent reviews, audits, or designs for you.

## Agents

| Agent | File | Purpose |
|---|---|---|
| Ethics Reviewer | `ethics-reviewer.md` | Reviews prompts, policies, and agent behavior for ethical concerns |
| Empathy Style Checker | `empathy-style-checker.md` | Checks communication for tone, empathy, inclusivity, and respect |
| Misuse Auditor | `misuse-auditor.md` | Red-teams prompts and system configs for bypass vectors and weaponization risks |

More agents coming: advertising ethics, mental health support safety, robotics safety, mediation designer, warfare systems reviewer.

## How to Use

### Option 1: Copy-paste into a chat interface

1. Open the agent file (e.g. `agents/ethics-reviewer.md`)
2. Copy everything under `## System Prompt`
3. Paste it as the system prompt in your LLM interface
4. Paste the content you want reviewed into the conversation

### Option 2: Load programmatically

```python
from pathlib import Path

agent_prompt = Path("agents/ethics-reviewer.md").read_text()
# Extract the system prompt section (everything after "## System Prompt\n")
system_prompt = agent_prompt.split("## System Prompt\n", 1)[1]

response = llm.chat(
    system=system_prompt,
    messages=[{"role": "user", "content": content_to_review}]
)
```

See `runner.py` for a complete working example with multiple LLM providers.

## Relationship to `.claude/agents/`

The `.claude/agents/` directory contains **Claude Code subagent definitions** — the same agents reformatted for Claude Code's subagent system, with file-reading tools attached. Those only work inside Claude Code.

The agents in this directory are the portable equivalents. Same review logic, no platform dependency.

## Relationship to `skills/`

Agents draw on the skill modules in `skills/` for their underlying principles. When an agent produces a finding, the relevant skill file explains the full reasoning behind it. Agents and skills are complementary: skills define the behavioral rules; agents apply them analytically.
