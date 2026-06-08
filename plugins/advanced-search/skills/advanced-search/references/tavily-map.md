# Tavily Map — 参数参考

发现网站上的 URL 列表，不提取内容。比抓取更快，适合需要了解有哪些页面的场景。

## MCP 工具

`tavily_map`

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | string | (必填) | 起始 URL |
| `max_depth` | integer | 1 | 发现深度（1-5） |
| `max_breadth` | integer | 20 | 每页最多跟随的链接数 |
| `limit` | integer | 50 | 最多发现的 URL 数 |
| `instructions` | string | — | 自然语言指引，描述优先发现哪些 URL |
| `select_paths` | array | — | 仅返回匹配这些正则的 URL |
| `select_domains` | array | — | 仅返回这些域名下的 URL |
| `allow_external` | boolean | true | 是否包含外部链接 |

## Map + Extract 组合模式

先用 `tavily_map` 找到正确的页面，再用 `tavily_extract` 获取内容。通常比直接抓取整个网站更高效：

1. **Map**：`tavily_map(url="https://docs.example.com", instructions="认证")` — 发现相关 URL
2. **Extract**：`tavily_extract(urls=["https://docs.example.com/api/authentication"])` — 提取内容

## 使用技巧

- **Map 只发现 URL** — 不提取内容。需要内容时用 `tavily_extract` 或 `tavily_crawl`
- **Map + Extract 比 Crawl 更优**当只需要网站上少数几个特定页面时
- **使用 `instructions`** 进行语义过滤，当路径模式不够用时
- **从浅层开始** — `max_depth=1` 对大多数网站足够了
