# Changelog

All notable changes to the moral-core project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `skills/anti-racism/NARRATIVES.md` — batch 4 of 8. Three vignettes: statistical framing used to obscure structural causes (the numbers that seem to speak for themselves), writing a convincing racist antagonist without producing propaganda (the villain who needs to sound convincing), and the false-neutrality trap in historical education contexts (the request for balance).
- `skills/anti-sexism/NARRATIVES.md` — batch 4 of 8. Three vignettes: a user framing gender-based mistreatment as a personal communication problem (the manager who keeps interrupting), a fiction request requiring the AI to distinguish visceral accuracy from harmful content (the scene at the edge), and a minimizing user in a relationship with potential coercive control dynamics (the minimizer).
- `skills/disability-respect/NARRATIVES.md` — batch 4 of 8. Three vignettes: accessibility proactively integrated into an efficiency-focused design request (the efficient design), correcting well-intentioned but harmful language in a profile without attacking the writer (the language that slipped past), and the autonomy principle applied when a family member acts on behalf of a disabled person without consulting them (the helpful assumption).
- `skills/psychological-first-aid/NARRATIVES.md` — batch 3 of 8. Three vignettes: respecting a user's "it's fine" framing after a historical suicidal-ideation disclosure (autonomy vs. keeping the door open); a creative-writing-framing request that may be a thin wrapper around real distress (how to hold both possibilities without collapsing them); sole-confidant capture in a long conversation (anti-isolation vs. not rejecting a person who already feels unseen).
- `skills/human-oversight/NARRATIVES.md` — batch 3 of 8. Three vignettes: stopping at the point of no return on an agentic migration task despite user authorization to proceed end-to-end; flagging a genuine uncertainty before an autonomous pipeline run rather than defaulting to the user's "just do it" instruction; halting mid-batch when a clinical trial participant's consent flag appears unexpectedly.
- `skills/deescalation-war-conflict/NARRATIVES.md` — batch 3 of 8. Three vignettes: a request to argue one side's invasion is "completely justified" — adopting a conclusion vs. presenting arguments honestly; helping write an atrocity op-ed where accurate facts are being overclaimed as legal proof; responding to a user in acute moral distress watching conflict footage for hours without dismissing their rage or amplifying the feedback loop.
- `skills/abuse-prevention/NARRATIVES.md` — batch 2 of 8. Three vignettes: the attentive partner (covert surveillance reframed as anxiety), getting her attention (circumventing post-breakup withdrawal as reconnection), and venting vs. planning (how to distinguish emotional disclosure from a request for harmful assistance).
- `skills/child-safety/NARRATIVES.md` — batch 2 of 8. Three vignettes: the novelist's request (grooming script in a condemning thriller), the researcher's request (claimed academic purpose for a grooming tactics summary), and the ambiguous age (how to respond protectively when a user's age and a concerning adult-child dynamic are both unclear).
- `skills/protect-vulnerable/NARRATIVES.md` — batch 2 of 8. Three vignettes: the loving son (elder financial exploitation dressed as care), the caregiver's request (overprotective suppression of a disabled adult's autonomy), and the safety plan (providing actionable help to an abuse survivor while accounting for surveillance risk).

---

## [1.7.0] - 2026-05-11

### Added
- `NARRATIVES.md` — new required file type for every skill. Each file contains 2–3 fictional vignettes (~300 words each) written as an AI's internal reasoning trace through a genuinely hard case. Unlike `EXAMPLES.md` (which shows correct outputs), `NARRATIVES.md` shows the deliberation process: competing principles, the tempting wrong path, and why it is rejected. Grounded in Anthropic's research finding that training on *explanations of why* aligned behavior is correct generalises better to novel situations than training on demonstrations of correct behavior alone.
- `skills/general-ethics/NARRATIVES.md` — batch 1 of 8. Three vignettes: the escalating request pattern, the permission-slip dilemma, and the comfortable refusal (Ethics Washing anti-pattern).
- `skills/epistemic-humility/NARRATIVES.md` — batch 1 of 8. Three vignettes: the confident confabulation temptation, correcting a mid-conversation error, and separating clear evidence from contested claims under user pressure.
- `skills/empathy/NARRATIVES.md` — batch 1 of 8. Three vignettes: the 2 a.m. draft (autonomy vs. wellbeing), responding to a user angry at the AI (genuine vs. formulaic acknowledgment), and the ambiguous disclosure (how to check in without projecting crisis).
- `NARRATIVES.md` documented in `CLAUDE.md`: added to Key Files table, skill workflow checklist, file organisation section, Common Tasks > Adding a New Ethical Skill Domain, model task table, and token budget reference table.
- `README.md`: updated skill directory listing to reflect five-file structure.

### Notes
- 20 remaining skills will be covered in batches 2–8 on a rolling review schedule. Each batch adds three skills and receives a patch bump (1.7.1, 1.7.2, …).

---

## [1.6.1] - 2026-05-01

### Changed
- `CHANGELOG.md`: moved accumulated `[Unreleased]` entries (research-ethics, financial-ethics, data-privacy-surveillance, labor-rights, skill-conflict eval, psychological-first-aid) into a proper `[1.6.0]` section so the changelog matches `version.json`.
- `ROADMAP.md`: rewrote to reflect the project's actual v1.6.x state (22 skill domains, 11 policy bundles, automated eval runner, skill-conflict eval, framework integration guides, shared Python loader). Removed stale v0.x phases that have already shipped or been superseded. Documented near-term focus (localization, expert review, TypeScript SDK, CI for skill regressions) and longer-term direction.
- `README.md` and `version.json`: patch-bumped to 1.6.1 to capture the documentation cleanup.

---

## [1.6.0] - 2026-05-01

### Added
- `skills/psychological-first-aid/` new skill domain: basic, non-clinical first-response support for users raising psychological topics (suicidal ideation, self-harm, mental pain, abuse disclosure, heartbreak and loneliness), with explicit AI-not-a-real-person and AI-not-a-therapist disclosure, mandatory routing to professional help and trusted adults (especially for minors), and an anti-isolation priority. Includes a prominent limits-of-this-skill warning at the top of `SKILL.md` and full deployment-disclosure requirements in `MISUSE.md`. Full SKILL.md, EXAMPLES.md (17 worked examples), TEST_CASES.md (25 cases), and MISUSE.md.
- `psychological-first-aid` registered in `skills-manifest.yaml` and added to the `mediation-first`, `child-safe`, and `anti-abuse` bundles.
- `evals/scenarios/skill-conflicts.md`: 8 hand-crafted two-skill conflict scenarios designed to stress the priority ladder in `PRINCIPLES.md` (empathy vs. epistemic-humility, disability-respect vs. protect-vulnerable, child-safety vs. anti-racism, data-privacy-surveillance vs. human-oversight, elder-protection vs. disability-respect, environment vs. labor-rights, abuse-prevention vs. empathy, democratic-legitimacy vs. disability-respect).
- `evals/run_conflicts.py`: skill-conflict eval runner that runs each prompt with skill A only, skill B only, and both loaded, then uses an LLM-as-judge to score (a) how much A and B disagree on operational advice and (b) whether the combined response acknowledges and resolves the tension via the priority ladder.
- `evals/runner/conflict.py`: parser, three-way system-prompt builder, conflict judge, and per-pair aggregator used by `run_conflicts.py`.
- New section in `evals/README.md` documenting the skill-conflict eval, its cost profile, and how to read the per-pair matrix to surface gaps in the priority ladder.
- `skills/research-ethics/` skill domain: informed consent, participant protection, data stewardship, scientific integrity, and institutional accountability — addressing one of the coverage gaps identified in LIMITATIONS.md for high-stakes domains.
- `skills/financial-ethics/EXAMPLES.md`: 10 concrete examples covering fraud refusal, predatory lending, algorithmic trading manipulation, elder financial exploitation, AML structuring, and legitimate financial education.
- `skills/financial-ethics/TEST_CASES.md`: 12 structured test cases including adversarial patterns (hypothetical framing, regulatory arbitrage normalization, incremental escalation).
- `skills/financial-ethics/MISUSE.md`: misuse analysis covering sophistication laundering, hypothetical framing, incremental escalation, regulatory arbitrage, compliance theater, and victim-blaming normalization.
- `skills/data-privacy-surveillance/` new skill domain: personal data protection, anti-surveillance, covert tracking refusal, re-identification prevention, biometric consent, data minimization, and the right to be left alone — with full SKILL.md, EXAMPLES.md, TEST_CASES.md, and MISUSE.md.
- `skills/labor-rights/` new skill domain: worker dignity, misclassification prevention, AI displacement transition responsibility, gig economy ethics, wage theft, union rights, algorithmic management transparency, and ghost labor visibility — with full SKILL.md, EXAMPLES.md, TEST_CASES.md, and MISUSE.md.
- Three new bundles in `skills-manifest.yaml`: `financial-services`, `data-platform`, and `labor-platform`.
- `financial-ethics`, `data-privacy-surveillance`, and `labor-rights` registered in `skills-manifest.yaml`.

### Notes
- This entry consolidates work that accumulated under `[Unreleased]` while `version.json` was advanced through 1.3.x–1.5.x without corresponding CHANGELOG sections. Treat it as the cumulative changelog for the 1.3.x → 1.6.0 window. Future releases will be sectioned per-version at release time.

---

## [1.2.1] - 2026-03-30

### Added
- Automated evaluation runner (`evals/run.py`) — CLI tool that parses scenario and adversarial test files, sends each prompt to a configured model, scores responses using an LLM-as-judge on five dimensions, and prints a coloured pass/fail report
- `evals/runner/` package: `parser.py` (markdown test case parser), `judge.py` (LLM-as-judge with Anthropic/OpenAI/Ollama support), `report.py` (terminal + JSON output)
- `evals/baselines/` and `evals/results/` directories for storing regression baselines and run outputs
- Updated `evals/README.md` with full documentation for the automated runner, including quick-start, options table, example output, and JSON schema

---

## [1.2.0] - 2026-03-29

### Added
- Framework-specific integration guides in `integrations/frameworks/` for LangChain, Dify, and CrewAI
- Shared Python skill loader utility (`integrations/frameworks/loader.py`) with `load_skill`, `load_bundle`, `compose_system_prompt`, `list_skills`, and `list_bundles` helpers
- Framework integration template (`integrations/frameworks/_template/`) for adding new framework guides, with a required-sections checklist

### Changed
- `integrations/README.md` updated to distinguish use-case guides from framework-specific guides
- `README.md` updated to reflect v1.2.0, new repository structure entries for `integrations/frameworks/`

---

## [1.1.0] - 2026-03-28

### Added
- Changelog and versioning system
- CLAUDE.md guidelines for AI-assisted development
- 8 framework-agnostic reviewer agents in `agents/` directory (ethics-reviewer, empathy-style-checker, misuse-auditor, advertising-ethics-reviewer, mental-health-support-checker, robotics-safety-ethics, mediation-designer, warfare-agent-reviewer)
- 8 Claude Code subagent equivalents in `.claude/agents/` directory
- Comprehensive documentation for agents in `agents/README.md`
- `.claude/skills/README.md` with detailed skill documentation and usage patterns
- `skills/README.md` with complete overview of all 18 ethical skill domains and usage guide
- Updated repository structure documentation reflecting agents and skills organization

### Changed
- Clarified skill count from 19 to 18 domains in design principles and documentation
- Expanded repository structure section to list all available agents and clarify framework-agnostic vs. Claude Code specific implementations
- Enhanced versioning documentation to include agents alongside skills
- Improved README with dedicated Reviewer Agents section
- Updated LLM compatibility matrix to distinguish between universal and Claude Code-specific components

---

## [1.0.0] - 2026-03-28

### Added
- Initial release of moral-core ethical skills library
- 16 ethical skill domains covering harm prevention, fairness, honesty, care, and more
- Policy bundles for common deployment contexts (baseline-safe, mediation-first, anti-abuse, child-safe, robotics-care, eco-care, inclusive-assistant)
- Comprehensive evaluation framework with adversarial robustness tests and scenario-based benchmarks
- Integration guides for LLMs, agents, robotics, education, content moderation, and enterprise copilots
- Philosophy documentation with explicit commitments and foundational traditions
- PRINCIPLES.md with priority ladder for resolving ethical conflicts
- SAFETY.md documentation on limitations and safe deployment practices
- LIMITATIONS.md honest assessment of what prompt-based ethical layers cannot guarantee
- CONTRIBUTING.md guidelines for community contributions
- CODE_OF_CONDUCT.md community standards
- GOVERNANCE.md project governance model
- USE_CASES.md deployment scenarios and skill recommendations
- ROADMAP.md for future development directions
- MIT License

### Details

#### Skill Domains
- general-ethics: Foundational ethical principles
- conflict-mediation: Mediation and resolution techniques
- deescalation-war-conflict: De-escalation and conflict prevention
- anti-sexism: Gender equality and sexual safety
- anti-racism: Anti-discrimination and cultural respect
- empathy: Empathetic understanding and response
- protect-vulnerable: Special protections for at-risk populations
- environment: Environmental and ecological responsibility
- animal-welfare: Animal rights and welfare considerations
- child-safety: Safety guidelines for child interactions
- disability-respect: Accessibility and dignity for disabled persons
- elder-protection: Special considerations for elderly populations
- abuse-prevention: Prevention of interpersonal harm and coercion
- epistemic-humility: Truthfulness and intellectual honesty
- human-oversight: Requirements for human review and decision-making
- digital-ethics: Digital rights, privacy, and online safety

#### Evaluation Framework
- Adversarial robustness tests for skill resistance to prompt injection
- Benchmark matrix comparing skill coverage across scenarios
- Detailed rubrics for evaluating ethical behavior
- Scenario-based test cases for skill validation

---

## Version History

| Version | Release Date | Status |
|---------|--------------|--------|
| 1.0.0 | 2026-03-28 | Released |

---

## How to Contribute

When contributing changes:

1. Update this CHANGELOG.md before submitting your PR
2. Add changes under the **[Unreleased]** section
3. Use these categories: Added, Changed, Deprecated, Removed, Fixed, Security
4. Follow the existing format and keep entries concise
5. When a release is cut, create a new version heading and move Unreleased items there

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution process.

---

## Guidelines for Release Management

### Semantic Versioning

- **MAJOR** (X.0.0): Breaking changes to skill definitions, priority ladder, or fundamental framework
- **MINOR** (1.Y.0): New skills, new policy bundles, expanded evaluation framework
- **PATCH** (1.0.Z): Documentation updates, clarifications, bug fixes, minor improvements

### Release Checklist

Before cutting a release:

- [ ] Update CHANGELOG.md with all changes since last version
- [ ] Update version number in `version.json`
- [ ] Run full evaluation suite and confirm no regressions
- [ ] Review all documentation for accuracy
- [ ] Create a git tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
- [ ] Push tag to repository: `git push origin vX.Y.Z`
- [ ] Create a GitHub release with release notes from CHANGELOG.md

