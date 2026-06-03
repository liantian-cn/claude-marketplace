# MCP 工具名 → 缓存文件名映射表

> **共享引用**: 所有 skill 均复用此映射表。每个 skill 的 SKILL.md 中引用本文件。
> **缓存目录**: `./[公司名]MCP查询结果/` —— 所有 MCP 查询结果按公司分目录存储。

## 使用约定

1. 调用 MCP 工具前，先检查 `./[公司名]MCP查询结果/[缓存文件名]` 是否存在且为今日数据
2. 若文件已存在且为今日 → 跳过 MCP 调用，直接读取文件
3. 若文件不存在 → 调用 MCP 工具，将结果保存为语义化的 Markdown 文件到 `./[公司名]MCP查询结果/` 目录下
4. 文件命名规则：`[序号]-[语义名称].md`，如 `01-工商登记信息.md`

## 一、qcc-company（企业基座，16 工具）

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__qcc-company__get_company_registration_info` | `01-工商登记信息.md` | 工商登记基本信息 |
| `mcp__qcc-company__get_company_profile` | `02-企业简介.md` | 业务简介与行业分类 |
| `mcp__qcc-company__verify_company_accuracy` | `03-主体核验.md` | 企业名+USCC+法代三项匹配 |
| `mcp__qcc-company__get_shareholder_info` | `04-股东信息.md` | 直接股东构成 |
| `mcp__qcc-company__get_actual_controller` | `05-实际控制人.md` | 实际控制人穿透 |
| `mcp__qcc-company__get_beneficial_owners` | `06-受益所有人.md` | UBO 识别(AML口径) |
| `mcp__qcc-company__get_key_personnel` | `07-主要人员.md` | 董监高名单 |
| `mcp__qcc-company__get_financial_data` | `08-财务数据.md` | 核心财务指标 |
| `mcp__qcc-company__get_annual_reports` | `09-年度报告.md` | 工商年报 |
| `mcp__qcc-company__get_external_investments` | `10-对外投资.md` | 对外投资企业列表 |
| `mcp__qcc-company__get_branches` | `11-分支机构.md` | 分公司信息 |
| `mcp__qcc-company__get_change_records` | `12-工商变更记录.md` | 工商变更历史 |
| `mcp__qcc-company__get_contact_info` | `13-联系方式.md` | 电话/邮箱/网站 |
| `mcp__qcc-company__get_tax_invoice_info` | `14-税号开票信息.md` | 纳税人信息 |
| `mcp__qcc-company__get_listing_info` | `15-上市信息.md` | 当前上市信息 |

## 二、qcc-risk（风控大脑，34 工具）

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__qcc-risk__get_dishonest_info` | `20-失信被执行人.md` | 失信记录 |
| `mcp__qcc-risk__get_judgment_debtor_info` | `21-被执行人.md` | 被执行记录 |
| `mcp__qcc-risk__get_high_consumption_restriction` | `22-限制高消费.md` | 限高记录 |
| `mcp__qcc-risk__get_exit_restriction` | `23-限制出境.md` | 企业相关人员限制出境 |
| `mcp__qcc-risk__get_terminated_cases` | `24-终本案件.md` | 终本案件 |
| `mcp__qcc-risk__get_bankruptcy_reorganization` | `25-破产重整.md` | 破产重整信息 |
| `mcp__qcc-risk__get_liquidation_info` | `26-清算信息.md` | 清算信息 |
| `mcp__qcc-risk__get_business_exception` | `27-经营异常.md` | 经营异常名录 |
| `mcp__qcc-risk__get_serious_violation` | `28-严重违法失信.md` | 严重违法失信名单 |
| `mcp__qcc-risk__get_administrative_penalty` | `29-行政处罚.md` | 行政处罚记录 |
| `mcp__qcc-risk__get_environmental_penalty` | `30-环保处罚.md` | 环保处罚记录 |
| `mcp__qcc-risk__get_equity_freeze` | `31-股权冻结.md` | 股权冻结 |
| `mcp__qcc-risk__get_equity_pledge_info` | `32-股权出质.md` | 股权出质 |
| `mcp__qcc-risk__get_chattel_mortgage_info` | `33-动产抵押.md` | 动产抵押 |
| `mcp__qcc-risk__get_land_mortgage_info` | `34-土地抵押.md` | 土地抵押 |
| `mcp__qcc-risk__get_guarantee_info` | `35-担保信息.md` | 对外担保 |
| `mcp__qcc-risk__get_tax_arrears_notice` | `36-欠税公告.md` | 欠税记录 |
| `mcp__qcc-risk__get_tax_abnormal` | `37-税务异常.md` | 税务非正常户 |
| `mcp__qcc-risk__get_tax_violation` | `38-税收违法.md` | 税收违法记录 |
| `mcp__qcc-risk__get_judicial_documents` | `39-裁判文书.md` | 法院判决文书 |
| `mcp__qcc-risk__get_case_filing_info` | `40-立案信息.md` | 法院立案 |
| `mcp__qcc-risk__get_hearing_notice` | `41-开庭公告.md` | 开庭公告 |
| `mcp__qcc-risk__get_court_notice` | `42-法院公告.md` | 法院公告 |
| `mcp__qcc-risk__get_service_notice` | `43-送达公告.md` | 法律文书送达 |
| `mcp__qcc-risk__get_pre_litigation_mediation` | `44-诉前调解.md` | 诉前调解 |
| `mcp__qcc-risk__get_stock_pledge_info` | `45-股票质押.md` | 上市公司股权质押 |
| `mcp__qcc-risk__get_judicial_auction` | `46-司法拍卖.md` | 司法拍卖 |
| `mcp__qcc-risk__get_cancellation_record_info` | `47-注销备案.md` | 企业注销备案 |
| `mcp__qcc-risk__get_simple_cancellation_info` | `48-简易注销.md` | 简易注销 |
| `mcp__qcc-risk__get_disciplinary_list` | `49-惩戒名单.md` | 惩戒名单 |
| `mcp__qcc-risk__get_default_info` | `50-违约事项.md` | 债券/票据违约 |
| `mcp__qcc-risk__get_property_asset_announcement` | `51-财产悬赏.md` | 财产悬赏公告 |
| `mcp__qcc-risk__get_public_exhortation` | `52-公示催告.md` | 公示催告(票据) |
| `mcp__qcc-risk__get_service_announcement` | `53-劳动仲裁公告.md` | 劳动仲裁公告 |

## 三、qcc-executive（人员画像，42 工具）

> **重要**: 所有 qcc-executive 工具必须同时传入 `searchKey`（企业名/USCC）和 `personName`（人员姓名）进行双锚定查询，避免同名误查。

### 当前状态工具

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__qcc-executive__get_executive_dishonest` | `[人名]-01-失信.md` | 个人失信 |
| `mcp__qcc-executive__get_executive_high_consumption_ban` | `[人名]-02-限高.md` | 个人限高 |
| `mcp__qcc-executive__get_executive_exit_restriction` | `[人名]-03-限制出境.md` | 个人限制出境 |
| `mcp__qcc-executive__get_executive_judgment_debtor` | `[人名]-04-被执行.md` | 个人被执行 |
| `mcp__qcc-executive__get_executive_terminated_cases` | `[人名]-05-终本.md` | 个人终本案件 |
| `mcp__qcc-executive__get_executive_equity_freeze` | `[人名]-06-股权冻结.md` | 个人股权冻结 |
| `mcp__qcc-executive__get_executive_equity_pledge` | `[人名]-07-股权出质.md` | 个人股权出质 |
| `mcp__qcc-executive__get_executive_stock_pledge` | `[人名]-08-股票质押.md` | 个人股票质押 |
| `mcp__qcc-executive__get_executive_admin_penalty` | `[人名]-09-行政处罚.md` | 个人行政处罚 |
| `mcp__qcc-executive__get_executive_tax_violation` | `[人名]-10-税收违法.md` | 个人税收违法 |
| `mcp__qcc-executive__get_executive_case_filing` | `[人名]-11-立案.md` | 个人法院立案 |
| `mcp__qcc-executive__get_executive_hearing_notice` | `[人名]-12-开庭.md` | 个人开庭公告 |
| `mcp__qcc-executive__get_executive_court_notice` | `[人名]-13-法院公告.md` | 个人法院公告 |
| `mcp__qcc-executive__get_executive_service_notice` | `[人名]-14-送达.md` | 个人送达公告 |
| `mcp__qcc-executive__get_executive_judicial_docs` | `[人名]-15-裁判文书.md` | 个人裁判文书 |
| `mcp__qcc-executive__get_executive_pre_litigation_mediation` | `[人名]-16-诉前调解.md` | 个人诉前调解 |
| `mcp__qcc-executive__get_executive_property_reward_notice` | `[人名]-17-财产悬赏.md` | 个人财产悬赏 |
| `mcp__qcc-executive__get_executive_valuation_inquiry` | `[人名]-18-询价评估.md` | 个人资产询价评估 |
| `mcp__qcc-executive__get_executive_positions` | `[人名]-19-在外任职.md` | 当前在外任职 |
| `mcp__qcc-executive__get_executive_legal_rep_roles` | `[人名]-20-担任法代.md` | 当前担任法代企业 |
| `mcp__qcc-executive__get_executive_controlled_companies` | `[人名]-21-控制企业.md` | 当前实际控制企业 |
| `mcp__qcc-executive__get_executive_related_companies` | `[人名]-22-关联企业.md` | 当前全部关联企业 |
| `mcp__qcc-executive__get_executive_investments` | `[人名]-23-对外投资.md` | 个人对外投资 |
| `mcp__qcc-executive__get_executive_beneficial_owner` | `[人名]-24-受益所有人.md` | 作为UBO的企业列表 |

### 历史状态工具

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__qcc-executive__get_executive_historical_dishonest` | `[人名]-H01-历史失信.md` | 个人历史失信 |
| `mcp__qcc-executive__get_executive_historical_high_consumption_ban` | `[人名]-H02-历史限高.md` | 个人历史限高 |
| `mcp__qcc-executive__get_executive_historical_judgment_debtor` | `[人名]-H03-历史被执行.md` | 个人历史被执行 |
| `mcp__qcc-executive__get_executive_historical_terminated_cases` | `[人名]-H04-历史终本.md` | 个人历史终本 |
| `mcp__qcc-executive__get_executive_historical_equity_freeze` | `[人名]-H05-历史股权冻结.md` | 个人历史股权冻结 |
| `mcp__qcc-executive__get_executive_historical_equity_pledge` | `[人名]-H06-历史股权出质.md` | 个人历史股权出质 |
| `mcp__qcc-executive__get_executive_historical_admin_penalty` | `[人名]-H07-历史行政处罚.md` | 个人历史行政处罚 |
| `mcp__qcc-executive__get_executive_historical_case_filing` | `[人名]-H08-历史立案.md` | 个人历史立案 |
| `mcp__qcc-executive__get_executive_historical_hearing_notice` | `[人名]-H09-历史开庭.md` | 个人历史开庭 |
| `mcp__qcc-executive__get_executive_historical_court_notice` | `[人名]-H10-历史法院公告.md` | 个人历史法院公告 |
| `mcp__qcc-executive__get_executive_historical_service_notice` | `[人名]-H11-历史送达.md` | 个人历史送达 |
| `mcp__qcc-executive__get_executive_historical_judicial_docs` | `[人名]-H12-历史裁判文书.md` | 个人历史裁判文书 |
| `mcp__qcc-executive__get_executive_historical_pre_litigation_mediation` | `[人名]-H13-历史诉前调解.md` | 个人历史诉前调解 |
| `mcp__qcc-executive__get_executive_historical_positions` | `[人名]-H14-历史任职.md` | 个人历史在外任职 |
| `mcp__qcc-executive__get_executive_historical_legal_rep_roles` | `[人名]-H15-历史担任法代.md` | 个人历史担任法代 |
| `mcp__qcc-executive__get_executive_historical_investments` | `[人名]-H16-历史投资.md` | 个人历史对外投资 |
| `mcp__qcc-executive__get_executive_historical_related_companies` | `[人名]-H17-历史关联企业.md` | 个人历史全部关联企业 |
| `mcp__qcc-executive__get_executive_historical_partners` | `[人名]-H18-历史合作伙伴.md` | 个人历史合作伙伴 |

## 四、qcc-operation（经营罗盘）

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__qcc-operation__get_import_export_credit` | `60-进出口信用.md` | 海关信用等级 |
| `mcp__qcc-operation__get_qualifications` | `61-资质证书.md` | 企业资质 |
| `mcp__qcc-operation__get_credit_evaluation` | `62-信用评价.md` | 纳税信用/海关信用 |
| `mcp__qcc-operation__get_honor_info` | `63-荣誉信息.md` | 企业荣誉 |
| `mcp__qcc-operation__get_bidding_info` | `64-招投标.md` | 招投标项目 |
| `mcp__qcc-operation__get_recruitment_info` | `65-招聘信息.md` | 招聘信息 |
| `mcp__qcc-operation__get_random_check` | `66-双随机抽查.md` | 双随机抽查 |
| `mcp__qcc-operation__get_news_sentiment` | `67-新闻舆情.md` | 新闻情感分析 |
| `mcp__qcc-operation__get_financing_records` | `68-融资记录.md` | 融资信息 |
| `mcp__qcc-operation__get_administrative_license` | `69-行政许可.md` | 行政许可 |
| `mcp__qcc-operation__get_taxpayer_qualification` | `70-纳税人资质.md` | 增值税纳税人资质 |
| `mcp__qcc-operation__get_telecom_license` | `71-电信许可.md` | 电信业务许可 |

## 五、qcc-ipr（知识产权）

| MCP 工具完整名 | 缓存文件名 | 业务语义 |
|---|---|---|
| `mcp__qcc-ipr__get_patent_info` | `80-专利信息.md` | 专利 |
| `mcp__qcc-ipr__get_trademark_info` | `81-商标信息.md` | 商标 |
| `mcp__qcc-ipr__get_software_copyright_info` | `82-软著信息.md` | 软件著作权 |
| `mcp__qcc-ipr__get_copyright_work_info` | `83-作品著作权.md` | 作品著作权 |
| `mcp__qcc-ipr__get_international_patent` | `84-国际专利.md` | 国际专利 |
| `mcp__qcc-ipr__get_ipr_pledge` | `85-知产出质.md` | 知识产权出质 |
| `mcp__qcc-ipr__get_standard_info` | `86-标准信息.md` | 参与制定标准 |
| `mcp__qcc-ipr__get_trademark_document` | `87-商标文书.md` | 商标评审文书 |
| `mcp__qcc-ipr__get_internet_service_info` | `88-网络服务备案.md` | ICP/APP/小程序备案 |

## ⚠️ 不可用的历史企业数据

以下业务场景原计划通过 `qcc-history` server 提供，但当前 MCP 环境中该 server 未加载。**替代方案**：

| 原计划工具 | 替代方案 |
|---|---|
| 企业历史失信 | 从 `get_dishonest_info` + 人工对比时间范围推断 |
| 企业历史被执行 | 从 `get_judgment_debtor_info` + 人工对比时间范围推断 |
| 企业历史股东 | 从 `get_shareholder_info` 当前快照 + `get_change_records` 变更记录推断 |
| 企业历史法代 | 从 `get_change_records` 变更记录中的法代变更推断 |
| 企业历史经营异常 | 从 `get_business_exception` 中的移出记录判断(已移出=历史) |
| 历史融资/上市 | 从 `get_financing_records` + `get_listing_info` 当前数据推断 |
