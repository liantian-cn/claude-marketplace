# QCC Due Diligence — 企查查企业尽职调查插件

面向金融机构的企业尽职调查工具包，通过企查查（QCC）商业数据库提供覆盖企业全生命周期风控的 13 项业务技能。

## 功能概览

| # | Skill | 中文名称 | 业务场景 |
|---|-------|---------|---------|
| 1 | `kyb-verification` | 企业主体核验 (KYB) | 对公开户、授信准入的主体真实性核验 + 34 类司法风险扫描 |
| 2 | `ubo-screening` | 受益所有人 (UBO) 穿透 | 反洗钱合规：多层股权穿透至自然人 UBO + 个人画像 + 关联企业合规联动 |
| 3 | `credit-due-diligence` | 授信尽调报告 | 授信审批前的全方位尽调 — 治理、财务、风险、关联方、行业比较 |
| 4 | `credit-monitoring` | 贷后风险定期监控 | 存量客户定期风险扫描，识别信用恶化、风险事件与预警信号 |
| 5 | `bankruptcy-monitor` | 破产预警与重整监控 | 7 大破产先行指标 + 正式破产程序跟踪 + 债权申报窗口期计算 |
| 6 | `litigation-analysis` | 诉讼风险评估 | 企业现状 × 历史 × 核心人员三层诉讼全景扫描与司法风险评级 |
| 7 | `counterparty-risk` | 交易对手风险评估 | 供应商/客户/合作方准入前的综合风险评估 |
| 8 | `trade-finance-compliance` | 贸易融资合规核查 | 信用证/保理/福费廷/出口退税的合规准入核查 (A/B/C/D 四档评级) |
| 9 | `guarantor-check` | 担保方资信核查 | 担保方代偿能力评估 + 关联担保圈识别 + 历史代偿记录核查 |
| 10 | `executive-background` | 高管背景核查 | 董监高个人失信/限高/被执行/限出境 + 在外任职 + 关联企业回溯 |
| 11 | `equity-structure` | 股权结构穿透分析 | 多层股权穿透 + 持股比例计算 + 控制链可视化 + VIE/代持架构识别 |
| 12 | `business-health-scan` | 企业经营健康度扫描 | 财务、经营活跃度、知识产权、资质荣誉多维度经营健康度评估 |
| 13 | `enterprise-info-retrieval-env-setup` | 企业信息检索基本环境配置 | Python/Pandoc/markitdown 工具链安装 + QCC_API_KEY 环境变量配置 |

## 前置条件

### 环境依赖

- **Python** >= 3.12
- **Pandoc** >= 2.0（用于 Markdown → DOCX/PPTX 格式转换）
- **markitdown**（Python 库，`pip install 'markitdown[all]'`）

如遇到环境问题，请先使用 `enterprise-info-retrieval-env-setup` skill 完成环境配置。

### API Key

所有 MCP 服务器通过 `QCC_API_KEY` 环境变量鉴权：

**Windows (PowerShell):**
```powershell
$env:QCC_API_KEY = "your-api-key-here"
# 或永久设置：
[System.Environment]::SetEnvironmentVariable('QCC_API_KEY', 'your-api-key-here', 'User')
```

**macOS / Linux:**
```bash
export QCC_API_KEY="your-api-key-here"
# 追加到 ~/.bashrc 或 ~/.zshrc 以持久化
```

## MCP 服务器

插件配置了 5 个企查查 MCP 服务器：

| 服务器 | 用途 | 端点 |
|--------|------|------|
| `qcc-company` | 企业基座 — 工商登记、股东、实控人、UBO、财报、对外投资 | `https://agent.qcc.com/mcp/company/stream` |
| `qcc-risk` | 风控大脑 — 失信、被执行、限高、股权冻结、破产重整、裁判文书等 34 类风险 | `https://agent.qcc.com/mcp/risk/stream` |
| `qcc-ipr` | 知识产权 — 专利、商标、软著、国际专利、知产出质 | `https://agent.qcc.com/mcp/ipr/stream` |
| `qcc-operation` | 经营罗盘 — 资质证书、招投标、招聘、新闻舆情、融资记录、信用评价 | `https://agent.qcc.com/mcp/operation/stream` |
| `qcc-executive` | 人员画像 — 董监高个人失信/限高/被执行/限出境 + 任职+关联企业（含历史状态） | `https://agent.qcc.com/mcp/executive/stream` |

所有端点均使用 HTTPS，通过 `Authorization: Bearer ${QCC_API_KEY}` 鉴权。

## 安装

```bash
# 克隆仓库
git clone <repo-url> qcc-due-diligence

# 在 Claude Code 中加载插件
cc --plugin-dir ./qcc-due-diligence
```

## 使用

插件中的 13 个 skill 会根据用户查询自动激活。例如：

- "帮我对这家公司做 KYB 核验" → 自动激活 `kyb-verification`
- "穿透一下这个企业的受益所有人" → 自动激活 `ubo-screening`
- "这个债务人有没有破产风险？" → 自动激活 `bankruptcy-monitor`
- "帮我做一份授信尽调报告" → 自动激活 `credit-due-diligence`

### 输出格式

所有 skill 默认输出 Markdown 格式报告。可通过 `--format` 参数转换为 Word 或 PowerPoint：

```bash
# 使用 pandoc 转换
pandoc 报告.md -o 报告.docx --from markdown --to docx
pandoc 报告.md -o 报告.pptx --from markdown --to pptx
```

## 项目结构

```
qcc-due-diligence/
├── .claude-plugin/
│   └── plugin.json          # 插件清单
├── .mcp.json                # MCP 服务器配置
├── skills/                  # 13 个业务技能
│   ├── bankruptcy-monitor/  # 破产预警
│   ├── business-health-scan/
│   ├── counterparty-risk/
│   ├── credit-due-diligence/
│   ├── credit-monitoring/
│   ├── enterprise-info-retrieval-env-setup/
│   ├── equity-structure/
│   ├── executive-background/
│   ├── guarantor-check/
│   ├── kyb-verification/
│   ├── litigation-analysis/
│   ├── trade-finance-compliance/
│   └── ubo-screening/
├── LICENSE
└── README.md
```

每个 skill 目录包含：
- `SKILL.md` — 技能定义（含 YAML frontmatter、工作流、评级矩阵、输出模板）
- `mcp-tools-map.md` — MCP 工具名 → 缓存文件名映射表
- `mcp-cache-guide.md` — MCP 查询缓存约定

## 许可证

MIT License — 参见 [LICENSE](LICENSE)

## 数据来源

所有数据来自企查查（QCC）商业数据库，通过企查查开放平台 MCP 接口获取。
