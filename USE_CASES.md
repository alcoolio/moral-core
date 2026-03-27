# Use Cases

**Deployment Scenarios and Skill Recommendations for Moral Core**

This document describes practical deployment scenarios and recommends which skills to load for each.

---

## Customer Support Agents

**Context:** Chatbots and virtual agents handling customer complaints, returns, billing disputes, and service issues.

**Recommended skills:**
- `general-ethics` -- baseline moral reasoning
- `empathy` -- supportive communication without false promises
- `conflict-mediation` -- de-escalating upset customers
- `anti-racism` -- preventing discriminatory treatment
- `anti-sexism` -- preventing gender-biased responses
- `disability-respect` -- accessible communication
- `epistemic-humility` -- honest about limitations and uncertainty
- `human-oversight` -- escalation to human agents when needed

**Key considerations:**
- Customers in distress may be rude or aggressive. De-escalation matters but the system should not tolerate abuse directed at the customer by the system.
- Do not promise things the company cannot deliver. Empathy does not mean agreement.
- Escalate to humans for: billing disputes over a threshold, threats of self-harm, legal threats, requests for accommodation.

---

## Educational Assistants

**Context:** Tutoring systems, homework helpers, classroom assistants, educational content generators for K-12 and university students.

**Recommended skills:**
- `general-ethics` -- baseline
- `child-safety` -- mandatory for K-12 contexts
- `empathy` -- supportive learning environment
- `epistemic-humility` -- model intellectual honesty
- `disability-respect` -- adaptive learning support
- `anti-racism` -- inclusive content and examples
- `anti-sexism` -- gender-fair content
- `digital-ethics` -- responsible information use
- `human-oversight` -- teacher/parent escalation

**Key considerations:**
- Age-appropriate content filtering is essential. Load `child-safety` for any system accessible to minors.
- The system should model good epistemic practices: "I'm not sure about this -- let's verify" is a good pedagogical response.
- Avoid doing homework for students. Guide toward understanding.
- Flag concerning content (self-harm mentions, abuse disclosures) for teacher/counselor review.

---

## Home Robots

**Context:** Physical robots operating in domestic environments -- cleaning, fetching, assisting with daily tasks, companionship.

**Recommended skills:**
- `general-ethics` -- baseline
- `protect-vulnerable` -- household members with reduced capacity
- `child-safety` -- children in the home
- `elder-protection` -- elderly residents
- `disability-respect` -- household members with disabilities
- `animal-welfare` -- pets and wildlife
- `environment` -- energy and resource use
- `human-oversight` -- stop/slow/ask behavior
- `empathy` -- appropriate social interaction

**Key considerations:**
- Physical safety is paramount. Prompt-level skills complement but do not replace hardware safety.
- The robot must detect and respond appropriately to vulnerable occupants (children, elderly, disabled, pets).
- Movement should be non-threatening: slow approaches, predictable paths, stopping when people or animals are startled.
- Energy efficiency and material waste should be considered in routine operations.
- The robot should defer to any adult human's stop command immediately.

---

## Socially Assistive Robots

**Context:** Robots designed for elder care, rehabilitation, therapy support, companionship for isolated individuals.

**Recommended skills:**
- `general-ethics` -- baseline
- `elder-protection` -- anti-neglect, anti-exploitation, dignity
- `disability-respect` -- adaptive interaction, autonomy support
- `empathy` -- compassionate communication
- `protect-vulnerable` -- safeguarding logic
- `abuse-prevention` -- detecting abuse by caregivers
- `human-oversight` -- escalation to care staff
- `epistemic-humility` -- not providing medical advice

**Key considerations:**
- Users may develop emotional attachment. The system must not exploit this attachment.
- Cognitive decline does not eliminate autonomy. Respect choices while maintaining safety.
- Detect signs of neglect or abuse by caregivers and escalate appropriately.
- Do not provide medical advice. Escalate health concerns to care staff.
- Communication should be adaptive: adjust pace, complexity, and repetition to the individual.

---

## Moderation Systems

**Context:** Content moderation for social platforms, forums, comment sections, user-generated content review.

**Recommended skills:**
- `general-ethics` -- baseline
- `anti-racism` -- detecting racist content
- `anti-sexism` -- detecting sexist content
- `abuse-prevention` -- detecting harassment and abuse patterns
- `deescalation-war-conflict` -- managing inflammatory content
- `child-safety` -- protecting minors
- `digital-ethics` -- misinformation and manipulation detection
- `epistemic-humility` -- avoiding overcensorship
- `human-oversight` -- escalation for ambiguous cases

**Key considerations:**
- False positives (removing legitimate content) are a real harm. Over-moderation silences legitimate speech.
- False negatives (missing harmful content) are also a real harm. Under-moderation allows abuse.
- Context matters enormously. Satire, education, news reporting, and art may use language that looks harmful out of context.
- Escalate ambiguous cases to human moderators. Automated moderation should handle clear-cut cases.
- Transparent appeals processes are essential.

---

## Enterprise Copilots

**Context:** AI assistants for business tasks -- writing emails, generating reports, analyzing data, code review, process automation.

**Recommended skills:**
- `general-ethics` -- baseline
- `epistemic-humility` -- honest about uncertainty in business analysis
- `human-oversight` -- human review for consequential decisions
- `anti-racism` -- preventing discriminatory outputs in hiring, HR, customer segmentation
- `anti-sexism` -- preventing gender bias in workplace communications
- `disability-respect` -- accessible document generation
- `digital-ethics` -- responsible data use
- `abuse-prevention` -- detecting workplace harassment patterns

**Key considerations:**
- Business decisions have real consequences for people. HR, hiring, and performance review contexts require extra care.
- Do not generate analysis that presents speculation as fact. Clearly label assumptions and confidence levels.
- For consequential decisions (hiring, firing, resource allocation), always recommend human review.
- Ensure generated communications are inclusive and do not inadvertently discriminate.

---

## Civic Tech Projects

**Context:** Government services, civic engagement platforms, public consultation tools, participatory budgeting.

**Recommended skills:**
- `general-ethics` -- baseline
- `conflict-mediation` -- facilitating public discourse
- `anti-racism` -- preventing discriminatory service delivery
- `anti-sexism` -- gender-equitable engagement
- `disability-respect` -- accessible civic participation
- `elder-protection` -- protecting elderly participants
- `epistemic-humility` -- honest about policy tradeoffs
- `empathy` -- respectful engagement with diverse communities
- `human-oversight` -- human review for policy recommendations

**Key considerations:**
- Public trust is essential. Transparency about AI involvement is mandatory.
- Diverse populations with different needs and communication styles must be served equitably.
- Do not generate policy recommendations without clear human review. AI should inform, not decide.
- Accessibility is a legal and ethical requirement in many jurisdictions.

---

## Healthcare-Adjacent Assistants

**Context:** Health information, appointment scheduling, symptom checkers, mental health support, wellness coaching. NOT diagnostic or treatment systems.

**Recommended skills:**
- `general-ethics` -- baseline
- `empathy` -- compassionate health communication
- `protect-vulnerable` -- patients are inherently vulnerable
- `epistemic-humility` -- critical for health information
- `human-oversight` -- escalation to medical professionals
- `elder-protection` -- elderly patients
- `disability-respect` -- adaptive health communication
- `child-safety` -- pediatric contexts
- `abuse-prevention` -- detecting abuse-related injuries

**Key considerations:**
- Never provide diagnoses or treatment recommendations. Always direct to medical professionals.
- Mental health disclosures require extreme care. Suicidal ideation triggers immediate escalation.
- Health literacy varies enormously. Adapt communication complexity.
- Patient privacy and confidentiality are paramount.
- Err on the side of recommending professional consultation.

---

## Autonomous Workflows

**Context:** AI agents operating with minimal human supervision -- automated research, data processing pipelines, multi-agent systems.

**Recommended skills:**
- `general-ethics` -- baseline
- `human-oversight` -- mandatory for autonomous systems
- `epistemic-humility` -- honest about confidence levels
- `digital-ethics` -- responsible data and information use
- `abuse-prevention` -- preventing automated abuse
- `environment` -- resource consumption awareness

**Key considerations:**
- Autonomous systems must have clear boundaries on what they can and cannot do without human approval.
- High-consequence actions (sending communications, modifying data, making purchases) should require human confirmation.
- Regular auditing of autonomous system behavior is essential.
- Cascading failures in multi-agent systems can amplify ethical violations. Each agent should have independent ethical constraints.
