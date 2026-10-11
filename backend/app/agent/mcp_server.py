"""MCP server exposing the ABM tools (read-only, verified data) to any MCP client: Claude Desktop,
Claude Code, or another agent.  Run:  python -m app.agent.mcp_server   (stdio transport)

No model is called here: the client's own model uses the tools, so no Anthropic key is needed.
The tool list and schemas are the same as the agent's (app/agent/tools.py).
"""

from __future__ import annotations

import asyncio
import json

import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

from app.agent import tools
from app.agent.feed import Feed, FeedError
from app.agent.prompt import SYSTEM

server = Server("africa-bonds-monitor", instructions=SYSTEM)
_feed = Feed()


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [types.Tool(name=d["name"], description=d["description"], inputSchema=d["input_schema"]) for d in tools.definitions()]


@server.call_tool()
async def call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    try:
        out = await asyncio.to_thread(tools.run, _feed, name, {k: v for k, v in (arguments or {}).items() if v is not None})
    except (tools.ToolError, FeedError) as e:
        raise ValueError(str(e)) from e  # reported to the client as a tool error
    return [types.TextContent(type="text", text=json.dumps(out, ensure_ascii=False, default=str))]


async def main() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
