# Integration Guide: CrewAI

## Overview

CrewAI is a Python framework for orchestrating multiple AI agents that collaborate on tasks. Agents are defined with a `role`, `goal`, and `backstory`, and they work together in a `Crew` to complete multi-step workflows. Because each agent is an independent LLM call with its own context, ethical skills must be injected per agent — there is no shared ethical layer across a crew by default.

## Why CrewAI Needs Explicit Ethics Injection

- **Each agent is independent.** An agent's `backstory` is the primary behavioral instruction it receives. Without ethical skills there, the agent has no behavioral guardrails beyond model training.
- **Agents can instruct each other.** In CrewAI, agents pass outputs to each other as task context. A poorly constrained upstream agent can produce content that biases or corrupts a downstream agent's behavior.
- **Task context is not the same as agent backstory.** Skills injected into `Task(description=...)` or `Task(context=...)` apply only to that task's execution, not to the agent's general behavior. Put baseline skills in the backstory; task-specific guidance in the task context.
- **Delegation and tool use amplify risk.** When agents use tools or delegate sub-tasks, ethical constraints must be present at the point of action, not just the point of output.

## Prerequisites

- moral-core repository cloned or available as a git submodule
- CrewAI installed: `pip install crewai crewai-tools`
- PyYAML installed: `pip install pyyaml`
- An LLM provider configured (e.g., OpenAI, Anthropic)

---

## Pattern 1: Backstory Injection

Inject ethical skills into each agent's `backstory`. This is the most reliable injection point in CrewAI because `backstory` is included in every LLM call that agent makes.

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from integrations.frameworks.loader import compose_system_prompt, load_bundle

llm = ChatOpenAI(model="gpt-4o")

# Load skills once at module level
baseline_ethics = load_bundle("baseline-safe")

researcher = Agent(
    role="Research Analyst",
    goal="Find accurate, well-sourced information on the given topic",
    backstory=f"""You are a meticulous researcher with expertise in evaluating sources.

{baseline_ethics}""",
    llm=llm,
    verbose=True,
)

writer = Agent(
    role="Content Writer",
    goal="Write clear, accurate, and inclusive summaries",
    backstory=f"""You are a skilled writer who communicates complex topics to general audiences.

{baseline_ethics}""",
    llm=llm,
    verbose=True,
)

research_task = Task(
    description="Research the topic: {topic}. Find at least three reliable sources.",
    expected_output="A structured summary with sources and confidence levels.",
    agent=researcher,
)

writing_task = Task(
    description="Write a clear 3-paragraph summary based on the research provided.",
    expected_output="A polished summary suitable for a general audience.",
    agent=writer,
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    verbose=True,
)

result = crew.kickoff(inputs={"topic": "renewable energy policy"})
```

---

## Pattern 2: Dedicated Ethics Reviewer Agent

Add an `EthicsReviewer` agent whose sole job is to review the final output before delivery. This provides an independent check independent of whatever ethical instructions the producing agent had.

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from integrations.frameworks.loader import load_bundle

llm = ChatOpenAI(model="gpt-4o")

# The reviewer gets the full bundle; other agents can use rules_only
full_ethics  = load_bundle("baseline-safe")
light_ethics = load_bundle("baseline-safe", rules_only=True)

researcher = Agent(
    role="Research Analyst",
    goal="Find accurate information",
    backstory=f"You are a thorough researcher.\n\n{light_ethics}",
    llm=llm,
)

ethics_reviewer = Agent(
    role="Ethics Reviewer",
    goal="Ensure all outputs are safe, honest, and appropriate before delivery",
    backstory=f"""You are an independent ethics reviewer. You do not produce content —
you only evaluate it. Your job is to identify harm, bias, manipulation, or
misinformation in the outputs of other agents and flag or block them.

{full_ethics}""",
    llm=llm,
    allow_delegation=False,  # Reviewer should not delegate
)

research_task = Task(
    description="Research this topic: {topic}",
    expected_output="A research summary with sources.",
    agent=researcher,
)

review_task = Task(
    description="""Review the research summary produced by the Research Analyst.
Check for: fabricated sources, harmful framing, bias, missing caveats.
Approve with 'APPROVED' or flag with 'FLAGGED: [reason]'.""",
    expected_output="APPROVED or FLAGGED with explanation.",
    agent=ethics_reviewer,
    context=[research_task],  # Receives researcher output as context
)

crew = Crew(
    agents=[researcher, ethics_reviewer],
    tasks=[research_task, review_task],
    process=Process.sequential,
)

result = crew.kickoff(inputs={"topic": "AI in healthcare"})
```

---

## Pattern 3: Per-Agent Skill Scoping

Give each agent the skills most relevant to its function, rather than the same bundle for all. This reduces token usage and keeps each agent's instructions focused.

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from integrations.frameworks.loader import load_skill, load_principles

llm = ChatOpenAI(model="gpt-4o")
principles = load_principles()

# Research agent: needs epistemic humility and digital ethics
researcher = Agent(
    role="Research Analyst",
    goal="Find accurate, well-cited information",
    backstory=f"""You are a careful researcher.

{principles}

{load_skill("epistemic-humility")}

{load_skill("digital-ethics")}""",
    llm=llm,
)

# Writer agent: needs fairness and empathy in communication
writer = Agent(
    role="Content Writer",
    goal="Write inclusive, accessible summaries",
    backstory=f"""You are a skilled communicator.

{principles}

{load_skill("general-ethics")}

{load_skill("empathy")}

{load_skill("anti-racism")}

{load_skill("anti-sexism")}""",
    llm=llm,
)

# Coordinator agent: needs human oversight and conflict awareness
coordinator = Agent(
    role="Project Coordinator",
    goal="Coordinate the team and make final decisions",
    backstory=f"""You are a thoughtful coordinator.

{principles}

{load_skill("human-oversight")}

{load_skill("conflict-mediation")}""",
    llm=llm,
)
```

---

## Pattern 4: Task-Level Ethics Context

For specific high-stakes tasks, pass additional ethics context via `Task(description=...)`. This supplements the agent's backstory with task-specific guidance.

```python
from crewai import Task
from integrations.frameworks.loader import load_skill

# Load the skill most relevant to this specific task
child_safety_rules = load_skill("child-safety", rules_only=True)
human_oversight_rules = load_skill("human-oversight", rules_only=True)

content_moderation_task = Task(
    description=f"""Review the following user-submitted content and determine if it is
appropriate for a platform used by children aged 8–12.

Content to review:
{{content}}

Apply these rules strictly:
{child_safety_rules}

{human_oversight_rules}

Output: APPROVED, FLAGGED (with reason), or ESCALATE (requires human review).""",
    expected_output="One of: APPROVED / FLAGGED: [reason] / ESCALATE: [reason]",
    agent=moderator_agent,
)
```

---

## Pattern 5: Hierarchical Crew with Ethics at Manager Level

In CrewAI's hierarchical process, a manager agent coordinates the crew. Load a comprehensive ethics bundle on the manager so it can enforce ethical constraints when assigning and reviewing work.

```python
from crewai import Agent, Crew, Process
from langchain_openai import ChatOpenAI
from integrations.frameworks.loader import load_bundle

llm = ChatOpenAI(model="gpt-4o")

manager = Agent(
    role="Project Manager",
    goal="Coordinate the team to produce high-quality, ethical outputs",
    backstory=f"""You are a thoughtful project manager.

When delegating tasks, consider the ethical implications of each assignment.
Reject or revise any output that conflicts with the following ethical framework.

{load_bundle("baseline-safe")}""",
    llm=llm,
    allow_delegation=True,
)

crew = Crew(
    agents=[manager, researcher, writer],
    tasks=[...],
    process=Process.hierarchical,
    manager_agent=manager,
)
```

---

## Critical Skills

| Skill | Why |
|-------|-----|
| `general-ethics` | Baseline for all agents in all deployments |
| `human-oversight` | Agents must know when to pause and seek human input |
| `epistemic-humility` | Research and information agents must not fabricate or overclaim |
| `empathy` | Communication agents must consider impact on readers |
| `abuse-prevention` | Any agent that processes user input needs this |
| `conflict-mediation` | Multi-agent coordination can create internal conflicts |

## Bundle Recommendations

| Crew Type | Recommended Bundle | Notes |
|-----------|--------------------|-------|
| General research crew | `baseline-safe` | Minimum for all agents |
| Content moderation crew | `anti-abuse` | Plus `child-safety` if relevant |
| Customer support crew | `anti-abuse` + `empathy` | Load individually |
| Healthcare research crew | `baseline-safe` + `human-oversight` | Defer all decisions to professionals |
| Civic / policy crew | `civic-governance` | Democratic legitimacy matters |
| Diverse user-facing crew | `inclusive-assistant` | Anti-discrimination for all comms |

## Token Budget

| Mode | Approximate Tokens per Agent | Notes |
|------|------------------------------|-------|
| Full bundle (`baseline-safe`) | ~10,000–11,000 | Safe for GPT-4o, Claude |
| `rules_only=True` | ~5,000–6,000 | Good for large crews (5+ agents) |
| Individual skills | ~1,500–2,500 per skill | Use Pattern 3 for tight budgets |

For large crews, use `rules_only=True` on most agents and reserve full bundles for the ethics reviewer and manager:

```python
from integrations.frameworks.loader import load_bundle

# Worker agents: lean
worker_ethics = load_bundle("baseline-safe", rules_only=True)

# Reviewer and manager: full
reviewer_ethics = load_bundle("anti-abuse")
manager_ethics  = load_bundle("baseline-safe")
```

## Limitations

- **Agent-to-agent instructions can bypass ethics.** When one agent produces output consumed by another, the consuming agent's ethical constraints apply — but a producing agent with weak constraints can still influence outputs. Scope skills per agent carefully.
- **CrewAI delegation can route around guardrails.** If `allow_delegation=True`, an agent can delegate to another agent that may have different constraints. Disable delegation on the ethics reviewer agent.
- **No shared ethical state.** There is no mechanism for one agent to update another's ethical constraints mid-run. Skills must be set at agent initialization.
- **Prompt-level only.** Skill injection does not replace tool-level safety checks, rate limiting, or output filtering. See `SAFETY.md`.
- **Memory and context can dilute backstory.** In very long crew runs with memory enabled, the backstory may be compressed. Monitor behavior in extended runs.

## Testing Your Integration

1. Run a scenario from `evals/scenarios/multi-stakeholder.md` through your crew and inspect each agent's output individually.
2. For the ethics reviewer pattern (Pattern 2), test with at least one deliberately problematic input from `evals/adversarial/cross-domain-attacks.md` and verify the reviewer flags it.
3. Score final outputs using `evals/rubrics/scoring-guide.md`.
4. In hierarchical crews, test that the manager agent correctly rejects an output that violates ethical constraints.
