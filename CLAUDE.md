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
| `skills/*/SKILL.md` | Individual ethical skill definitions | Contributors + maintainers | This is the main deliverable—keep clear and actionable |
| `skills/*/EXAMPLES.md` | Scenario-based examples for each skill | Contributors + maintainers | Must match the skill's scope and priority |
| `skills/*/TEST_CASES.md` | Test cases for skill validation | Contributors + maintainers | Used in `evals/` to validate behavior |
| `skills/*/MISUSE.md` | Known limitations and misuse risks | Contributors + maintainers | Honest about what the skill can't do |
| `agents/*.md` | Framework-agnostic reviewer agents | Contributors + maintainers | Plain markdown system prompts — work with any LLM |
| `.claude/agents/*.md` | Claude Code subagent definitions | Contributors + maintainers | Reformatted for Claude Code tool access — Claude Code only |
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
- [ ] Check if a similar skill already exists (see `skills/`)
- [ ] If extending an existing skill, read its `SKILL.md`, `EXAMPLES.md`, and `MISUSE.md`

### 2. **Create or Update the Skill**
- [ ] Write/update the main skill definition in `skills/{skill-name}/SKILL.md`
  - Be explicit about scope and behavior
  - Keep language clear and unambiguous
  - Reference the priority ladder if relevant
- [ ] Add concrete examples in `skills/{skill-name}/EXAMPLES.md`
  - Show what compliance looks like
  - Include edge cases and near-misses
- [ ] Write test cases in `skills/{skill-name}/TEST_CASES.md`
  - Use scenario format from `evals/scenarios/`
  - Ensure test cases are exhaustive but practical
- [ ] Document limitations in `skills/{skill-name}/MISUSE.md`
  - What can this skill NOT do?
  - What are known failure modes?
  - When should this skill not be used?

### 3. **Evaluate Your Work**
- [ ] Run relevant tests from `evals/scenarios/` to validate the skill
- [ ] Check for conflicts with other skills (use priority ladder if they exist)
- [ ] Red-team: Try to find cases where the skill breaks or conflicts
- [ ] Review adversarial robustness tests in `evals/adversarial/`

### 4. **Update Documentation — Always Required**

> **This step is mandatory after every contribution, no exceptions.**
> Do not wait to be reminded. Do not skip it. Do not batch it with a future PR.

- [ ] Update `CHANGELOG.md` under the **[Unreleased]** section with what was added/changed/fixed
- [ ] Update `README.md` if the scope, structure, or feature set changed (new file paths, new bundles, new guides, version number)
- [ ] Bump `version.json` according to the versioning scheme:
  - New skills, bundles, or framework guides → **MINOR** bump (e.g., 1.1.0 → 1.2.0)
  - Documentation fixes or clarifications only → **PATCH** bump (e.g., 1.2.0 → 1.2.1)
  - Breaking changes to skill definitions or priority ladder → **MAJOR** bump (discuss with maintainers first)
- [ ] Update the version badge in `README.md` to match `version.json`
- [ ] Set `releaseDate` in `version.json` to today's date

**What counts as a "scope or structure" change that requires a README update:**
- New directory or file added to the repository
- New integration guide, skill, agent, or bundle
- Changes to how skills are loaded or composed
- Any change a user scanning the README would need to know about

### 5. **Submit for Review**
- [ ] Ensure all files are in the correct directory structure
- [ ] Commit with a clear message (e.g., "feat: add skill for X" or "fix: clarify language in Y skill")
- [ ] Push to your feature branch (do not push to main/master)
- [ ] Create a PR with a description of your changes
- [ ] Link any related issues or discussions

---

## Code Style and Conventions

### File Organization

**Skills** (universal — work with any LLM or framework):
```
skills/{domain-name}/
├── SKILL.md          # Main skill definition (required)
├── EXAMPLES.md       # Scenario-based examples (required)
├── TEST_CASES.md     # Test cases for evaluation (required)
└── MISUSE.md         # Limitations and misuse risks (required)
```

**Agents** (two versions — one universal, one Claude Code-specific):
```
agents/{agent-name}.md          # Framework-agnostic — plain markdown system prompt,
                                #   works with any LLM that accepts a system prompt

.claude/agents/{agent-name}.md  # Claude Code only — same agent reformatted with
                                #   file-reading tools attached for tighter integration
```

When adding a new reviewer agent, create **both** versions. The `agents/` version is the canonical definition; the `.claude/agents/` version is a Claude Code adapter. Keep them in sync.

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

1. Create directory: `skills/{domain-name}/`
2. Create four files: `SKILL.md`, `EXAMPLES.md`, `TEST_CASES.md`, `MISUSE.md`
3. Update `skills-manifest.yaml` to register the new skill
4. Update `README.md` repository structure if adding a new category
5. Update `CHANGELOG.md` with "Added: {skill name} skill domain"
6. Test against `evals/` framework
7. Submit PR for review

### Adding a New Reviewer Agent

1. Create `agents/{agent-name}.md` — framework-agnostic version (plain markdown system prompt, no tool references)
2. Create `.claude/agents/{agent-name}.md` — Claude Code version (same agent with file-reading tools attached)
3. Update `agents/README.md` to document the new agent
4. Update `README.md` if the agents list in the repository structure changes
5. Update `CHANGELOG.md` with "Added: {agent name} reviewer agent"
6. Submit PR for review

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

## Token Cost Saving Strategies

When building applications with moral-core, context window cost and token consumption matter. Apply these strategies to keep prompt size manageable without sacrificing ethical coverage.

### 1. Use `rules_only=True` for Tight Contexts

Each `SKILL.md` file is ~1,500–2,500 tokens. The **Behavioral Rules** section (Section 6) is ~300–500 tokens and covers the essential do/don't instructions. Use the loader utility's `rules_only=True` flag when context is limited:

```python
from integrations.frameworks.loader import load_bundle, compose_system_prompt

# Full bundle: ~10,000–13,000 tokens
system = compose_system_prompt(role="...", bundle="baseline-safe")

# Rules-only bundle: ~5,000–6,000 tokens (60% reduction)
system = compose_system_prompt(role="...", bundle="baseline-safe", rules_only=True)
```

### 2. Load Skills at Module Level, Not Per-Request

Skill files are read from disk. Load them once at startup and reuse the string across requests. Never call `load_skill()` or `load_bundle()` inside a request handler or per-LLM-call function.

```python
# Good: load once
ETHICS_CONTEXT = load_bundle("baseline-safe")

def handle_request(user_input):
    return llm.chat(system=ETHICS_CONTEXT, user=user_input)
```

### 3. Scope Skills to the Agent's Role

Not every agent needs every skill. A research agent needs `epistemic-humility`; a moderation agent needs `abuse-prevention`. Loading only the relevant skills per agent saves tokens and keeps instructions focused:

```python
researcher_ethics = load_bundle("baseline-safe", rules_only=True)
moderator_ethics  = load_bundle("anti-abuse")  # full bundle — this is high-stakes
```

### 4. Skip PRINCIPLES.md for Simple Single-Skill Loads

`PRINCIPLES.md` (~4,000 tokens) contains the priority ladder for resolving conflicts between skills. If you are loading **one skill only** and there are no other skills to conflict with, you can skip it:

```python
# Single skill, no conflict resolution needed — skip PRINCIPLES.md
skill_text = load_skill("empathy")
system = f"You are a support assistant.\n\n{skill_text}"
```

Only include `PRINCIPLES.md` when loading two or more skills that could conflict.

### 5. Use Cheaper Models for Simple Tasks

Not every task needs a powerful model. Route lightweight work to smaller, faster, cheaper models to reduce cost without sacrificing quality.

| Task type | Recommended model |
|-----------|-------------------|
| Searching files, reading docs, exploring structure | Haiku |
| Updating CHANGELOG.md, README.md, version.json | Haiku |
| Small clarifications or wording fixes in skill files | Haiku |
| Formatting, renaming, minor restructuring | Haiku |
| Writing new skills, EXAMPLES.md, TEST_CASES.md | Sonnet |
| Complex ethical reasoning, adversarial test design | Sonnet or Opus |
| Reviewing PRINCIPLES.md, SAFETY.md, LIMITATIONS.md | Opus |

In Claude Code, you can target a specific model for a subagent by passing `model: haiku` in the agent configuration. Reserve Sonnet/Opus for tasks that genuinely require deep reasoning or careful judgment.

### 6. Token Budget Reference Table

| What you load | Approximate tokens |
|---------------|--------------------|
| `PRINCIPLES.md` alone | ~4,000 |
| One full `SKILL.md` | ~1,500–2,500 |
| One skill, Behavioral Rules only | ~300–500 |
| `baseline-safe` bundle (full) | ~10,000–11,000 |
| `baseline-safe` bundle (`rules_only`) | ~5,000–6,000 |
| `child-safe` bundle (full, 5 skills) | ~14,000–17,000 |
| `child-safe` bundle (`rules_only`) | ~6,000–8,000 |

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

