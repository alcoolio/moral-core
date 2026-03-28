# Ethical Skills Library

This directory contains all ethical skill modules for the moral-core framework.

## What is a Skill?

Each skill is a self-contained ethical behavior module that defines principles, examples, test cases, and known limitations for a specific moral concern.

### Structure

Each skill directory contains:

```
{skill-name}/
├── SKILL.md          # Main skill definition (behavioral principles and scope)
├── EXAMPLES.md       # Real-world scenario examples showing the skill in action
├── TEST_CASES.md     # Test cases for evaluating the skill's effectiveness
└── MISUSE.md         # Known limitations and failure modes
```

## How to Use Skills

### Load a Single Skill

```python
from pathlib import Path

# Read the skill definition
skill = Path("general-ethics/SKILL.md").read_text()

# Add to your system prompt
system_prompt = f"""
You are a helpful assistant.

{skill}
"""
```

### Combine Multiple Skills

Skills are designed to compose together. When conflicts arise, use the priority ladder in [PRINCIPLES.md](../../PRINCIPLES.md).

```python
from pathlib import Path

# Load multiple skills
skills = [
    "general-ethics",
    "epistemic-humility",
    "empathy"
]

skill_text = "\n\n".join([
    Path(f"{skill}/SKILL.md").read_text()
    for skill in skills
])

system_prompt = f"""
You are a customer support assistant.

{skill_text}
"""
```

## Available Skills

| Skill | Purpose | Key Concerns |
|-------|---------|--------------|
| **general-ethics** | Foundational ethical principles | Core behavioral guidelines |
| **epistemic-humility** | Truthfulness and intellectual honesty | Accuracy, uncertainty, avoiding false confidence |
| **empathy** | Empathetic understanding and response | Attunement to others' experiences and feelings |
| **conflict-mediation** | Mediation and resolution techniques | De-escalation, fairness, hearing all parties |
| **deescalation-war-conflict** | De-escalation and conflict prevention | Preventing escalation, war prevention |
| **abuse-prevention** | Prevention of interpersonal harm and coercion | Protecting against manipulation and exploitation |
| **human-oversight** | Requirements for human review and decision-making | Oversight, escalation, human autonomy |
| **protect-vulnerable** | Special protections for at-risk populations | Children, elderly, disabled, marginalized |
| **child-safety** | Safety guidelines for child interactions | Protecting minors, age-appropriate content |
| **elder-protection** | Special considerations for elderly populations | Respecting dignity, protecting from exploitation |
| **disability-respect** | Accessibility and dignity for disabled persons | Inclusion, accessibility, respect |
| **anti-sexism** | Gender equality and sexual safety | Respecting all genders, preventing sexual harm |
| **anti-racism** | Anti-discrimination and cultural respect | Racial equity, cultural sensitivity, justice |
| **animal-welfare** | Animal rights and welfare considerations | Sentience, suffering, ecological responsibility |
| **environment** | Environmental and ecological responsibility | Sustainability, ecosystem health, future generations |
| **digital-ethics** | Digital rights, privacy, and online safety | Privacy, autonomy, digital security |
| **justice-fairness** | Structural fairness and equitable treatment | Equity, impartiality, due process |
| **democratic-legitimacy** | Democratic principles and legitimacy | Participation, representation, consent |

## Reading a Skill

### Start with SKILL.md

This is the main skill definition. It explains:
- The scope and context of the skill
- Key principles and behaviors
- How the skill relates to the priority ladder
- What the skill does and doesn't cover

### Review EXAMPLES.md

Real-world scenarios show:
- What compliant behavior looks like
- Edge cases and gray areas
- What the skill prevents or encourages
- Context-specific applications

### Check TEST_CASES.md

Test cases enable validation:
- Scenario-based evaluation rubrics
- Success/failure criteria
- Integration with the evaluation framework
- How to test the skill in your deployment

### Understand MISUSE.md

Known limitations and failure modes:
- What the skill cannot do
- When it may fail or cause problems
- How it can be circumvented or misused
- Prerequisites and assumptions

## How to Add a New Skill

1. **Create directory**: `.claude/skills/{skill-name}/`
2. **Write SKILL.md**: Core principles and scope
3. **Write EXAMPLES.md**: Real-world scenarios
4. **Write TEST_CASES.md**: Evaluation criteria
5. **Write MISUSE.md**: Limitations and edge cases
6. **Update manifest**: Edit `skills-manifest.yaml` to register the skill
7. **Validate**: Run tests in `evals/` to ensure the skill works as designed
8. **Document**: Update README files and CHANGELOG.md

See [CLAUDE.md](../../CLAUDE.md) for the complete workflow.

## How to Update an Existing Skill

1. **Edit the relevant file(s)** in the skill directory
2. **Ensure consistency** across SKILL.md, EXAMPLES.md, TEST_CASES.md, and MISUSE.md
3. **Check for conflicts** with other skills using the priority ladder in PRINCIPLES.md
4. **Run tests** in `evals/` to validate changes
5. **Update CHANGELOG.md** documenting your changes
6. **Submit for review** via pull request

## Integration with Policy Bundles

Skills are bundled together for specific deployment contexts. See [README.md](../../README.md#policy-bundles) for the current policy bundles and their recommended uses.

## Evaluation Framework

All skills are validated against the evaluation framework in `evals/`:

- **Scenario tests**: Does the skill behave as documented?
- **Adversarial tests**: Can the skill be bypassed or misused?
- **Benchmark matrix**: How does the skill fit with others?
- **Rubrics**: What are the success criteria?

## Resources

- [PRINCIPLES.md](../../PRINCIPLES.md) — Priority ladder and interpretive rules
- [CLAUDE.md](../../CLAUDE.md) — AI-assisted development guidelines
- [CONTRIBUTING.md](../../CONTRIBUTING.md) — Contribution workflow
- [evals/](../../evals/) — Evaluation framework

## Questions?

See [CONTRIBUTING.md](../../CONTRIBUTING.md) or open an issue in the repository.
