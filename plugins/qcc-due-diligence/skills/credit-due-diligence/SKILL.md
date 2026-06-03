---
name: 授信尽调报告
description: 信贷审批放款前的全维度企业尽调，自动完成工商核验、财务分析、司法扫描、实控人风险评估，输出授信决策底稿。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers:
  - qcc-company
  - qcc-risk
  - qcc-executive
tags:
  - 授信
  - 尽调
  - 信贷审批
  - 财务分析
  - 偿债能力
  - 信用修复
model: deepseek-v4-pro
---

> **⚠️ 环境依赖提醒**：如遇到 Python/pandoc/markitdown 未安装或命令找不到等电脑环境问题，请访问 "企业信息检索基本环境配置" skill 完成环境配置。

# 授信尽调报告
## SKILL 定位
服务于银行对公贷款审批、供应链金融授信、融资租赁风控、保理业务准入等场景的放款前企业尽调。输入目标企业全称或统一社会信用代码后，自动完成"工商核验 × 真实财务底盘 × 司法风险扫描 × 信用修复追溯 × 实控人个人风险"五位一体的授信画像，输出可直接归档的标准化尽调底稿。
本 SKILL 通过企查查商业数据库，串联 qcc-company / qcc-risk / qcc-executive 三大 MCP Server。
## 共享引用
- MCP 工具映射表：参见本目录下的 `mcp-tools-map.md`
- MCP 缓存约定：参见本目录下的 `mcp-cache-guide.md`
> **核心原则**：调用 MCP 前先检查 `./[公司名]MCP查询结果/` 目录下的缓存文件。命中则跳过调用。
## MCP 依赖
- **必选**: `qcc-company` — 工商登记、股东、实控人、对外投资、**财务数据**
- **必选**: `qcc-risk` — 失信、被执行、限高、终本、股权冻结、股权质押、动产抵押
- **强烈建议**: `qcc-executive` — 法代+实控人个人画像，识别"企业清洁×个人出险"的隐性风险
## 通用执行原则
1. **财务硬指标先行，事件信号为辅**——资产负债率/流动比率/速动比率/有息负债/EBITDA 五项核心比率
2. **历史修复必须加权评估**——5 年内已履行事件须在评级中起保守作用
3. **实控人个人兜底单独评估**——企业授信的最后防线是实控人个人偿债能力
4. **授信金额与风险敞口必须对比注册资本**——拟授信金额占注册资本比例超过 20%需特别审议
5. **数据时效明示**——所有 MCP 数据均须附采集时间戳
## 工作流
### 维度一：主体工商核验与实控人穿透
工具链：
- `mcp__qcc-company__get_company_registration_info` — 工商登记
- `mcp__qcc-company__verify_company_accuracy` — 三项匹配核验
- `mcp__qcc-company__get_shareholder_info` — 股东结构
- `mcp__qcc-company__get_actual_controller` — 实控人穿透链路
- `mcp__qcc-company__get_key_personnel` — 主要人员名单
产出：《主体身份档案》——企业全称、USCC、法代、成立年限、登记状态、注册资本与实缴率、股权结构简图、实控人识别。
### 维度二：真实财务底盘（核心能力）
工具链：
- `mcp__qcc-company__get_financial_data` — **核心工具**，3 年完整财报
- `mcp__qcc-company__get_annual_reports` — 企业年报（补充）
- `mcp__qcc-company__get_tax_invoice_info` — 税号信息
核心偿债比率矩阵：
| 指标 | 行业正常值 | 警戒线 | 致命线 |
|------|-----------|-------|-------|
| 资产负债率 | < 70% | 70-90% | > 100%（资不抵债） |
| 流动比率 | > 1.5 | 1.0-1.5 | < 1.0 |
| 速动比率 | > 1.0 | 0.5-1.0 | < 0.3 |
| 有息负债/EBITDA | < 3 倍 | 3-5 倍 | > 5 倍 |
| 经营现金流 | 正 | 微正或微负 | 持续负 |
任何一项触及致命线即直接触发 D 级评级。
### 维度三：司法风险扫描
工具链（当前层）：
- `mcp__qcc-risk__get_dishonest_info` — 失信
- `mcp__qcc-risk__get_judgment_debtor_info` — 被执行
- `mcp__qcc-risk__get_high_consumption_restriction` — 限高
- `mcp__qcc-risk__get_terminated_cases` — 终本
- `mcp__qcc-risk__get_equity_freeze` / `get_equity_pledge_info` — 股权冻结/出质
- `mcp__qcc-risk__get_chattel_mortgage_info` / `get_land_mortgage_info` — 动产/土地抵押
- `mcp__qcc-risk__get_tax_arrears_notice` — 欠税
- `mcp__qcc-risk__get_business_exception` — 经营异常
分析要点：
- 当前失信 1 条即触发 D 级
- 股权出质+股权冻结是"融资已枯竭"信号
- 对外担保余额（`mcp__qcc-risk__get_guarantee_info`）须作为表外负债纳入总负债
### 维度四：信用修复追溯
> ⚠️ 企业级历史数据需通过以下途径推断：
> - 历史失信/被执行：从当前 `get_dishonest_info` 等工具的历史数据 + `mcp__qcc-executive__get_executive_historical_dishonest`（人员维度）推断
> - 历史经营异常：`get_business_exception` 中的移出记录
> - 工商变更历史：`mcp__qcc-company__get_change_records`
5 种偿债模式识别：
- **模式 A · 始终清洁型**（10 年零失信零被执行）：评级上浮半级
- **模式 B · 修复型**（5-10 年前曾出险但已修复+近 3 年清洁）：维持标准评级
- **模式 C · 间歇失信型**（每 2-3 年一轮）：评级下调一级
- **模式 D · 连年失信型**（近 5 年每年新增失信）：直接触发 D 级
- **模式 E · 集中爆发型**（近 12-24 月突发）：增强监测+评级至少 C 级
### 维度五：实控人 × 法代个人风险
工具链（对法代和实控人分别扫描）：
- `mcp__qcc-executive__get_executive_dishonest` / `_high_consumption_ban` / `_judgment_debtor` / `_exit_restriction`
- `mcp__qcc-executive__get_executive_controlled_companies` / `_investments`
- `mcp__qcc-executive__get_executive_historical_dishonest`
分析要点：
- 实控人/法代任何一人当前失信直接触发 D 级
- 实控人限制出境是"跑路风险"最强信号 → D 级+拒绝授信
- 实控人控制的其他企业如有 3 家以上失信/被执行，整个授信建议重新评估
## 综合授信评级
| 评级 | 核心标准 | 授信建议 |
|------|---------|---------|
| **A 级** | 财务五项全部达标+无司法风险+实控人清洁+历史清洁 | 正常授信，额度上限为近3年平均净利润×3 |
| **B 级** | 财务一项警戒线+近3年清洁+历史有已修复事件 | 可授信，额度为A级的60-80%，增加风险缓释 |
| **C 级** | 财务两项以上警戒线或历史间歇失信 | 谨慎授信，要求强担保，额度为A级的30-50% |
| **D 级** | 任何致命线触发或当前失信/限高/资不抵债 | **不建议授信** |
### 授信额度建议公式
```
基础额度 = MIN(近3年平均净利润×3, 净资产×30%, 年营收×10%)
调整后额度 = 基础额度 × 评级系数
  评级系数：A=1.0 / B=0.7 / C=0.4 / D=0
```
### 风险缓释条款
- A 级：可信用贷款，仅需基础财务承诺条款
- B 级：要求实控人个人连带责任保证+关键财务承诺
- C 级：要求土地抵押/应收账款质押+实控人连带责任+交叉违约条款
- D 级：放弃信用类授信
## 输出模板
1. 执行摘要 · Decision Pack（评级+建议授信额度+关键风险信号+T+0/T+3/T+7 Action）
2. 数据来源与互证方法
3. 主体身份档案
4. 真实财务底盘（3 年对比+核心比率矩阵）
5. 司法风险扫描（当前层×历史层双层）
6. 信用修复追溯与偿债模式识别
7. 实控人与法代个人风险
8. 综合评级×授信额度×风险缓释条款
9. 数据来源、采集时间戳、免责声明
## 参数
- `--amount <金额>`：拟授信金额（必填）
- `--tenor <期限>`：授信期限（1年/3年/5年）
- `--type <类型>`：授信类型（流贷/项目贷/并购贷/供应链金融）
- `--format md|docx|pptx`：输出格式，默认 md
## 边界与免责
本 SKILL 基于企查查商业数据库公开工商+财务+司法数据生成。`get_financial_data` 对非上市小微企业可能返回空，此时会明示并保守处理。最终授信决策应由信贷审批委员会综合评审。
