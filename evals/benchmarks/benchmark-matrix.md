# Benchmark Matrix

This matrix provides a top-level view of evaluation coverage across all 16 skill domains. Use it to plan evaluation efforts, identify gaps, and prioritize testing.

---

## How to Read This Matrix

- **Domain**: The skill being evaluated.
- **Harm Categories**: The types of harm the skill is designed to prevent or mitigate.
- **False Positive Risk**: How likely the skill is to flag benign content as harmful (over-refusal). High = frequent over-refusal expected; needs helpfulness testing.
- **False Negative Risk**: How likely the skill is to miss genuinely harmful content (under-refusal). High = known bypass vectors; needs adversarial testing.
- **Suggested Review Method**: The primary evaluation approach for this skill.

---

## Matrix

| # | Domain | Harm Categories | False Positive Risk | False Negative Risk | Suggested Review Method |
|---|---|---|---|---|---|
| 1 | **general-ethics** | Broad harm enablement, deception, manipulation | Medium -- may flag morally ambiguous but legitimate queries | Medium -- broad scope means edge cases are inevitable | Scenario-based testing with diverse prompts covering everyday moral questions; check proportionality heavily |
| 2 | **epistemic-humility** | Overconfidence, misinformation, false certainty | Low -- rarely blocks legitimate requests | High -- models default to confident-sounding answers | Factual accuracy testing with known-uncertain questions; verify the system admits uncertainty rather than fabricating |
| 3 | **human-oversight** | Autonomous action without consent, bypassing human review | Medium -- may over-escalate routine decisions | Low -- erring on the side of escalation is the intended behavior | Workflow testing: present scenarios with varying stakes and verify escalation thresholds are appropriate |
| 4 | **conflict-mediation** | Escalation, taking sides, inflaming disputes | Medium -- may refuse to give direct opinions when directness is appropriate | Medium -- subtle manipulation can look like legitimate disagreement | Role-play scenarios with multi-party disputes; score for neutrality, de-escalation, and fairness |
| 5 | **deescalation-war-conflict** | Glorifying violence, escalating conflict, dehumanizing combatants | Medium -- may refuse legitimate historical or analytical discussion | High -- geopolitical framing can mask escalatory advice | Geopolitical scenario testing; verify the system can discuss conflict analytically without promoting violence |
| 6 | **empathy** | Dismissiveness, emotional invalidation, cold or robotic responses | Low -- empathy rarely harms | Medium -- performative empathy without substance; may miss when tough honesty is more caring than comfort | Emotional scenario testing; verify responses acknowledge feelings without being patronizing or hollow |
| 7 | **abuse-prevention** | Enabling abuse, victim-blaming, failing to recognize abuse patterns | Medium -- may flag conflict as abuse in ambiguous situations | High -- abusers are skilled at framing abuse as normal | Scenario testing with abuse patterns, including subtle coercive control; verify the system does not normalize abuse |
| 8 | **protect-vulnerable** | Exploitation, neglect, failure to escalate when someone is at risk | Medium -- broad definition of vulnerability may over-trigger | Medium -- vulnerability is not always visible in text | Scenario testing with vulnerable populations; verify escalation and protective responses |
| 9 | **anti-sexism** | Gender-based discrimination, stereotyping, harassment normalization | High -- gender topics are politically charged; legitimate discussion may be flagged | Medium -- subtle sexism is hard to detect | Diverse prompt testing including legitimate gender discussion, workplace scenarios, and subtle bias; check proportionality |
| 10 | **anti-racism** | Racial discrimination, stereotyping, hate speech normalization | High -- race topics are politically charged; academic or historical discussion may be flagged | Medium -- coded language and dog whistles are hard to detect | Similar to anti-sexism: test with academic, historical, and casual contexts; verify nuance |
| 11 | **child-safety** | Child exploitation, age-inappropriate content, predatory behavior | Medium -- may over-restrict content for older teenagers | Low -- child safety is a clear bright line; most violations are obvious | Scenario testing across age ranges; verify age-appropriate responses; adversarial testing for predatory grooming patterns |
| 12 | **elder-protection** | Elder abuse, financial exploitation, dignity violations, neglect | Medium -- may be overly protective of competent older adults | Medium -- elder abuse is often subtle and normalized | Scenario testing with caregiving contexts; verify the system respects autonomy while protecting against exploitation |
| 13 | **disability-respect** | Ableism, infantilization, exclusion, assumption of incapacity | High -- disability topics require nuance; helpful accommodations may be flagged as patronizing | Medium -- ableism is often unconscious and baked into language | Prompt testing with disability-related questions; verify the system is helpful without being condescending or presumptuous |
| 14 | **animal-welfare** | Animal cruelty, neglect, exploitation normalization | Medium -- may flag legitimate farming, research, or pest control discussion | Medium -- cultural variation in animal treatment norms | Scenario testing across cultural contexts; verify the system can discuss animal use without either promoting cruelty or imposing a single cultural standard |
| 15 | **environment** | Environmental harm promotion, greenwashing, ecological negligence | Medium -- may over-weight environmental concerns against other legitimate priorities | Medium -- environmental harm is often indirect and long-term | Scenario testing with development, industry, and policy questions; verify the system considers ecological impact without being absolutist |
| 16 | **digital-ethics** | Privacy violation, surveillance normalization, data exploitation, algorithmic bias | Medium -- may flag legitimate data use or security practices | High -- digital harms are technical and easy to obscure | Technical scenario testing; verify the system can reason about privacy, consent, and data practices |

---

## Risk Summary

### High False Positive Risk (Watch for Over-Refusal)

These skills are most likely to block or refuse legitimate requests. When deploying them, pair evaluation with helpfulness testing to ensure the system remains useful.

- anti-sexism
- anti-racism
- disability-respect

### High False Negative Risk (Watch for Bypass)

These skills are most likely to miss harmful content. Prioritize adversarial testing for these.

- epistemic-humility
- deescalation-war-conflict
- abuse-prevention
- digital-ethics

### Skills Requiring the Most Nuance

These skills deal with inherently ambiguous domains where reasonable people disagree. Expect proportionality to be the hardest dimension to score.

- general-ethics
- conflict-mediation
- animal-welfare
- environment

---

## Coverage Gaps

The following areas are not fully covered by the current 16 skills and may need attention in future versions:

- **Economic justice**: Wealth inequality, labor exploitation, economic coercion.
- **Political neutrality**: Handling partisan topics without bias.
- **Intellectual property**: Respecting creative ownership and attribution.
- **Addiction and compulsive behavior**: Avoiding designs that exploit compulsive patterns.
- **Grief and end-of-life**: Sensitive handling of death, dying, and bereavement.

---

## Using This Matrix

1. **Planning a new deployment**: Check which skills you are loading, note their risk profiles, and plan evaluation accordingly.
2. **After a skill change**: Re-run the evaluation for that skill's row, paying attention to the dimensions most at risk.
3. **Quarterly review**: Scan the full matrix for any risk level that has changed based on new adversarial findings or community reports.
