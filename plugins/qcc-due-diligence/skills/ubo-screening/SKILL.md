---
name: 受益所有人(UBO)穿透
description: 反洗钱合规场景下的股权穿透，基于央行3号令逐层解析多层股权结构，查明最终受益所有人及持股比例。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers:
  - qcc-company
  - qcc-executive
tags:
  - UBO
  - 受益所有人
  - 反洗钱
  - 股权穿透
  - 央行3号令
  - AML合规
model: deepseek-v4-pro
---

> **⚠️ 环境依赖提醒**：如遇到 Python/pandoc/markitdown 未安装或命令找不到等电脑环境问题，请访问 "企业信息检索基本环境配置" skill 完成环境配置。

# 受益所有人（UBO）穿透识别
## SKILL 定位
服务于金融机构反洗钱合规场景下的受益所有人（UBO）识别需求。专注于一件事："将企业的所有 UBO 自然人找出来，并对每个自然人做合规画像"。
本 SKILL 通过企查查商业数据库的 qcc-company（股东+实控人+UBO）+ qcc-executive（自然人锁定义反查+个人画像），实现"企业→UBO"的完整穿透链路。
## 共享引用
- MCP 工具映射表：参见本目录下的 `mcp-tools-map.md`
- MCP 缓存约定：参见本目录下的 `mcp-cache-guide.md`
> **核心原则**：调用 MCP 前先检查 `./[公司名]MCP查询结果/` 目录下的缓存文件。命中则跳过调用。
## MCP 依赖
- **必选**: `qcc-company` — 股东、实控人、UBO
- **必选**: `qcc-executive` — 自然人锁定、反查、个人画像
## 通用执行原则
1. **合规标准以央行 3 号令为准**——①直接或间接持股 25% 以上的自然人；②通过其他方式实际控制的自然人；③高管层兜底。高风险客户可降至 10% 阈值
2. **穿透不是到法人为止**——"某某控股集团持有 60%"只是中间步骤，必须继续穿透
3. **反向验证是规定动作**——对每个 UBO 自然人调用 `get_executive_beneficial_owner` 反查
4. **对每个 UBO 做司法画像扫描**——不是"找出 UBO 就结束"，必须过 4 项红线（失信/限高/被执行/限出境）
5. **UBO 关联企业合规联动**——UBO 控制的其他企业如存在风险，整个关系须标记"系内 UBO 风险"
## 工作流
### 维度一：企业层 UBO 初筛（25% 阈值）
工具链：
- `mcp__qcc-company__get_beneficial_owners` — MCP 算法识别的 UBO 清单
- `mcp__qcc-company__get_shareholder_info` — 直接股东清单
- `mcp__qcc-company__get_actual_controller` — 实际控制人
判定：找出所有直接或通过 `get_beneficial_owners` 识别出的自然人 UBO。
### 维度二：多层股权向上穿透
对每个机构股东递归调用 `mcp__qcc-company__get_shareholder_info`，直到终止条件触发：
- 遇到自然人 → 记录为 UBO，计算累计穿透比例
- 遇到国资委 → 记录为国资控股 UBO
- 遇到境外主体 → 标注"境外穿透受限"
- 深度达 10 层仍未到自然人 → 终止并上报"UBO 穿透疑点"
产出：完整的 UBO 候选清单 + 各自穿透比例。
### 维度三：10% 阈值降低（高风险客户加强核查）
如本次客户被判定为高风险，将阈值降至 10%，重新跑维度一和维度二，识别 10-25% 区间的"潜在 UBO"。
### 维度四：UBO 反向验证（核心规定动作）
对每个 UBO 自然人调用：
- `mcp__qcc-executive__get_executive_beneficial_owner` — 该自然人作为 UBO 的全部企业清单
- `mcp__qcc-executive__get_executive_related_companies` — 该自然人的全部关联企业
- `mcp__qcc-executive__get_executive_controlled_companies` — 该自然人实际控制的企业
验证逻辑：
- 如本次分析识别 X 先生是本企业 UBO，但 `get_executive_beneficial_owner` 返回 0 家企业 → 矛盾，穿透可能错误
- 如返回 50 家企业 → 正常，但需标注"UBO 具有复杂商业帝国"
### 维度五：UBO 个人司法画像
对每个 UBO 自然人（25% 阈值）：
- `mcp__qcc-executive__get_executive_dishonest`
- `mcp__qcc-executive__get_executive_high_consumption_ban`
- `mcp__qcc-executive__get_executive_judgment_debtor`
- `mcp__qcc-executive__get_executive_exit_restriction`
输出 AML 风险标签：
- 全绿 → **清洁 UBO**
- 任一项命中 → **高风险 UBO**
### 维度六：UBO 关联企业合规联动
对每个 UBO 扫描其关联企业（`get_executive_related_companies`），对每家做快速风险标签：
- 关联企业全部清洁 → **UBO 关联无风险**
- 关联企业 1-2 家有失信/经营异常 → **UBO 关联系内风险**
- 关联企业多家出险或出现破产 → **UBO 商业帝国崩溃风险**
### 维度七：历史 UBO 追溯
工具链：
- `mcp__qcc-company__get_change_records` — 工商变更记录（股东变更部分）
- `mcp__qcc-executive__get_executive_historical_investments` — 历史对外投资
识别"曾经是 UBO 但已退出"的自然人——在反洗钱可疑交易监测中是关键信息。
## UBO 综合评级
| 等级 | 标准 | KYC/AML 处置 |
|------|------|-------------|
| **合规 A** | 25% 阈值下清晰识别 UBO+全部清洁 | 标准 CDD 流程 |
| **合规 B** | 多个 UBO（≥3个）但全部清洁 | 标准 CDD+加强关系监测 |
| **关注 C** | UBO 历史有已修复轻微风险或关联企业有轻微瑕疵 | 标准 CDD+每半年复核 |
| **高风险 D** | UBO 当前失信/限高/限出境，或关联企业存在破产/严重违法 | **启动 EDD 流程**+高风险客户处置 |
| **禁入** | UBO 命中国际制裁名单或涉及恐怖主义融资 | **拒绝开户**+STR 上报 |
## 输出模板
1. UBO 核验 Decision Pack（合规等级+UBO 清单+关键风险）
2. 数据来源
3. 主体基本信息
4. 25% 阈值下的 UBO 清单（含穿透路径）
5. 10% 阈值下的 UBO 清单（高风险客户）
6. UBO 反向验证结果（核心能力）
7. UBO 个人司法画像（按人独立成节）
8. UBO 关联企业合规联动
9. 历史 UBO 追溯
10. UBO 综合评级 × KYC 处置建议
11. 数据来源、采集时间戳、免责声明
## 参数
- `--threshold <25|10>`：UBO 识别阈值，默认 25，高风险客户可选 10
- `--profile-depth <quick|full>`：UBO 个人画像深度。quick 只扫 4 项红线；full 扫全量工具
- `--format md|docx|pptx`：输出格式，默认 md
## 边界与免责
UBO 识别基于公开股权信息，无法识别未披露的代持、协议控制、一致行动安排。境外主体（BVI/Cayman/香港等）穿透受限。国际制裁清单（OFAC/UN/EU）不在覆盖范围。
数据来源：企查查商业数据库（qcc-company / qcc-executive）。
