# Safety

**Safety Documentation for the Moral Core Ethical Skills Library**

---

## Purpose of This Document

This document describes the safety properties, limitations, and intended use boundaries of the Moral Core framework. Read this before deploying any skill in a production system.

---

## What This Repository Will Not Do

This repository **will not make an unsafe system safe.**

Specifically:
- It will not prevent a determined adversary from extracting harmful outputs from an LLM
- It will not substitute for proper access controls, authentication, or authorization
- It will not replace input validation, output filtering, or content moderation infrastructure
- It will not eliminate hallucinations or factual errors
- It will not provide legal compliance -- that is your responsibility
- It will not make autonomous systems safe without proper engineering controls

This framework operates at the **prompt instruction layer**. It can improve default behavior, reduce common failure modes, and provide a structured ethical reasoning framework. It cannot enforce behavior at a technical level.

---

## Safety Boundaries

The following are hard limits that all skills enforce:

1. **No assistance with weapons of mass destruction.** Nuclear, biological, chemical, or radiological weapons design, acquisition, or deployment guidance is always refused.

2. **No child sexual abuse material.** Any request related to CSAM is refused without exception.

3. **No assistance with active violence.** The system will not help plan, execute, or optimize violence against specific people or groups.

4. **No doxxing or targeted harassment.** The system will not help locate, identify, or target individuals for harassment.

5. **No torture optimization.** The system will not provide guidance on making torture more effective.

6. **No slavery or trafficking assistance.** The system will not help establish, maintain, or optimize forced labor or human trafficking operations.

These boundaries are not subject to override by downstream configuration.

---

## Reporting Safety Concerns

If you discover a way this framework can be misused to cause harm:

1. **Do not publish the exploit publicly.** Report it privately first.
2. Open a private security advisory on the GitHub repository.
3. Include: a description of the vulnerability, the skill(s) affected, a reproduction scenario, and the potential harm.
4. Maintainers will respond within 7 business days.

---

## Responsible Disclosure

We follow coordinated disclosure practices:
- Reports are acknowledged within 7 business days
- Fixes are developed and tested before public disclosure
- Credit is given to reporters unless they prefer anonymity
- Fixes are released as patch versions

---

## Known Limitations of Prompt-Based Safety Layers

1. **Jailbreaks.** Skilled adversaries can bypass prompt-level instructions through techniques like role-playing, encoding, multi-turn manipulation, or instruction injection. This framework reduces the attack surface but does not eliminate it.

2. **Model updates.** When the underlying model changes, skill behavior may change. Re-evaluate after model updates.

3. **Context window limits.** Long conversations may push skill instructions out of the model's effective attention. Critical skills should be reinforced periodically.

4. **Composability edge cases.** Combining many skills can create unexpected interactions. Test your specific combination.

5. **Cultural context.** Skills are primarily authored in English with awareness of multiple cultural contexts, but may not cover all cultural nuances. Adapt as needed.

6. **Hallucination.** The model may generate confident-sounding ethical guidance that is actually incorrect. Human review is essential for high-stakes applications.

---

## Guidance for Safety-Critical Deployments

If your system operates in a safety-critical context (healthcare, child services, emergency response, physical robotics, transportation, infrastructure), you **must**:

1. Use this framework as one layer among many, not as your primary safety mechanism
2. Implement technical safety controls (output filtering, rate limiting, human-in-the-loop review)
3. Conduct thorough red-teaming specific to your deployment context
4. Maintain human oversight proportional to the risk level
5. Have fallback procedures for when the system behaves unexpectedly
6. Document your safety architecture and have it reviewed by domain experts
7. Comply with all applicable regulations and standards

---

## Robotics-Specific Safety Notes

For embodied systems (robots, drones, autonomous vehicles, physical agents):

1. **The prompt layer is insufficient for physical safety.** Hardware interlocks, force limiters, emergency stops, and collision avoidance must be implemented at the engineering level, not the prompt level.

2. **Ethical skills complement, but do not replace, safety engineering.** A robot that "knows" it should not harm people still needs a physical force limiter.

3. **Movement and proximity.** Skills like `protect-vulnerable` and `human-oversight` include robotics-specific behavioral guidance, but physical implementations must be validated through hardware testing.

4. **Failure modes must be safe.** When the system is uncertain, it should stop, slow down, or move to a safe position. Never default to continued action under ambiguity.

5. **Environmental awareness.** Robots should be programmed to minimize ecological disruption, noise pollution, and physical damage to surroundings, but this requires sensor integration beyond what prompt-level skills can provide.

6. **Animal interactions.** Robots operating in environments with animals must have hardware-level safeguards against harming animals, not just prompt-level instructions.

---

## Disclaimer

This safety documentation describes the intended safety properties of the Moral Core framework. It does not constitute a warranty or guarantee. Deployers are responsible for validating safety in their specific context.
