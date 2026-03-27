# Governance

This document describes how moral-core is maintained, how decisions are made, and how contributions are evaluated. Because this project encodes normative positions into machine-readable skills, governance carries more weight than in a typical open-source library. Every decision about what to include, exclude, or modify is a decision about what values get shipped to downstream systems.

## Maintainers structure

### Project lead

The project lead has final decision authority on:
- Accepting or rejecting skills and domains.
- Resolving disagreements that maintainers cannot resolve by consensus.
- Enforcement actions under the Code of Conduct.
- Release decisions.

The project lead is currently the repository owner. Transfer of lead authority requires a public announcement and a 30-day transition period.

### Core maintainers

Core maintainers can:
- Approve and merge pull requests.
- Triage issues.
- Participate in governance decisions.
- Propose new domains and skills.

To become a core maintainer, a contributor must:
- Have at least three merged skill contributions or significant evaluation contributions.
- Demonstrate understanding of the project's standards (justification, tradeoffs, misuse analysis, testing).
- Be nominated by an existing maintainer and approved by the project lead.

### Domain maintainers

Domain maintainers have expertise in a specific deployment context (e.g., healthcare, robotics, education). They:
- Review contributions within their domain.
- Advise on domain-specific tradeoffs and risks.
- Flag cultural or legal considerations that general maintainers might miss.

Domain maintainers do not need to meet the same contribution threshold as core maintainers. Demonstrated professional expertise in the relevant domain is the primary criterion.

### All maintainers

All maintainers must:
- Follow the Code of Conduct.
- Disclose conflicts of interest (e.g., working for a company that would directly benefit from a particular skill being included or excluded).
- Recuse themselves from decisions where they have a material conflict.

## Review expectations

### Response times

- **Issues:** Initial triage within one week.
- **Pull requests:** First review within two weeks. If a PR sits without review for more than two weeks, the author may ping maintainers.
- **Security reports:** Acknowledged within 48 hours. Resolved or mitigated within 30 days.

### Review depth

Skill reviews are not rubber stamps. Reviewers must:
- Read every instruction and its justification.
- Evaluate the misuse analysis for completeness.
- Run or review all tests, including adversarial tests.
- Check for conflicts with existing skills.
- Consider deployment contexts the author may not have anticipated.

A review that says only "LGTM" is not sufficient for skill content. Reviewers must leave substantive comments demonstrating they engaged with the content.

## Criteria for accepting new ethical domains

A new domain is accepted when:

1. **Clear deployment context.** The domain maps to a real-world deployment scenario (e.g., "elder care robotics" not "being nice").
2. **Distinct behavioral requirements.** The domain requires instructions that are not adequately covered by existing domains.
3. **Testable scope.** The domain's boundaries are clear enough that contributors can write meaningful tests.
4. **Identified stakeholders.** The proposal identifies who is affected by system behavior in this domain (users, bystanders, vulnerable populations, etc.).
5. **At least one champion.** Someone commits to maintaining the domain, reviewing contributions, and responding to issues.
6. **Legal and regulatory awareness.** If the domain intersects with regulated industries (healthcare, finance, education), the proposal must identify relevant regulatory frameworks and explain how skills in this domain relate to them. Skills are not legal compliance tools, but they must not contradict or undermine applicable regulations.

## Criteria for rejecting harmful contributions

A contribution is rejected if it:

- **Enables direct harm.** The skill, if followed, would predictably lead to physical, psychological, or financial harm.
- **Targets specific groups.** The skill singles out individuals or groups for negative treatment based on protected characteristics.
- **Undermines informed consent.** The skill instructs systems to deceive users about what the system is doing or why.
- **Concentrates power without accountability.** The skill removes human oversight or appeals processes in high-stakes decisions.
- **Lacks honesty about its normative position.** The skill presents a contested value judgment as objective fact without acknowledging the judgment.

Rejection is not censorship. Contributors are free to fork the project and maintain their own version. Rejection means the maintainers have determined that the contribution does not meet the project's standards for safety, honesty, and specificity.

## Versioning philosophy

moral-core uses semantic versioning, adapted for ethical skill content:

- **Patch (0.0.x):** Typo fixes, clarifications that do not change behavioral expectations, test improvements.
- **Minor (0.x.0):** New skills, new domains, new evaluation scenarios. Non-breaking additions. Existing skills remain unchanged or receive backward-compatible modifications.
- **Major (x.0.0):** Breaking changes to existing skills. This includes removing instructions, changing the meaning of existing instructions, or restructuring the skill format. Major versions require a migration guide.

### What counts as a breaking change

If a downstream system loading a skill would behave differently after an update, that is a breaking change. Examples:
- Removing an instruction from a skill.
- Changing an instruction's priority from `critical` to `low`.
- Modifying an instruction's text in a way that changes the behavioral expectation.
- Changing the skill schema in a way that requires updated parsers.

### Release cadence

There is no fixed release schedule. Releases happen when there is a meaningful set of changes ready for downstream consumption. Every release includes a changelog.

## Change proposal process

### For new skills or domains

1. Open an issue using the skill proposal template.
2. Maintainers triage and provide feedback.
3. If approved in principle, the contributor opens a PR following CONTRIBUTING.md.
4. PR undergoes review.
5. After merge, the skill enters a 30-day observation period.

### For modifications to existing skills

1. Open an issue explaining what you want to change and why.
2. If the change is a breaking change, the issue must include:
   - Impact analysis: what downstream systems would be affected?
   - Migration path: how do downstream consumers adapt?
   - Justification: why is the current instruction inadequate?
3. Maintainers evaluate the change against the breaking change threshold.
4. PR process proceeds as normal.

### For emergency changes

If a skill is found to enable harm in production, maintainers may:
- Issue a patch release removing or modifying the harmful instruction immediately.
- Notify downstream consumers via the changelog and, if contact information is available, directly.
- Open a retrospective issue documenting what went wrong and how to prevent similar issues.

Emergency changes bypass the normal review timeline but still require two maintainer approvals.

## Transparency about normative choices

This project makes value judgments. We do not pretend otherwise.

When moral-core encodes a specific ethical position, the project commits to:

1. **Stating the position explicitly.** No hidden value judgments. If a skill assumes that user autonomy outweighs paternalistic safety in a given context, the skill says so.
2. **Citing the reasoning.** Every normative choice must be justified. The justification does not need to be airtight -- reasonable people can disagree -- but it must exist and be specific.
3. **Acknowledging alternatives.** If a reasonable person could hold a different position, the skill or its documentation must acknowledge that the chosen position is one of several defensible options.
4. **Marking cultural specificity.** If a norm is specific to a particular legal system, cultural context, or philosophical tradition, the skill must say so. "This instruction reflects privacy norms common in European and North American legal frameworks" is honest. Presenting the same instruction as universal is not.
5. **Accepting feedback.** Contributors and users can challenge any normative choice by opening an issue. The maintainers will engage with substantive challenges, though engaging does not guarantee changing the position.

## How disagreements about ethical positions are resolved

Disagreements about ethical positions are expected. They are resolved through the following process:

### Step 1: Clarify the disagreement

Both parties must state their positions in writing, in an issue thread. Each position must include:
- The specific instruction or skill in question.
- The alternative position being proposed.
- The reasoning behind each position.
- The anticipated consequences of each approach.

### Step 2: Seek additional input

Maintainers may invite domain experts, affected community members, or external reviewers to comment. The goal is to ensure the decision is informed, not to achieve unanimity.

### Step 3: Maintainer deliberation

Core maintainers discuss the issue and attempt to reach consensus. Consensus means all core maintainers can accept the decision, even if it is not every individual's first choice.

### Step 4: Project lead decision

If consensus cannot be reached within 30 days, the project lead makes the final call. The project lead must publish their reasoning.

### Step 5: Documentation

The resolution is documented in the issue thread and, if it changes a skill, in the skill's changelog. The losing position is recorded alongside the winning position so that future contributors understand the decision history.

### What "resolution" does not mean

Resolution does not mean the losing side was wrong. It means the project has made a specific engineering decision for specific reasons. If new evidence or arguments emerge, the decision can be revisited by opening a new issue.

## Downstream responsibility notice

moral-core provides ethical skill definitions. It does not provide legal compliance, safety certification, or moral absolution.

Downstream consumers are responsible for:

- **Evaluating fitness for purpose.** A skill that works well for a customer support chatbot may be inappropriate for a surgical robot. Consumers must evaluate whether each skill is appropriate for their specific deployment context.
- **Testing in context.** moral-core's tests verify skill behavior in isolation and in standard scenarios. Consumers must test skills in their actual deployment environment with their actual user base.
- **Regulatory compliance.** Skills are not legal advice. If your deployment context is subject to regulation (healthcare, finance, education, etc.), you must ensure that your system -- including the skills it loads -- complies with applicable law. moral-core does not make that guarantee.
- **Monitoring and incident response.** Loading a skill does not eliminate the need for monitoring. Systems can still behave unexpectedly. Consumers must maintain monitoring, logging, and incident response processes.
- **Attribution and transparency.** If you use moral-core skills in a consumer-facing product, consider disclosing that fact to your users. Transparency about the ethical frameworks guiding system behavior builds trust.

moral-core is a tool. Like any tool, it can be used well or poorly. The project provides the best skill definitions it can, tests them rigorously, and documents their limitations honestly. What happens after that is the responsibility of the people who deploy them.
