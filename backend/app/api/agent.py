"""POST /api/v1/agent/chat: ask the ABM agent (app/agent). Each call spends model tokens, so it needs
an API key (analyst or admin); the security gateway also rate-limits it per key.

Only plain-text history is accepted from callers: tool calls and tool results are produced on the
server, never supplied by the client (a caller cannot inject fake "data" into the conversation).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

import anthropic
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.agent.core import BondAgent
from app.agent.feed import FeedError
from app.models.enums import Role
from app.security.auth import require_role

router = APIRouter(prefix="/agent", tags=["agent"], dependencies=[Depends(require_role(Role.ANALYST, Role.ADMIN))])


class Turn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=8000)


class ChatIn(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    history: list[Turn] = Field(default_factory=list, max_length=20)


class ChatOut(BaseModel):
    answer: str
    sources: list[str]
    tool_calls: list[dict]
    stop_reason: str
    disclaimer: str = "Information only, not investment advice. Figures come from the cited official documents."


@lru_cache
def get_agent() -> BondAgent:
    return BondAgent()


@router.post("/chat", response_model=ChatOut)
def chat(body: ChatIn, agent: BondAgent = Depends(get_agent)) -> ChatOut:
    history = [{"role": t.role, "content": t.content} for t in body.history]
    try:
        r = agent.ask(body.question, history)
    except anthropic.AuthenticationError as e:
        raise HTTPException(503, "The agent is not configured (model credentials missing).") from e
    except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.InternalServerError) as e:
        raise HTTPException(503, "The model service is busy or unreachable; retry later.") from e
    except FeedError as e:
        raise HTTPException(503, "The verified data feed is unavailable; retry later.") from e
    return ChatOut(answer=r.answer, sources=r.sources, tool_calls=r.tool_calls, stop_reason=r.stop_reason)
