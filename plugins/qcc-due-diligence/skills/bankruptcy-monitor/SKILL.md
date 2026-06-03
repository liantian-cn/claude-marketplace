---
name: 破产预警与重整监控
description: 对重要客户、债务人、担保方进行破产风险的持续监控，覆盖破产预警与重整跟踪两个子场景。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers:
  - qcc-company
  - qcc-risk
  - qcc-executive
tags:
  - 破产
  - 重整
  - 清算
  - 预警
  - 债权申报
  - 贷后监控
model: deepseek-v4-pro
---

> **⚠️ 环境依赖提醒**：如遇到 Python/pandoc/markitdown 未安装或命令找不到等电脑环境问题，请访问 "企业信息检索基本环境配置" skill 完成环境配置。

# 破产预警与重整监控
## SKILL 定位
对重要客户、债务人、担保方进行破产风险的持续监控。覆盖两个子场景：
- **破产预警**（pre-bankruptcy）：通过 7 大先行指标识别破产概率
- **破产重整跟踪**（restructuring-alert）：跟踪已进入破产程序的企业节点并推算债权申报窗口期
本 SKILL 通过企查查商业数据库的 qcc-risk（司法信号）+ qcc-company（企业基座）+ qcc-executive（人员画像）三层数据融合，在关键节点实时推送预警。
## 共享引用
- MCP 工具映射表：参见本目录下的 `mcp-tools-map.md`
- MCP 缓存约定：参见本目录下的 `mcp-cache-guide.md`
> **核心原则**：调用 MCP 前先检查 `./[公司名]MCP查询结果/` 目录下的缓存文件。命中则跳过调用。
## MCP 依赖
- **必选**: `qcc-company` — 工商登记、财报、对外投资
- **必选**: `qcc-risk` — 破产重整、清算、失信、被执行、限高、终本、股权冻结
- **强烈建议**: `qcc-executive` — 核心人员跑路信号（法代被执行、实控人限制出境）
## 通用执行原则
1. **破产先行指标权重高于破产程序本身**——正式程序前 6-24 个月通过先行指标发出预警
2. **法代与实控人分离判断**——法代更替 ≠ 实控人变化，含义不同
3. **重整 vs 清算分叉识别**——基于财务底盘 × 司法泥潭 × 实控人现状三元组合预判
4. **债权申报窗口期不容错过**——按破产法规定的 30/60/90 日窗口动态计算
5. **担保债权 vs 普通债权区分**——持有担保权益的债权人与普通债权人 Action 建议不同
## 工作流
### 维度一：破产先行指标扫描（7 大指标）
| 序号 | 指标 | MCP 工具 | 警戒阈值 | 致命阈值 |
|------|------|---------|---------|---------|
| 1 | 失信被执行人累计 | `mcp__qcc-risk__get_dishonest_info` | > 50 条 | > 200 条 |
| 2 | 终本案件未履行金额 | `mcp__qcc-risk__get_terminated_cases` | > 1 亿元 | > 10 亿元 |
| 3 | 股权冻结扩散 | `mcp__qcc-risk__get_equity_freeze` | > 10 条 | > 50 条 |
| 4 | 法代个人被执行 | `mcp__qcc-executive__get_executive_judgment_debtor` | > 0 条 | — |
| 5 | 实控人限制出境 | `mcp__qcc-executive__get_executive_exit_restriction` | > 0 条 | — |
| 6 | 连年失信模式 | `mcp__qcc-executive__get_executive_historical_dishonest` | 近 3 年每年新增 | 近 5 年每年新增 |
| 7 | 资产负债率 | `mcp__qcc-company__get_financial_data` | > 100% | > 150% |
**破产概率分级**：
- 命中 0-1 个警戒阈值：低风险（< 10%）
- 命中 2-3 个警戒阈值：中风险（10-30%）
- 命中 ≥ 4 个警戒阈值或任一致命阈值：**高风险（> 50%）**
- 命中 ≥ 2 个致命阈值：**极高风险（> 80%）**
### 维度二：正式破产程序识别
工具链：
- `mcp__qcc-risk__get_bankruptcy_reorganization` — 破产重整
- `mcp__qcc-risk__get_liquidation_info` — 清算信息
- `mcp__qcc-risk__get_cancellation_record_info` — 注销备案
- `mcp__qcc-risk__get_simple_cancellation_info` — 简易注销
识别：破产程序状态、程序类型、关键节点日期。
### 维度三：核心人员跑路信号
工具链：
- `mcp__qcc-executive__get_executive_exit_restriction` — 实控人/法代限制出境（最强跑路信号）
- `mcp__qcc-executive__get_executive_dishonest` — 个人失信
- `mcp__qcc-executive__get_executive_judgment_debtor` — 个人被执行
- `mcp__qcc-executive__get_executive_high_consumption_ban` — 个人限高
- `mcp__qcc-executive__get_executive_historical_legal_rep_roles` — 法代更替时间线
判定标准：
- 实控人限制出境 → 破产概率极高
- 法代 6 个月内连续更替 → 正在切割责任链
- 核心高管 3 个月内 ≥ 3 人离任 → 内部已知情
### 维度四：重整 vs 清算分叉预判
| 组合 | 特征 | 预判 |
|------|------|------|
| 负债率 < 200% + 主营业务有价值 + 实控人未被追责 | "重生希望" | **重整**（清偿率 25-45%） |
| 负债率 > 200% + 主营业务萎缩 + 实控人被追责 | "无人接手" | **清算**（清偿率 5-15%） |
| 负债率 100-200% + 业务尚可 + 实控人在位但压力大 | "被动重整" | **重整但可能失败** |
### 维度五：债权申报窗口期计算
一旦 MCP 返回"破产受理"信号：
- T+3 日内：提交债权申报材料初稿
- T+7 日内：正式向清算组/管理人提交债权申报
- T+30 日内：跟进第一次债权人会议
## 预警分级 × 推荐 Action
| 预警级别 | 触发条件 | 推荐 Action |
|---------|---------|------------|
| **L0（无风险）** | 先行指标全绿 + 无正式破产程序 | 标准贷后周期监测 |
| **L1（警戒）** | 命中 2-3 个警戒阈值 | T+7 内召集风控会议 |
| **L2（高风险）** | 命中 ≥ 4 警戒或任一致命 | T+3 内启动诉前保全 + 上报分行 |
| **L3（极高风险）** | 命中 ≥ 2 致命或法代/实控人出险 | T+24h 内紧急三方会议 + 重分类为"可疑类" |
| **L4（已破产）** | 破产重整/清算返回 > 0 | T+0 立即提交债权申报 |
## 输出模板
1. 执行摘要 · Decision Pack（预警级别 + 破产概率 + 重整/清算预判）
2. 数据来源与互证方法
3. 被监控主体基本信息
4. 7 大破产先行指标扫描结果
5. 正式破产程序状态（如已进入）
6. 核心人员跑路信号分析
7. 重整 vs 清算分叉预判
8. 债权申报窗口期计算（如已受理）
9. 预警分级结论 × 推荐 Action 清单
10. 数据来源、采集时间戳、下次监控日建议
## 参数
- `--scenario <warning|restructuring|both>`：监控场景模式，默认 both
- `--claim-amount <金额>`：债权金额
- `--claim-type <secured|unsecured>`：债权类型
- `--format md|docx|pptx`：输出格式，默认 md
## 边界与免责
破产先行指标基于统计规律，命中警戒阈值不等于企业一定破产。重整可行性预判是方向性判断，最终是否启动重整由法院和主要债权人决定。债权申报的法律时效以 MCP 返回的实时公告日期为准，正式法律操作应以人民法院公告原文为准。
数据来源：企查查商业数据库（qcc-company / qcc-risk / qcc-executive）。
