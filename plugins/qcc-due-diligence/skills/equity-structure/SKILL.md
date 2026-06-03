---
name: 股权结构穿透分析
description: 投资决策前的控制权核查，多层股权穿透+历史变迁分析，识别实控人、一致行动人、隐性关联与关联交易风险。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers:
  - qcc-company
  - qcc-executive
  - qcc-operation
tags:
  - 股权穿透
  - 控制权
  - 一致行动人
  - UBO
  - 关联交易
  - 投资尽调
model: deepseek-v4-pro
---

> **⚠️ 环境依赖提醒**：如遇到 Python/pandoc/markitdown 未安装或命令找不到等电脑环境问题，请访问 "企业信息检索基本环境配置" skill 完成环境配置。

# 股权结构穿透分析
## SKILL 定位
服务于投资尽调和并购审查场景的控制权核查。股权结构是商业帝国的骨架——表面上的 CEO 可能不是真正的控制人，登记上的大股东可能是代持人。
本 SKILL 通过企查查商业数据库，执行多层股权穿透 + 历史股权变迁双层分析，识别实际控制人、一致行动人、隐性关联关系，输出控制权脆弱性评估。
## 共享引用
- MCP 工具映射表：参见本目录下的 `mcp-tools-map.md`
- MCP 缓存约定：参见本目录下的 `mcp-cache-guide.md`
> **核心原则**：调用 MCP 前先检查 `./[公司名]MCP查询结果/` 目录下的缓存文件。命中则跳过调用。
## MCP 依赖
- **必选**: `qcc-company` — 当前股东、实控人、UBO、对外投资
- **强烈建议**: `qcc-executive` — UBO 自然人画像与关联企业
> ⚠️ 历史股权变迁：通过 `mcp__qcc-company__get_change_records`（工商变更中的股东变更记录）+ `mcp__qcc-executive__get_executive_historical_investments`（人员历史投资变化）推断。`get_historical_shareholders` 工具当前不可用。
## 通用执行原则
1. **穿透到自然人为止**——终点是自然人，不是合伙企业或控股公司
2. **交叉持股的循环要切断**——识别 A→B→C→A 三角交叉，做对等抵消处理
3. **一致行动人从证据链推断**——MCP 不直接披露协议，但可通过共同投资/共同任职/同一控制人推断
4. **历史股权变迁反映估值曲线**——通过历轮融资时的股东进入与退出识别估值拐点
5. **控制权争议预警**——最大股东 < 30% 且 Top3 合计 < 50%，控制权争议概率高
## 工作流
### 维度一：当前股权结构（直接股东）
工具链：
- `mcp__qcc-company__get_shareholder_info` — 直接股东清单
- `mcp__qcc-company__get_actual_controller` — 实际控制人
产出：直接股东列表（姓名/机构名、类型、持股比例、认缴/实缴出资额）。
### 维度二：向上穿透（第 2-N 层）
对每个机构股东递归调用：
- `mcp__qcc-company__get_shareholder_info`
- 直到遇到"自然人"或"国资委"或"境外主体"为止
**穿透终止条件**：
- 下一层是自然人 → 终止，记录该自然人+穿透路径累计持股比例
- 下一层是国资委 → 终止，标注"国资控股"
- 下一层是境外主体（BVI/Cayman/香港公司等）→ 标注"境外穿透受限"
- 循环交叉持股 → 对等抵消后终止
### 维度三：UBO 识别与自然人画像
工具链：
- `mcp__qcc-company__get_beneficial_owners` — 平台算法识别 UBO
- `mcp__qcc-executive__get_executive_beneficial_owner` — 以自然人为锚反查 UBO 地位
**UBO 阈值判定**（对齐央行 3 号令）：
- 直接+间接持股 ≥ 25% 的自然人
- 通过协议/投票权实际控制的自然人
- 高管层兜底（如无 25%+ 股东，则法代/董事长/CEO 作为 UBO）
### 维度四：历史股权变迁
工具链：
- `mcp__qcc-company__get_change_records` — 工商变更记录（重点看股东变更）
- `mcp__qcc-executive__get_executive_historical_investments` — 历史对外投资
- `mcp__qcc-operation__get_financing_records` — 融资记录（估值推算用）
**历史股权变迁输出**：
- 已退出股东姓名+曾持股比例+退出日期（从变更记录推断）
- 新进入股东+持股比例+进入日期
- 形成"股东进退时间轴"
**估值曲线推算**：
- 结合历史融资记录，推算历轮投资估值
- 识别"估值跃升 > 5 倍"或"估值倒挂"等异常点
### 维度五：一致行动人与关联关系识别
工具链：
- `mcp__qcc-executive__get_executive_related_companies` — UBO 自然人的关联企业
- `mcp__qcc-executive__get_executive_historical_partners` — 历史合作伙伴
- `mcp__qcc-company__get_external_investments` — 企业对外投资
**一致行动人启发式判定**：
- 两个股东的实控人为同一自然人或近亲属
- 两个股东长期共同投资于本企业外的其他项目
- 两个股东存在历史合作伙伴关系
输出：疑似一致行动人清单+证据链+人工复核建议。
### 维度六：控制权脆弱性评估
| 最大股东持股 | Top3 合计 | 判定 |
|------------|----------|------|
| > 50% | — | **稳定** |
| 30-50% | > 60% | **相对稳定** |
| < 30% | < 50% | **脆弱**（控制权争议概率高） |
## 输出模板
1. Decision Pack（股权复杂度+控制权稳定性+UBO 清晰度+关联交易风险）
2. 数据来源
3. 主体基本信息
4. 当前股权结构（多层穿透图）
5. UBO 识别清单（含自然人快扫）
6. 历史股权变迁——股东进退时间轴+估值曲线
7. 一致行动人与关联关系识别
8. 控制权脆弱性评估
9. 潜在关联交易风险清单
10. 数据来源、采集时间戳、免责声明
## 参数
- `--depth <shallow|full>`：shallow 穿透 3 层，full 深度穿透
- `--historical <true|false>`：是否包含历史变迁，默认 true
- `--format md|docx|pptx`：输出格式，默认 md
## 边界与免责
境外主体（BVI/Cayman/香港公司）经常无法穿透。一致行动人识别基于启发式推断，不替代法律认定。股权代持/协议控制/双重股权（AB股）等特殊安排无法识别。
数据来源：企查查商业数据库（qcc-company / qcc-executive / qcc-operation）。
