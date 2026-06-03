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
