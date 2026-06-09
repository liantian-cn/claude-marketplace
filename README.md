# liantian-cc-market

**liantian-cn 的 Claude Code 插件市场** — 面向企业尽职调查与合规风控场景。

[![Validate Plugins](https://github.com/liantian-cn/cc-marketplace//actions/workflows/validate.yml/badge.svg)](https://github.com/liantian-cn/cc-marketplace//actions/workflows/validate.yml)

## 快速开始

### 第一步：添加市场

```bash
claude plugin marketplace add --scope user https://gitee.com/liantian-cn/cc-marketplace.git
```

### 第二步：安装必备基础环境插件

```bash
claude plugin install --scope user essentials@liantian-cc-market
```

### 第三步：配置环境

按照 [INSTALLER.md](./INSTALLER.md) 完成工具链安装和 API Key 配置：

- Python 3.12+、Pandoc 2.0+、markitdown 工具链安装
- 企查查（QCC）、Tavily、博查、百度等第三方平台 API Key 配置

### 第四步（可选）：安装企查查尽职调查工具包

```bash
claude plugin install --scope user qcc-due-diligence@liantian-cc-market
```

> **提示**：`essentials` 已内置五引擎并行搜索（WebSearch + Tavily + Bailian + Bocha + Baidu），支持优雅降级——未配置的引擎自动跳过。如需启用全部引擎，请按照 [INSTALLER.md](./INSTALLER.md) 完成相关 API Key 配置。

> 后续如需单独安装某个业务插件，可使用 `claude plugin install --scope user <插件名>@liantian-cc-market`。

## 已收录插件

| 插件                                              | 版本  | 描述                                                                                |
| ------------------------------------------------- | ----- | ----------------------------------------------------------------------------------- |
| [essentials](./plugins/essentials/)               | 1.0.5 | liantian cc market 必备基础环境，包含 15 个技能——高效开发方法（构思、规划、TDD、调试、代码审查等）及五合一搜索引擎编排（WebSearch + Tavily + Bailian + Bocha + Baidu） |
| [qcc-due-diligence](./plugins/qcc-due-diligence/) | 1.0.1 | 面向金融机构的企业尽职调查工具包，通过企查查（QCC）商业数据库提供 KYB 核验、UBO 穿透、授信尽调、贷后监控、破产预警、诉讼分析、贸易融资合规等 12 项核心业务能力 |

## 仓库结构

```
claude-marketplace/
├── .claude-plugin/
│   └── marketplace.json          # 市场清单（插件目录、元数据）
├── .github/workflows/
│   └── validate.yml              # CI 自动校验 marketplace 与插件结构
├── plugins/                      # 插件存放目录
│   ├── essentials/               # 必备基础环境
│   └── qcc-due-diligence/        # 企查查企业尽职调查插件
├── scripts/
│   └── set_env.py                # 安全读写 settings.json 的辅助脚本
├── INSTALLER.md                  # 环境配置指南
├── .gitignore                    # 忽略本地配置与缓存
└── README.md                     # 本文件
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
