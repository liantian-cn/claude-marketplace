# MCP 工具名 → 缓存文件名映射表

> **共享引用**: 所有 iFinD skill 均复用此映射表。
> **缓存目录**: `./金融数据缓存/` —— 按数据域分目录存储，每个查询结果以独立文件保存。

## 使用约定

1. 调用 MCP 工具前，先检查 `./金融数据缓存/[域]/[缓存文件名]` 是否存在且有效（日频数据看日期，实时数据跳过缓存）
2. 若缓存文件存在且有效 → 跳过 MCP 调用，直接读取
3. 若缓存未命中 → 调用 MCP 工具（或脚本兜底），将结果保存到对应缓存文件
4. 文件命名规则：`[序号]-[语义名称].md`，如 `01-智能选股.md`
5. 对于 MCP 暂未覆盖的工具（标记 ⚠️），使用脚本兜底：`call("server_type", "tool_name", params)`

## 一、hexin-ifind-ds-stock-mcp（A股股票，10 工具）

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__plugin_ifind_hexin-ifind-ds-stock-mcp__search_stocks` | `01-智能选股.md` | 自然语言条件选股 |
| `mcp__plugin_ifind_hexin-ifind-ds-stock-mcp__get_stock_summary` | `02-股票信息摘要.md` | 快速信息概览 |
| `mcp__plugin_ifind_hexin-ifind-ds-stock-mcp__get_stock_info` | `03-股票基本资料.md` | 基本信息、发行上市 |
| `mcp__plugin_ifind_hexin-ifind-ds-stock-mcp__get_stock_performance` | `04-行情与技术指标.md` | 日频行情、技术指标、技术形态 |
| `mcp__plugin_ifind_hexin-ifind-ds-stock-mcp__get_stock_financials` | `05-财务数据.md` | 财报、财务指标、估值 |
| `mcp__plugin_ifind_hexin-ifind-ds-stock-mcp__get_stock_shareholders` | `06-股本股东.md` | 股本结构、股东分布 |
| `mcp__plugin_ifind_hexin-ifind-ds-stock-mcp__get_risk_indicators` | `07-风险指标.md` | alpha、beta、波动率等 |
| `mcp__plugin_ifind_hexin-ifind-ds-stock-mcp__get_stock_events` | `08-重大事件.md` | IPO、增发、并购、股权激励等 |
| `mcp__plugin_ifind_hexin-ifind-ds-stock-mcp__get_esg_data` | `09-ESG评级.md` | ESG 评级与报告 |
| `mcp__plugin_ifind_hexin-ifind-ds-stock-mcp__stock_highfreq_quotes` | `10-高频行情.md` | 日内高频数据（不缓存） |

## 二、hexin-ifind-ds-fund-mcp（公募基金，7 工具）

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__plugin_ifind_hexin-ifind-ds-fund-mcp__get_fund_profile` | `11-基金基本资料.md` | 基金名称、代码、分类、费率 |
| `mcp__plugin_ifind_hexin-ifind-ds-fund-mcp__get_fund_market_performance` | `12-基金行情业绩.md` | 净值、收益率、排名、绩效评价 |
| `mcp__plugin_ifind_hexin-ifind-ds-fund-mcp__get_fund_ownership` | `13-基金份额持有人.md` | 份额变动、持有人结构 |
| `mcp__plugin_ifind_hexin-ifind-ds-fund-mcp__get_fund_portfolio` | `14-基金投资组合.md` | 资产配置、行业分布、持仓明细 |
| `mcp__plugin_ifind_hexin-ifind-ds-fund-mcp__get_fund_financials` | `15-基金财报.md` | 基金利润、资产、分红数据 |
| `mcp__plugin_ifind_hexin-ifind-ds-fund-mcp__get_fund_company_info` | `16-基金公司信息.md` | 基金公司、基金经理 |
| `mcp__plugin_ifind_hexin-ifind-ds-fund-mcp__fund_highfreq_quotes` | `17-基金高频行情.md` | 日内高频数据（不缓存） |

## 三、hexin-ifind-ds-edb-mcp（宏观经济与行业，1 工具）

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__plugin_ifind_hexin-ifind-ds-edb-mcp__get_edb_data` | `18-经济指标数据.md` | 宏观/行业经济指标 |

## 四、hexin-ifind-ds-news-mcp（新闻公告，2 工具）

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__plugin_ifind_hexin-ifind-ds-news-mcp__search_news` | `19-财经新闻.md` | 新闻资讯语义搜索 |
| `mcp__plugin_ifind_hexin-ifind-ds-news-mcp__search_notice` | `20-上市公司公告.md` | 公告全文语义搜索 |

## 五、hexin-ifind-ds-bond-mcp（债券市场，5 工具）

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__plugin_ifind_hexin-ifind-ds-bond-mcp__bond_basic_info` | `21-债券基本信息.md` | 债券及发行主体资料 |
| `mcp__plugin_ifind_hexin-ifind-ds-bond-mcp__bond_market_data` | `22-债券行情估值.md` | 行情、估值、久期、凸性 |
| `mcp__plugin_ifind_hexin-ifind-ds-bond-mcp__bond_financial_data` | `23-债券主体财务.md` | 发行体财务报表与指标 |
| `mcp__plugin_ifind_hexin-ifind-ds-bond-mcp__bond_special_data` | `24-债券特殊指标.md` | 信用评级、回购、可转债转股 |
| `mcp__plugin_ifind_hexin-ifind-ds-bond-mcp__bond_highfreq_quotes` | `25-债券高频行情.md` | 日内高频数据（不缓存） |

## 六、hexin-ifind-ds-global-stock-mcp（港美股，4 工具）

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__plugin_ifind_hexin-ifind-ds-global-stock-mcp__global_stock_profile` | `26-港美股基本资料.md` | 基本信息、上市公司资料 |
| `mcp__plugin_ifind_hexin-ifind-ds-global-stock-mcp__global_stock_quotes` | `27-港美股行情.md` | 日频行情、技术指标 |
| `mcp__plugin_ifind_hexin-ifind-ds-global-stock-mcp__global_stock_financial` | `28-港美股财务.md` | 财务数据、估值、盈利预测 |
| `mcp__plugin_ifind_hexin-ifind-ds-global-stock-mcp__global_stock_events` | `29-港美股事件.md` | IPO、回购、分红、ESG |

## 七、hexin-ifind-ds-index-mcp（指数板块，3 工具）

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__plugin_ifind_hexin-ifind-ds-index-mcp__index_data` | `30-指数数据.md` | 指数行情、估值、成分 |
| `mcp__plugin_ifind_hexin-ifind-ds-index-mcp__sector_data` | `31-板块数据.md` | 板块行情、成分股 |
| `mcp__plugin_ifind_hexin-ifind-ds-index-mcp__index_highfreq_quotes` | `32-指数高频行情.md` | 日内高频数据（不缓存） |

## ⚠️ MCP 暂未覆盖的工具（脚本兜底）

以下工具当前仅在脚本端（`call.py` / `call-node.js`）可用，MCP 中暂未暴露：

| 脚本调用 | 所属服务 | 替代方案 |
|---|---|---|
| `call("fund", "search_funds", {query})` | fund | 使用脚本直接调用，或通过 MCP `get_fund_profile` 间接检索 |
| `call("edb", "search_edb", {query})` | edb | 使用脚本直接调用，先搜索指标名再用 MCP `get_edb_data` 查询 |
| `call("news", "search_trending_news", {keyword, ...})` | news | 使用脚本直接调用 |
| `call("global_stock", "search_global_stocks", {query, market})` | global_stock | 使用脚本直接调用，或通过 MCP `global_stock_profile` 间接检索 |

> **降级策略**：当 `call()` 脚本也不可用时，尝试通过参数化 MCP 查询间接实现搜索功能——例如用 `get_stock_summary` 查询具体股票来替代模糊选股。
