---
name: advanced-search
description: |
  The primary and default way to search the web, find information, or research any topic. Use this skill for ALL web searches, information lookups, research tasks, news queries, and content discovery — even if the user doesn't explicitly ask for a "search." This includes: searching the web, finding articles, looking up facts, getting current information, checking news, researching topics, comparing products/companies/technologies, gathering sources, exploring websites, extracting web content, reading URLs, crawling documentation, and any task where current or external information would help. This skill orchestrates SIX search engines simultaneously — built-in WebSearch, Tavily API, Bailian Web Search, Bocha Web Search, Baidu Web Search, AND Sogou WeChat Search — deduplicates results, and routes complex tasks (deep research, site crawling, URL discovery) to specialized subagents. NEVER use raw WebSearch, individual tavily-* tools, bailian_web_search, bocha_web_search, baidu_web_search, or python search_wechat.py directly — always go through this skill for any web-facing information retrieval.
---

# Advanced Search

Combines six search engines in parallel — built-in WebSearch (broad coverage), Tavily (AI-optimized, English-focused), Bailian Web Search (Chinese internet ecosystem), Bocha Web Search (semantic understanding, rich metadata), Baidu Web Search (Chinese domestic content, 50 free queries/day), and Sogou WeChat Search (微信公众号 articles, unique Chinese long-form content) — to give you the best of all worlds: breadth + depth + language coverage + semantic precision + WeChat ecosystem access. Every search runs through ALL SIX engines simultaneously, results are deduplicated and merged, and complex operations are dispatched to subagents so you get comprehensive answers without waiting.

## Engine overview

| Engine | Strength | Best for |
|--------|----------|----------|
| **WebSearch** | Broad global coverage | General queries, quick lookups |
| **Tavily** | AI-optimized, rich metadata, content extraction | Deep research, English content, structured data |
| **Bailian** | Chinese internet ecosystem (百度/CSDN/知乎等) | Chinese-language queries, China-market topics |
| **Bocha** | Semantic understanding, freshness filter, rich metadata | Ambiguous queries, time-sensitive searches, Chinese content with dates |
| **Baidu** | Chinese domestic content (百家号/百度百科), 50 free/day | Non-technical Chinese info, social/news/entertainment queries |
| **WeChat** | 微信公众号 articles, unique Chinese long-form content | Chinese in-depth analysis, industry insights, policy interpretation |

## Graceful degradation

All six engines are attempted on every search. If any engine is unavailable (API key not configured, auth error, service down, tool not found, script fails), the search continues with the remaining engines. This rule applies to ALL engines equally.

**Degradation rules:**
- **6 engines available** → Full coverage: breadth + depth + Chinese (triple-source) + semantic + WeChat ecosystem
- **5 engines available** → Reduced but still comprehensive — missing one dimension (e.g., no WeChat = no WeChat ecosystem content)
- **4 engines available** → Still strong — dual Chinese coverage may drop to single source
- **3 engines available** → Limited — merge what you can, note which engines are missing
- **2 engines available** → More limited — significant coverage gaps
- **1 engine available** → Minimal but functional — use what's left, clearly note the limitation
- **0 engines available** → **严格告知用户：** "无任何可靠信息来源，无法完成搜索。请检查网络连接、API Key 配置（TAVILY_API_KEY、DASHSCOPE_API_KEY、BOCHA_API_KEY、BAIDU_API_KEY）以及 MCP 服务状态。"

**How to detect unavailability:**
- If a subagent returns an error about authentication, API key, tool not found, or service unavailable → that engine is unavailable for this session
- If a direct tool call (WebSearch) fails → that engine is unavailable
- If the WeChat Bash command returns a non-zero exit code or JSON with `"total": 0, "error": "..."` → WeChat is unavailable for this query (anti-crawl or network issue); retry on next search
- Note which engines failed and continue with the rest
- If ALL engines fail → follow the 0-engine rule above

**Note on WeChat availability:** WeChat search uses web scraping without an API key — it can fail due to Sogou anti-crawling measures, network issues, or page structure changes. This is expected and normal. When WeChat fails, the other five engines still provide comprehensive coverage. Never wait for WeChat or retry it more than once per search.

**Note on Bocha pricing:** Bocha is a paid/premium search service. If the user hasn't configured `BOCHA_API_KEY`, the Bocha subagent will fail — this is expected. The other four engines (WebSearch, Tavily, Bailian, Baidu) will still provide comprehensive coverage.

**Note on Baidu free tier:** Baidu Web Search provides 50 free queries per day. To stay within this limit, use conservative `count` values (5 for quick lookups, 10 for general search). The skill automatically limits Baidu usage to stay under this threshold. For high-volume workloads, consider prioritizing other engines.

## Core principle

**Every web information need goes through this skill.** Don't reach for WebSearch, individual tavily-* tools, bailian_web_search, bocha_web_search, baidu_web_search, or the wechat search script — this skill orchestrates them better than you can manually, because it:
- Runs all six engines simultaneously (no serial waiting)
- Picks the right Tavily tool for the intent (not just `tavily_search`)
- Adds Bailian for Chinese-language coverage that other engines may miss
- Adds Bocha for semantic understanding and freshness-filtered results with publication dates
- Adds Baidu for Chinese domestic content (百家号/百度百科) with 50 free queries/day
- Adds WeChat for 微信公众号 articles — unique Chinese long-form content no other engine can reach
- Deduplicates across sources without losing detail
- Offloads heavy work to subagents so you stay responsive
- Gracefully degrades when engines are unavailable

## Decision tree: which tools to use

Read the user's query and classify the intent. Then launch the appropriate combination:

### 1. Quick lookup (simple facts, definitions, short answers)

**Triggers:** "what is X", "who is Y", "when did Z", "define", "how tall/long/many", single-fact questions

**Launch in parallel:**
- `WebSearch` tool (direct call) — fast, broad coverage
- `Agent` subagent calling `tavily_search` with `search_depth="fast"` and `max_results=5`
- `Agent` subagent calling `bailian_web_search` with `count=5`
- `Agent` subagent calling `bocha_web_search` with `count=10`
- `Agent` subagent calling `baidu_web_search` with `count=5`
- `Bash` command: `python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{query}" -n 5` — WeChat public account articles (Chinese)

**Subagent prompt templates:**
```
# Tavily subagent
Search Tavily for: {query}
Use tavily_search with search_depth="fast", max_results=5.
Return the raw results — do not summarize.

# Bailian subagent
Search Bailian for: {query}
Use bailian_web_search with count=5.
Return the raw results — do not summarize.

# Bocha subagent
Search Bocha for: {query}
Use bocha_web_search with count=10.
When constructing the query, extract core search terms from the user's question, preserving time range descriptions like "recently", "this year", "January this year". Set freshness based on the user's described time context (default "noLimit" — Bocha will auto-rewrite the best freshness value based on the query).
Return the raw results — do not summarize.

# Baidu subagent
Search Baidu for: {query}
Use baidu_web_search with count=5.
Search with Chinese keywords — Baidu excels at Chinese domestic content (百家号, 百度百科, 搜狐, etc.).
Return the raw results — do not summarize.

# WeChat command
If the user's query is NOT in Chinese, translate it to Chinese keywords first.
Run: python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{Chinese query}" -n 5
Read the JSON from stdout. Parse the "articles" array — each article has title, url, summary, source (公众号名称), published_at.
Return the raw results — do not summarize.
```

### 2. News and recent events

**Triggers:** "latest", "news", "today", "this week", "recent", "just happened", "breaking", "announced", any time-sensitive query

**Launch in parallel:**
- `WebSearch` tool (direct call)
- `Agent` subagent calling `tavily_search` with `time_range="week"` (or `day` for very recent), `search_depth="advanced"`, `max_results=10`
- `Agent` subagent calling `bailian_web_search` with `count=10` (Bailian has no time_range filter — the subagent should append "最新" or "2026" to the query for recency)
- `Agent` subagent calling `bocha_web_search` with `count=10`, `freshness="{oneWeek|oneDay|oneMonth}"`
- `Agent` subagent calling `baidu_web_search` with `count=10`, `freshness="{pd|pw|pm}"`
- `Bash` command: `python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{query}" -n 10` — WeChat articles for recent Chinese news

**Subagent prompt templates:**
```
# Tavily subagent
Search Tavily for recent news about: {query}
Use tavily_search with search_depth="advanced", time_range="{day|week|month}", max_results=10.
Return the raw results — do not summarize.

# Bailian subagent
Search Bailian for recent news about: {query}
Use bailian_web_search with count=10.
If the query is time-sensitive, append the current year or "最新" to the search query to bias for recency (Bailian does not have a built-in time_range filter).
Return the raw results — do not summarize.

# Bocha subagent
Search Bocha for recent news about: {query}
Use bocha_web_search with count=10, freshness="{oneWeek|oneDay|oneMonth}".
Choose the freshness value matching the user's time context — "oneDay" for today's news, "oneWeek" for this week, "oneMonth" for this month.
When constructing the query, extract core search terms preserving time context like "latest" or "just announced".
Return the raw results — do not summarize.

# Baidu subagent
Search Baidu for recent news about: {query}
Use baidu_web_search with count=10, freshness="{pd|pw|pm}".
Choose the freshness value matching the user's time context — "pd" (past day) for today's news, "pw" (past week) for this week, "pm" (past month) for this month.
Baidu's freshness filter works well for Chinese domestic news (百家号, 搜狐新闻, etc.).
Return the raw results — do not summarize.

# WeChat command
If the user's query is NOT in Chinese, translate it to Chinese keywords first. Append "最新" to the query for recency (WeChat has no freshness filter — compensate with query crafting).
Run: python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{Chinese query + 最新}" -n 10
Read the JSON from stdout. Parse the "articles" array.
Return the raw results — do not summarize.
```

### 3. Deep research and comprehensive analysis

**Triggers:** "research", "analyze", "compare X vs Y", "in-depth", "comprehensive report", "market analysis", "trends", "landscape", multi-part questions, "tell me everything about", "investigate"

**Launch in parallel:**
- `WebSearch` tool (direct call) — get broad surface results immediately
- `Agent` subagent calling `tavily_research` with `model="pro"` (or `auto` for moderate complexity) — this takes 30-120s but returns a deeply researched report
- `Agent` subagent calling `bailian_web_search` with `count=10` — captures Chinese-language perspectives and China-market angles
- `Agent` subagent calling `bocha_web_search` with `count=10` — semantic search for nuanced angles the other engines might miss
- `Agent` subagent calling `baidu_web_search` with `count=10` — Chinese domestic content and Baidu ecosystem perspectives
- `Bash` command: `python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{query}" -n 10` — WeChat in-depth long-form articles (Chinese)

**Subagent prompt templates:**
```
# Tavily subagent
Conduct deep research using Tavily on: {query}
Use tavily_research with model="{pro|auto}".
Include these angles in the research input: {key angles from user query}
Return the complete research report and all source URLs.

# Bailian subagent
Search Bailian for: {query}
Use bailian_web_search with count=10.
Search for Chinese-language perspectives by breaking the topic into 2-3 Chinese sub-queries. For example, if the topic is "AI regulation", also search for "AI监管政策" and "人工智能法规".
Return the raw results — do not summarize.

# Bocha subagent
Search Bocha for multiple angles on: {query}
Use bocha_web_search with count=10.
Break the topic into 2-3 distinct search queries to capture different angles and perspectives. Use semantic variations of the key terms — Bocha's semantic understanding will surface results that keyword matching might miss.
Return the raw results — do not summarize.

# Baidu subagent
Search Baidu for: {query}
Use baidu_web_search with count=10.
Search with Chinese keywords — Baidu excels at Chinese domestic content. For China-market topics, Baidu's coverage of 百家号 and 百度百科 is often complementary to Bailian's coverage.
Return the raw results — do not summarize.

# WeChat command
Translate the user's query into Chinese keywords if not already in Chinese. Break the topic into 2-3 Chinese sub-queries for broader coverage (e.g., the main topic + "深度分析" + "行业趋势").
Run: python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{Chinese query}" -n 10
Run multiple times with different sub-queries if the topic has multiple angles.
Read the JSON from stdout. Parse the "articles" array.
Return the raw results — do not summarize.
```

**When results arrive:** Show WebSearch, Bailian, Bocha, Baidu, and WeChat results immediately. The Tavily research report takes 30-120s — note "Deep research report being prepared..." while waiting. Merge all results when the report arrives. Bocha results often surface unique sources due to its semantic matching. Baidu results complement Bailian for Chinese domestic content coverage. WeChat results provide unique Chinese long-form perspectives from public account articles.

### 4. Site exploration and URL discovery

**Triggers:** "what pages are on X.com", "find the page about Y on site Z", "site structure", "map the site", "list all URLs", domain-focused queries where the user wants to know what's available

**Launch in parallel:**
- `WebSearch` tool (direct call) with `site:domain.com` in the query
- `Agent` subagent calling `tavily_map` on the target domain
- `Agent` subagent calling `bailian_web_search` using `site:{domain}` query — covers Chinese-hosted or China-accessible pages
- `Agent` subagent calling `bocha_web_search` with query="{domain} {topic}" — semantic exploration of the domain
- `Agent` subagent calling `baidu_web_search` with query="{domain} {topic}" — Chinese search perspective on the domain
- `Bash` command: `python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{domain/topic}" -n 5` — WeChat articles discussing the domain

**Subagent prompt templates:**
```
# Tavily subagent
Map the site structure of: {url}
Use tavily_map with url="{url}", max_depth=2, limit=100.
If the user is looking for something specific, use instructions="{what they're looking for}".
Return the full URL list, organized by section/path.

# Bailian subagent
Search Bailian for pages on: {domain}
Use bailian_web_search with query="site:{domain} {topic if applicable}", count=10.
Return the raw results — do not summarize.

# Bocha subagent
Search Bocha for pages on: {domain}
Use bocha_web_search with query="{domain} {topic if applicable}", count=10.
Bocha's semantic search may find relevant pages on the domain that keyword-based engines miss.
Return the raw results — do not summarize.

# Baidu subagent
Search Baidu for pages on: {domain}
Use baidu_web_search with query="{domain} {topic if applicable}", count=10.
Baidu may surface Chinese-hosted pages or Chinese-language discussions about the domain.
Return the raw results — do not summarize.

# WeChat command
Search WeChat for articles mentioning or discussing {domain}.
Run: python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{domain name} {topic if applicable}" -n 5
WeChat articles may contain discussions, reviews, or references to the site.
Return the raw results — do not summarize.
```

**Follow-up:** After map results arrive, offer to extract key pages using `tavily_extract`.

### 5. Bulk site content extraction

**Triggers:** "crawl", "get all docs from", "extract everything under /docs", "download all pages", "get all articles from", bulk extraction from a known site

**Launch in parallel:**
- `WebSearch` tool (direct call) — for context and alternative sources
- `Agent` subagent calling `tavily_crawl` on the target site
- `Agent` subagent calling `bailian_web_search` with `site:{domain}` — surface check for additional content
- `Agent` subagent calling `bocha_web_search` with query="{domain}" — surface scan for additional discovery
- `Agent` subagent calling `baidu_web_search` with query="{domain}" — Chinese search surface scan
- `Bash` command: `python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{domain/topic}" -n 5` — WeChat articles related to the domain

**Subagent prompt templates:**
```
# Tavily subagent
Crawl and extract content from: {url}
Use tavily_crawl with url="{url}", max_depth={1-3}, limit={50-200}, select_paths={path patterns if applicable}.
If the user wants specific content, use instructions="{what to focus on}".
Return all extracted content with source URLs. Preserve all details — do not truncate.

# Bailian subagent
Search Bailian for content on: {domain}
Use bailian_web_search with query="site:{domain}", count=10.
This provides a quick surface scan of what Bailian can find on the site.
Return the raw results — do not summarize.

# Bocha subagent
Search Bocha for content on: {domain}
Use bocha_web_search with query="{domain}", count=10.
Bocha may discover pages on the domain through semantic matching that pure keyword/site: queries miss.
Return the raw results — do not summarize.

# Baidu subagent
Search Baidu for content on: {domain}
Use baidu_web_search with query="{domain}", count=10.
Baidu may find Chinese-hosted content or discussions about the domain.
Return the raw results — do not summarize.

# WeChat command
Search WeChat for articles discussing {domain} or its content topics.
Run: python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{domain name or key topic}" -n 5
WeChat may surface Chinese-language analysis, reviews, or discussions about the site's content.
Return the raw results — do not summarize.
```

### 6. Specific URL content extraction

**Triggers:** User provides one or more URLs, "extract from", "get content from", "read this page", "pull text from"

**Launch in parallel:**
- `WebSearch` tool (direct call) — for context about the same topic
- `Agent` subagent calling `tavily_extract` on the provided URLs
- `Agent` subagent calling `bailian_web_search` — search for the same domain/page to find related Chinese-language discussion
- `Agent` subagent calling `bocha_web_search` — semantic search for related discussion of the same content
- `Agent` subagent calling `baidu_web_search` — Chinese domestic discussion about the same content
- `Bash` command: `python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{page topic}" -n 5` — WeChat articles about the same topic

**Subagent prompt templates:**
```
# Tavily subagent
Extract content from these URLs: {urls}
Use tavily_extract with urls={url_list}, extract_depth="{basic|advanced}".
Use advanced extraction for JavaScript-heavy sites.
Return the full extracted content with source URLs. Preserve all details.

# Bailian subagent
Search Bailian for related content about: {domain/topic from the URLs}
Use bailian_web_search with query="{page title or domain}", count=5.
Look for Chinese-language discussions or coverage of the same content.
Return the raw results — do not summarize.

# Bocha subagent
Search Bocha for related content about: {domain/topic from the URLs}
Use bocha_web_search with query="{page title or domain}", count=5.
Use semantic variations to find discussions and coverage of the same content.
Return the raw results — do not summarize.

# Baidu subagent
Search Baidu for related content about: {domain/topic from the URLs}
Use baidu_web_search with query="{page title or domain}", count=5.
Search for Chinese-language discussions or coverage of the same content.
Return the raw results — do not summarize.

# WeChat command
Search WeChat for articles discussing the same topic as the extracted URLs.
Run: python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{page title or key topic in Chinese}" -n 5
WeChat may provide Chinese-language analysis or commentary on the same content.
Return the raw results — do not summarize.
```

### 7. General web search (default)

**Triggers:** Everything else — any query that doesn't clearly match the above categories

**Launch in parallel:**
- `WebSearch` tool (direct call) — broad web coverage
- `Agent` subagent calling `tavily_search` with `search_depth="advanced"`, `max_results=10`
- `Agent` subagent calling `bailian_web_search` with `count=10` — Chinese internet coverage
- `Agent` subagent calling `bocha_web_search` with `count=10` — semantic search with freshness awareness
- `Agent` subagent calling `baidu_web_search` with `count=10` — Chinese domestic content
- `Bash` command: `python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{query}" -n 10` — WeChat public account articles (Chinese)

**Subagent prompt templates:**
```
# Tavily subagent
Search Tavily for: {query}
Use tavily_search with search_depth="advanced", max_results=10.
If the query has multiple aspects, break it into sub-queries and search each separately.
Return the raw results — do not summarize.

# Bailian subagent
Search Bailian for: {query}
Use bailian_web_search with count=10.
Also search for a Chinese translation of the key terms to capture Chinese-language results.
Return the raw results — do not summarize.

# Bocha subagent
Search Bocha for: {query}
Use bocha_web_search with count=10.
When constructing the query, extract core search terms from the user's question, preserving time range descriptions like "recently", "this year". Set freshness based on the user's described time context (default "noLimit").
Bocha's semantic understanding may surface relevant results that keyword-based engines miss — this is its key strength.
Return the raw results — do not summarize.

# Baidu subagent
Search Baidu for: {query}
Use baidu_web_search with count=10.
Search with Chinese keywords — Baidu excels at Chinese domestic content (百家号, 百度百科, CSDN, 知乎, 搜狐, etc.). Use `count=5` for simple queries to conserve the daily 50-query free limit.
Return the raw results — do not summarize.

# WeChat command
If the user's query is NOT in Chinese, translate it to Chinese keywords first (WeChat content is almost entirely Chinese).
Run: python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{Chinese query}" -n 10
Read the JSON from stdout. Parse the "articles" array — each article has title, url, summary, source (公众号名称), published_at.
If the query has multiple aspects, run multiple WeChat searches with different Chinese sub-queries for broader coverage.
Return the raw results — do not summarize.
```

## Merging and deduplication

When results from all five engines come back:

### Step 1: Collect all results
- Gather all URLs, titles, and snippets from WebSearch
- Gather all URLs, titles, content, and scores from Tavily subagent(s)
- Gather all URLs, titles, and snippets from Bailian subagent
- Gather all URLs, titles, snippets, site names, and publication dates from Bocha subagent
- Gather all URLs, titles, and snippets from Baidu subagent
- Gather all articles (title, url, summary, source, published_at) from WeChat stdout JSON
- Keep ALL unique URLs — don't discard just because there are many

### Step 2: Deduplicate by URL
- Normalize URLs (strip trailing slashes, www prefixes, tracking params like `?utm_*`)
- WeChat URLs are always unique (搜狗中间链接) — they won't match any other engine's URLs. Do NOT deduplicate WeChat articles against other engines by URL; instead, check title similarity for cross-engine dedup (see below)
- When the same URL appears in multiple engines, keep the richest version:
  - Tavily version preferred (has content + relevance scores)
  - Bocha version next (has publication dates + site names)
  - WeChat version next (has source/publication time — unique to WeChat ecosystem)
  - Bailian/Baidu/WebSearch versions fallback (snippets only)
  - Mark source provenance to show which engines found each result
- When URLs differ but point to the same domain and have very similar titles (>80% title overlap), flag them as likely duplicates but keep both — let the user decide

### Step 3: Organize
- Group results by topic/subtopic when the query has multiple aspects
- Within each group, sort by relevance (use Tavily scores where available, otherwise position in results)
- Bailian and Baidu results for Chinese queries often surface unique sources not found by other engines — highlight these, especially when they complement each other (Bailian favors tech/dev content, Baidu favors general/social content)
- WeChat results are uniquely valuable for Chinese-language queries — they provide long-form public account articles no other engine can reach. Always highlight WeChat results prominently; they often contain the deepest Chinese-language analysis
- Bocha results often include publication dates — use these to identify the most current information
- Mark source provenance for each result: `[Tavily]`, `[WebSearch]`, `[Bailian]`, `[Bocha]`, `[Baidu]`, `[WeChat]`, or combined tags like `[Tavily+Bocha]`, `[Bailian+Baidu]`, `[All 6]`

### Step 4: Present
Use this structure:

```
## Search Results: {query}

**Sources:** X unique results (A from all six, B from Tavily only, C from WebSearch only, D from Bailian only, E from Bocha only, F from Baidu only, G from WeChat only, ...)
**Engines available:** {which engines contributed — note any that were unavailable}

### {Topic/Subtopic 1}
- **[Title]**([URL]) `[source tags]`
  Snippet/description...
  (Published: {date}, if available from Bocha or WeChat)
  (Source: {公众号名称}, if from WeChat)
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
- If Bocha returned publication dates, include them — they help users assess recency
- If WeChat returned articles, include the 公众号名称 (source) and published_at — these are unique metadata other engines don't provide
- Bailian-only, Bocha-only, Baidu-only, and WeChat-only results are particularly valuable — call them out. Bailian and Baidu often cover different Chinese source ecosystems; WeChat covers the unique 微信公众号 ecosystem
- For research reports, present the full report body, not just a summary
- When results are still arriving from a subagent, show what you have and note which engines are still pending
- **Always note which engines were unavailable** if any failed — this is critical for transparency

## Parallel execution pattern

The key to speed is running everything at once:

```
1. Classify intent (takes <1 second of thought)
2. Fire ALL calls simultaneously in a single turn:
   - WebSearch tool call (direct)
   - One or more Agent subagent calls for Tavily operations
   - One Agent subagent call for Bailian search
   - One Agent subagent call for Bocha search
   - One Agent subagent call for Baidu search
   - One Bash command for WeChat search (direct, not subagent)
3. Wait for all to complete
4. Note any engine failures
5. Merge and present
```

**Do NOT** run engines sequentially. All six engines have complementary strengths — run them together. The subagent pattern means even slow Tavily operations (research, crawl) don't block the main conversation. Bailian, Bocha, Baidu, WeChat, and WebSearch typically return first, giving immediate results while Tavily deep research continues. WeChat runs as a direct Bash command (no subagent overhead) and typically returns in 2-5 seconds.

## When NOT to use this skill

Only skip this skill when:
- The user's question is purely about code in the current repository (use Grep/Glob instead)
- The user is asking about a file on their local filesystem (use Read/Glob)
- The user is asking about a mathematical calculation with no external information needed
- The user explicitly says "don't search the web"

Even if you're 80% sure you know the answer, if the query could benefit from current or verified information, use this skill. It's better to confirm than to give outdated answers.

## Subagent configuration

### Tavily subagents
For all Tavily subagents, use these settings:
- `subagent_type`: `"general-purpose"` (has access to all MCP tools including tavily-mcp)
- `description`: short description of the tavily operation (e.g., "Tavily search for {query}")
- `run_in_background`: `false` (we need the results to merge)

### Bailian subagent
For the Bailian subagent, use these settings:
- `subagent_type`: `"general-purpose"` (has access to all MCP tools including bailian_web_search)
- `description`: short description (e.g., "Bailian search for {query}")
- `run_in_background`: `false` (we need the results to merge)

### Bocha subagent
For the Bocha subagent, use these settings:
- `subagent_type`: `"general-purpose"` (has access to all MCP tools including bocha_web_search)
- `description`: short description (e.g., "Bocha search for {query}")
- `run_in_background`: `false` (we need the results to merge)

The subagent's only job is to call the MCP tool (`tavily_search`, `tavily_research`, `tavily_map`, `tavily_crawl`, `tavily_extract`, `bailian_web_search`, or `bocha_web_search`) and return raw results. It should NOT summarize or analyze — the main agent does the merging and presentation.

### Bocha subagent parameter extraction

When the Bocha subagent calls `bocha_web_search`, it should determine parameters as follows:

1. **`query`**: Extract core search terms from the user's question. Preserve time range descriptions like "recently", "this year", "January this year", "latest" in the query — Bocha uses these to refine results.
2. **`freshness`**: Determine based on the user's described time range. Default to `"noLimit"` — Bocha will combine this with the `query` time descriptions to auto-select the best freshness value. Use explicit values when the user clearly specifies a time range:
   - "today" / "just now" / "past day" → `"oneDay"`
   - "this week" / "past few days" → `"oneWeek"`
   - "this month" / "recently" → `"oneMonth"`
   - "this year" → `"oneYear"`
3. **`count`**: Default `10`. Increase to `20` or more only if the user explicitly requests more results.

Note: `bocha_web_search` does NOT have a `summary` parameter. All results include full metadata (title, URL, description, site name, site icon, publication date, image links) by default.

### Baidu subagent

For the Baidu subagent, use these settings:
- `subagent_type`: `"general-purpose"` (has access to all MCP tools including baidu_web_search)
- `description`: short description (e.g., "Baidu search for {query}")
- `run_in_background`: `false` (we need the results to merge)

The subagent's only job is to call `baidu_web_search` with `webSearch` and return raw results. It should NOT summarize or analyze — the main agent does the merging and presentation.

### Baidu subagent parameter extraction

When the Baidu subagent calls `baidu_web_search`'s `webSearch`, it should determine parameters as follows:

1. **`query`**: Use Chinese keywords whenever possible — Baidu's strength is Chinese domestic content. Even for English-origin queries, translate key terms to Chinese for better coverage.
2. **`freshness`**: Apply for time-sensitive queries. Baidu uses a different format from Bocha:
   - "today" / "just now" → `"pd"` (past day)
   - "this week" / "past few days" → `"pw"` (past week)
   - "this month" / "recently" → `"pm"` (past month)
   - "this year" → `"py"` (past year)
   - Specific date range → `"YYYY-MM-DDtoYYYY-MM-DD"` (e.g., `"2026-01-01to2026-06-08"`)
   - Default: omit the parameter for no time restriction
3. **`count`**: Default `5` for quick lookups, `10` for general/news search. Be conservative — Baidu has a 50 queries/day free limit. Use `count=5` whenever possible to stretch the daily quota.

### WeChat command (direct Bash)

WeChat search does NOT use a subagent — it is a direct Bash command. There is no MCP tool for WeChat; instead, run the local Python script:

```bash
python plugins/essentials/skills/advanced-search/scripts/search_wechat.py "{query}" -n {count}
```

The script outputs JSON to stdout. Parse `result["articles"]` for the article list. Each article has: `title`, `url`, `summary`, `source` (公众号名称), `published_at`.

**Key differences from other engines:**
- **No subagent** — run directly via Bash, not via Agent tool. The script is fast (2-5 seconds) and has no MCP dependency
- **No API key** — completely free, no configuration needed
- **Chinese-only** — WeChat content is almost entirely Chinese. Always translate English queries to Chinese before searching
- **Anti-crawling risk** — if the script returns `"total": 0` or an `"error"` field, WeChat is unavailable for this query. This is normal — continue with the other five engines
- **URL format** — WeChat URLs are 搜狗中间链接 (`weixin.sogou.com/link?...`), not `mp.weixin.qq.com` direct links. Users can still click through to read articles
- **No freshness/date filter** — WeChat search has no built-in time filter. Compensate by appending time words to the query (e.g., "最新", "2026")

**WeChat command parameter guidelines:**
- `query`: Chinese keywords only. Translate English queries. Use 2-4 core keywords for best results (not long natural language sentences)
- `-n`: Result count — `5` for quick lookups and site/URL exploration (intents #1, #4, #5, #6), `10` for news, deep research, and general search (intents #2, #3, #7)
- `-o`: Optional output file — not needed for normal use (stdout is sufficient)

**Daily quota management:** Baidu provides 50 free queries per day. To stay within this limit:
- Quick lookups (intent #1): `count=5`
- News/general search (intents #2, #7): `count=10`
- Deep research (intent #3): `count=10`
- Site exploration/extraction (intents #4, #5, #6): `count=5-10`
- If the user runs many searches in one session, reduce Baidu `count` to 5 across all intent types
- If the quota is exhausted, the Baidu subagent will fail — this is expected. The other four engines will still provide coverage.

## Bundled references

Detailed MCP tool parameter documentation is in the `references/` directory. Read the corresponding file when you need full parameter options, search depth guidance, or usage tips:

| 文件 | 对应 MCP 工具 | 用途 |
|------|--------------|------|
| `references/tavily-search.md` | `tavily_search` | Tavily Web 搜索参数参考 |
| `references/tavily-extract.md` | `tavily_extract` | Tavily 网页内容提取参数参考 |
| `references/tavily-crawl.md` | `tavily_crawl` | Tavily 网站批量抓取参数参考 |
| `references/tavily-map.md` | `tavily_map` | Tavily 网站 URL 发现参数参考 |
| `references/tavily-research.md` | `tavily_research` | Tavily 深度研究参数参考 |
| `references/bailian-search.md` | `bailian_web_search` | Bailian 百炼 Web 搜索参数参考 |
| `references/bocha-search.md` | `bocha_web_search` | Bocha 博查 Web 搜索参数参考 |
| `references/baidu-search.md` | `baidu_web_search` / `webSearch` | Baidu 百度 Web 搜索参数参考 |
| `references/wechat-search.md` | `search_wechat.py` (Bash) | 搜狗微信搜索参数参考 |

These are not standalone skills — they exist only as reference documentation for this skill. Read them when you need parameter details beyond what's covered in the decision tree templates above.

## Tips

- **When in doubt, use intent #7 (general web search).** It's the safest fallback.
- **If the query mentions a specific domain**, consider site exploration (#4) or bulk extraction (#5) instead of general search.
- **If the user says "I need a report on..."**, that's deep research (#3), not general search.
- **For Chinese-language queries**, Bailian, Bocha, Baidu, and WeChat fill critical gaps — WebSearch and Tavily have weaker Chinese coverage. Bailian (阿里生态), Baidu (百度生态), and WeChat (微信生态) cover three different Chinese source ecosystems — running all three gives the broadest Chinese coverage. WeChat is the ONLY engine that accesses 微信公众号 articles. Search with Chinese keywords even if the user asked in English.
- **For Chinese in-depth topics**, WeChat is invaluable — 微信公众号 hosts high-quality long-form analysis, industry reports, and policy interpretation not available on the open web. Always include WeChat for Chinese deep research, market analysis, and industry insight queries.
- **For time-sensitive queries**, Bocha's `freshness` filter and publication dates are unique advantages — use them. Baidu also has a `freshness` filter (`pd`/`pw`/`pm`/`py`). Bailian and WeChat have no time filter, so compensate with query crafting (append "最新" or year).
- **For ambiguous or fuzzy queries**, Bocha's semantic understanding often finds results that keyword-based engines miss.
- **Break complex queries into sub-queries** within the Tavily subagent for better coverage. For WeChat, run multiple searches with different Chinese sub-queries.
- **Tavily research takes 30-120 seconds** — show WebSearch, Bailian, Bocha, Baidu, and WeChat results immediately and note that the deep research report is being prepared.
- **Crawl conservatively** — start with `max_depth=1`, `limit=50` and suggest scaling up if the user needs more.
- **Bailian has no advanced filters** — no time_range, search_depth, or domain filters. Compensate by crafting better query strings (append year, use `site:` operator, use multiple sub-queries).
- **Baidu has 50 free queries/day** — use conservative `count` values (5 for quick lookups, 10 max for general search). Reduce `count` if doing many searches in one session. Prioritize Baidu for Chinese domestic/non-technical queries where it has unique coverage.
- **Bocha has freshness and returns publication dates** — use these to filter and prioritize recent content in the merged results.
- **WeChat has no API key but is vulnerable to anti-crawling** — if the script returns empty results or an error, mark WeChat as unavailable and continue. Never retry more than once per search. WeChat results may also be slightly slower (2-5 seconds) due to Cookie acquisition and page fetching.
- **WeChat is Chinese-only** — always translate English queries to Chinese before running the WeChat command. Use 2-4 core Chinese keywords for best matching.
- **Engine failures are normal** — Bocha requires a paid API key, Baidu has a 50/day free limit, WeChat can be blocked by anti-crawling, and any engine can be temporarily unavailable. Always note which engines contributed and which were unavailable. Never fail the entire search because one engine is down.
