---
name: 企业主体核验(KYB)
description: 金融机构对公开户、授信审批、年检场景的主体自动化核验，完成工商核验、UBO穿透、34类司法风险扫描，输出合规底稿。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers:
  - qcc-company
  - qcc-risk
  - qcc-executive
  - qcc-operation
tags:
  - KYB
  - 对公开户
  - 主体核验
  - UBO穿透
  - 司法风险
  - 合规底稿
model: deepseek-v4-pro
---

> **⚠️ 环境依赖提醒**：如遇到 Python/pandoc/markitdown 未安装或命令找不到等电脑环境问题，请访问 "企业信息检索基本环境配置" skill 完成环境配置。

# 企业主体核验（KYB）
## SKILL 定位
服务于金融机构对公客户全生命周期的主体核验需求——对公开户时的准入 KYB、授信前的背景调查、存量客户的年度体检、反洗钱尽调的主体基础核验。
本 SKILL 通过企查查商业数据库，自动完成"主体真实性核验 × 工商信息核验 × 历史治理稳定性回溯 × 受益所有人穿透 × 34 类司法风险扫描"，输出符合 FATF / 中国央行 3 号令标准的 KYB 合规底稿。
## 共享引用
- MCP 工具映射表：参见本目录下的 `mcp-tools-map.md`
- MCP 缓存约定：参见本目录下的 `mcp-cache-guide.md`
> **核心原则**：调用 MCP 前先检查 `./[公司名]MCP查询结果/` 目录下的缓存文件。命中则跳过调用。
## MCP 依赖
- **必选**: `qcc-company` — 工商核验、股东、实控人、UBO、主要人员
- **必选**: `qcc-risk` — 34 类司法风险全覆盖
- **强烈建议**: `qcc-executive` — UBO 自然人穿透
- **可选**: `qcc-operation` — 经营活跃度补充指标
## 通用执行原则
1. **KYB 的起点是"企业名×USCC×法代"三项一致性验证**——任一项不匹配即触发核验失败
2. **登记状态为"存续"只是必要条件**——须结合治理稳定性×财务底盘×司法风险综合判断"实质存续"
3. **治理稳定性必须入表**——法代 2 年内 ≥ 2 次变更、股东 1 年内 ≥ 2 次变更等触发"治理不稳定"标签
4. **UBO 穿透到自然人是合规硬要求**——根据央行 3 号令，必须穿透识别受益所有人
5. **关联企业合规联动**——UBO 控制的其他企业出现风险，整个客户关系须标记"系内合规风险"
## 工作流
### 维度一：主体真实性 × 工商信息核验
工具链：
- `mcp__qcc-company__verify_company_accuracy` — 企业名+法代+USCC 三项匹配
- `mcp__qcc-company__get_company_registration_info` — 工商基础信息
- `mcp__qcc-company__get_contact_info` — 联系方式（核验申请材料真实性）
- `mcp__qcc-company__get_tax_invoice_info` — 税号开票信息
- `mcp__qcc-company__get_shareholder_info` — **当前股东结构**（与客户申请材料交叉核验）
**股东结构核验要点**：
- 核验当前股东列表与客户申请材料的一致性
- 凡股东为企业法人/有限合伙/投资机构（非自然人），一律标记为"待穿透股东"，触发 UBO 强制穿透
- ⚠️ MCP 股东数据为查询时点快照，工商变更登记有约 3-12 个月滞后
**核验三道红线**（任一触发即拒绝 KYB 通过）：
- 企业名×USCC×法代三项任一不匹配
- 登记状态为"吊销/注销/异常"
- 成立日期在客户申请材料之后
### 维度二：历史治理稳定性
工具链：
- `mcp__qcc-company__get_change_records` — 工商变更记录（曾用名/历史注册地址/历史经营范围/法代变更/股东变更/注册资本变更）
- `mcp__qcc-executive__get_executive_historical_legal_rep_roles` — 历届法代
- `mcp__qcc-executive__get_executive_historical_positions` — 历届高管
**治理稳定性判定**：
| 指标 | 警戒阈值 | 含义 |
|------|---------|------|
| 法代近 2 年变更次数 | ≥ 2 次 | 治理极不稳定（危机企业信号） |
| 股东近 1 年变更次数 | ≥ 2 次 | 控制权频繁转移 |
| 注册资本近 3 年变更 | 有减资 | 可能抽逃出资或股东退出 |
| 注册地址近 2 年变更 | ≥ 2 次 | 疑似逃避监管或债权人 |
| 曾用名次数 | ≥ 2 次 | 可能涉及"摘牌+更名+复活"模式 |
| 历史法代数/成立年数 | > 0.3 | 治理更替频率过高 |
- 触发 ≥ 2 个警戒阈值：**治理不稳定**，KYB 评级下调一级
- 触发 ≥ 4 个警戒阈值：**治理高度不稳定**，评级下调两级
### 维度三：受益所有人穿透到自然人
工具链：
- `mcp__qcc-company__get_shareholder_info` — 股东结构
- `mcp__qcc-company__get_actual_controller` — 实际控制人
- `mcp__qcc-company__get_beneficial_owners` — 受益所有人
- `mcp__qcc-executive__get_executive_beneficial_owner` — 以自然人为锚反查 UBO
**UBO 识别三层穿透**：
1. 直接持股 25% 以上的自然人
2. 间接持股（通过中间层）累计 25% 以上的自然人
3. 通过协议/投票权/管理层任免实际控制的自然人
**持股平台穿透规则**：
| 持股平台类型 | 穿透要求 |
|------------|---------|
| 有限合伙（LP/GP结构）| 穿透至 GP + 最终 LP 自然人 |
| 投资机构/私募基金 | 穿透至最终受益人 |
| 上市公司 | 穿透至实际控制人 |
| 其他壳公司/持股平台 | 递归穿透至最终自然人 |
**⚠️ 持股形式变更 vs 股东实质性退出**：当历史股东退出+同时出现持股比例相近的新股东时，须核查新股东与原股东是否同一 UBO——若是持股平台替换，不触发治理稳定性预警。
对每个 UBO 自然人做简化画像扫描：
- `mcp__qcc-executive__get_executive_dishonest`
- `mcp__qcc-executive__get_executive_high_consumption_ban`
- `mcp__qcc-executive__get_executive_exit_restriction`
任何 UBO 存在当前失信/限高/限出境 → KYB 评级直接触发"高风险"。
### 维度四：34 类司法风险扫描
工具链（全量）：
- `mcp__qcc-risk__get_dishonest_info` / `get_judgment_debtor_info` / `get_high_consumption_restriction` / `get_terminated_cases`
- `mcp__qcc-risk__get_equity_freeze` / `get_equity_pledge_info` / `get_chattel_mortgage_info` / `get_land_mortgage_info`
- `mcp__qcc-risk__get_business_exception` / `get_tax_arrears_notice` / `get_tax_violation`
- `mcp__qcc-risk__get_administrative_penalty` / `get_environmental_penalty` / `get_serious_violation`
- `mcp__qcc-risk__get_bankruptcy_reorganization` / `get_liquidation_info`
- `mcp__qcc-risk__get_judicial_documents` / `get_case_filing_info` / `get_hearing_notice`
**分类处置**：
| 风险类别 | KYB 处置 |
|---------|---------|
| 当前失信/限高/限出境/股权冻结 | **拒绝开户/准入** |
| 严重违法失信名单/经营异常 | **拒绝+上报** |
| 破产重整/清算 | **拒绝+债权申报评估** |
| 税务违法/环保处罚/行政处罚 | 根据严重程度下调评级 1-2 级 |
| 民事诉讼（作为被告）> 50 件 | 下调评级 1 级 |
| 纳税信用 A 级+荣誉记录多 | 上调评级半级 |
### 维度五：关联关系排查
工具链：
- `mcp__qcc-company__get_external_investments` — 企业对外投资
- `mcp__qcc-company__get_branches` — 分支机构
- `mcp__qcc-executive__get_executive_related_companies` — 实控人其他关联企业
- `mcp__qcc-executive__get_executive_controlled_companies` — 实控人控制企业
排查清单：
- 同一实控人控制的其他企业是否存在失信/破产
- 集团客户识别
- 一致行动人识别
- 隐性关联
### 维度六：经营活跃度补充指标（可选）
工具链：
- `mcp__qcc-operation__get_qualifications` / `get_honor_info` / `get_credit_evaluation`
- `mcp__qcc-operation__get_random_check` — 双随机抽查
- `mcp__qcc-operation__get_bidding_info` / `get_recruitment_info`
用途：区分"形式存续但实质空壳"与"正常经营主体"。
## KYB 评级
| 评级 | 核心标准 | 处置 |
|------|---------|------|
| **A 级** | 主体真实+治理稳定+无司法风险+UBO 清洁+经营活跃 | **通过 KYB**，进入标准业务流程 |
| **B 级** | 主体真实+治理稳定+无致命风险+有历史已修复事件 | **通过 KYB**，启动标准监测 |
| **C 级** | 主体真实+治理不稳定或有轻微风险（行政处罚等）| **附条件通过**，加强监测+定期复核 |
| **D 级** | 主体真实性存疑或治理高度不稳定或致命风险命中 | **拒绝**，不得开户/准入 |
## 输出模板
1. KYB 核验结论 · Decision Pack（评级+关键核验结果+准入建议+后续监测要求）
2. 数据来源与互证方法
3. 主体真实性 × 工商信息核验（三项一致性）
4. 历史治理稳定性
5. 受益所有人穿透（自然人级）
6. 34 类司法风险扫描
7. 关联关系排查
8. 经营活跃度补充指标（可选）
9. KYB 综合评级 × 准入建议 × 后续监测要求
10. 数据来源、采集时间戳、免责声明
## 参数
- `--depth <standard|full>`：核查深度，standard 涵盖必选+强烈建议工具；full 额外覆盖经营活跃度
- `--format md|docx|pptx`：输出格式，默认 md
## 边界与免责
本 SKILL 完成的是"基于公开工商+司法+财务数据的主体侧 KYB"，不涉及客户身份文件的实物核验。UBO 识别基于公开股权信息，未披露的代持/协议控制/一致行动安排无法穿透。制裁清单命中（OFAC/UN/EU）不在覆盖范围。KYB 通过不代表客户可获得任何业务。
数据来源：企查查商业数据库（qcc-company / qcc-risk / qcc-executive / qcc-operation）。
