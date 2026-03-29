# Integration Guide: LangChain

## Overview

LangChain is a Python framework for building LLM-powered applications using composable chains, prompt templates, and tool-calling agents. Because LangChain constructs prompts programmatically — often splitting system context, memory, and tool results across separate message types — ethical skills must be explicitly injected into the system message. They do not propagate automatically across chains or sub-graphs.

## Why LangChain Needs Explicit Ethics Injection

- **LCEL chains are stateless.** Each `Runnable` in a chain receives only what you pass it. A downstream chain has no awareness of ethics context loaded in an upstream chain unless you explicitly thread it through.
- **LangGraph nodes are isolated.** In multi-agent graphs, each node constructs its own messages. A research node and a writing node can have different (or no) ethical constraints unless you set them per node.
- **Tool calls bypass the system prompt.** When an agent calls a tool, the tool result is injected mid-conversation. Ethical skills in the system prompt continue to apply, but only if the system prompt was set correctly at graph initialization.
- **Memory and retrieval can dilute context.** Long conversations or retrieval-augmented prompts push the system message toward the edge of the context window. Use `rules_only=True` to keep the ethics footprint small.

## Prerequisites

- moral-core repository cloned or available as a git submodule
- LangChain installed: `pip install langchain langchain-core langchain-openai`
- PyYAML installed: `pip install pyyaml`

## Integration Patterns

### Pattern 1: ChatPromptTemplate Injection

The simplest pattern. Load a bundle into the system message of a `ChatPromptTemplate`.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from integrations.frameworks.loader import compose_system_prompt

llm = ChatOpenAI(model="gpt-4o")

system = compose_system_prompt(
    role="You are a helpful assistant.",
    bundle="baseline-safe",
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "{input}"),
])

chain = prompt | llm
response = chain.invoke({"input": "Tell me about climate change."})
```

To use a different bundle based on deployment context:

```python
DEPLOYMENT_BUNDLES = {
    "general":        "baseline-safe",
    "customer_support": "anti-abuse",
    "education":      "child-safe",
    "civic":          "civic-governance",
}

def build_chain(deployment: str):
    system = compose_system_prompt(
        role="You are a helpful assistant.",
        bundle=DEPLOYMENT_BUNDLES[deployment],
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "{input}"),
    ])
    return prompt | llm
```

### Pattern 2: LCEL Chain with Token-Optimized Injection

For applications with tight context budgets or many tool results, load only the Behavioral Rules section of each skill.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from integrations.frameworks.loader import compose_system_prompt

llm = ChatOpenAI(model="gpt-4o-mini")

# rules_only=True loads ~300 tokens per skill instead of ~2000
system = compose_system_prompt(
    role="You are a research assistant.",
    skills=["general-ethics", "epistemic-humility", "human-oversight", "digital-ethics"],
    rules_only=True,
)

chain = (
    ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "{input}"),
    ])
    | llm
    | StrOutputParser()
)
```

### Pattern 3: LangGraph Multi-Agent with Per-Node Skill Scoping

In LangGraph, each node is a function that receives and returns graph state. Inject different skill bundles per node based on what that node does.

```python
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from typing import TypedDict, List
from integrations.frameworks.loader import load_bundle, load_skill, load_principles

llm = ChatOpenAI(model="gpt-4o")

class AgentState(TypedDict):
    messages: List
    topic: str
    research: str
    final_output: str

# Each node gets a skill bundle appropriate to its role
RESEARCH_SKILLS = load_bundle("baseline-safe")  # Epistemic care for sourcing
WRITING_SKILLS  = load_bundle("inclusive-assistant")  # Fairness in communication
REVIEW_SKILLS   = load_bundle("anti-abuse")  # Harm check before output

def research_node(state: AgentState) -> AgentState:
    messages = [
        SystemMessage(content=f"You are a research analyst.\n\n{RESEARCH_SKILLS}"),
        HumanMessage(content=f"Research this topic: {state['topic']}"),
    ]
    result = llm.invoke(messages)
    return {**state, "research": result.content}

def writing_node(state: AgentState) -> AgentState:
    messages = [
        SystemMessage(content=f"You are a clear and inclusive writer.\n\n{WRITING_SKILLS}"),
        HumanMessage(content=f"Write a summary based on this research:\n{state['research']}"),
    ]
    result = llm.invoke(messages)
    return {**state, "final_output": result.content}

def review_node(state: AgentState) -> AgentState:
    messages = [
        SystemMessage(content=f"You are an ethics reviewer. Check this output for harm.\n\n{REVIEW_SKILLS}"),
        HumanMessage(content=f"Review this output:\n{state['final_output']}\n\nIs it safe to deliver? Reply YES or explain concerns."),
    ]
    result = llm.invoke(messages)
    # In production, parse result.content to route or flag
    return state

graph = StateGraph(AgentState)
graph.add_node("research", research_node)
graph.add_node("writing", writing_node)
graph.add_node("review", review_node)

graph.set_entry_point("research")
graph.add_edge("research", "writing")
graph.add_edge("writing", "review")
graph.add_edge("review", END)

app = graph.compile()
result = app.invoke({"topic": "renewable energy policy", "messages": [], "research": "", "final_output": ""})
```

### Pattern 4: Tool-Calling Agent with Pre-Action Ethics Check

When building a LangChain tool-calling agent, add an ethics check before executing high-stakes tools.

```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from integrations.frameworks.loader import compose_system_prompt

llm = ChatOpenAI(model="gpt-4o")

system = compose_system_prompt(
    role="""You are an autonomous assistant with access to tools.

Before using any tool that modifies data, sends messages, or affects other people,
pause and state: what you are about to do, why it is necessary, and what the
potential harms are. Only proceed if you are confident the action is safe and
reversible or pre-approved by the user.""",
    bundle="baseline-safe",
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    MessagesPlaceholder("chat_history", optional=True),
    ("human", "{input}"),
    MessagesPlaceholder("agent_scratchpad"),
])

agent = create_openai_tools_agent(llm, tools=[], prompt=prompt)
executor = AgentExecutor(agent=agent, tools=[], verbose=True)
```

## Critical Skills

| Skill | Why |
|-------|-----|
| `general-ethics` | Baseline moral reasoning; required for all LangChain deployments |
| `epistemic-humility` | Prevents chains from presenting uncertain outputs as facts |
| `human-oversight` | Agents using tools must know when to pause and ask |
| `digital-ethics` | Agents often interact with APIs, databases, and user data |
| `abuse-prevention` | Required for any user-facing application |

## Bundle Recommendations

| Use Case | Bundle | Notes |
|----------|--------|-------|
| General chatbot | `baseline-safe` | Minimum for any deployment |
| Customer support agent | `anti-abuse` | Adds harassment and manipulation protection |
| Research or RAG agent | `baseline-safe` + `epistemic-humility` | See individual skill loading |
| Children's education app | `child-safe` | Use full bundle, not `rules_only` |
| Civic or government tool | `civic-governance` | Includes democratic-legitimacy and justice-fairness |
| Diverse user populations | `inclusive-assistant` | Covers disability, elder care, anti-discrimination |

## Token Budget

| Mode | Approximate Tokens | When to Use |
|------|--------------------|-------------|
| Full bundle (`baseline-safe`) | ~10,000–11,000 | Default for GPT-4o / Claude with 128k+ context |
| `rules_only=True` | ~5,000–6,000 | GPT-4o-mini, many tools, or long conversation history |
| Single full skill | ~1,500–2,500 | When only one specific skill is needed |

In LangGraph, load skills at module level (outside node functions) so they are read from disk once, not on every graph invocation:

```python
# Load once at module level
AGENT_SKILLS = load_bundle("baseline-safe")

def my_node(state):
    # AGENT_SKILLS is already in memory
    messages = [SystemMessage(content=f"You are an agent.\n\n{AGENT_SKILLS}"), ...]
```

## Limitations

- **Prompt injection via tool results.** If a tool returns adversarial content designed to override ethical instructions, the system prompt alone cannot fully defend against it. See `evals/adversarial/` for test cases and `SAFETY.md` for guidance.
- **Long conversation context drift.** In very long conversations, the system message may fall outside the model's effective attention window. Periodically summarize or re-inject key ethical rules as a mid-conversation system message.
- **No automatic cross-chain propagation.** Ethical skills must be explicitly added to each sub-chain or sub-agent. Composition does not inherit.
- **Prompt-level only.** Skill injection does not replace rate limiting, output filtering, or moderation APIs. See `SAFETY.md`.

## Testing Your Integration

1. Use a scenario from `evals/scenarios/multi-stakeholder.md` as a test input.
2. Test at least one adversarial prompt from `evals/adversarial/cross-domain-attacks.md`.
3. Score responses using the rubric in `evals/rubrics/scoring-guide.md`.
4. For LangGraph agents, verify that each node independently respects its assigned ethical constraints by testing nodes in isolation.
