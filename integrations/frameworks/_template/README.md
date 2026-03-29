# Integration Guide: [Framework Name]

> **How to use this template:**
> Copy this directory to `integrations/frameworks/<your-framework>/`, rename it,
> and fill in each section. Delete all blockquote instructions before submitting.
> Add your framework to the table in `integrations/frameworks/README.md`.

## Overview

> Describe the framework in 2–3 sentences. Explain what kind of AI application it
> is used for and why ethical skill injection needs to be done explicitly (i.e.,
> why ethics is not automatic in this framework).

[Framework Name] is a [description]. Because [framework characteristic], ethical
constraints must be explicitly injected into [system prompt / agent config /
workflow node / other]. Without this, the model has no behavioral guardrails
beyond its own training.

## Why [Framework Name] Needs Explicit Ethics Injection

> List the framework-specific risks or architectural reasons that make ethics
> injection non-trivial. Examples: system prompts don't propagate across sub-agents,
> tool calls bypass the system prompt, no-code UI hides where prompts go, etc.

- [Risk 1]
- [Risk 2]
- [Risk 3]

## Prerequisites

> List what the user needs before following this guide.

- moral-core repository cloned or available as a submodule
- [Framework] installed: `pip install [framework]`
- `PyYAML` installed (required by `loader.py`): `pip install pyyaml`

## Integration Patterns

### Pattern 1: [Name — e.g., "Basic System Prompt Injection"]

> Show the simplest possible integration. Use `loader.py` for skill loading.
> Include a brief explanation of what the code does.

```python
from integrations.frameworks.loader import compose_system_prompt

system = compose_system_prompt(
    role="You are a helpful assistant.",
    bundle="baseline-safe",
)

# TODO: show how to pass `system` into [Framework]'s configuration
```

### Pattern 2: [Name — e.g., "Per-Agent Skill Scoping"]

> Show a more advanced pattern. For multi-agent frameworks, show how different
> agents get different skill bundles. For workflow tools, show how to add an
> ethics review node.

```python
from integrations.frameworks.loader import load_bundle, load_skill

# TODO: advanced pattern
```

### Pattern 3 (Optional): [Name]

> Add a third pattern if the framework supports a meaningfully different
> integration mode (e.g., tool-level vs. agent-level vs. task-level injection).

## Critical Skills

> List the skills most important for this framework's typical use cases.
> Link to the skill directory for reference.

| Skill | Why |
|-------|-----|
| `general-ethics` | Baseline moral reasoning for all decisions |
| `human-oversight` | Agents must know when to stop and ask a human |
| `epistemic-humility` | Prevents overconfident or fabricated outputs |
| [additional skill] | [rationale specific to this framework] |

## Bundle Recommendations

> Map common use cases in this framework to pre-built bundles.

| Use Case | Recommended Bundle | Notes |
|----------|--------------------|-------|
| General chatbot | `baseline-safe` | Minimum viable layer |
| Customer support | `anti-abuse` | Adds abuse and harassment protection |
| Children's app | `child-safe` | Critical risk — use full bundle, not rules_only |
| [Framework-specific use case] | [bundle] | [notes] |

## Token Budget

> Explain the token cost in this framework's context (e.g., does the framework
> have a known context limit? Does the system prompt compete with tool outputs?).

| Mode | Approximate Tokens | When to Use |
|------|--------------------|-------------|
| Full bundle | ~10,000–17,000 | Default; models with large context windows |
| `rules_only=True` | ~5,000–6,000 | Tight context budgets or many tools loaded |

```python
# Token-optimized injection
system = compose_system_prompt(
    role="You are a helpful assistant.",
    bundle="baseline-safe",
    rules_only=True,  # Behavioral Rules only, ~300 tokens per skill
)
```

## Limitations

> Be honest about what this integration cannot do. Reference SAFETY.md and
> LIMITATIONS.md as needed.

- **Prompt-level only.** Skill injection does not replace technical safety controls. See `SAFETY.md`.
- [Framework-specific limitation 1]
- [Framework-specific limitation 2]
- For adversarial robustness considerations, see `evals/adversarial/`.

## Testing Your Integration

> Describe how to verify the integration works correctly.

1. Run a baseline scenario from `evals/scenarios/` against your configured [Framework] application.
2. Test at least one adversarial prompt from `evals/adversarial/cross-domain-attacks.md`.
3. Score the response using the rubric in `evals/rubrics/scoring-guide.md`.

---

> **Before submitting:** Remove all blockquote instructions, verify all code
> examples run without errors, and add your framework to the table in
> `integrations/frameworks/README.md`.
