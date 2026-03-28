"""
Moral Core Agent Runner
-----------------------
Minimal example for running Moral Core agents with any OpenAI-compatible API.
Works with OpenAI, Anthropic (via compatibility endpoint), Mistral, Ollama, etc.

Usage:
    python runner.py --agent ethics-reviewer --content "your content here"
    python runner.py --agent empathy-style-checker --file path/to/text.txt
    python runner.py --agent misuse-auditor --file path/to/system-prompt.md
"""

import argparse
import os
from pathlib import Path


def load_agent(agent_name: str) -> str:
    """Load the system prompt from an agent file."""
    agent_file = Path(__file__).parent / f"{agent_name}.md"
    if not agent_file.exists():
        available = [f.stem for f in Path(__file__).parent.glob("*.md") if f.stem != "README"]
        raise FileNotFoundError(
            f"Agent '{agent_name}' not found. Available: {', '.join(available)}"
        )
    raw = agent_file.read_text()
    # Extract everything after the "## System Prompt" heading
    marker = "## System Prompt\n"
    if marker not in raw:
        return raw  # Fall back to full file if no marker
    return raw.split(marker, 1)[1].strip()


def run_with_openai(system_prompt: str, content: str, model: str = "gpt-4o") -> str:
    """Run using the OpenAI SDK (also works with any OpenAI-compatible endpoint)."""
    from openai import OpenAI

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL"),  # Override for local/compatible endpoints
    )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ],
    )
    return response.choices[0].message.content


def run_with_anthropic(system_prompt: str, content: str, model: str = "claude-sonnet-4-6") -> str:
    """Run using the Anthropic SDK."""
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": content}],
    )
    return response.content[0].text


def run_with_ollama(system_prompt: str, content: str, model: str = "llama3") -> str:
    """Run using Ollama (local models)."""
    import requests

    response = requests.post(
        "http://localhost:11434/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": content},
            ],
            "stream": False,
        },
    )
    response.raise_for_status()
    return response.json()["message"]["content"]


PROVIDERS = {
    "openai": run_with_openai,
    "anthropic": run_with_anthropic,
    "ollama": run_with_ollama,
}


def main():
    parser = argparse.ArgumentParser(description="Run a Moral Core agent")
    parser.add_argument("--agent", required=True, help="Agent name (e.g. ethics-reviewer)")
    parser.add_argument("--content", help="Content to review (inline string)")
    parser.add_argument("--file", help="Path to file containing content to review")
    parser.add_argument("--provider", default="anthropic", choices=PROVIDERS.keys())
    parser.add_argument("--model", help="Model name (uses provider default if omitted)")
    args = parser.parse_args()

    if not args.content and not args.file:
        parser.error("Provide --content or --file")

    content = args.content or Path(args.file).read_text()
    system_prompt = load_agent(args.agent)
    runner = PROVIDERS[args.provider]

    kwargs = {"system_prompt": system_prompt, "content": content}
    if args.model:
        kwargs["model"] = args.model

    result = runner(**kwargs)
    print(result)


if __name__ == "__main__":
    main()
