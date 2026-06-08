# Tavily Crawl — 参数参考

从网站抓取多个页面的内容。适合批量提取文档或参考资料。

## MCP 工具

`tavily_crawl`

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | string | (必填) | 抓取起始 URL |
| `max_depth` | integer | 1 | 抓取深度（1-5） |
| `max_breadth` | integer | 20 | 每页最多跟随的链接数 |
| `limit` | integer | 50 | 处理的总页面数上限 |
| `instructions` | string | — | 自然语言指引，描述需要关注的内容 |
| `select_paths` | array | — | 仅抓取匹配这些正则的 URL |
| `select_domains` | array | — | 仅抓取这些域名下的 URL |
| `allow_external` | boolean | true | 是否跟随外部链接 |
| `extract_depth` | string | `basic` | `basic` 或 `advanced`（JS 重页面用后者） |
| `format` | string | `markdown` | 输出格式：`markdown` 或 `text` |

## 两种抓取模式

**回答问题时**（结果喂给 LLM）：使用 `instructions` 聚焦相关内容，返回相关片段而非完整页面。

```
tavily_crawl(
  url="https://docs.example.com",
  instructions="API 认证设置"
)
```

**全面提取**（获取所有内容）：省略 `instructions` 获取完整页面内容，配合路径过滤。

```
tavily_crawl(
  url="https://docs.example.com",
  max_depth=2,
  select_paths=["/docs/.*"]
)
```

## 使用技巧

- **从保守开始** — `max_depth=1`，`limit=20` — 需要时再扩大
- **使用 `select_paths`** 聚焦实际需要的区域
- **先用 `tavily_map` 了解网站结构**再决定抓取范围
- **务必设置 `limit`** 防止意外的超大抓取
