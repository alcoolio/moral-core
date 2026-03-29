# Integration Guides

This directory contains guides for integrating Moral Core skills into specific deployment contexts.

## Use-Case Guides

| Guide | Context |
|---|---|
| [generic-llm-apps.md](generic-llm-apps.md) | Any LLM-powered application |
| [agent-frameworks.md](agent-frameworks.md) | Autonomous agent frameworks |
| [customer-support.md](customer-support.md) | Customer support chatbots |
| [educational-assistants.md](educational-assistants.md) | Educational and tutoring systems |
| [home-robots.md](home-robots.md) | Domestic and home robotics |
| [social-robots.md](social-robots.md) | Socially assistive robotics |
| [moderation-systems.md](moderation-systems.md) | Content moderation |
| [enterprise-copilots.md](enterprise-copilots.md) | Enterprise AI copilots |
| [policy-bundles.md](policy-bundles.md) | Pre-built policy bundle definitions |

## Framework-Specific Guides

Framework guides show how to load skills using the native patterns of each orchestration framework. They include working code examples and a shared Python loader utility.

| Framework | Type | Guide |
|-----------|------|-------|
| [LangChain](frameworks/langchain/README.md) | Python orchestration | ChatPromptTemplate, LCEL, LangGraph multi-agent |
| [Dify](frameworks/dify/README.md) | No-code / low-code platform | System Prompt UI, Code nodes, workflow ethics review |
| [CrewAI](frameworks/crewai/README.md) | Multi-agent crews | Agent backstory injection, dedicated ethics reviewer, task-level scoping |

See [`frameworks/README.md`](frameworks/README.md) for the shared loader utility and instructions for adding more framework guides.

## General Approach

All integrations follow the same pattern:

1. **Load PRINCIPLES.md** as a shared foundation.
2. **Select skills** appropriate to your deployment context.
3. **Compose skills** into a system prompt or instruction layer.
4. **Test** using the eval framework in `evals/`.
5. **Monitor** for unexpected behavior and iterate.

See [policy-bundles.md](policy-bundles.md) for pre-built skill combinations.
