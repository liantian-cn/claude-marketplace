---
name: 高管背景核查
description: 对目标企业董监高、实控人进行个人风险穿透与关联网络测绘，输出结构化背调档案，支持全员/核心/单人三种模式。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers:
  - qcc-company
  - qcc-executive
  - qcc-risk
tags:
  - 高管背调
  - 董监高
  - 个人司法
  - 任职履历
  - 关联企业
  - 利益冲突
model: deepseek-v4-pro
---

> **⚠️ 环境依赖提醒**：如遇到 Python/pandoc/markitdown 未安装或命令找不到等电脑环境问题，请访问 "企业信息检索基本环境配置" skill 完成环境配置。

# 高管背景核查
## SKILL 定位
服务于投资尽调、人才引进、高管聘任、IPO 核查、反洗钱 KYC 等场景的关键人员背调需求。以"企业+姓名双锚"方式通过企查查商业数据库的人员画像工具，形成个人司法、任职履历、关联企业、利益冲突四位一体的结构化背调报告。
### 三种使用模式
- **模式1 · 全员核查（默认）**：核查全体董监高（含董事/监事/独立董事/职工代表董事）+实际控制人+主要高管
- **模式2 · 快速核查（--depth quick）**：仅核查 4 位核心管理层（法定代表人、实际控制人、董事长、总经理）
- **模式3 · 单人深度核查（--person 姓名）**：仅对指定一人做完整画像（全量工具）
## 共享引用
- MCP 工具映射表：参见本目录下的 `mcp-tools-map.md`
- MCP 缓存约定：参见本目录下的 `mcp-cache-guide.md`
> **核心原则**：调用 MCP 前先检查 `./[公司名]MCP查询结果/` 目录下的缓存文件。人员相关数据以 `[人名]-` 前缀存储。
## MCP 依赖
- **必选**: `qcc-company` — 企业基础信息、主要人员清单、股东、实际控制人
- **必选**: `qcc-executive` — 本 SKILL 核心数据源，所有个人级查询
- **建议**: `qcc-risk` — 对关联企业做快速风险标签
## 通用执行原则
1. **时间维度必须穿透**——任何现任职务、控制企业、任职履历、司法记录均须同步查询 historical 版本
2. **个人风险不等于企业风险**——同一自然人在 A 企业清洁、在 B 企业被执行，须以"人"为主体独立成章
3. **法代/实控人/董事长/总经理必须分别画像**——四类角色法律责任、经济利益、决策权重差异显著
4. **利益冲突排查优先于关联企业清点**——须对每家关联企业标注业务重叠度、是否为供应商/客户/竞对
5. **数据时效必须明示**——所有输出项均须标注 MCP 采集时间戳
6. **同名误查须人工兜底**——双参数锚定已大幅降低同名误查，但职务/任职时间/关联企业三条线索矛盾时须标注"疑似同名"
## 工作流
### 维度一：主体确认与人员锁定
工具链：
- `mcp__qcc-company__get_company_registration_info` — 工商登记，核验企业信息
- `mcp__qcc-company__get_key_personnel` — 当前董监高全名单
- `mcp__qcc-company__get_shareholder_info` — 股东结构
- `mcp__qcc-company__get_actual_controller` — 实际控制人
产出：《本次背调人员清单》——分为"必背"（法代/实控人/董事长/总经理）与"选背"（其他董监高）。
### 维度二：个人司法风险穿透（核心调用）
**现状扫描**（18 个工具）：
身份限制与失信类：
- `mcp__qcc-executive__get_executive_dishonest` — 当前失信
- `mcp__qcc-executive__get_executive_high_consumption_ban` — 限制高消费
- `mcp__qcc-executive__get_executive_exit_restriction` — 限制出境
- `mcp__qcc-executive__get_executive_property_reward_notice` — 财产悬赏公告
执行与资产冻结类：
- `mcp__qcc-executive__get_executive_judgment_debtor` — 被执行人
- `mcp__qcc-executive__get_executive_terminated_cases` — 终本案件
- `mcp__qcc-executive__get_executive_equity_freeze` — 股权冻结
- `mcp__qcc-executive__get_executive_equity_pledge` — 股权出质
- `mcp__qcc-executive__get_executive_stock_pledge` — 股票质押
- `mcp__qcc-executive__get_executive_valuation_inquiry` — 资产询价评估
行政与税务类：
- `mcp__qcc-executive__get_executive_admin_penalty` — 行政处罚
- `mcp__qcc-executive__get_executive_tax_violation` — 税收违法
司法程序类：
- `mcp__qcc-executive__get_executive_case_filing` / `_hearing_notice` / `_court_notice` / `_service_notice` / `_judicial_docs` / `_pre_litigation_mediation`
**历史追溯**（14 个工具）：
- `mcp__qcc-executive__get_executive_historical_dishonest` / `_historical_high_consumption_ban` / `_historical_judgment_debtor` / `_historical_terminated_cases`
- `mcp__qcc-executive__get_executive_historical_equity_freeze` / `_historical_equity_pledge` / `_historical_admin_penalty`
- `mcp__qcc-executive__get_executive_historical_case_filing` / `_historical_hearing_notice` / `_historical_court_notice` / `_historical_service_notice` / `_historical_judicial_docs` / `_historical_pre_litigation_mediation`
**分析要点**：
- 🔴 红色信号（硬性失信/限高/限出境/股权冻结未解除）→ 直接触发 D 级
- 历史层识别"修复型主体"——已履行的失信记录可作为评级缓解因素
- 5 年内事件 → 视同现状事件处理；5-10 年 → 单独成段；10 年以上 → 历史标注
### 维度三：任职履历与职业轨迹
工具链：
- `mcp__qcc-executive__get_executive_positions` — 当前在外任职
- `mcp__qcc-executive__get_executive_historical_positions` — 历史在外任职
- `mcp__qcc-executive__get_executive_legal_rep_roles` — 当前担任法代的企业
- `mcp__qcc-executive__get_executive_historical_legal_rep_roles` — 历史担任法代
分析要点：
- 任职稳定性：平均任期 < 1 年且密集出现 → 职业稳定性不佳
- 职业梯度：职位级别持续下降、企业规模持续缩水 → 负面信号
- 跳槽可疑点：3 个月内连续离任 3 个董事职务 → "高管集体跑路"模式
### 维度四：关联企业网络与控制力
工具链：
- `mcp__qcc-executive__get_executive_controlled_companies` — 当前控制企业
- `mcp__qcc-executive__get_executive_related_companies` — 当前全部关联企业
- `mcp__qcc-executive__get_executive_investments` — 当前对外投资
- `mcp__qcc-executive__get_executive_beneficial_owner` — 作为 UBO 的企业
- `mcp__qcc-executive__get_executive_historical_related_companies` — 历史关联企业
- `mcp__qcc-executive__get_executive_historical_investments` — 历史对外投资
分析要点：
- 关联企业按"业务重叠度"分级：高重叠（同业务/上下游）、中重叠、低重叠
- 对每家关联企业同步打风险标签（绿/黄/红）
### 维度五：利益冲突与历史合作伙伴
工具链：
- `mcp__qcc-executive__get_executive_historical_partners` — 历史合作伙伴
- `mcp__qcc-operation__get_bidding_info` — 招投标对手方
- `mcp__qcc-company__get_external_investments` — 对外投资
利益冲突判定：关联企业集合 ∩（供应商集合 ∪ 客户集合 ∪ 竞对集合）≠ ∅ → 关联交易嫌疑。
## 综合评级
| 评级 | 标准 | 建议 |
|------|------|------|
| **A 级** | 无现状个人风险+无历史重大事件+任职稳定+关联企业清洁 | 可正常聘任/合作 |
| **B 级** | 无现状风险+5-10年内轻度历史事件 | 可合作，建议加入信息披露条款 |
| **C 级** | 5年内已解除中等风险历史事件或关联企业有1-2家可疑 | 谨慎合作，签约前法务逐项澄清 |
| **D 级** | 当前硬性失信/限高/限出境/股权冻结未解除 | 建议不聘任/不合作 |
整体评级采用"最短板原则"——多人中最低等级决定整体评级。
## 输出模板
1. 执行摘要 · Decision Pack（一句话结论+关键判断表+推荐 Action 清单）
2. 数据来源与互证方法
3. 被核查企业基本信息
4. 核心管理层背景核查（按人逐一成节）
   - 个人基本信息
   - 个人司法风险——现状×历史×时间轴
   - 任职履历与职业轨迹
   - 关联企业网络（按业务重叠度分层）
   - 利益冲突提示
   - 人员评级及依据
5. 关联企业风险地图
6. 利益冲突综合研判
7. 综合评级与聘任/合作建议
8. 数据来源、采集时间戳、免责声明
## 参数
- 不传参数（默认·模式1）：全体董监高+实控人+主要高管完整画像
- `--depth quick`（模式2）：仅 4 位核心管理层快速背调
- `--person <姓名>`（模式3）：仅对指定一人完整画像
- `--period <N年>`：历史事件追溯年限，默认 10 年
- `--format md|docx|pptx`：输出格式，默认 md
## 边界与免责
本 SKILL 基于企查查商业数据库公开工商+司法数据生成。出境限制状态、国际制裁清单（OFAC/UN/EU）、PEP 名单筛查不在覆盖范围内。关键人事决策前应结合面试、第三方背调、人工验证综合判断。
