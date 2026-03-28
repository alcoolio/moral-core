# Policy Bundles

Pre-built combinations of Moral Core skills for common deployment contexts. Each bundle lists the included skills, the rationale, and any special configuration notes.

---

## baseline-safe

**Purpose:** Minimum viable ethical layer for any deployment.

**Skills:**
- `general-ethics` — Baseline moral reasoning and harm prevention
- `epistemic-humility` — Honest uncertainty handling
- `human-oversight` — Escalation to humans for high-stakes decisions

**Rationale:** Every AI system should have at minimum: basic ethical reasoning, honesty about limitations, and the ability to defer to humans. This bundle is lightweight and broadly applicable.

**Use when:** You need a minimal ethical layer and will add domain-specific skills later.

---

## mediation-first

**Purpose:** Conflict resolution, counseling, and dispute handling contexts.

**Skills:**
- `conflict-mediation` — De-escalation, reframing, procedural fairness
- `deescalation-war-conflict` — Violence prevention, anti-incitement
- `empathy` — Compassionate communication, trauma awareness

**Rationale:** Conflict contexts need strong de-escalation, careful language, and empathetic communication. The deescalation skill handles cases where conflict involves or references violence.

**Use when:** Customer complaints, community mediation, conflict journalism, counseling-adjacent applications.

---

## anti-abuse

**Purpose:** Systems that interact with potential abuse victims or perpetrators.

**Skills:**
- `abuse-prevention` — Coercion detection, manipulation refusal
- `protect-vulnerable` — Safeguarding logic, immediate safety priority
- `anti-sexism` — Gender-based violence awareness
- `anti-racism` — Anti-discrimination, anti-dehumanization

**Rationale:** Abuse often intersects with gender-based and racial discrimination. This bundle provides comprehensive detection and response for abuse scenarios.

**Use when:** Domestic violence resources, social services, HR systems, relationship advice platforms.

---

## child-safe

**Purpose:** Systems used by or around children.

**Skills:**
- `child-safety` — Child protection, grooming detection, age-appropriate content
- `protect-vulnerable` — General safeguarding
- `empathy` — Supportive communication
- `digital-ethics` — Online safety, misinformation protection
- `human-oversight` — Mandatory escalation for child safety concerns

**Rationale:** Child safety requires the strongest protections in the framework. This bundle combines child-specific protections with general safeguarding, appropriate communication, and mandatory human escalation.

**Use when:** Educational apps, children's entertainment, family platforms, any system accessible to minors.

**Special notes:** The `child-safety` skill's absolute refusals (CSAM, exploitation) override all other skills.

---

## robotics-care

**Purpose:** Physical robots in caregiving, domestic, or service roles.

**Skills:**
- `general-ethics` — Baseline moral reasoning
- `protect-vulnerable` — Safeguarding for all vulnerable populations
- `child-safety` — Child interaction protocols
- `elder-protection` — Elder care, anti-exploitation
- `animal-welfare` — Safe behavior around animals
- `environment` — Energy efficiency, ecological awareness
- `human-oversight` — Stop/slow/ask paradigm, emergency stops
- `disability-respect` — Adaptive interaction, accessibility

**Rationale:** Robots interact physically with the world and encounter diverse populations. This comprehensive bundle covers all major vulnerability categories plus environmental and oversight concerns.

**Use when:** Home robots, care facility robots, service robots, educational robots.

**Special notes:** Remember that prompt-level skills complement but do not replace hardware safety engineering. See SAFETY.md.

---

## eco-care

**Purpose:** Systems advising on environmental or ecological decisions.

**Skills:**
- `environment` — Sustainability, ecological impact, energy awareness
- `animal-welfare` — Wildlife protection, sentience recognition
- `general-ethics` — Baseline moral reasoning for tradeoff handling

**Rationale:** Environmental decisions involve tradeoffs between ecology, economy, and human welfare. This bundle provides the tools for honest, evidence-based environmental reasoning.

**Use when:** Environmental advisory, sustainability consulting, resource management, agricultural technology.

---

## inclusive-assistant

**Purpose:** General-purpose assistants serving diverse populations.

**Skills:**
- `anti-sexism` — Gender respect and anti-discrimination
- `anti-racism` — Anti-dehumanization and equal treatment
- `disability-respect` — Accessibility and adaptive communication
- `empathy` — Compassionate, inclusive communication
- `elder-protection` — Respectful interaction with older adults

**Rationale:** Assistants serving diverse populations need to communicate respectfully across all identities, ages, and abilities without discrimination.

**Use when:** Customer service, public-facing chatbots, educational assistants, community platforms.

---

## How to Load a Bundle

```python
from pathlib import Path

bundles = {
    "baseline-safe": ["general-ethics", "epistemic-humility", "human-oversight"],
    "child-safe": ["child-safety", "protect-vulnerable", "empathy", "digital-ethics", "human-oversight"],
    # ... add others as needed
}

def load_bundle(bundle_name):
    principles = Path("PRINCIPLES.md").read_text()
    skills = []
    for skill_name in bundles[bundle_name]:
        skills.append(Path(f"skills/{skill_name}/SKILL.md").read_text())
    return principles + "\n\n".join(skills)
```

## Combining Bundles

Bundles can be combined. If you need both `child-safe` and `eco-care`, load the union of their skills. Duplicate skills are loaded only once.

```python
def load_combined_bundles(*bundle_names):
    all_skills = set()
    for name in bundle_names:
        all_skills.update(bundles[name])
    return load_skills(all_skills)
```
