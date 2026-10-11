"""ABM agent: African sovereign bond intelligence on top of the published, verified data feed.

The agent answers questions with Claude and a small set of read-only tools (app/agent/tools.py).
Every number it states must come from a tool result, with its source document; derived numbers
are labelled CALCULATION. It gives information only, never investment advice. See docs/AGENT.md.
"""
