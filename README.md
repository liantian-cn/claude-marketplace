# claude-marketplace

**liantian-cn 的 Claude Code 插件市场** — 面向企业尽职调查与合规风控场景。

[![Validate Plugins](https://github.com/liantian-cn/claude-marketplace/actions/workflows/validate.yml/badge.svg)](https://github.com/liantian-cn/claude-marketplace/actions/workflows/validate.yml)

## 添加此市场

```bash
claude plugin marketplace add liantian-cn https://github.com/liantian-cn/claude-marketplace
```

## 安装插件

```bash
# 安装 qcc-due-diligence（从本市场）
claude plugin install qcc-due-diligence@liantian-cn

# 安装所有可用插件
claude plugin install --from-marketplace liantian-cn
```

## 已收录插件

| 插件 | 版本 | 描述 |
|------|------|------|
| [qcc-due-diligence](./plugins/qcc-due-diligence/) | 0.1.0 | 企查查企业尽职调查 — 13 项风控技能（KYB、UBO、授信、贷后、破产、诉讼等） |

### qcc-due-diligence 详情

面向金融机构的企业尽职调查工具包，通过企查查（QCC）商业数据库提供 13 项业务技能：

| # | Skill | 业务场景 |
|---|-------|---------|
| 1 | `kyb-verification` | 对公开户、授信准入的主体真实性核验 + 34 类司法风险扫描 |
| 2 | `ubo-screening` | 多层股权穿透至自然人 UBO + 个人画像 + 关联企业合规联动 |
| 3 | `credit-due-diligence` | 授信审批前全方位尽调 — 治理、财务、风险、关联方、行业比较 |
| 4 | `credit-monitoring` | 存量客户定期风险扫描，识别信用恶化与预警信号 |
| 5 | `bankruptcy-monitor` | 7 大破产先行指标 + 正式破产程序跟踪 + 债权申报窗口期 |
| 6 | `litigation-analysis` | 企业 × 历史 × 核心人员三层诉讼全景扫描与司法风险评级 |
| 7 | `counterparty-risk` | 供应商/客户/合作方准入前综合风险评估 |
| 8 | `trade-finance-compliance` | 信用证/保理/福费廷/出口退税合规准入核查 |
| 9 | `guarantor-check` | 担保方代偿能力评估 + 关联担保圈识别 |
| 10 | `executive-background` | 董监高个人失信/限高/被执行/限出境 + 任职回溯 |
| 11 | `equity-structure` | 多层股权穿透 + 持股比例计算 + 控制链可视化 |
| 12 | `business-health-scan` | 财务、经营活跃度、知识产权多维度健康度评估 |
| 13 | `enterprise-info-retrieval-env-setup` | Python/Pandoc/markitdown 工具链安装 + API Key 配置 |

**前置条件：** 需要 `QCC_API_KEY` 环境变量。详见 [插件 README](./plugins/qcc-due-diligence/README.md)。

## 仓库结构

```
claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # 市场清单
├── .github/workflows/
│   └── validate.yml              # CI 自动校验
├── plugins/
│   └── qcc-due-diligence/        # 企查查尽职调查插件
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── .mcp.json             # 5 个 QCC MCP 服务器
│       └── skills/               # 13 个业务技能
│           ├── kyb-verification/
│           ├── ubo-screening/
│           ├── credit-due-diligence/
│           ├── credit-monitoring/
│           ├── bankruptcy-monitor/
│           ├── litigation-analysis/
│           ├── counterparty-risk/
│           ├── trade-finance-compliance/
│           ├── guarantor-check/
│           ├── executive-background/
│           ├── equity-structure/
│           ├── business-health-scan/
│           └── enterprise-info-retrieval-env-setup/
├── .gitignore
└── README.md
```

## 如何贡献新插件

1. Fork 本仓库
2. 在 `plugins/` 下创建插件目录，包含 `.claude-plugin/plugin.json`
3. 在 `.claude-plugin/marketplace.json` 的 `plugins` 数组中添加条目
4. 提交 PR

## 许可证

本仓库结构采用 MIT License。各插件使用各自的许可证。

---

**维护者：** [liantian-cn](https://github.com/liantian-cn)
