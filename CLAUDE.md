# CLAUDE.md: AI Development Guidelines for moral-core

This document provides guidance for AI assistants (like Claude) contributing to the moral-core project via Claude Code or other AI-assisted development workflows.

---

## Overview

**moral-core** is an ethical skills library for LLMs, agents, and robots. It encodes behavioral guidelines into plain-text skill modules that can be loaded into AI systems as system prompts or instruction layers.

When working on this project:
- **Respect the existing framework.** Don't refactor core files without explicit authorization.
- **Prioritize clarity and auditability.** Plain text. No hidden logic. Anyone should be able to read and understand.
- **Follow the priority ladder** in [PRINCIPLES.md](PRINCIPLES.md) when resolving design conflicts.
- **Test your changes** against the evaluation framework in `evals/`.

---

## Key Files and Their Purpose

| File | Purpose | Who Edits | Notes |
|------|---------|-----------|-------|
| `PRINCIPLES.md` | Shared doctrine, priority ladder, interpretive rules | Core maintainers only | Foundational framework—changes require careful review |
| `.claude/skills/*/SKILL.md` | Individual ethical skill definitions | Contributors + maintainers | This is the main deliverable—keep clear and actionable |
| `.claude/skills/*/EXAMPLES.md` | Scenario-based examples for each skill | Contributors + maintainers | Must match the skill's scope and priority |
| `.claude/skills/*/TEST_CASES.md` | Test cases for skill validation | Contributors + maintainers | Used in `evals/` to validate behavior |
| `.claude/skills/*/MISUSE.md` | Known limitations and misuse risks | Contributors + maintainers | Honest about what the skill can't do |
| `evals/` | Evaluation framework and benchmarks | Contributors + maintainers | Validate all new skills against these |
| `SAFETY.md` | Safety documentation and limitations | Core maintainers only | Critical for deployment—be very careful |
| `LIMITATIONS.md` | What prompt-level ethics cannot guarantee | Core maintainers only | Honest disclaimer about framework limits |
| `CHANGELOG.md` | Version history and change documentation | All contributors | Update before submitting a PR |
| `version.json` | Current version metadata | Release manager | Updated during release process only |

---

## Workflow for Adding or Updating a Skill

### 1. **Before Starting**
- [ ] Read [PRINCIPLES.md](PRINCIPLES.md) to understand the priority ladder and interpretive rules
- [ ] Identify which ethical concern your skill addresses
- [ ] Check if a similar skill already exists (see `.claude/skills/`)
- [ ] If extending an existing skill, read its `SKILL.md`, `EXAMPLES.md`, and `MISUSE.md`

### 2. **Create or Update the Skill**
- [ ] Write/update the main skill definition in `.claude/skills/{skill-name}/SKILL.md`
  - Be explicit about scope and behavior
  - Keep language clear and unambiguous
  - Reference the priority ladder if relevant
- [ ] Add concrete examples in `.claude/skills/{skill-name}/EXAMPLES.md`
  - Show what compliance looks like
  - Include edge cases and near-misses
- [ ] Write test cases in `.claude/skills/{skill-name}/TEST_CASES.md`
  - Use scenario format from `evals/scenarios/`
  - Ensure test cases are exhaustive but practical
- [ ] Document limitations in `.claude/skills/{skill-name}/MISUSE.md`
  - What can this skill NOT do?
  - What are known failure modes?
  - When should this skill not be used?

### 3. **Evaluate Your Work**
- [ ] Run relevant tests from `evals/scenarios/` to validate the skill
- [ ] Check for conflicts with other skills (use priority ladder if they exist)
- [ ] Red-team: Try to find cases where the skill breaks or conflicts
- [ ] Review adversarial robustness tests in `evals/adversarial/`

### 4. **Update Documentation**
- [ ] Update `CHANGELOG.md` under the **[Unreleased]** section
- [ ] Add a summary of your changes (what was added/changed/fixed)
- [ ] Reference the skill or domain you modified
- [ ] Update `README.md` if the scope or structure changed

### 5. **Submit for Review**
- [ ] Ensure all files are in the correct directory structure
- [ ] Commit with a clear message (e.g., "feat: add skill for X" or "fix: clarify language in Y skill")
- [ ] Push to your feature branch (do not push to main/master)
- [ ] Create a PR with a description of your changes
- [ ] Link any related issues or discussions

---

## Code Style and Conventions

### File Organization

```
.claude/skills/{domain-name}/
├── SKILL.md          # Main skill definition (required)
├── EXAMPLES.md       # Scenario-based examples (required)
├── TEST_CASES.md     # Test cases for evaluation (required)
└── MISUSE.md         # Limitations and misuse risks (required)
```

### Writing Skills

**DO:**
- Be explicit and actionable
- Use clear, precise language
- Reference the priority ladder when appropriate
- Provide concrete examples
- Document known limitations

**DON'T:**
- Use vague, philosophical abstractions ("be good")
- Assume readers have domain knowledge
- Hide complexity—make it visible and auditable
- Add code, APIs, or SDK dependencies
- Reference external URLs (the framework should be self-contained)

### Naming Conventions

- Skill directory names: lowercase with hyphens (e.g., `deescalation-war-conflict`)
- File names: UPPERCASE (e.g., `SKILL.md`, `EXAMPLES.md`)
- Section headings in skill files: Clear, hierarchical (H2, H3, H4 as needed)

---

## Testing and Validation

All skills must be validated before merging:

### Run Manual Tests

```bash
# Navigate to the project root
cd /home/user/moral-core

# Review your skill and check it against test cases
# (Test execution depends on your evaluation framework)
```

### Use the Evaluation Framework

- **Scenario-based tests** (`evals/scenarios/`): Does the skill behave as documented?
- **Adversarial tests** (`evals/adversarial/`): Can the skill be bypassed or misused?
- **Benchmark matrix** (`evals/benchmarks/`): Does the skill fit within the broader framework?

---

## Git Workflow

### Branch Naming
- Feature branches: `claude/{feature-description}-{random-suffix}` (e.g., `claude/add-changelog-versioning-oQZC3`)
- Do **not** commit to `main` or `master` directly

### Commits
- Write clear, descriptive commit messages
- Use conventional commit format: `type: description`
  - `feat:` for new skills or features
  - `fix:` for bug fixes or clarifications
  - `docs:` for documentation updates
  - `refactor:` for restructuring without functional change (use sparingly)

### Example Commits
```
feat: add conflict-mediation skill
fix: clarify harm prevention priority in epistemic-humility skill
docs: update CHANGELOG and add versioning system
```

### Pull Requests
- Link to relevant issues using `Closes #issue-number`
- Describe what changed and why
- Reference any skills or documentation updates
- Keep PRs focused (one feature or bug fix per PR)

---

## Common Tasks

### Adding a New Ethical Skill Domain

1. Create directory: `.claude/skills/{domain-name}/`
2. Create four files: `SKILL.md`, `EXAMPLES.md`, `TEST_CASES.md`, `MISUSE.md`
3. Update `skills-manifest.yaml` to register the new skill
4. Update `README.md` repository structure if adding a new category
5. Update `CHANGELOG.md` with "Added: {skill name} skill domain"
6. Test against `evals/` framework
7. Submit PR for review

### Updating Existing Documentation

1. Edit the relevant `.md` file
2. Ensure the change doesn't contradict [PRINCIPLES.md](PRINCIPLES.md)
3. Update `CHANGELOG.md` with your change under **[Unreleased]**
4. Commit and push to your feature branch

### Creating a New Policy Bundle

1. Edit `README.md` to add a row to the Policy Bundles table
2. Create example usage in `examples/` if helpful
3. Document the bundle in `USE_CASES.md`
4. Update `CHANGELOG.md`
5. Submit PR with description of bundle rationale

### Preparing a Release

1. Review all changes since the last version
2. Update `CHANGELOG.md`: move items from **[Unreleased]** to a new version section
3. Update `version.json` with the new version number and date
4. Create a commit: `release: version X.Y.Z`
5. Tag it: `git tag -a vX.Y.Z -m "Release vX.Y.Z"`
6. Push tag to repository
7. Create a GitHub release with notes from `CHANGELOG.md`

---

## When to Ask for Help

**Reach out to maintainers if:**
- You're unsure whether your skill fits within the framework
- Your skill conflicts with existing skills and you can't resolve it via the priority ladder
- You need clarification on PRINCIPLES.md or the priority ladder
- Your evaluation tests are failing and you don't understand why
- You're proposing a change to core files like PRINCIPLES.md or SAFETY.md

**Don't:**
- Edit PRINCIPLES.md, SAFETY.md, or LIMITATIONS.md without explicit authorization
- Refactor the core directory structure without discussion
- Add external dependencies or SDK integrations
- Create skills that are too narrow or too broad (discuss first)

---

## Resources

- [PRINCIPLES.md](PRINCIPLES.md) — Shared doctrine and priority ladder
- [SAFETY.md](SAFETY.md) — Safety considerations and deployment guidance
- [CONTRIBUTING.md](CONTRIBUTING.md) — Community contribution guidelines
- [USE_CASES.md](USE_CASES.md) — Deployment scenarios and skill recommendations
- [PHILOSOPHY.md](PHILOSOPHY.md) — Philosophical foundations
- [evals/](evals/) — Evaluation framework and test cases

---

## Questions?

If you have questions about this workflow, the project structure, or how to contribute, see [CONTRIBUTING.md](CONTRIBUTING.md) or open an issue in the repository.

