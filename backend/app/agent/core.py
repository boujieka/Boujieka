"""The agent loop: Claude + the read-only tools of app/agent/tools.py.

A manual loop (no beta tool runner) so every tool call is recorded, its sources collected and the
number of steps bounded. One instance can serve many conversations; it holds no conversation state.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any

import anthropic

from app.agent import tools
from app.agent.feed import Feed, FeedError
from app.agent.prompt import SYSTEM

MODEL = os.environ.get("ABM_AGENT_MODEL", "claude-opus-5-5")
EFFORT = os.environ.get("ABM_AGENT_EFFORT", "high")  # factual, multi-tool questions: depth over speed
MAX_STEPS = 10
MAX_TOKENS = 16000
FALLBACK_BETA = "server-side-fallback-2026-07-01"  # on a safety decline, re-run on Anthropic's recommended model


@dataclass
class AgentResult:
    answer: str
    stop_reason: str
    tool_calls: list[dict] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    usage: dict[str, int] = field(default_factory=dict)
    messages: list[dict] = field(default_factory=list)  # full transcript, to continue the conversation


def _sources(obj: Any, out: list[str]) -> None:
    """Collect every source URL found in a tool result (order of first appearance)."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("source_url", "pdf") and isinstance(v, str) and v.startswith("https://") and v not in out:
                out.append(v)
            else:
                _sources(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _sources(v, out)


class BondAgent:
    def __init__(self, client: anthropic.Anthropic | None = None, feed: Feed | None = None,
                 model: str = MODEL, effort: str = EFFORT, max_steps: int = MAX_STEPS):
        self.client = client or anthropic.Anthropic()
        self.feed = feed or Feed()
        self.model, self.effort, self.max_steps = model, effort, max_steps
        self.tool_defs = tools.definitions()

    def _call(self, messages: list[dict]):
        return self.client.beta.messages.create(
            model=self.model,
            max_tokens=MAX_TOKENS,
            system=SYSTEM,
            tools=self.tool_defs,
            messages=messages,
            output_config={"effort": self.effort},
            cache_control={"type": "ephemeral"},  # tools + system + history prefix
            betas=[FALLBACK_BETA],
            fallbacks="default",
        )

    def run(self, messages: list[dict]) -> AgentResult:
        """messages: the conversation so far, ending with the user's question (Messages API format)."""
        messages = list(messages)
        calls: list[dict] = []
        sources: list[str] = []
        usage = {"input_tokens": 0, "output_tokens": 0, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}
        for _ in range(self.max_steps):
            response = self._call(messages)
            for k in usage:
                usage[k] += getattr(response.usage, k, 0) or 0
            if response.stop_reason == "refusal":
                return AgentResult("I can't help with that request. I can answer questions about African government securities using ABM's verified data.",
                                   "refusal", calls, sources, usage, messages)
            # Keep the whole content (thinking blocks included) so the next request continues the same turn.
            messages.append({"role": "assistant", "content": [b.to_dict() for b in response.content]})
            uses = [b for b in response.content if b.type == "tool_use"]
            if response.stop_reason != "tool_use" or not uses:
                text = "\n".join(b.text for b in response.content if b.type == "text").strip()
                if response.stop_reason == "max_tokens":
                    text += "\n\n[Answer cut short: it reached the length limit.]"
                return AgentResult(text, response.stop_reason, calls, sources, usage, messages)
            results = []
            for u in uses:  # all results go back in one user message
                try:
                    out = tools.run(self.feed, u.name, u.input)
                    _sources(out, sources)
                    results.append({"type": "tool_result", "tool_use_id": u.id, "content": json.dumps(out, ensure_ascii=False, default=str)})
                    calls.append({"tool": u.name, "input": u.input, "ok": True})
                except (tools.ToolError, FeedError) as e:
                    results.append({"type": "tool_result", "tool_use_id": u.id, "content": f"Error: {e}", "is_error": True})
                    calls.append({"tool": u.name, "input": u.input, "ok": False, "error": str(e)})
            messages.append({"role": "user", "content": results})
        return AgentResult("I could not finish within the allowed number of steps. Please narrow the question.",
                           "max_steps", calls, sources, usage, messages)

    def ask(self, question: str, history: list[dict] | None = None) -> AgentResult:
        return self.run([*(history or []), {"role": "user", "content": question}])
