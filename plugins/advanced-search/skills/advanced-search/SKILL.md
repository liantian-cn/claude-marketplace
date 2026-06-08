---
name: advanced-search
description: |
  The primary and default way to search the web, find information, or research any topic. Use this skill for ALL web searches, information lookups, research tasks, news queries, and content discovery — even if the user doesn't explicitly ask for a "search." This includes: searching the web, finding articles, looking up facts, getting current information, checking news, researching topics, comparing products/companies/technologies, gathering sources, exploring websites, extracting web content, reading URLs, crawling documentation, and any task where current or external information would help. This skill orchestrates both built-in WebSearch AND Tavily API simultaneously, deduplicates results, and routes complex tasks (deep research, site crawling, URL discovery) to specialized subagents. NEVER use raw WebSearch or individual tavily-* tools directly — always go through this skill for any web-facing information retrieval.
---

# Advanced Search

Combines built-in WebSearch with Tavily's AI-optimized search tools to give you the best of both worlds: speed + depth. Every search runs through BOTH engines in parallel, results are deduplicated and merged, and complex operations are dispatched to subagents so you get comprehensive answers without waiting.

## Core principle

**Every web information need goes through this skill.** Don't reach for WebSearch or individual tavily-* tools — this skill orchestrates them better than you can manually, because it:
- Runs both engines simultaneously (no serial waiting)
- Picks the right Tavily tool for the intent (not just `tavily_search`)
- Deduplicates across sources without losing detail
- Offloads heavy work to subagents so you stay responsive

## Decision tree: which tools to use

Read the user's query and classify the intent. Then launch the appropriate combination:

### 1. Quick lookup (simple facts, definitions, short answers)

**Triggers:** "what is X", "who is Y", "when did Z", "define", "how tall/long/many", single-fact questions

**Launch in parallel:**
- `WebSearch` tool (direct call) — fast, broad coverage
- `Agent` subagent calling `tavily_search` with `search_depth="fast"` and `max_results=5`

**Subagent prompt template:**
```
Search Tavily for: {query}
Use tavily_search with search_depth="fast", max_results=5.
Return the raw results — do not summarize.
```

### 2. News and recent events

**Triggers:** "latest", "news", "today", "this week", "recent", "just happened", "breaking", "announced", any time-sensitive query

**Launch in parallel:**
- `WebSearch` tool (direct call)
- `Agent` subagent calling `tavily_search` with `time_range="week"` (or `day` for very recent), `search_depth="advanced"`, `max_results=10`

**Subagent prompt template:**
```
Search Tavily for recent news about: {query}
Use tavily_search with search_depth="advanced", time_range="{day|week|month}", max_results=10.
Return the raw results — do not summarize.
```

### 3. Deep research and comprehensive analysis

**Triggers:** "research", "analyze", "compare X vs Y", "in-depth", "comprehensive report", "market analysis", "trends", "landscape", multi-part questions, "tell me everything about", "investigate"

**Launch in parallel:**
- `WebSearch` tool (direct call) — get broad surface results immediately
- `Agent` subagent calling `tavily_research` with `model="pro"` (or `auto` for moderate complexity) — this takes 30-120s but returns a deeply researched report

**Subagent prompt template:**
```
Conduct deep research using Tavily on: {query}
Use tavily_research with model="{pro|auto}".
Include these angles in the research input: {key angles from user query}
Return the complete research report and all source URLs.
```

**When results arrive:** Merge WebSearch results (immediate) with the research report (when ready). Present the research report as the main answer, with WebSearch results as supplementary sources.

### 4. Site exploration and URL discovery

**Triggers:** "what pages are on X.com", "find the page about Y on site Z", "site structure", "map the site", "list all URLs", domain-focused queries where the user wants to know what's available

**Launch in parallel:**
- `WebSearch` tool (direct call) with `site:domain.com` in the query
- `Agent` subagent calling `tavily_map` on the target domain

**Subagent prompt template:**
```
Map the site structure of: {url}
Use tavily_map with url="{url}", max_depth=2, limit=100.
If the user is looking for something specific, use instructions="{what they're looking for}".
Return the full URL list, organized by section/path.
```

**Follow-up:** After map results arrive, offer to extract key pages using `tavily_extract`.

### 5. Bulk site content extraction

**Triggers:** "crawl", "get all docs from", "extract everything under /docs", "download all pages", "get all articles from", bulk extraction from a known site

**Launch in parallel:**
- `WebSearch` tool (direct call) — for context and alternative sources
- `Agent` subagent calling `tavily_crawl` on the target site

**Subagent prompt template:**
```
Crawl and extract content from: {url}
Use tavily_crawl with url="{url}", max_depth={1-3}, limit={50-200}, select_paths={path patterns if applicable}.
If the user wants specific content, use instructions="{what to focus on}".
Return all extracted content with source URLs. Preserve all details — do not truncate.
```

### 6. Specific URL content extraction

**Triggers:** User provides one or more URLs, "extract from", "get content from", "read this page", "pull text from"

**Launch in parallel:**
- `WebSearch` tool (direct call) — for context about the same topic
- `Agent` subagent calling `tavily_extract` on the provided URLs

**Subagent prompt template:**
```
Extract content from these URLs: {urls}
Use tavily_extract with urls={url_list}, extract_depth="{basic|advanced}".
Use advanced extraction for JavaScript-heavy sites.
Return the full extracted content with source URLs. Preserve all details.
```

### 7. General web search (default)

**Triggers:** Everything else — any query that doesn't clearly match the above categories

**Launch in parallel:**
- `WebSearch` tool (direct call) — broad web coverage
- `Agent` subagent calling `tavily_search` with `search_depth="advanced"`, `max_results=10`

**Subagent prompt template:**
```
Search Tavily for: {query}
Use tavily_search with search_depth="advanced", max_results=10.
If the query has multiple aspects, break it into sub-queries and search each separately.
Return the raw results — do not summarize.
```

## Merging and deduplication

When both WebSearch and Tavily results come back:

### Step 1: Collect all results
- Gather all URLs, titles, and snippets from WebSearch
- Gather all URLs, titles, content, and scores from Tavily subagent(s)
- Keep ALL unique URLs — don't discard just because there are many

### Step 2: Deduplicate by URL
- Normalize URLs (strip trailing slashes, www prefixes, tracking params like `?utm_*`)
- When the same URL appears in both sources, keep the Tavily version (it has richer content and relevance scores) but note that WebSearch also found it (adds credibility)
- When URLs differ but point to the same domain and have very similar titles (>80% title overlap), flag them as likely duplicates but keep both — let the user decide

### Step 3: Organize
- Group results by topic/subtopic when the query has multiple aspects
- Within each group, sort by relevance (use Tavily scores where available, otherwise position in results)
- Mark source provenance for each result: `[Tavily]`, `[WebSearch]`, or `[Both]`

### Step 4: Present
Use this structure:

```
## Search Results: {query}

**Sources:** X unique results (Y from both engines, Z from Tavily only, W from WebSearch only)

### {Topic/Subtopic 1}
- **[Title]**([URL]) `[source tag]`
  Snippet/description...
  (Tavily score: N/A, if available)

### {Topic/Subtopic 2}
...

### Additional results
(Results that don't fit the main topics but may be relevant)
```

**Critical rules for presentation:**
- NEVER discard results to save space — detail preservation is more important than brevity
- Always include source attribution for every result
- If Tavily returned content (not just snippets), include it under the result
- For research reports, present the full report body, not just a summary
- When results are still arriving from a subagent, show what you have and note "More results incoming..."

## Parallel execution pattern

The key to speed is running everything at once:

```
1. Classify intent (takes <1 second of thought)
2. Fire ALL calls simultaneously in a single turn:
   - WebSearch tool call
   - One or more Agent subagent calls for Tavily operations
3. Wait for all to complete
4. Merge and present
```

**Do NOT** run WebSearch first, look at results, then decide to run Tavily. Both engines have different strengths — run them together. The subagent pattern means even slow Tavily operations (research, crawl) don't block the main conversation.

## When NOT to use this skill

Only skip this skill when:
- The user's question is purely about code in the current repository (use Grep/Glob instead)
- The user is asking about a file on their local filesystem (use Read/Glob)
- The user is asking about a mathematical calculation with no external information needed
- The user explicitly says "don't search the web"

Even if you're 80% sure you know the answer, if the query could benefit from current or verified information, use this skill. It's better to confirm than to give outdated answers.

## Subagent configuration

For all Tavily subagents, use these settings:
- `subagent_type`: `"general-purpose"` (has access to all MCP tools including tavily-mcp)
- `description`: short description of the tavily operation (e.g., "Tavily search for {query}")
- `run_in_background`: `false` (we need the results to merge)

The subagent's job is to call the Tavily MCP tool and return raw results. It should NOT summarize or analyze — the main agent does the merging and presentation.

## Bundled references

详细的 Tavily MCP 工具参数文档存放在 `references/` 目录下。当需要了解某个工具的全部参数选项、搜索深度、使用技巧时，按需读取对应文件：

| 文件 | 对应 MCP 工具 | 用途 |
|------|--------------|------|
| `references/tavily-search.md` | `tavily_search` | Web 搜索参数参考 |
| `references/tavily-extract.md` | `tavily_extract` | 网页内容提取参数参考 |
| `references/tavily-crawl.md` | `tavily_crawl` | 网站批量抓取参数参考 |
| `references/tavily-map.md` | `tavily_map` | 网站 URL 发现参数参考 |
| `references/tavily-research.md` | `tavily_research` | 深度研究参数参考 |

These are not standalone skills — they exist only as reference documentation for this skill. Read them when you need parameter details beyond what's covered in the decision tree templates above.

## Tips

- **When in doubt, use intent #7 (general web search).** It's the safest fallback.
- **If the query mentions a specific domain**, consider site exploration (#4) or bulk extraction (#5) instead of general search.
- **If the user says "I need a report on..."**, that's deep research (#3), not general search.
- **Break complex queries into sub-queries** within the Tavily subagent for better coverage.
- **Tavily research takes 30-120 seconds** — show WebSearch results immediately and note that the deep research report is being prepared.
- **Crawl conservatively** — start with `max_depth=1`, `limit=50` and suggest scaling up if the user needs more.
