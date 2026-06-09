# Bocha Web Search — 参数参考

Bocha (博查) 是博查 AI 提供的 Web 搜索 MCP 服务，具备语义理解能力，可搜索数十亿网页文档。通过 HTTP 传输，使用 `${BOCHA_API_KEY}` 认证。

## MCP 工具

`mcp__bocha-mcp__bocha_web_search`
→ 实际调用时使用工具名 `bocha_web_search`

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | string | (必填) | 搜索查询字符串。支持自然语言，Bocha 会进行语义理解 |
| `freshness` | string | `noLimit` | 时间范围过滤。可选值：`noLimit`、`oneYear`、`oneMonth`、`oneWeek`、`oneDay`，也支持具体日期 `YYYY-MM-DD` 或日期范围 `YYYY-MM-DD..YYYY-MM-DD` |
| `count` | integer | 10 | 返回结果数量，范围 1-50 |

**无 `summary` 参数。** 与用户可能期望的不同，该接口没有 `summary` 开关 — 所有结果默认返回标题、URL、摘要、站点名称、发布日期等完整字段。

## 响应结构

```json
{
  "pages": [
    {
      "title": "页面标题",
      "url": "完整 URL",
      "description": "页面摘要文本",
      "site_name": "来源站点名称（如 CSDN、github.com）",
      "site_icon": "网站 favicon URL",
      "published_date": "发布日期（ISO 8601 格式）",
      "image_links": ["页面内图片 URL 数组"]
    }
  ]
}
```

- `site_name` — 来源站点名称，比 Bailian 的 `hostname` 更精确
- `site_icon` — 提供 favicon URL，便于展示来源图标
- `published_date` — **关键优势**：Bocha 返回发布日期，而 Bailian 不返回此字段
- `image_links` — 页面内嵌图片链接，某些场景有用

## 特点与优势

| 维度 | 评价 |
|------|------|
| **语义理解** | ★★★★☆ — 具备语义搜索能力，对模糊查询的理解优于纯关键词匹配 |
| **中文内容覆盖** | ★★★★☆ — CSDN、腾讯云、知乎、博客园等中文来源覆盖良好 |
| **国际内容** | ★★★☆☆ — 可返回 GitHub、学术论文等国际来源，覆盖面中等 |
| **速度** | ★★★★☆ — 响应较快 |
| **结果丰富度** | ★★★★☆ — 返回标题、摘要、站点名、图标、发布日期、图片链接 |
| **高级过滤** | ★★★☆☆ — 支持 freshness 时间过滤，但不支持域名过滤、搜索深度控制 |
| **成本** | 💰💰💰 — 付费/高价服务，可能因用户未开通而不可用 |

**定位：** 作为四引擎搜索中的语义增强层，弥补 WebSearch（关键词匹配为主）和 Bailian（无时间过滤、无发布日期）的不足。当用户查询表达模糊或需要语义理解时，Bocha 的搜索结果质量通常优于纯关键词引擎。

## 与 bocha_ai_search 的区别

Bocha 提供两个搜索工具：

| 特性 | `bocha_web_search` | `bocha_ai_search` |
|------|-------------------|-------------------|
| 搜索方式 | 语义增强的 Web 搜索 | AI 深度语义搜索 |
| 结构化卡片 | 无 | 有（垂直领域结构化数据） |
| 适用场景 | 通用搜索、信息查找 | 需要结构化答案的场景 |
| 本技能使用 | ✅ 默认使用 | 暂不集成 |

本技能默认使用 `bocha_web_search`，因为它提供更通用的 Web 搜索结果，与 WebSearch、Tavily、Bailian 形成互补。

## 与其他引擎对比

| 维度 | Bocha | Tavily | Bailian | WebSearch |
|------|-------|--------|---------|-----------|
| 语义理解 | ★★★★ | ★★★★★ | ★★ | ★★ |
| 中文覆盖 | ★★★★ | ★★★ | ★★★★★ | ★★★ |
| 英文覆盖 | ★★★ | ★★★★★ | ★★ | ★★★★ |
| 时间过滤 | ✅ freshness | ✅ time_range | ❌ 不支持 | ❌ 不支持 |
| 发布日期 | ✅ 返回 | ✅ 返回 | ❌ 不返回 | ❌ 不返回 |
| 内容提取 | ❌ | ✅ extract/crawl | ❌ | ❌ |
| 域名过滤 | ❌ | ✅ include/exclude | ❌ | ❌ |
| 结果上限 | 50 | 20 | 无明确上限 | 不固定 |
| 成本 | 付费 | 有免费额度 | — | 内置 |

## 搜索技巧

- **中文查询优先** — Bocha 对中文查询的语义理解最好
- **利用 freshness 参数** — 这是 Bailian 没有的能力，时效性查询时优先使用
- **保留时间范围描述** — 在 query 中保留"最近"、"今年"等描述，Bocha 会结合 freshness 自动优化
- **count 可适当调大** — 默认 10 条，上限 50，复杂查询建议 `count=10-20`
- **英文查询可用** — 但覆盖面不如中文，英文查询建议更多依赖 Tavily

## 局限

- **付费服务** — 用户可能未开通 Bocha API Key，此时该引擎不可用
- **无内容提取能力** — 无法像 Tavily 那样获取页面正文
- **无域名过滤** — 不支持 include_domains/exclude_domains
- **无搜索深度控制** — 不像 Tavily 有 basic/advanced 深度选择
- **语义理解偶尔过度** — 对于高度歧义的简短查询，语义理解可能引入无关结果
- **无相关性评分** — 不像 Tavily 返回 relevance score
