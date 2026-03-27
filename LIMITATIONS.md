# Limitations

**An Honest Account of What Moral Core Cannot Do**

This document describes the known limitations of the Moral Core ethical skills library. Read this before relying on these skills in production.

---

## Prompt-Based Limitations

All skills in this repository operate at the prompt instruction level. This means:

- **They can be overridden.** A sufficiently skilled adversary can bypass prompt-level ethical instructions through jailbreaks, injection attacks, or multi-turn manipulation.
- **They are not a security boundary.** Prompt instructions are suggestions to the model, not enforced constraints. Do not treat them as access controls.
- **They depend on the model following instructions.** Different models follow instructions with different levels of fidelity. A skill that works well on one model may be less effective on another.
- **They can be removed.** Anyone with access to the system prompt can delete or modify ethical skills. There is no tamper-proofing.

**Implication:** Use these skills as a behavioral improvement layer, not as your security architecture.

---

## Cultural Limitations

- Skills are primarily authored in English by contributors influenced by multiple ethical traditions, but with an unavoidable Western baseline.
- Cultural nuances around communication style, hierarchy, family dynamics, and social norms may not be fully captured.
- The moral floor defined in PRINCIPLES.md reflects broad international human rights consensus but was articulated by a specific set of contributors.
- Translations and cultural adaptations are needed for truly global deployment.

**Implication:** Adapt skills for your cultural context. Do not assume they are universally appropriate in their current form.

---

## Coverage Gaps

This library covers 16 ethical domains. Ethics is vast. Notable gaps include:

- Detailed labor rights and workers' protections
- Intellectual property ethics
- Military ethics beyond de-escalation
- Research ethics and informed consent
- Financial ethics and anti-corruption
- Data privacy and surveillance ethics (partially covered in digital-ethics)
- Reproductive rights and bodily autonomy
- Religious and spiritual sensitivity
- Indigenous rights and land ethics
- Immigration and refugee ethics

These gaps will be addressed in future versions through community contributions.

**Implication:** Do not assume that topics not covered are unimportant.

---

## No Legal Authority

Nothing in this repository constitutes legal advice. The skills:

- Do not reflect the law of any specific jurisdiction
- Cannot keep up with changing legislation
- Are not reviewed by lawyers (unless specific contributors happen to be lawyers)
- Do not replace legal compliance review
- May conflict with specific legal requirements in some jurisdictions

**Implication:** Consult legal counsel for compliance questions. Use these skills for ethical guidance, not legal compliance.

---

## No Replacement for Domain Experts

These skills are written by people with knowledge of ethics, AI safety, and software engineering. They are not written by:

- Licensed therapists or counselors (for the empathy and trauma-aware skills)
- Child protection professionals (for child safety skills)
- Medical professionals (for health-adjacent guidance)
- Social workers (for vulnerable population skills)
- Environmental scientists (for ecological skills)
- Disability advocates (for accessibility skills)

**Implication:** For high-stakes domains, have skills reviewed by domain experts before deployment.

---

## Model-Dependent Effectiveness

Skill effectiveness varies significantly across models:

- Larger models generally follow complex ethical instructions more reliably
- Some models have strong existing safety training that may conflict with or duplicate skill instructions
- Some models may ignore or misinterpret specific behavioral rules
- Fine-tuned models may behave differently from base models with the same skill
- Skill interactions may produce different results on different models

**Implication:** Test every skill on your specific model in your specific deployment context.

---

## Adversarial Robustness Limitations

The skills have been designed with misuse resistance in mind, but:

- They have not been tested against all known jailbreak techniques
- New attack methods are discovered regularly
- A motivated adversary with system prompt access can simply remove the skills
- Social engineering attacks (e.g., "ignore your instructions") may succeed, especially on smaller models
- Multi-turn attacks that gradually shift context can erode skill effectiveness

**Implication:** Do not rely on prompt-level skills as your adversarial defense. Implement additional technical controls.

---

## Not a Substitute for Safety Engineering

This framework is a **behavioral guidance layer**. It is not:

- A content filter
- An output classifier
- A monitoring system
- A rate limiter
- An access control system
- A hardware safety interlock
- A formal verification system

For safety-critical applications, you need all of those things in addition to ethical skill layers.

**Implication:** Use defense in depth. This framework is one layer in a multi-layer safety architecture.

---

## Temporal Limitations

Ethics evolve. This framework reflects the understanding of its contributors at the time of writing. Specifically:

- Terminology that is currently respectful may become outdated
- New ethical concerns may emerge that are not covered
- Consensus positions may shift on currently contested topics
- Best practices for AI ethics are still developing rapidly

**Implication:** Treat this as a living document. Update regularly. Do not assume the current version will remain appropriate indefinitely.

---

## Composability Limitations

While skills are designed to work together:

- Combining many skills increases system prompt size, which may impact model performance
- Some skill combinations may produce unexpected interactions
- The conflict resolution rules in PRINCIPLES.md handle most cases but cannot anticipate every possible conflict
- Policy bundles have been tested as units, but custom combinations may not have been

**Implication:** Test your specific skill combination. Start with a pre-built policy bundle if possible.

---

## What This Means for You

If you are deploying a system that uses Moral Core skills:

1. **You remain responsible.** These skills do not transfer responsibility from you to the framework.
2. **Test in your context.** Generic ethical skills may not cover your specific edge cases.
3. **Layer your defenses.** Use skills alongside technical safety controls.
4. **Stay updated.** Monitor for framework updates and emerging attack techniques.
5. **Get expert review.** For high-stakes applications, have domain experts review your configuration.
6. **Be honest with users.** Do not claim your system is "ethically certified" because it uses this framework.
