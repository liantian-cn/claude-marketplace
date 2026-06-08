# Advanced Search

Search, extract, crawl, and research the web — powered by Tavily MCP. AI-optimized results with built-in WebSearch + Tavily dual-engine orchestration.

> Adapted from [tavily-ai/skills](https://github.com/tavily-ai/skills) (MIT License). Modified to use Tavily MCP instead of the Tavily CLI. Consolidated into a single advanced-search skill that orchestrates all search operations.

## Setup

This plugin includes a pre-configured `.mcp.json`. All you need is a Tavily API key:

1. Get an API key at [tavily.com](https://tavily.com)
2. Set it in your Claude Code settings as `TAVILY_API_KEY`

The MCP server connects automatically — no installation, no CLI, no login commands.

## Available Skills

| Skill | What it does |
|-------|-------------|
| **[advanced-search](skills/advanced-search/SKILL.md)** | The single entry point for all web information retrieval. Orchestrates WebSearch + Tavily dual-engine search, with automatic routing to the right tool (search, extract, crawl, map, research) based on query intent. |

## How it works

The `advanced-search` skill automatically classifies your query intent and picks the right Tavily MCP tool:

1. **Quick lookup** — Simple facts → `tavily_search` (fast)
2. **News & recent events** — Time-sensitive → `tavily_search` with time filters
3. **Deep research** — Comprehensive analysis → `tavily_research`
4. **Site exploration** — URL discovery → `tavily_map`
5. **Bulk extraction** — Many pages → `tavily_crawl`
6. **Page reading** — Specific URLs → `tavily_extract`
7. **General search** — Everything else → dual-engine `WebSearch` + `tavily_search`

All searches run through both WebSearch and Tavily in parallel, with results deduplicated and merged.
