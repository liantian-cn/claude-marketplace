---
name: 贷后风险定期监控
description: 对存量借款客户持续风险监控，本期扫描×历史对比×异动归因，识别经营恶化、司法新增、财务退化等负面信号。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers:
  - qcc-company
  - qcc-risk
  - qcc-executive
tags:
  - 贷后管理
  - 风险监控
  - 增量风险
  - 异动归因
  - 财务退化
  - 预警
model: deepseek-v4-pro
---

> **⚠️ 环境依赖提醒**：如遇到 Python/pandoc/markitdown 未安装或命令找不到等电脑环境问题，请访问 "企业信息检索基本环境配置" skill 完成环境配置。

# 贷后风险定期监控
## SKILL 定位
服务于贷后管理的周期性风险复核场景。相较于授信前的"点式尽调"，贷后监控关注的是"时间轴上的变化"——本期扫描结果必须与上期快照对比，识别增量风险、变化趋势和异动归因。
本 SKILL 通过企查查商业数据库，执行"本期扫描 × 历史对比 × 异动归因"三位一体分析，核心产出是"增量风险清单 + 趋势分析 + 预警分级 + 推荐 Action"。
## 共享引用
- MCP 工具映射表：参见本目录下的 `mcp-tools-map.md`
- MCP 缓存约定：参见本目录下的 `mcp-cache-guide.md`
> **核心原则**：调用 MCP 前先检查 `./[公司名]MCP查询结果/` 目录下的缓存文件。命中则跳过调用。
## MCP 依赖
- **必选**: `qcc-company` — 工商登记本期快照、财务数据对比
- **必选**: `qcc-risk` — 本期司法与经营风险全量快照
- **强烈建议**: `qcc-executive` — 核心人员的跨周期状态变化
> ⚠️ 历史对比依赖：企业级历史数据通过 `mcp__qcc-company__get_change_records`（工商变更）、`mcp__qcc-risk__get_business_exception`（移出记录）等推断。人员级历史通过 qcc-executive 历史工具获取。
## 通用执行原则
1. **基准日期必须明示**——所有"新增/恶化/收敛"判断都相对于基准日期
2. **增量信号优先于存量信号**——本期新增的 2 条比存量 48 条更重要
3. **变化方向必须标注**——资产负债率从 70% 升到 80% vs 从 70% 降到 60% 含义完全不同
4. **法代变更视为最高优先级异动**——授信后法代变更需立即上报
5. **预警分级与上报路径严格对齐**
## 工作流
### 维度一：本期风险全景快照
工具链（当前层）：
- `mcp__qcc-risk__get_dishonest_info` / `get_judgment_debtor_info` / `get_high_consumption_restriction` / `get_terminated_cases`
- `mcp__qcc-risk__get_equity_freeze` / `get_equity_pledge_info` / `get_chattel_mortgage_info`
- `mcp__qcc-risk__get_tax_arrears_notice` / `get_business_exception`
- `mcp__qcc-company__get_company_registration_info` — 工商基础信息
- `mcp__qcc-company__get_financial_data` — 本期财务数据
产出：本期风险全景一张总表。
### 维度二：历史基准对比（核心能力）
工具链：
- `mcp__qcc-company__get_change_records` — 工商变更记录（法代/股东/注册资本/地址变更等）
- `mcp__qcc-executive__get_executive_historical_dishonest` / `_historical_judgment_debtor` / `_historical_high_consumption_ban` / `_historical_terminated_cases` — 人员级历史
- `mcp__qcc-executive__get_executive_historical_legal_rep_roles` — 历届法代
- `mcp__qcc-risk__get_business_exception` — 含移出记录
对比逻辑：本期 MCP 全集 减去 基准日 MCP 全集 = 本期增量。
分类归因：
- **增量失信/被执行/限高**：按案号、立案日期、涉案金额排序，输出 Top 5
- **法代变更**：新旧法代对比
- **股东变更**：大股东退出或新增均需标注
- **注册资本变更**：减资是风险信号
- **经营异常新增**：识别未按时报送年报等常见轻微异常
### 维度三：财务指标 YoY 退化预警
基于 `mcp__qcc-company__get_financial_data` 返回的 3 年财报做同比对比：
| 指标 | 正常波动 | 警戒区间 | 致命区间 |
|------|---------|---------|---------|
| 资产负债率同比 | < 5% 上升 | 5-15% 上升 | > 15% 上升 |
| 营收同比 | > 0% | -10%~0% | < -10% |
| 净利润同比 | 任何 | 由正转负 | 连续 2 年净亏损 |
| 经营现金流 | 正 | 由正转负 | 连续 2 年负 |
| 速动比率下降 | < 0.2 | 0.2-0.5 | > 0.5 |
任何一项触及致命区间即触发 S 级预警。
### 维度四：核心人员状态变化
工具链：
- `mcp__qcc-executive__get_executive_dishonest` / `_high_consumption_ban` / `_judgment_debtor` / `_exit_restriction` — 法代+实控人本期扫描
- `mcp__qcc-executive__get_executive_historical_dishonest` — 对比基准日
识别内容：
- 法代/实控人本期新增任何个人风险 → 最高优先级上报
- 核心高管团队变动（CFO、总经理离任）→ 中优先级关注
- 实控人新增控制企业出险 → "系内风险传染"
## 预警分级 × 推荐 Action
**S 级（24 小时内上报+紧急处置）**：
- 企业当前新增失信/限高/被执行
- 实控人或法代新增任何个人风险
- 财务指标触及致命区间
- 动作：启动加速回收、重新评估贷款分类、考虑提前收贷
**A 级（T+3 内上报+加强监测）**：
- 历史曾清洁，本期新增经营异常/欠税/行政处罚
- 财务指标触及警戒区间
- 法代或大股东发生变更
- 动作：召集三方会议、提高监测频率到月度
**B 级（T+7 内记录+正常监测）**：
- 无新增风险，历史存量无恶化
- 财务指标正常波动
**C 级（持续优质客户）**：
- 连续两期无任何增量负面信号
- 财务指标稳中有升
- 动作：可讨论续贷/提额
## 输出模板
1. 执行摘要 · 预警 Decision Pack（预警级别+3-5条核心判断+T+0/T+3/T+7 Action）
2. 基准日期声明与数据来源
3. 本期×基准日增量风险清单（按预警级别分层）
4. 财务指标 YoY 退化分析（近 3 年对比表）
5. 历史趋势分析（近 5 年时间序列）
6. 核心人员状态变化
7. 预警分级结论×推荐 Action 清单
8. 数据来源、采集时间戳、下次监控日建议
## 参数
- `--baseline <日期>`：对比基准日期（默认上期监控日或授信放款日）
- `--tolerance <阈值>`：风险变化容忍度
- `--format md|docx|pptx`：输出格式，默认 md
## 边界与免责
本 SKILL 输出的是"主体侧"风险监控，不覆盖行业风险、区域政策、利率变化、宏观经济等维度。2015 年前的历史记录可能不全。
数据来源：企查查商业数据库（qcc-company / qcc-risk / qcc-executive）。
