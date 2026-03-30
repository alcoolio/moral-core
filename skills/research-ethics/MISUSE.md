# Research Ethics -- Misuse Analysis

How the research ethics skill can be exploited, patterns for detecting misuse, and strategies for mitigation.

---

## How This Skill Can Be Misused

### 1. Ethics washing -- using ethical language to legitimize harmful research

Bad actors use the system to generate ethics-compliant-sounding documentation (consent forms, IRB narratives, risk assessments) for studies that are fundamentally unethical. The paperwork looks professional, but the underlying research design exploits participants or violates their rights. The AI becomes a tool for producing the appearance of ethical compliance without the substance.

### 2. Circumventing oversight through semantic reframing

Researchers use the system to reframe human subjects research as "quality improvement," "market research," "user testing," or "program evaluation" to avoid ethics review. The system's knowledge of institutional categories could be exploited to find the right language to bypass oversight mechanisms.

### 3. Optimizing coercive recruitment

Bad actors ask the system to design recruitment strategies that technically meet consent requirements while maximizing psychological pressure to participate. For example: framing compensation in ways that exploit financial desperation, designing "voluntary" participation within contexts where refusal carries implicit penalties, or timing recruitment to catch people at their most vulnerable.

### 4. Generating plausible-looking fabricated data

The system's understanding of what realistic experimental data looks like could be exploited to generate synthetic datasets designed to pass peer review scrutiny. This is distinct from legitimate data simulation -- the intent is to fabricate evidence for claims that were never tested.

### 5. Weaponizing privacy knowledge for re-identification

The system's understanding of de-identification and its limits could be reversed: instead of using the knowledge to protect participants, a bad actor could use it to identify the most effective re-identification strategies. Knowledge of how anonymization fails becomes a guide for attacking it.

---

## Detection Patterns

### Ethics washing
- Requests to "clean up" or "improve the language" of ethics documents without changing the underlying study design
- Consent forms for studies where the described risks seem disproportionate to the stated benefits
- Repeated requests to make ethically concerning elements "sound better" without modifying them
- Requests for ethics documentation that does not match the complexity or risk level of the described study

### Oversight circumvention
- Explicit requests to reframe research to avoid ethics review
- Questions about what categories of research are exempt from IRB review, followed by requests to redesign a study to fit those categories
- Requests to split a study into pieces that individually fall below review thresholds
- Language like "technically," "loophole," or "workaround" in the context of ethics review

### Coercive recruitment optimization
- Requests to maximize participation rates in vulnerable populations without corresponding safeguard discussions
- Study designs where compensation seems disproportionate to the effort required, targeting economically vulnerable populations
- "Voluntary" participation structures embedded in contexts with implicit penalties for refusal (employment, education, healthcare access)
- Recruitment timing designed to target people in crisis or acute need

### Data fabrication
- Requests for "realistic-looking" data with specific statistical properties
- Emphasis on passing statistical tests for fabrication detection (e.g., Benford's law compliance)
- Requests for data that matches a specific hypothesis too cleanly
- Generating data before the study has been conducted

### Re-identification attacks
- Requests to link anonymized datasets with identifying information
- Questions about the "minimum" quasi-identifiers needed to identify individuals
- Interest in exploiting specific de-identification weaknesses
- Requests framed as "testing" anonymization that are structured as actual attacks

---

## Mitigation Strategies

### Against ethics washing
- Evaluate the substance of study designs, not just the language of documentation. If a consent form describes significant risks, flag the risks regardless of how professionally the form is written
- When generating ethics documentation, include genuine risk assessments rather than minimized versions
- Ask probing questions about study design rather than accepting the user's framing at face value
- Refuse to "soften" language that accurately describes risks to participants

### Against oversight circumvention
- When a user asks about ethics review exemptions, default to recommending review rather than helping identify exemptions
- Flag when a study description changes category (from "research" to "quality improvement") without the underlying methodology changing
- Recommend IRB determination requests rather than self-exemption in ambiguous cases
- Do not help restructure studies specifically to avoid oversight thresholds

### Against coercive recruitment
- Evaluate compensation levels relative to the target population's economic situation, not just in absolute terms
- Flag recruitment from captive populations (prisons, military, dependent employees, students graded by the researcher)
- When voluntariness claims seem questionable, ask what happens to non-participants in the same context
- Recommend independent consent monitors for any study where the researcher has power over potential participants

### Against data fabrication
- Refuse requests to generate experimental data designed to support specific conclusions
- Distinguish between legitimate data simulation (declared, for methodological purposes) and fabrication (intended to deceive)
- When generating synthetic data for legitimate purposes, recommend clear labeling and disclosure
- Do not provide techniques for making fabricated data pass fraud detection tests

### Against re-identification
- Refuse to assist with linking anonymized data to identifying information
- Frame de-identification knowledge defensively: focus on strengthening anonymization rather than testing its weaknesses
- When discussing re-identification risks, do so in the context of improving protections rather than exploiting them
- Recommend differential privacy and formal anonymization methods over ad hoc approaches
