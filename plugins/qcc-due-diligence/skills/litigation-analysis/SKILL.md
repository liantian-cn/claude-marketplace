---
name: 诉讼风险评估
description: 对企业执行"现状+历史+核心人员"三层诉讼全景扫描，识别活跃诉讼、执行风险、关键人员涉诉，输出司法风险评估报告。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers:
  - qcc-risk
  - qcc-executive
  - qcc-company
tags:
  - 诉讼
  - 司法风险
  - 执行风险
  - 裁判文书
  - 涉诉分析
  - 法律尽调
model: deepseek-v4-pro
---

> **⚠️ 环境依赖提醒**：如遇到 Python/pandoc/markitdown 未安装或命令找不到等电脑环境问题，请访问 "企业信息检索基本环境配置" skill 完成环境配置。

# 诉讼风险评估
## SKILL 定位
服务于立案前对手方核查、授信尽调、投资尽调、供应商准入、客户信用评估、破产预警等场景的涉诉深度分析。执行"企业现状 × 企业历史 × 核心人员"三层扫描，识别活跃诉讼、历史诉讼、执行风险、关键人员个人涉诉，输出综合诉讼风险评级与决策建议。
本 SKILL 通过企查查商业数据库的 qcc-risk（当前司法）+ qcc-executive（人员涉诉+历史追溯）双引擎，实现真正的涉诉全景透视。
## 共享引用
- MCP 工具映射表：参见本目录下的 `mcp-tools-map.md`
- MCP 缓存约定：参见本目录下的 `mcp-cache-guide.md`
> **核心原则**：调用 MCP 前先检查 `./[公司名]MCP查询结果/` 目录下的缓存文件。命中则跳过调用。
## MCP 依赖
- **必选**: `qcc-risk` — 当前司法记录全量
- **必选**: `qcc-executive` — 核心人员诉讼档案维度
- **建议**: `qcc-company` — 注册资本、实控人、主要人员名单
> ⚠️ 企业历史层：企业级历史数据通过 `mcp__qcc-executive__get_executive_historical_*`（人员维度历史）推断。企业自身的裁判文书历史可从当前数据中的旧日期记录推断趋势。
## 通用执行原则
1. **不止于统计数量**——核心是案件的性质、金额、角色、结果，不得仅呈现汇总数字
2. **涉诉金额与注册资本比必算**——30% 以下可承受，30-50% 警戒，50% 以上可能触发资本重组
3. **历史数据必须入表**——不能只看当前数据
4. **未结案件的风险敞口必须量化**——按起诉金额的 30-70% 做合理估算
5. **核心人员涉诉不可缺失**——企业诉讼数据可能"被漂白"，但核心人员个人涉诉是跟人走的
6. **数据时效必须明示**——所有输出项均须标注 MCP 采集时间戳
## 工作流
### 维度一：涉诉全景 × 历史累积
工具链：
企业现状（qcc-risk）：
- `mcp__qcc-risk__get_judicial_documents` — 裁判文书
- `mcp__qcc-risk__get_case_filing_info` — 立案信息
- `mcp__qcc-risk__get_hearing_notice` — 开庭公告
- `mcp__qcc-risk__get_court_notice` — 法院公告
- `mcp__qcc-risk__get_service_notice` — 送达公告
- `mcp__qcc-risk__get_pre_litigation_mediation` — 诉前调解
人员历史（qcc-executive）：
- `mcp__qcc-executive__get_executive_historical_judicial_docs` — 历史裁判文书
- `mcp__qcc-executive__get_executive_historical_case_filing` — 历史立案
- `mcp__qcc-executive__get_executive_historical_hearing_notice` — 历史开庭
- `mcp__qcc-executive__get_executive_historical_court_notice` — 历史法院公告
- `mcp__qcc-executive__get_executive_historical_service_notice` — 历史送达
- `mcp__qcc-executive__get_executive_historical_pre_litigation_mediation` — 历史诉前调解
产出：一张"涉诉全景总表"，按"作为原告/作为被告/作为第三人"三角色、按案件性质交叉分布，区分"已结/未结/执行中"三种状态。
### 维度二：案件性质深度分类
按案由做风险特征解读：
- **合同纠纷高发** → 履约能力不足/客户质量偏差，被告合同纠纷占比超过 50% → 履约能力列为独立质疑项
- **劳动争议集中** → 用工合规瑕疵，被告劳动仲裁+诉讼 > 20 件/年 → 触发劳动合规专项审查
- **知识产权纠纷** → 细分角色：原告=正面信号，被告=产品上市威胁
- **股权/公司纠纷** → 内部治理不稳定的直接信号
- **债务纠纷** → 现金流紧张的前哨信号
- **侵权/行政/环保类** → 合规风险，IPO 审核周期内可能致命
### 维度三：执行风险双层扫描
工具链（当前层）：
- `mcp__qcc-risk__get_judgment_debtor_info` — 当前被执行人
- `mcp__qcc-risk__get_dishonest_info` — 当前失信
- `mcp__qcc-risk__get_high_consumption_restriction` — 当前限高
- `mcp__qcc-risk__get_terminated_cases` — 当前终本
- `mcp__qcc-risk__get_exit_restriction` — 限制出境
- `mcp__qcc-risk__get_equity_freeze` — 股权冻结
工具链（历史层）：
- `mcp__qcc-executive__get_executive_historical_dishonest` — 历史失信
- `mcp__qcc-executive__get_executive_historical_judgment_debtor` — 历史被执行
- `mcp__qcc-executive__get_executive_historical_high_consumption_ban` — 历史限高
- `mcp__qcc-executive__get_executive_historical_terminated_cases` — 历史终本
- `mcp__qcc-executive__get_executive_historical_equity_freeze` — 历史股权冻结
分析要点：
- 当前失信未履行/限高生效/股权冻结未解除 → 直接触发 C 级或更低
- 历史失信已全部履行 → "信用修复"正面信号
- 历史失信次数 ≥ 3 次 → 即便全部已履行，反映"不主动履行"行为模式
- "终本案件"≠"结案"，债务仍存在并可申请恢复执行
### 维度四：诉讼趋势与时间序列分析
基于数据做 5-10 年时间序列分析：
- **平稳型**：年度诉讼量变化在 ±20% 内
- **收敛型**：近 2-3 年明显下降，需判断"主动改善"还是"业务萎缩"
- **扩张型**：连续 2 年以上上升，尤其涉案金额增速快于案件数增速
- **集中爆发型**：某一年突增 3 倍以上，常见于实控人出事/重大违约
### 维度五：重点案件深度解析
重点案件识别标准：
- 涉案金额 > 注册资本 10%
- 作为被告的未结案件
- 涉及核心资产/核心业务/核心品牌
- 群体性诉讼/系列案件（> 5 件同一类型/同一对手方）
- 与实控人/法定代表人直接相关
对每件重点案件输出：案由/角色/涉案金额/案件状态/判决结果（如已结）/影响评估/风险提示。
### 维度六：核心人员诉讼档案（核心能力）
对法代、实控人、董事长、总经理 4 人分别做个人涉诉档案：
工具链：
- `mcp__qcc-executive__get_executive_judicial_docs` / `_historical_judicial_docs`
- `mcp__qcc-executive__get_executive_case_filing` / `_historical_case_filing`
- `mcp__qcc-executive__get_executive_hearing_notice` / `_historical_hearing_notice`
- `mcp__qcc-executive__get_executive_court_notice` / `_historical_court_notice`
- `mcp__qcc-executive__get_executive_service_notice` / `_historical_service_notice`
- `mcp__qcc-executive__get_executive_pre_litigation_mediation` / `_historical_pre_litigation_mediation`
- `mcp__qcc-executive__get_executive_judgment_debtor` / `_historical_judgment_debtor`
- `mcp__qcc-executive__get_executive_dishonest` / `_historical_dishonest`
- `mcp__qcc-executive__get_executive_high_consumption_ban` / `_historical_high_consumption_ban`
- `mcp__qcc-executive__get_executive_exit_restriction`
- `mcp__qcc-executive__get_executive_terminated_cases` / `_historical_terminated_cases`
- `mcp__qcc-executive__get_executive_property_reward_notice`
每人输出独立一节：个人诉讼时间轴、案由分布、角色比例、硬性失信检查、与企业诉讼的重叠度。
## 综合评级
| 评级 | 标准 | 建议 |
|------|------|------|
| **A 级** | 无当前被执行/失信；历史诉讼密度低（<2件/年）；无未结重大诉讼；核心人员无硬性失信 | 可正常合作 |
| **B 级** | 历史被执行但已全部履行；年均诉讼2-5件；或有未结但标的较小诉讼；核心人员无当前失信 | 可合作，加强监测 |
| **C 级** | 当前有被执行人或5年内历史失信；或年均诉讼>5件；或未结重大诉讼（金额>注册资本10%）| 谨慎合作，要求担保 |
| **D 级** | 当前失信；或涉诉金额>注册资本50%；或群体性诉讼；或核心人员当前失信/限高/限出境 | 强烈建议避免 |
| **F 级** | 诉讼泥潭级（文书>5000份或涉案>10亿元）；或实控人出走/刑事被告；或企业已注销/破产清算 | **绝对禁合作** |
评级采用"同时触发多项以取最低"原则。
## 输出模板
1. 执行摘要 · Decision Pack（一句话结论+关键判断表+推荐 Action+抗辩清单）
2. 数据来源与互证方法
3. 重大风险预警（仅在评级为 D 或 F 时出现）
4. 诉讼全景双源对标
5. 涉诉案件分类与趋势
   - 按角色/案由分布
   - 时间序列趋势（近 10 年分年分桶）
6. 执行风险双层扫描
7. 重点案件深度解析（Top 5-10 + 潜在风险敞口汇总）
8. 核心人员诉讼档案（每人独立成节）
9. 综合评级与合作建议
10. 数据来源、采集时间戳、免责声明
## 参数
- `--period <N年>`：历史事件追溯年限，默认 10 年
- `--type <案由>`：仅分析指定案由，默认全量
- `--person-scan <true|false>`：是否对核心人员做诉讼档案，默认 true
- `--format md|docx|pptx`：输出格式，默认 md
## 边界与免责
本 SKILL 基于企查查商业数据库公开司法数据生成。未公开判决的涉密案件、调解协议、仲裁案件不在覆盖范围。涉案金额估算基于起诉金额与判决结果，对"调解和解"类案件可能存在系统性高估。
