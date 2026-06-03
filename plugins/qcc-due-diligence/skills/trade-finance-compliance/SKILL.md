---
name: 贸易融资合规核查
description: 跨境贸易与信用证/保理/福费廷/出口退税业务的合规准入核查，输出A/B/C/D四档评级，D级直接拒绝业务。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers:
  - qcc-company
  - qcc-risk
  - qcc-operation
  - qcc-executive
tags:
  - 贸易融资
  - 合规
  - 海关信用
  - 出口退税
  - 反洗钱
  - AML
model: deepseek-v4-pro
---

> **⚠️ 环境依赖提醒**：如遇到 Python/pandoc/markitdown 未安装或命令找不到等电脑环境问题，请访问 "企业信息检索基本环境配置" skill 完成环境配置。

# 贸易融资合规核查
## SKILL 定位
贸易融资业务（信用证/保理/福费廷/出口退税）的合规核查工具。本 SKILL 通过企查查商业数据库，覆盖海关信用等级、进出口资质、关键人员限出境、历史行政处罚、出口退税资格、反洗钱 AML 合规六大维度，输出 A/B/C/D 四档准入评级。
## 共享引用
- MCP 工具映射表：参见本目录下的 `mcp-tools-map.md`
- MCP 缓存约定：参见本目录下的 `mcp-cache-guide.md`
> **核心原则**：调用 MCP 前先检查 `./[公司名]MCP查询结果/` 目录下的缓存文件。命中则跳过调用。
## MCP 依赖
- **必选**: `qcc-company` — 工商登记、UBO 穿透
- **必选**: `qcc-risk` — 司法风险、税收违法
- **强烈建议**: `qcc-operation` — 海关信用（核心）、资质证书、纳税信用
- **强烈建议**: `qcc-executive` — 关键人员限出境
## 工作流
### 维度一：海关信用等级
工具：`mcp__qcc-operation__get_import_export_credit`
海关信用等级处置：
| 海关信用等级 | 建议 |
|------------|------|
| 高级认证企业（AEO Advanced）| A 级准入，优先受理 |
| 一般认证企业 | B 级准入，正常受理 |
| 一般信用企业 | C 级准入，加强审查 |
| 失信企业 | **D 级，拒绝业务** |
### 维度二：进出口资质证书
工具：`mcp__qcc-operation__get_qualifications`
核查：进出口经营资格、品类专项许可、资质有效期。
### 维度三：进出口关键人员限出境（核心否决项）
工具：`mcp__qcc-executive__get_executive_exit_restriction`
对法定代表人、实际控制人做限制出境扫描：
- 任一方被限制出境 → **D 级，拒绝业务**
- 跨境业务中，关键人员无法出境意味着业务连续性、单据流转、境外收付款全部受阻
### 维度四：历史行政处罚
工具：
- `mcp__qcc-risk__get_administrative_penalty` — 当前行政处罚
- `mcp__qcc-executive__get_executive_historical_admin_penalty` — 历史行政处罚（人员维度参考）
识别"修复型 vs 连年违规型"主体：
- 海关/税务违规已超过 3 年且无复发 → 修复型，可准入
- 近 3 年内有海关/税务违规 → 连年违规型，下调评级
### 维度五：出口退税资格
工具：
- `mcp__qcc-risk__get_tax_violation` — 税收违法（直接影响退税资格）
- `mcp__qcc-risk__get_tax_arrears_notice` — 欠税公告
- `mcp__qcc-risk__get_tax_abnormal` — 税务异常
税收违法 → 出口退税资格暂停或取消 → 直接 D 级。
### 维度六：反洗钱 AML 合规
工具：
- `mcp__qcc-company__get_beneficial_owners` — UBO 识别
- `mcp__qcc-executive__get_executive_beneficial_owner` — 反查 UBO
- `mcp__qcc-executive__get_executive_dishonest` — UBO 个人失信
FATF Recommendation 对标：UBO 识别 + 制裁筛查 + PEP 检测（基于公开信息推断）。
## 综合评级
| 评级 | 核心标准 | 处置 |
|------|---------|------|
| **A 级** | 高级认证+资质齐全+人员清洁+无违规+UBO 清洁 | 通过，正常开展业务 |
| **B 级** | 一般认证+资质齐全+有已修复历史+UBO 清洁 | 通过，加强单证审核 |
| **C 级** | 一般信用+轻微历史违规或资质临期+UBO 有轻微瑕疵 | 附条件通过，追加保证金 |
| **D 级** | 失信企业/海关失信/税收违法/关键人员限出境/UBO 严重风险 | **拒绝业务** |
## 输出模板
1. Decision Pack（评级+关键判断+推荐 Action）
2. 数据来源
3. 主体基本信息
4. 海关信用等级
5. 进出口资质证书
6. 关键人员限出境
7. 历史行政处罚追溯
8. 出口退税资格
9. 反洗钱 AML 合规
10. 综合评级 × 处置建议
## 参数
- `--format md|docx|pptx`：输出格式，默认 md
## 边界与免责
本 SKILL 基于企查查商业数据库公开数据生成，不替代专业财务审计/律师尽调/技术评估。国际制裁清单（OFAC/UN/EU）不在覆盖范围内。
