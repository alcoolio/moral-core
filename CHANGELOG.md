# Changelog

All notable changes to the moral-core project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `skills/research-ethics/` skill domain: informed consent, participant protection, data stewardship, scientific integrity, and institutional accountability — addressing one of the coverage gaps identified in LIMITATIONS.md for high-stakes domains
- `skills/financial-ethics/EXAMPLES.md`: 10 concrete examples covering fraud refusal, predatory lending, algorithmic trading manipulation, elder financial exploitation, AML structuring, and legitimate financial education
- `skills/financial-ethics/TEST_CASES.md`: 12 structured test cases including adversarial patterns (hypothetical framing, regulatory arbitrage normalization, incremental escalation)
- `skills/financial-ethics/MISUSE.md`: misuse analysis covering sophistication laundering, hypothetical framing, incremental escalation, regulatory arbitrage, compliance theater, and victim-blaming normalization
- `skills/data-privacy-surveillance/` new skill domain: personal data protection, anti-surveillance, covert tracking refusal, re-identification prevention, biometric consent, data minimization, and the right to be left alone — with full SKILL.md, EXAMPLES.md, TEST_CASES.md, and MISUSE.md
- `skills/labor-rights/` new skill domain: worker dignity, misclassification prevention, AI displacement transition responsibility, gig economy ethics, wage theft, union rights, algorithmic management transparency, and ghost labor visibility — with full SKILL.md, EXAMPLES.md, TEST_CASES.md, and MISUSE.md
- Three new bundles in `skills-manifest.yaml`: `financial-services`, `data-platform`, and `labor-platform`
- `financial-ethics`, `data-privacy-surveillance`, and `labor-rights` registered in `skills-manifest.yaml`

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

