---
name: 担保方资信核查
description: 贷款担保审批前对保证人的实质偿付能力核查，计算剩余可用担保额度，评估担保占用、历史履约及法代个人偿债力。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers:
  - qcc-company
  - qcc-risk
  - qcc-executive
  - qcc-ipr
tags:
  - 担保
  - 保证人
  - 偿付能力
  - 担保额度
  - 抵押
  - 质押
  - 反担保
model: deepseek-v4-pro
---

> **⚠️ 环境依赖提醒**：如遇到 Python/pandoc/markitdown 未安装或命令找不到等电脑环境问题，请访问 "企业信息检索基本环境配置" skill 完成环境配置。

# 担保方资信核查
## SKILL 定位
服务于贷款担保审批、债券发行担保人核查、融资租赁担保方评估等场景。核心问题是"当主债务人违约时，担保方能否实际履行代偿责任？"
这不仅看担保方自身的财务状况，更要看担保方**当前还有多少未被占用的担保能力**。一家账面净资产 10 亿元的担保方，如果已对外担保 8 亿元、股权已质押 70%、土地已抵押殆尽——实际兜底能力可能不到 1 亿元。
本 SKILL 通过企查查商业数据库，执行"财务底盘 × 担保占用 × 历史履约 × 法代个人偿债力"四个维度的深度穿透评估。
## 共享引用
- MCP 工具映射表：参见本目录下的 `mcp-tools-map.md`
- MCP 缓存约定：参见本目录下的 `mcp-cache-guide.md`
> **核心原则**：调用 MCP 前先检查 `./[公司名]MCP查询结果/` 目录下的缓存文件。命中则跳过调用。
## MCP 依赖
- **必选**: `qcc-company` — 基础工商+财务数据
- **必选**: `qcc-risk` — 全量担保类工具：股权出质/股票质押/动产抵押/土地抵押/对外担保/股权冻结
- **建议**: `qcc-executive` — 担保方法代个人偿债力
## 通用执行原则
1. **净资产不等于担保能力**——理论担保上限是净资产，但实际可调度额度要扣除已被占用的部分
2. **担保关系的传递性风险必须识别**——互保圈一旦爆雷将同时击穿多个担保链
3. **连带责任与一般保证必须区分评级**——连带责任风险暴露远高于一般保证
4. **关联担保与非关联担保必须区分**——关联担保有效性需额外打折
5. **担保期限与资产有效期须对齐**——土地使用权 20 年，担保期限若超过需折价
## 工作流
### 维度一：担保方基本信息 × 财务底盘
工具链：
- `mcp__qcc-company__get_company_registration_info` — 工商登记
- `mcp__qcc-company__get_actual_controller` — 实际控制人
- `mcp__qcc-company__get_shareholder_info` — 股东结构
- `mcp__qcc-company__get_financial_data` — **3 年完整财报**（核心）
- `mcp__qcc-company__get_external_investments` — 对外投资
核心担保能力指标：
| 指标 | 计算方法 | 担保能力意义 |
|------|---------|------------|
| 净资产 | 所有者权益总计 | 理论担保上限 |
| 速动资产 | 流动资产-存货 | 紧急兑现能力 |
| 货币资金 | 资产负债表直接取 | 立即可用现金 |
| 资产负债率 | 负债合计/资产合计 | 担保能力被负债侵蚀程度 |
| 有息负债 | 负债合计-应付账款等营运负债（估算）| 真实偿债压力 |
| 对外担保/净资产 | `get_guarantee_info` 汇总/净资产 | 担保额度透支率 |
### 维度二：担保占用情况（核心维度）
工具链：
- `mcp__qcc-risk__get_equity_pledge_info` — 股权出质（非上市公司）
- `mcp__qcc-risk__get_stock_pledge_info` — 股票质押（上市公司）
- `mcp__qcc-risk__get_chattel_mortgage_info` — 动产抵押
- `mcp__qcc-risk__get_land_mortgage_info` — 土地抵押
- `mcp__qcc-risk__get_guarantee_info` — 对外担保明细
- `mcp__qcc-risk__get_equity_freeze` — 股权冻结
- `mcp__qcc-ipr__get_ipr_pledge` — 知识产权出质
**剩余可用担保额度 = 净资产 - 已质押股权对应净资产 - 已抵押资产价值 - 已对外担保余额 - 已冻结股权对应净资产**
- 若"剩余可用担保额度 < 拟担保金额 × 1.5" → 评级下调一级
- 若担保方净资产为负（资不抵债）→ 任何担保承诺均为"形式担保"，触发 D 级
- 动产抵押和土地抵押评估值打 70% 折扣后作为可变现值
### 维度三：司法风险与历史履约能力
工具链（当前层）：
- `mcp__qcc-risk__get_dishonest_info` / `get_judgment_debtor_info` / `get_high_consumption_restriction`
- `mcp__qcc-risk__get_case_filing_info` / `get_judicial_documents`
工具链（历史层）：
- `mcp__qcc-executive__get_executive_historical_dishonest` — 人员维度历史失信参考
- `mcp__qcc-risk__get_business_exception` — 含移出记录
分析要点：
- 当前失信被执行 → 已失去履约资格
- 当前股权冻结 → 现有资产已被先行债权人封锁
- 历史曾有 3 次以上被执行 → 履约意愿存疑
- 近 3 年有 1 次以上已履行的失信（"修复型"）→ 评级下调半级至一级
### 维度四：法代与实控人个人偿债力
工具链：
- `mcp__qcc-executive__get_executive_dishonest` / `_judgment_debtor` / `_high_consumption_ban` / `_exit_restriction`
- `mcp__qcc-executive__get_executive_controlled_companies` / `_investments`
- `mcp__qcc-executive__get_executive_historical_dishonest`
分析要点：
- 企业层偿付不足时，是否可刺破公司面纱追究法代/实控人责任？
- 法代/实控人是否签署了个人连带担保条款？
- 法代/实控人是否有跑路风险（限制出境）？
- 如担保方法代同时为主债务人的法代/实控人 → 关联担保不提供额外兜底
## 综合评级 × 担保建议
| 评级 | 核心标准 | 担保建议 |
|------|---------|---------|
| **A 级** | 净资产充沛+担保占用<30%+无司法风险+实控人清洁 | 可接受连带责任担保，上限净资产×50% |
| **B 级** | 净资产良好+担保占用30-50%+有已履行历史事件 | 需附加反担保或保证金，上限净资产×30% |
| **C 级** | 担保占用50-80%或近3年有已修复失信 | 需换人或补充抵押，上限净资产×10% |
| **D 级** | 担保占用>80%或当前失信/股权冻结/实控人出险 | **不建议接受担保** |
### 增信措施建议
- A 级：标准连带责任保证合同即可
- B 级：要求反担保+实控人个人连带责任+交叉违约条款
- C 级：要求追加土地抵押/应收账款质押+担保方每季财报
- D 级：建议放弃该担保方，重选新担保主体
## 输出模板
1. Decision Pack（评级+剩余可用担保额度+关键风险+T+0/T+3/T+7 Action）
2. 数据来源与互证方法
3. 担保方基本信息×财务底盘（6项核心担保能力指标）
4. 担保占用情况（详细清单）
5. 司法风险与历史履约能力
6. 法代与实控人个人偿债力
7. 综合评级×建议担保金额×增信措施
8. 数据来源、采集时间戳、免责声明
## 参数
- `--guarantee-amount <金额>`：拟担保金额（必填）
- `--guarantee-type <类型>`：担保类型（连带责任/一般保证/物保）
- `--related <true|false>`：是否关联担保，默认 false
- `--format md|docx|pptx`：输出格式，默认 md
## 边界与免责
本 SKILL 基于担保方企业主体侧数据评估，不涉及合同条款实质审查。对外担保明细可能存在披露不完整（如民间担保、隐性担保）。担保决策最终判断应由信贷审批委员会综合评审。
数据来源：企查查商业数据库（qcc-company / qcc-risk / qcc-executive / qcc-ipr）。
