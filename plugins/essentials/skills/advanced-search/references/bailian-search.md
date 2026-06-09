# Bailian Web Search — 参数参考

百炼 (Bailian) 是阿里云 DashScope 平台提供的 Web 搜索 MCP 服务。通过 HTTP 传输，使用 `${DASHSCOPE_API_KEY}` 认证。

## MCP 工具

`mcp__bailian_web_search__bailian_web_search`
→ 实际调用时使用工具名 `bailian_web_search`

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query` | string | (必填) | 搜索查询字符串 |
| `count` | integer | 5 | 返回结果数量 |

**无其他高级参数。** 不支持 `time_range`、`search_depth`、`include_domains` 等过滤 — 这是一个精简的基础搜索接口。

## 响应结构

```json
{
  "pages": [
    {
      "snippet": "页面摘要文本",
      "hostname": "来源站点名称（可能为\"无\"）",
      "hostlogo": "网站 favicon URL",
      "title": "页面标题",
      "url": "完整 URL"
    }
  ],
  "request_id": "唯一请求标识",
  "tools": [],
  "status": 0
}
```

- `hostname` 可能为空或显示"无"（部分国际站点和特殊页面）
- `hostlogo` 提供 favicon URL，便于在搜索结果中展示来源图标
- `tools` 字段当前始终为空数组

## 特点与优势

| 维度 | 评价 |
|------|------|
| **中文内容覆盖** | ★★★★★ — 百度百家号、CSDN、知乎、腾讯云等中文来源覆盖极好 |
| **国际内容** | ★★★☆☆ — 可返回 GitHub、python.org 等国际站点，但覆盖面不如中文 |
| **速度** | ★★★★★ — 轻量级接口，响应快 |
| **结果丰富度** | ★★★☆☆ — 仅返回 snippet + URL，无完整内容提取、无相关性评分 |
| **高级过滤** | ★☆☆☆☆ — 无 time_range、domain filter、search depth 等 |

**定位：** 作为中文互联网生态的补充搜索引擎，弥补 WebSearch（通用）和 Tavily（英文优化）在中文内容上的不足。

## 搜索技巧

- **中文查询优先** — 这个引擎对中文查询的返回质量最高
- **使用 `site:` 操作符** — 支持 `site:github.com keyword` 形式的域名限定搜索
- **适当增加 count** — 默认 5 条可能不够，复杂查询建议 `count=10`
- **英文查询可用但覆盖率低** — 英文查询建议更多依赖 Tavily 和 WebSearch

## 局限

- 无内容提取能力（无法像 Tavily 那样获取页面正文）
- 无时间范围过滤（无法限定"最近一周"等）
- 无法限定/排除特定域名（不支持 include_domains/exclude_domains）
- 响应结构简单，无相关性评分
- hostname 字段有时为空，来源识别不够精确
