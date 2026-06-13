# liantian-cc-market

**liantian-cn 的 Claude Code 插件市场** — 面向企业尽职调查与合规风控场景。

[![Validate Plugins](https://github.com/liantian-cn/cc-marketplace//actions/workflows/validate.yml/badge.svg)](https://github.com/liantian-cn/cc-marketplace//actions/workflows/validate.yml)

## 快速开始

对 Claude 说：

```plain
请克隆https://gitee.com/liantian-cn/cc-marketplace.git，然后按根目录的INSTALLER.md 帮我安装环境。
```

## 已收录插件

| 插件                                              | 版本  | 描述                                                                                                                                                                   |
| ------------------------------------------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [essentials](./plugins/essentials/)               | 1.0.5 | liantian cc market 必备基础环境，包含 15 个技能——高效开发方法（构思、规划、TDD、调试、代码审查等）及五合一搜索引擎编排（WebSearch + Tavily + Bailian + Bocha + Baidu） |
| [qcc-due-diligence](./plugins/qcc-due-diligence/) | 1.0.1 | 面向金融机构的企业尽职调查工具包，通过企查查（QCC）商业数据库提供 KYB 核验、UBO 穿透、授信尽调、贷后监控、破产预警、诉讼分析、贸易融资合规等 12 项核心业务能力         |

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

## 许可证

本仓库结构采用 MIT License。各插件使用各自的许可证。

---

**维护者：** [liantian-cn](https://github.com/liantian-cn)
