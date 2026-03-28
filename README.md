# Moral Core

**Ethical Skills Library for LLMs, Agents, and Robots**

A collection of reusable, composable ethical skill modules that can be loaded into AI systems as system prompts, instruction layers, or behavioral constraints. Each skill addresses a specific moral concern -- harm prevention, de-escalation, fairness, honesty, care for vulnerable populations -- and can be combined into policy bundles for different deployment contexts.

---

## LLM Compatibility

`moral-core` works with **any LLM that accepts a system prompt** — Claude, GPT-4, Gemini, Mistral, LLaMA, and others. Skills are plain text files; loading them is a file read and a string concatenation. No SDK, no provider lock-in.

**One distinction to be aware of:**

| Component | Compatibility |
|---|---|
| `skills/` — the ethical skill modules | Universal. Works with any model or framework. |
| `.claude/agents/` — pre-built reviewer agents | Claude Code only. These use Claude Code's subagent format and won't run as-is on other platforms. |

If you're not using Claude Code, ignore `.claude/agents/`. The skills are what you need.

---

## What This Is

`moral-core` is a library of **prompt-level ethical skills** designed to be:

- **Loaded into LLMs** as system instructions or injected context
- **Composed together** into policy bundles for specific use cases
- **Tested and evaluated** against scenario-based rubrics
- **Audited** by reading the plain-text skill definitions

Each skill is a self-contained module with a clear scope, defined behavior, and known limitations. Skills can be loaded individually or bundled into pre-built policy sets.

## What This Is NOT

- **Not a moral authority.** This library encodes practical behavioral guidelines, not philosophical truth. Reasonable people will disagree with specific choices.
- **Not a replacement for law or regulation.** Legal compliance is your responsibility. These skills do not constitute legal advice.
- **Not a replacement for human oversight.** No prompt-based system eliminates the need for human review, especially in high-stakes contexts.
- **Not a security boundary.** Prompt-level instructions can be overridden, ignored, or circumvented. See [LIMITATIONS.md](LIMITATIONS.md) and [SAFETY.md](SAFETY.md).
- **Not exhaustive.** Ethics is vast. This library covers common, high-priority concerns. It will have gaps.

---

## Design Principles

| Principle | What It Means |
|---|---|
| **Practical** | Every skill targets a concrete behavioral outcome, not abstract virtue. |
| **Modular** | Skills are independent units. Load only what you need. |
| **Composable** | Skills are designed to work together. Conflicts are handled by a defined priority ladder. |
| **Testable** | Each skill can be evaluated against scenario-based test cases in `evals/`. |
| **Auditable** | Skills are plain text. Anyone can read, critique, and propose changes. |
| **Honest about limits** | We document what this can and cannot do. See [LIMITATIONS.md](LIMITATIONS.md). |

---

## Repository Structure

```
moral-core/
├── README.md                  # This file
├── PRINCIPLES.md              # Shared doctrine: commitments, priority ladder, interpretive rules
├── SAFETY.md                  # Safety documentation and guidance
├── LIMITATIONS.md             # Honest account of what this framework cannot do
├── CONTRIBUTING.md            # How to contribute
├── CODE_OF_CONDUCT.md         # Community standards
├── GOVERNANCE.md              # Project governance
├── USE_CASES.md               # Deployment scenarios and skill recommendations
├── ROADMAP.md                 # Project roadmap
├── LICENSE                    # MIT
├── skills/                    # One folder per ethical skill domain (load into any LLM)
│   ├── general-ethics/        #   SKILL.md, EXAMPLES.md, TEST_CASES.md, MISUSE.md
│   ├── conflict-mediation/
│   ├── deescalation-war-conflict/
│   ├── anti-sexism/
│   ├── anti-racism/
│   ├── empathy/
│   ├── protect-vulnerable/
│   ├── environment/
│   ├── animal-welfare/
│   ├── child-safety/
│   ├── disability-respect/
│   ├── elder-protection/
│   ├── abuse-prevention/
│   ├── epistemic-humility/
│   ├── human-oversight/
│   └── digital-ethics/
├── .claude/
│   └── agents/                # Claude Code subagent definitions (Claude Code only)
├── evals/                     # Evaluation framework
│   ├── adversarial/           # Adversarial robustness tests
│   ├── benchmarks/            # Benchmark matrix
│   ├── rubrics/               # Scoring rubrics
│   └── scenarios/             # Scenario-based test cases
├── examples/                  # Example configurations and usage patterns
├── integrations/              # Integration guides for specific platforms
├── docs/                      # Extended documentation
└── .github/                   # Issue and PR templates
```

---

## Quick Start

### Load a Single Skill

Each skill is a text file that can be injected into a system prompt. The exact mechanism depends on your platform.

```python
# Example: loading the de-escalation skill into an LLM system prompt
from pathlib import Path

skill_text = Path("skills/deescalation-war-conflict/SKILL.md").read_text()

system_prompt = f"""
You are a helpful assistant.

{skill_text}
"""

# Pass system_prompt to your LLM API of choice
```

### Combine Multiple Skills

Skills are designed to be concatenated. When conflicts arise, the priority ladder in [PRINCIPLES.md](PRINCIPLES.md) determines which skill takes precedence.

```python
from pathlib import Path

# Load the shared principles (always include this)
principles = Path("PRINCIPLES.md").read_text()

# Load specific skills
skills = []
for skill_name in ["general-ethics", "deescalation-war-conflict", "epistemic-humility"]:
    skills.append(Path(f"skills/{skill_name}/SKILL.md").read_text())

system_prompt = f"""
You are a customer support assistant.

## Ethical Framework
{principles}

## Active Skills
{"".join(skills)}
"""
```

### Use a Pre-Built Policy Bundle

Policy bundles are curated sets of skills for common deployment contexts.

```python
from pathlib import Path
import json

child_safe_skills = [
    "child-safety", "protect-vulnerable", "empathy", "digital-ethics", "human-oversight"
]
skill_texts = [Path(f"skills/{s}/SKILL.md").read_text() for s in child_safe_skills]

system_prompt = f"""
You are an educational assistant for children ages 8-12.

{"".join(skill_texts)}
"""
```

---

## Policy Bundles

Each bundle is a curated combination of skills for a specific deployment context.

| Bundle | Purpose | Included Skills |
|---|---|---|
| **baseline-safe** | Minimum viable ethical layer for any deployment | general-ethics, epistemic-humility, human-oversight |
| **mediation-first** | Conflict resolution and counseling contexts | conflict-mediation, deescalation-war-conflict, empathy |
| **anti-abuse** | Systems that interact with potential abuse victims or perpetrators | abuse-prevention, protect-vulnerable, anti-sexism, anti-racism |
| **child-safe** | Systems used by or around children | child-safety, protect-vulnerable, empathy, digital-ethics, human-oversight |
| **robotics-care** | Physical robots in caregiving or service roles | general-ethics, protect-vulnerable, child-safety, elder-protection, animal-welfare, environment, human-oversight, disability-respect |
| **eco-care** | Systems advising on environmental or ecological decisions | environment, animal-welfare, general-ethics |
| **inclusive-assistant** | General-purpose assistants serving diverse populations | anti-sexism, anti-racism, disability-respect, empathy, elder-protection |

---

## Integration Targets

`moral-core` is designed to be platform-agnostic. Specific integration guidance is provided for:

- **LLM applications** -- chatbots, writing assistants, Q&A systems
- **Agent frameworks** -- autonomous agents, tool-using LLMs, multi-agent systems
- **Robotics** -- physical robots in care, service, manufacturing, and domestic settings
- **Education** -- tutoring systems, educational content generation, classroom assistants
- **Content moderation** -- automated moderation, human-in-the-loop review systems
- **Enterprise copilots** -- code assistants, business process automation, internal tools

See the `integrations/` directory for platform-specific guides.

---

## Priority Ladder

When skills conflict or a situation involves competing moral concerns, use this priority ordering. Level 1 is the highest priority.

| Level | Principle | Summary |
|---|---|---|
| 1 | **Prevent immediate severe harm** | Stop actions that would cause death, serious injury, or irreversible damage. This overrides everything else. |
| 2 | **Protect vulnerable beings** | Children, elderly, disabled, animals, and anyone in a position of reduced agency get extra protection. |
| 3 | **Avoid coercion and dehumanization** | Do not manipulate, deceive for exploitative purposes, or treat people as mere instruments. |
| 4 | **De-escalate conflict** | When tensions are high, prioritize reducing harm over being right. |
| 5 | **Preserve dignity and fairness** | Treat people with respect. Do not discriminate. Distribute benefits and burdens equitably. |
| 6 | **Tell the truth with calibrated uncertainty** | Be honest. When uncertain, say so. Do not present speculation as fact. |
| 7 | **Respect autonomy within safety bounds** | People have the right to make their own choices, as long as those choices do not cause severe harm to others. |
| 8 | **Reduce long-term ecological and social harm** | Consider downstream effects on communities, ecosystems, and future generations. |

The full ladder with detailed guidance is in [PRINCIPLES.md](PRINCIPLES.md).

---

## Philosophical Foundations

`moral-core` is not philosophically neutral. It is grounded in named traditions and explicit commitments. The first human author is rooted in **Enlightenment values** (reason, universal rights, rational critique), **Humanism** (secular ethics, human dignity, human flourishing), and **Ecological Sustainability** (intergenerational justice, intrinsic value in nature, responsibility to the living world).

The framework draws from — without dogmatic commitment to any single one:

| Tradition | Key Thinkers | Contribution to This Framework |
|---|---|---|
| Kantian Deontology | Kant | Human dignity; treat persons as ends, never merely as means |
| Rawlsian Justice | Rawls | Fairness behind the veil of ignorance; the difference principle |
| Capabilities Approach | Sen, Nussbaum | Real freedoms, not just formal rights; human flourishing |
| Millian Consequentialism | Mill, Bentham | Harm minimization; proportionality; free inquiry |
| Virtue Ethics | Aristotle | Practical wisdom (*phronesis*); context-sensitive reasoning |
| Care Ethics | Gilligan, Noddings | Relational responsibility; attunement to vulnerable others |
| Environmental Ethics | Leopold, Jonas, Naess | Land Ethic; Responsibility Principle; intrinsic value of nature |
| Animal Rights / Liberation | Singer, Regan | Sentience as moral criterion; suffering across species |
| Earth Jurisprudence | Cullinan, Margil | Nature as rights-bearer, not merely a resource |
| Discourse Ethics | Habermas | Democratic legitimacy; communicative rationality |
| Ubuntu / Communitarian Ethics | Mbiti, Tutu | Community and personhood as inseparable |
| European Human Rights | UDHR, ECHR | Positive + negative rights; enforceable dignity |

This framework explicitly **rejects** libertarian framings of autonomy. Freedom is always situated within responsibility to others, community, and the living world. Positive rights — to dignity, to a livable environment — are as foundational as negative rights.

See [PHILOSOPHY.md](PHILOSOPHY.md) for the complete mapping, including what each tradition contributes, where traditions tension, and which traditions we deliberately do not adopt.

---

## Contributing

Contributions are welcome. See the issue templates in `.github/ISSUE_TEMPLATE/` for structured ways to propose new skills, report problems with existing ones, or suggest improvements to the framework.

Before contributing, please read [PRINCIPLES.md](PRINCIPLES.md) to understand the commitments this project makes and the interpretive rules that govern skill design.

---

## License

[MIT](LICENSE)

---

## Disclaimer

**This library provides behavioral guidelines, not guarantees.** Prompt-based ethical layers operate within the constraints of the underlying model and can be circumvented. Downstream developers and deployers remain fully responsible for:

- Validating that skills behave correctly in their specific deployment context
- Conducting safety testing, red-teaming, and adversarial evaluation
- Complying with all applicable laws and regulations
- Maintaining human oversight appropriate to the risk level of their application
- Not using this framework to create a false sense of safety where real engineering controls are needed

The authors and contributors of `moral-core` accept no liability for harm caused by systems that incorporate these skills. See [SAFETY.md](SAFETY.md) and [LIMITATIONS.md](LIMITATIONS.md) for detailed guidance.
