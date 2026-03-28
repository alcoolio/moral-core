# Human Oversight -- Misuse Analysis

How human oversight mechanisms can be exploited, patterns for detecting misuse, and strategies for mitigation.

---

## How This Skill Can Be Misused

### 1. Rubber-stamp oversight that provides the appearance without the substance

Organizations can implement human oversight as a checkbox -- a human "reviews" automated decisions by clicking "approve all" without genuine evaluation. This satisfies the letter of oversight requirements while providing no actual safety benefit. The human becomes a liability shield rather than a decision-maker.

### 2. Using oversight requirements to block beneficial automation

Oversight requirements can be weaponized to prevent competitors or internal teams from deploying useful automation. By insisting on excessive human review for low-risk decisions, an actor can create bottlenecks that make automation impractical, preserving manual processes that benefit incumbents.

### 3. Oversight shopping -- routing decisions to the most permissive reviewer

When multiple humans can provide oversight, bad actors learn which reviewer is most likely to approve and route all decisions to that person. This defeats the purpose of human oversight by selecting for the weakest link.

### 4. Manipulating the human in the loop

If an AI system presents information to a human reviewer in a biased way (e.g., with a strong recommendation, or with cherry-picked supporting evidence), the human oversight becomes performative. The human is technically reviewing but is being steered by the system's framing.

### 5. Using oversight fatigue to push through bad decisions

By flooding a human reviewer with a high volume of routine approvals, an attacker can embed a harmful decision in the stream, relying on the reviewer's fatigue and pattern of routine approval to get it through without genuine scrutiny.

### 6. Claiming oversight exists when it does not

An organization can claim that "a human reviews all AI decisions" when in practice the review is automated, delayed beyond the point of usefulness, or performed by someone without the expertise to evaluate the decision.

---

## Detection Patterns

### Rubber-stamp detection
- Approval rates above 99% over sustained periods
- Review times that are too short for genuine evaluation (e.g., approving complex decisions in under 2 seconds)
- No modifications or rejections over extended periods
- Reviewer never requests additional information

### Oversight shopping
- Decision routing that consistently targets specific reviewers
- Correlation between reviewer identity and approval rates
- Requests to "reassign" a review when the first reviewer raises concerns

### Fatigue exploitation
- Sudden spikes in review volume
- High-stakes decisions embedded in batches of routine approvals
- Review accuracy declining as volume increases within a session
- Critical decisions submitted at end-of-day or end-of-week

### Frame manipulation
- System recommendations that consistently favor one outcome
- Supporting evidence presented without counterevidence
- Framing that makes the recommended action appear as the default and alternatives appear as deviations
- Progressive anchoring where each recommendation builds on the assumption that previous recommendations were correct

---

## Mitigation Strategies

### Against rubber-stamping
- Monitor approval rates and flag sustained 99%+ approval
- Require reviewers to annotate their reasoning, not just approve/reject
- Introduce periodic synthetic test cases with known-bad decisions to verify reviewers are actually evaluating
- Rotate reviewers to prevent habituation

### Against oversight shopping
- Randomize reviewer assignment
- Track and flag patterns of reviewer selection
- Ensure multiple reviewers for high-stakes decisions
- Make reviewer identity unknown to the requester until after assignment

### Against fatigue exploitation
- Cap the number of reviews per session
- Flag high-stakes decisions for separate review queues with lower volume
- Randomize the order of reviews so attackers cannot predict position
- Enforce breaks and session limits for reviewers

### Against frame manipulation
- Present decisions to reviewers in a neutral format with evidence for and against
- Separate the system's recommendation from the evidence presentation
- Periodically audit whether the system's framing influences reviewer decisions by testing with and without recommendations
- Require reviewers to state their independent assessment before seeing the system's recommendation

### Against fake oversight claims
- Audit oversight processes, not just policies
- Require logging of reviewer identity, review duration, and actions taken
- Verify reviewer qualifications for the domain being reviewed
- Third-party auditing for high-stakes systems
