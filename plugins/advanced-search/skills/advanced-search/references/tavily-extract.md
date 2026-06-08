# Tavily Extract — 参数参考

从单个或多个 URL 提取干净的、可读的内容。可处理 JavaScript 渲染的页面。

## MCP 工具

`tavily_extract`

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `urls` | array | (必填) | URL 列表（最多 20 个） |
| `extract_depth` | string | `basic` | `basic` 用于简单页面，`advanced` 用于 JS 渲染的 SPA 和动态内容 |
| `format` | string | `markdown` | 输出格式：`markdown` 或 `text` |
| `include_images` | boolean | false | 是否包含页面中的图片 URL |
| `query` | string | — | 按相关性重排序，优先提取与此查询相关的内容 |

## 提取深度

| 深度 | 适用场景 |
|------|----------|
| `basic` | 简单页面，速度快 — 先试这个 |
| `advanced` | JS 渲染的 SPA、动态内容、含表格的页面 |

## 使用技巧

- **每次最多 20 个 URL** — 更多则分批调用
- **先试 `basic`**，内容缺失或不完整时回退到 `advanced`
- **使用 `query`** 聚焦长页面中最相关的部分
- **如果搜索结果已包含完整内容**（通过 `tavily_search` 的 `include_raw_content`），可能无需单独提取
