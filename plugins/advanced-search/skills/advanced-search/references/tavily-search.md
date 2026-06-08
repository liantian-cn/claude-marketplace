# Tavily Search — 参数参考

Web 搜索，返回 AI 优化的结果（含内容摘要和相关性评分）。

## MCP 工具

`tavily_search`

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | string | (必填) | 搜索查询，保持简洁（400 字符以内） |
| `max_results` | integer | 5 | 返回结果数（0-20） |
| `search_depth` | string | `basic` | 搜索深度 |
| `topic` | string | `general` | 固定为 `general` |
| `time_range` | string | — | 时间范围：`day`、`week`、`month`、`year` |
| `start_date` | string | — | 起始日期（YYYY-MM-DD） |
| `end_date` | string | — | 截止日期（YYYY-MM-DD） |
| `include_domains` | array | — | 限定域名，如 `["sec.gov", "reuters.com"]` |
| `exclude_domains` | array | — | 排除域名 |
| `country` | string | — | 国家偏向（全称，如 "United States"） |
| `include_raw_content` | boolean | false | 是否包含完整页面内容 |
| `include_images` | boolean | false | 是否包含图片结果 |
| `include_image_descriptions` | boolean | false | 是否包含图片的 AI 描述 |

## 搜索深度

| 深度 | 速度 | 相关性 | 适用场景 |
|------|------|--------|----------|
| `ultra-fast` | 最快 | 较低 | 快速查询、实时对话 |
| `fast` | 快 | 较好 | 需要速度也需要一定相关性 |
| `basic` | 中 | 高 | 通用搜索（默认） |
| `advanced` | 较慢 | 最高 | 精确查询、需要彻底搜索 |

## 使用技巧

- **保持查询简洁** — 使用搜索关键词而非完整句子
- **将复杂问题拆分为子查询** — 分别搜索每个方面以获得更好覆盖
- **需要完整页面内容时使用 `include_raw_content`** — 省去单独的 extract 调用
- **使用 `include_domains`** 聚焦可信或特定来源
- **需要最新信息时使用 `time_range`** — 尤其是新闻、事件
- **复杂或精确问题时使用 `search_depth=advanced`**
