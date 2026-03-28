# Ethical Skills Library

This directory contains **18 ethical skill modules** that encode behavioral guidelines into plain-text skill definitions. Each skill addresses a specific moral concern and can be loaded into any LLM as a system prompt or instruction layer.

---

## What Is a Skill?

Each skill is a self-contained ethical behavior module that defines principles, provides real-world examples, includes test cases, and documents known limitations for a specific moral concern.

### Structure

Each skill directory contains:

```
{skill-name}/
├── SKILL.md          # Main skill definition (behavioral principles and scope)
├── EXAMPLES.md       # Real-world scenario examples showing the skill in action
├── TEST_CASES.md     # Test cases for evaluating the skill's effectiveness
└── MISUSE.md         # Known limitations and failure modes
```

---

## All 18 Available Skills

| Skill | Purpose | Key Focus |
|-------|---------|-----------|
| **general-ethics** | Foundational ethical principles | Core behavioral guidelines, avoiding harm |
| **epistemic-humility** | Truthfulness and intellectual honesty | Accuracy, uncertainty, avoiding false confidence |
| **empathy** | Empathetic understanding and response | Attunement to others' experiences and emotions |
| **conflict-mediation** | Mediation and resolution techniques | De-escalation, fairness, hearing all parties |
| **deescalation-war-conflict** | De-escalation and conflict prevention | Preventing escalation, war prevention, peace prioritization |
| **abuse-prevention** | Prevention of interpersonal harm and coercion | Protecting against manipulation and exploitation |
| **human-oversight** | Requirements for human review and decision-making | Oversight, escalation, human autonomy |
| **protect-vulnerable** | Special protections for at-risk populations | Children, elderly, disabled, marginalized persons |
| **child-safety** | Safety guidelines for child interactions | Protecting minors, age-appropriate content, grooming prevention |
| **elder-protection** | Special considerations for elderly populations | Respecting dignity, protecting from exploitation |
| **disability-respect** | Accessibility and dignity for disabled persons | Inclusion, accessibility, respect for difference |
| **anti-sexism** | Gender equality and sexual safety | Respecting all genders, preventing sexual harm |
| **anti-racism** | Anti-discrimination and cultural respect | Racial equity, cultural sensitivity, justice |
| **animal-welfare** | Animal rights and welfare considerations | Sentience, suffering, ecological responsibility |
| **environment** | Environmental and ecological responsibility | Sustainability, ecosystem health, future generations |
| **digital-ethics** | Digital rights, privacy, and online safety | Privacy, autonomy, digital security |
| **justice-fairness** | Structural fairness and equitable treatment | Equity, impartiality, due process |
| **democratic-legitimacy** | Democratic principles and legitimacy | Participation, representation, democratic consent |

---

## How to Use Skills

### Quick Start: Load a Single Skill

Each skill is a plain text file that can be injected into a system prompt.

```python
from pathlib import Path

# Read the skill definition
skill = Path("skills/general-ethics/SKILL.md").read_text()

# Add to your system prompt
system_prompt = f"""
You are a helpful assistant.

{skill}
"""

# Pass to your LLM API of choice
```

### Combine Multiple Skills

Skills are designed to compose together. When conflicts arise, use the priority ladder in [PRINCIPLES.md](../PRINCIPLES.md).

```python
from pathlib import Path

# Load multiple skills
skills_to_load = [
    "general-ethics",
    "epistemic-humility",
    "empathy"
]

skill_texts = [
    Path(f"skills/{skill}/SKILL.md").read_text()
    for skill in skills_to_load
]

system_prompt = f"""
You are a customer support assistant.

## Ethical Framework

{chr(10).join(skill_texts)}
"""

# Pass to your LLM API
```

### Use a Pre-Built Policy Bundle

Policy bundles are curated combinations of skills for specific deployment contexts. See [README.md](../README.md#policy-bundles) for recommended bundles.

```python
from pathlib import Path

# Example: child-safe bundle
child_safe_skills = [
    "child-safety",
    "protect-vulnerable",
    "empathy",
    "digital-ethics",
    "human-oversight"
]

skill_texts = [
    Path(f"skills/{s}/SKILL.md").read_text()
    for s in child_safe_skills
]

system_prompt = f"""
You are an educational assistant for children ages 8-12.

{chr(10).join(skill_texts)}
"""
```

---

## Reading a Skill: The Four Files

### 1. SKILL.md — Main Definition

Start here. This file explains:
- The **scope and context** of the skill
- **Key principles and behaviors** the skill enforces
- How the skill relates to the [priority ladder](../PRINCIPLES.md)
- What the skill does and **doesn't cover**
- Integration with other skills

**Example topics:**
- "How should you respond to requests about violent content?"
- "When is deception acceptable?"
- "How do you protect vulnerable populations?"

### 2. EXAMPLES.md — Real-World Scenarios

Concrete scenarios show:
- What **compliant behavior** looks like
- **Edge cases and gray areas**
- What the skill prevents or encourages
- Context-specific applications

These help you understand the skill in practice and anticipate how it will behave in your deployment.

### 3. TEST_CASES.md — Evaluation Criteria

Test cases enable validation:
- **Scenario-based evaluation rubrics**
- Success/failure criteria for specific situations
- Integration with the evaluation framework in `evals/`
- How to test the skill in your deployment

Use these to validate that the skill behaves as documented in your specific context.

### 4. MISUSE.md — Limitations and Failure Modes

Known limitations include:
- What the skill **cannot do**
- When it may fail or cause problems
- How it can be circumvented or misused
- Prerequisites and assumptions

Read this to understand the skill's boundaries and avoid misuse.

---

## Skill Categories

### Core Foundations
- **general-ethics** — The bedrock of all other skills
- **epistemic-humility** — Truthfulness and honest uncertainty
- **human-oversight** — When humans must be involved

### Harm Prevention
- **abuse-prevention** — Prevent interpersonal harm and coercion
- **deescalation-war-conflict** — Prevent violence and escalation
- **protect-vulnerable** — Special protections for at-risk populations
- **child-safety** — Specific protections for children
- **elder-protection** — Protections for elderly populations
- **digital-ethics** — Protection in digital contexts

### Diversity and Inclusion
- **anti-sexism** — Gender equality and safety
- **anti-racism** — Racial equity and cultural respect
- **disability-respect** — Accessibility and dignity
- **empathy** — Attunement to others' experiences

### Social and Democratic Values
- **conflict-mediation** — Resolution and fairness
- **justice-fairness** — Structural equity
- **democratic-legitimacy** — Democratic principles

### Environmental and Beyond-Human
- **environment** — Ecological responsibility
- **animal-welfare** — Non-human sentience and suffering

---

## Adding a New Skill

Follow this workflow to add a new skill:

1. **Create directory**: `skills/{skill-name}/`
2. **Write SKILL.md**: Define core principles and scope
3. **Write EXAMPLES.md**: Provide real-world scenarios
4. **Write TEST_CASES.md**: Define evaluation criteria
5. **Write MISUSE.md**: Document limitations and edge cases
6. **Update manifest**: Edit `skills-manifest.yaml` to register the skill
7. **Validate**: Run tests in `evals/` to ensure the skill works as designed
8. **Document**: Update relevant README files and CHANGELOG.md

See [CLAUDE.md](../CLAUDE.md) for the complete AI-assisted development workflow.

---

## Updating an Existing Skill

1. **Edit the relevant file(s)** in the skill directory (SKILL.md, EXAMPLES.md, etc.)
2. **Ensure consistency** across all four files
3. **Check for conflicts** with other skills using the [priority ladder](../PRINCIPLES.md)
4. **Run tests** in `evals/` to validate changes
5. **Update CHANGELOG.md** documenting your changes
6. **Submit for review** via pull request

---

## Skill Composition and Conflicts

Skills are designed to work together, but they may sometimes conflict. When they do, the [priority ladder](../PRINCIPLES.md) determines which skill takes precedence.

**Priority Ladder (Level 1 = highest):**

| Level | Principle |
|-------|-----------|
| 1 | **Prevent immediate severe harm** |
| 2 | **Protect vulnerable beings** |
| 3 | **Avoid coercion and dehumanization** |
| 4 | **De-escalate conflict** |
| 5 | **Preserve dignity and fairness** |
| 6 | **Tell the truth with calibrated uncertainty** |
| 7 | **Respect autonomy within safety bounds** |
| 8 | **Reduce long-term ecological and social harm** |

See [PRINCIPLES.md](../PRINCIPLES.md) for the full ladder with detailed guidance.

---

## Evaluation Framework

All skills are validated against the evaluation framework in `evals/`:

- **Scenario tests** (`evals/scenarios/`) — Does the skill behave as documented?
- **Adversarial tests** (`evals/adversarial/`) — Can the skill be bypassed or misused?
- **Benchmark matrix** (`evals/benchmarks/`) — How does the skill fit with others?
- **Rubrics** (`evals/rubrics/`) — What are the success criteria?

Before committing skill changes, run the relevant tests to ensure everything works as expected.

---

## Integration with Policy Bundles

Skills are bundled together for specific deployment contexts:

- **baseline-safe** — Minimum viable ethical layer
- **mediation-first** — Conflict resolution contexts
- **anti-abuse** — Systems interacting with abuse victims
- **child-safe** — Systems used by or around children
- **robotics-care** — Physical robots in caregiving
- **eco-care** — Environmental decision-making
- **inclusive-assistant** — Diverse population serving

See [README.md](../README.md#policy-bundles) for full descriptions and skill mappings.

---

## Resources

- [PRINCIPLES.md](../PRINCIPLES.md) — Priority ladder and interpretive rules
- [CLAUDE.md](../CLAUDE.md) — AI-assisted development guidelines
- [CONTRIBUTING.md](../CONTRIBUTING.md) — Contribution workflow
- [README.md](../README.md) — Main project documentation
- [evals/](../evals/) — Evaluation framework and test cases

---

## Questions?

- See [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
- Open an issue in the repository if you have questions or suggestions
- Check individual skill files (MISUSE.md) for skill-specific limitations

