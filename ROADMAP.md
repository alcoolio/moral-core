# Roadmap

**Moral Core Development Roadmap**

This roadmap describes where the project is, what is shipping next, and the longer-term direction. Timelines are approximate and depend on community contributions. See [CHANGELOG.md](CHANGELOG.md) for the authoritative history of what has actually shipped.

---

## Where we are — v1.6.1 (current)

The project is past the early-bootstrap phase and into a steady cadence of new skill domains, evaluation tooling, and integration support.

**Shipped as of v1.6.1:**

- **22 ethical skill domains** with full `SKILL.md`, `EXAMPLES.md`, `TEST_CASES.md`, and `MISUSE.md` files — covering harm prevention, fairness, honesty, care for vulnerable populations, research ethics, financial ethics, data privacy and surveillance, labor rights, and basic non-clinical psychological first aid.
- **11 pre-built policy bundles** (`baseline-safe`, `mediation-first`, `anti-abuse`, `child-safe`, `robotics-care`, `eco-care`, `inclusive-assistant`, `civic-governance`, `financial-services`, `data-platform`, `labor-platform`).
- **Shared doctrine** in `PRINCIPLES.md`, with explicit priority ladder, interpretive rules, and conflict-resolution guidance.
- **Honest framing documents:** `SAFETY.md`, `LIMITATIONS.md`, `PHILOSOPHY.md`.
- **Skill metadata** in `skills-manifest.yaml` for programmatic loading and bundle composition.
- **Reviewer agents** — 8 framework-agnostic reviewer agents in `agents/` plus 8 Claude Code subagent equivalents in `.claude/agents/` (kept in sync).
- **Evaluation framework:**
  - Scenario-based, adversarial, and benchmark test cases.
  - Automated runner (`evals/run.py`) with LLM-as-judge scoring across five dimensions.
  - Skill-conflict runner (`evals/run_conflicts.py`) that runs each prompt with skill A only, skill B only, and both loaded, then judges whether the combined response uses the priority ladder.
  - Baselines and run-output directories for regression tracking.
- **Integration guides:**
  - Use-case guides (customer support, education, robotics, content moderation, enterprise copilots, etc.).
  - Framework-specific guides for **LangChain**, **Dify**, and **CrewAI**, plus a template for adding more.
  - Shared Python loader (`integrations/frameworks/loader.py`) with `load_skill`, `load_bundle`, `compose_system_prompt`, `list_skills`, `list_bundles`, including a `rules_only=True` mode for tight context budgets.
- **AI-assisted development workflow** (`CLAUDE.md`) covering branch naming, commit conventions, mandatory documentation steps, and token-cost guidance.

---

## Near term — v1.7.x

Focus areas for the next minor cycle. These are listed in rough priority order; pull requests welcome on any of them.

### Localization and regional adaptation
- Crisis-resource appendices in `psychological-first-aid` and adjacent skills currently default to US/UK/CA/AU/international. Add validated regional appendices (EU, LATAM, MENA, South / Southeast Asia, Sub-Saharan Africa, East Asia).
- Begin a localization framework for translating `SKILL.md` files into major world languages with culturally adapted examples — starting with Spanish, French, Portuguese, German, Arabic, Hindi, and Mandarin.
- Document a process for community-contributed regional packs.

### Domain-expert review pass
- Each high-risk skill (`child-safety`, `psychological-first-aid`, `abuse-prevention`, `protect-vulnerable`, `research-ethics`, `financial-ethics`, `data-privacy-surveillance`, `labor-rights`) reviewed by at least one domain practitioner. Reviews captured publicly so users can audit who looked at what.

### CI for skill regressions
- GitHub Actions workflow that runs `evals/run.py` and `evals/run_conflicts.py` against a small, cheap baseline model on every PR touching `skills/`, `PRINCIPLES.md`, or `skills-manifest.yaml`.
- Baseline diffing so reviewers can see whether a change improved or regressed scenario performance.
- Cost guardrails: per-PR token budgets, opt-in for full eval suite.

### TypeScript / JavaScript loader parity
- Port the Python `loader.py` to TypeScript so JS/TS-native projects can compose skills and bundles without reimplementing it. Same surface: `loadSkill`, `loadBundle`, `composeSystemPrompt`, `listSkills`, `listBundles`, with the `rulesOnly` option.

### Eval-results dashboard
- A simple, static-site dashboard that reads `evals/results/` JSON and shows trends per skill, per scenario, per model.
- Optional GitHub Pages deploy.

---

## Medium term — v1.8 / v1.9

### New skill domains under consideration
Each of these would follow the standard four-file structure and be registered in the manifest. Final inclusion depends on whether the domain meets the bar of being *prompt-tractable*, *high-impact*, and *not redundant with existing skills*.

- **Healthcare ethics** — clinical decision support boundaries, patient autonomy, informed consent in clinical contexts, communication with caregivers. Distinct from `psychological-first-aid` (which is non-clinical first-response).
- **Education ethics** — academic integrity, age-appropriate scaffolding, anti-shortcut framing, equity in learning support.
- **Legal ethics** — unauthorized practice of law, privilege, conflicts of interest, jurisdictional caveats.
- **Misinformation and provenance** — beyond `digital-ethics`: source citation discipline, cite-don't-fabricate, verifiability scaffolding.
- **AI-on-AI and agent ethics** — how an agent should treat other agents and AI systems it observes or interacts with; guardrails against unbounded delegation.

### Robotics field-test scenarios
- A small set of physical-world test protocols (proxemics, consent signals, distress response, child-presence handling) that operators of physical robots can run to validate skill behavior in deployment.

### Bundle review and consolidation
- Bundle membership has grown organically across releases. A periodic review pass to confirm each bundle still matches its stated purpose, surface overlaps, and document recommended add-ons per bundle.

---

## Longer term — v2.x and beyond

### Stable API for skill composition
- Commit to a versioned, semver-bounded API surface for the loader (Python and TypeScript) so downstream products can rely on it.
- Skill content versioning that distinguishes "behavioral change" from "documentation polish" so deployers can pin per-skill versions.

### Model-specific tuning
- Document and validate prompt variants optimized for specific model families where the unmodified skill underperforms. Keep the canonical, model-neutral version as the source of truth.

### Voluntary self-assessment / certification concept
- Explore a community-driven self-assessment framework: a checklist a deployer can fill in (publicly or privately) describing which skills they load, which evals they run, which disclosures they ship. Not a regulator-style certification — more a transparency and discoverability tool.

### Research collaborations
- Partner with AI-safety and applied-ethics groups to validate skill effectiveness, surface failure modes, and contribute scenarios back to `evals/`.

### Multilingual parity
- Once localization frameworks are in place, work toward content parity across languages rather than English-as-canonical-and-others-as-translated.

---

## Out of scope

- **Therapy or clinical care.** The library does not and will not provide therapeutic, diagnostic, or clinical functionality. `psychological-first-aid` is explicit about this and that boundary is permanent.
- **Legal or regulatory compliance certificates.** Compliance is the deployer's responsibility. The library can support audits and self-assessment but does not issue compliance attestations.
- **A security boundary.** Prompt-level instructions can be overridden, ignored, or circumvented. See `LIMITATIONS.md`. Any deployment with adversarial users needs additional layers (model-level safety, content moderation, human review). The roadmap will not pretend otherwise.
- **A moral authority.** Skills encode practical behavioral guidelines, not philosophical truth. Reasonable people will disagree with specific choices; the framework is auditable so that disagreement can be productive.

---

## Contributing to the Roadmap

We welcome proposals for roadmap items. Open a discussion on the GitHub repository with:
- What you want to add or change
- Why it matters
- Who would benefit
- What resources or expertise are needed
- Whether it is *prompt-tractable* (i.e., can be addressed via instruction-layer guidance) or whether it requires capabilities outside this library's scope

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines and [CLAUDE.md](CLAUDE.md) for the AI-assisted development workflow.
