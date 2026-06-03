---
name: 交易对手风险评估
description: 贸易融资、信用证、保理等场景的交易对手多维风险评估，综合进出口信用、司法风险、实控人个人风险输出评级。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers:
  - qcc-company
  - qcc-risk
  - qcc-operation
  - qcc-executive
tags:
  - 交易对手
  - 贸易融资
  - 信用证
  - 保理
  - 进出口信用
  - 风险评估
model: deepseek-v4-pro
---

> **⚠️ 环境依赖提醒**：如遇到 Python/pandoc/markitdown 未安装或命令找不到等电脑环境问题，请访问 "企业信息检索基本环境配置" skill 完成环境配置。

# 交易对手风险评估
## SKILL 定位
服务于银行贸易金融业务（信用证/保理/福费廷/应收账款贴现/远期结售汇）的交易对手多维风险评估。核心问题是"在特定交易敞口下，对手方能否如约履行合同义务"。
本 SKILL 通过企查查商业数据库，综合 7 大评估维度（工商+财务+司法+经营+人员+历史+关联），输出 A/B/C/D 四档评级。
## 共享引用
- MCP 工具映射表：参见本目录下的 `mcp-tools-map.md`
- MCP 缓存约定：参见本目录下的 `mcp-cache-guide.md`
> **核心原则**：调用 MCP 前先检查 `./[公司名]MCP查询结果/` 目录下的缓存文件。命中则跳过调用。
## MCP 依赖
- **必选**: `qcc-company` — 工商、股东、实控人、对外投资
- **必选**: `qcc-risk` — 失信、被执行、限高、股权冻结、行政处罚、破产重整
- **强烈建议**: `qcc-operation` — 进出口信用（核心）、资质、招投标、招聘
- **强烈建议**: `qcc-executive` — 法代+实控人个人风险
## 通用执行原则
1. **进出口信用等级是跨境贸易金融的第一门槛**——失信企业原则上不予受理
2. **法代与实控人限制出境是核心否决项**——任一方受限直接触发 D 级
3. **对外担保链必须专项核查**——或有负债不进入资产负债表但直接影响履约能力
4. **交易真实性辅助判定**——经营活跃度+业务范围匹配度+上下游关联企业综合判定
5. **评级与敞口金额挂钩**——小额敞口下 B 级可接受，大额敞口下需要强担保
## 工作流
### 维度一：主体核验 × 工商基础
工具链：
- `mcp__qcc-company__get_company_registration_info` — 工商登记
- `mcp__qcc-company__verify_company_accuracy` — 三项匹配
- `mcp__qcc-company__get_shareholder_info` — 股东结构
- `mcp__qcc-company__get_actual_controller` — 实控人
- `mcp__qcc-company__get_branches` — 分支机构
### 维度二：进出口信用与经营活跃度（核心能力）
工具链：
- `mcp__qcc-operation__get_import_export_credit` — **海关信用等级**（核心）
- `mcp__qcc-operation__get_qualifications` — 资质证书
- `mcp__qcc-operation__get_credit_evaluation` — 纳税信用等级
- `mcp__qcc-operation__get_bidding_info` — 招投标
- `mcp__qcc-operation__get_recruitment_info` — 招聘
- `mcp__qcc-operation__get_random_check` — 双随机抽查
海关信用等级处置：
| 海关信用等级 | 贸易金融建议 |
|------------|------------|
| 高级认证企业（AEO）| 优先受理，可享优惠费率 |
| 一般认证企业 | 正常受理 |
| 一般信用企业 | 受理但加强真实性审查 |
| 失信企业 | **原则上拒绝**或全额保证金业务 |
### 维度三：司法风险扫描
工具链：
- `mcp__qcc-risk__get_dishonest_info` / `get_judgment_debtor_info` / `get_high_consumption_restriction` / `get_terminated_cases`
- `mcp__qcc-risk__get_equity_freeze` / `get_administrative_penalty`
- `mcp__qcc-risk__get_guarantee_info` — **对外担保余额**（核心）
对外担保余额的贸易金融意义：
- 对外担保/净资产 > 30% → 表外负债显著
- 对外担保/净资产 > 50% → **严重风险**，互保圈传染高危
- 对外担保关联方有失信 → 触发连带代偿风险
### 维度四：法代与实控人个人风险
工具链（对法代+实控人分别）：
- `mcp__qcc-executive__get_executive_dishonest`
- `mcp__qcc-executive__get_executive_high_consumption_ban`
- `mcp__qcc-executive__get_executive_exit_restriction` — **贸易金融最关键**
- `mcp__qcc-executive__get_executive_judgment_debtor`
贸易金融特殊评估：
- 实控人/法代**被限制出境** → **D 级（否决）**
- 实控人/法代有当前失信 → **D 级**
- 实控人控制的其他贸易类企业存在信用证欺诈/单据造假司法记录 → 重点审查
### 维度五：历史治理稳定性
工具链：
- `mcp__qcc-executive__get_executive_historical_legal_rep_roles` — 历届法代
- `mcp__qcc-executive__get_executive_historical_positions` — 历史任职
- `mcp__qcc-company__get_change_records` — 工商变更记录（股东变更、注册资本变更）
### 维度六：关联企业与交易真实性
- 通过对外投资+实控人关联识别上下游
- 识别"自己与自己交易"（关联交易占比过高）
- 识别"虚假贸易"（业务范围不匹配、关联企业在离岸地）
## 综合评级 × 敞口建议
| 评级 | 核心标准 | 贸易金融建议 |
|------|---------|------------|
| **A 级** | 高级/一般认证 + 纳税A级 + 无司法风险 + 实控人清洁 | 正常受理，敞口上限净资产×50% |
| **B 级** | 一般认证/信用 + 无致命风险 + 历史有已修复事件 | 严格单证审核，敞口上限净资产×20% |
| **C 级** | 一般信用 + 有当前轻微风险或法代近期变更 | 追加保证金或担保，敞口上限净资产×5% |
| **D 级** | 失信企业或致命司法风险或实控人限制出境/失信 | **拒绝受理** |
### 敞口金额分级
| 敞口金额 | 建议 |
|---------|------|
| < 100 万 | A/B/C 级均可，D 级拒绝 |
| 100-1,000 万 | A/B 级可受理，C 级需担保 |
| > 1,000 万 | 仅 A 级标准受理，B 级需担保 |
## 输出模板
1. Decision Pack（评级+敞口建议+关键风险+单证审核要求）
2. 数据来源与互证方法
3. 主体核验与工商基础
4. 进出口信用 × 经营活跃度
5. 司法风险与对外担保
6. 法代与实控人个人风险
7. 历史治理稳定性
8. 关联企业与交易真实性判定
9. 综合评级 × 敞口建议 × 单证审核要求
10. 数据来源、采集时间戳、免责声明
## 参数
- `--business-type <进出口|贸易|跨境|国内>`：业务类型
- `--exposure <金额>`：敞口金额
- `--format md|docx|pptx`：输出格式，默认 md
## 边界与免责
本 SKILL 评估的是对手方主体的一般履约能力，不替代具体贸易合同的条款审核。海关信用等级每年核定一次，实时变化可能有滞后。对外担保余额可能存在披露不完整。
数据来源：企查查商业数据库（qcc-company / qcc-risk / qcc-operation / qcc-executive）。
