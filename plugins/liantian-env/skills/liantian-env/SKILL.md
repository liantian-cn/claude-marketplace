---
name: liantian-env
description: "liantian cc market 环境配置技能。通过 /liantian-env 手动调用。完成 Python/Pandoc/markitdown 工具链安装、第三方平台 API Key 配置（企查查/阿里云/Tavily/博查/百度）、以及业务插件的安装引导。当用户需要初始化 liantian cc market 环境、配置第三方 API Key、安装 qcc-due-diligence 等插件时使用此技能。"
version: "2026-06-08"
category: "环境配置"
mcp_servers: []
tags:
  - 环境配置
  - 工具安装
  - Python
  - Pandoc
  - markitdown
  - API Key
  - 初始化
---

# liantian cc market 环境配置

## SKILL 定位

本 SKILL 服务于 [liantian cc market](https://gitee.com/liantian-cn/claude-marketplace) 中所有插件的基础环境配置需求。当用户首次使用该市场中的插件，或插件在执行过程中遇到工具链缺失时，引导用户通过本 skill 完成环境初始化。

**核心目标**：在当前电脑上完成 Python 3.12+、Pandoc 2.0+、markitdown 的安装与验证，注册各第三方平台账号并获取 API Key，将 API Key 配置到 Claude Code 的 `~/.claude/settings.json` 中。

## 共享引用

- 本 skill 为 liantian cc market 中所有插件的基础依赖。
- 本 skill 仅通过用户手动执行 `/liantian-env` 或明确要求"环境配置"时触发，不会被自动调用。

---

## 一、安装基础工具链

首次使用前，确认以下工具已安装。

### Windows（通过 winget）

```bash
# 安装 Python 3.12+
winget install -e --id Python.Python.3.12

# 安装 Pandoc 2.0+
winget install --source winget --exact --id JohnMacFarlane.Pandoc

# 安装 markitdown（Python 库，用于将常见格式转换为 Markdown）
python -m pip install 'markitdown[all]'
```

### macOS（通过 Homebrew）

```bash
# 安装 Python 3.12+
brew install python@3.12

# 安装 Pandoc
brew install pandoc

# 安装 markitdown
python -m pip install 'markitdown[all]'
```

### Linux（Debian/Ubuntu）

```bash
# 安装 Python 3.12+
sudo apt update
sudo apt install python3.12 python3-pip

# 安装 Pandoc（建议通过官方 deb 包获取最新版）
sudo apt install pandoc

# 安装 markitdown
python -m pip install 'markitdown[all]'
```

---

## 二、验证工具链安装

安装完成后，运行以下命令验证：

```bash
python --version    # 应输出 3.12.x 或更高
pandoc --version    # 应输出 2.0 或更高
markitdown --version
```

---

## 三、注册第三方平台并获取 API Key

liantian cc market 中的插件依赖以下第三方平台服务，需要提前注册账号并获取 API Key。

> **关于 `set_env.py` 脚本**：本 skill 内置了一个 Python 脚本，用于安全读写 `~/.claude/settings.json`，支持以下子命令：
>
> - `set KEY VALUE [KEY VALUE ...]` — 写入一个或多个环境变量
> - `get KEY` — 查询单个环境变量的值
> - `list` — 列出所有已配置的环境变量（API Key 自动脱敏显示）
> - `delete KEY [KEY ...]` — 删除一个或多个环境变量

### 3.1 企查查（QCC）开放平台

**适用插件**：`qcc-due-diligence`

1. 访问 [https://agent.qcc.com/profile/api-key](https://agent.qcc.com/profile/api-key)
2. 登录/注册企查查开放平台账号
3. 在个人中心创建或复制 API Key

**配置方式**（写入 `~/.claude/settings.json` 的 `env` 字段，**不是操作系统环境变量**）：

使用本 skill 内置的 `set_env.py` 脚本（安全读写 settings.json，避免 JSON 格式错误）：

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/liantian-env/scripts/set_env.py" set QCC_API_KEY "your-api-key-here"
```

### 3.2 DeepSeek API（可选，Anthropic 兼容接口）

**说明**：Claude Code 原生支持 Anthropic 模型，直接使用无需额外模型配置。如果你需要使用 DeepSeek 或其他兼容 Anthropic 接口的模型提供商作为替代后端，可以按以下步骤配置。

1. 访问 [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
2. 登录/注册 DeepSeek 账号
3. 创建 API Key

**配置方式**：

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/liantian-env/scripts/set_env.py" set \
  ANTHROPIC_AUTH_TOKEN "sk-your-deepseek-api-key" \
  ANTHROPIC_BASE_URL "https://api.deepseek.com/anthropic" \
  ANTHROPIC_MODEL "deepseek-v4-pro[1m]" \
  ANTHROPIC_DEFAULT_OPUS_MODEL "deepseek-v4-pro[1m]" \
  ANTHROPIC_DEFAULT_SONNET_MODEL "deepseek-v4-pro[1m]" \
  ANTHROPIC_DEFAULT_HAIKU_MODEL "deepseek-v4-flash"
```

### 3.3 阿里云 DashScope API Key

**适用场景**：部分插件可能需要阿里云的模型能力。

1. 访问 [https://dashscope.console.aliyun.com/apiKey](https://dashscope.console.aliyun.com/apiKey)
2. 登录阿里云账号
3. 创建 API Key

**配置方式**：

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/liantian-env/scripts/set_env.py" set DASHSCOPE_API_KEY "sk-your-dashscope-key"
```

### 3.4 Tavily Search API（必须配置）

**适用插件**：`advanced-search`

> ⚠️ **重要**：`advanced-search` 插件**依赖** `TAVILY_API_KEY` 才能正常工作。使用插件的网络搜索、内容提取、网页抓取、深度研究等功能前，**必须**先完成此 API Key 的配置。

1. 访问 [https://app.tavily.com/home](https://app.tavily.com/home)
2. 登录/注册 Tavily 账号
3. 在控制台创建或复制 API Key（格式为 `tvly-` 开头）

**配置方式**：

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/liantian-env/scripts/set_env.py" set TAVILY_API_KEY "tvly-your-tavily-key"
```

### 3.5 博查（Bocha）搜索 API

**适用插件**：`advanced-search`

> **说明**：`advanced-search` 插件使用博查 MCP 服务提供中文搜索能力，该服务通过 `BOCHA_API_KEY` 认证。

1. 访问 [https://open.bochaai.com/overview](https://open.bochaai.com/overview)
2. 登录/注册博查开放平台账号
3. 在控制台创建或获取 API Key

**配置方式**：

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/liantian-env/scripts/set_env.py" set BOCHA_API_KEY "your-bocha-api-key"
```

### 3.6 百度搜索 API（Baidu Web Search）

**适用插件**：`advanced-search`

> **说明**：`advanced-search` 插件使用百度搜索 MCP 服务（千帆平台），提供中文互联网搜索能力，该服务通过 `BAIDU_API_KEY` 认证。

1. 访问 [https://console.bce.baidu.com/qianfan/tools/toolsCenter](https://console.bce.baidu.com/qianfan/tools/toolsCenter)，开通百度搜索服务
2. 访问 [https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey](https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey)
3. 登录/注册百度智能云账号
4. 在 API Key 管理页面创建或获取 API Key

**配置方式**：

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/liantian-env/scripts/set_env.py" set BAIDU_API_KEY "your-baidu-api-key"
```

---

## 四、配置 Claude Code Subagent 模型（可选）

如果你使用第三方模型提供商的 Anthropic 兼容接口，可按需指定子代理使用的模型：

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/liantian-env/scripts/set_env.py" set \
  CLAUDE_CODE_SUBAGENT_MODEL "your-preferred-model" \
  CLAUDE_CODE_EFFORT_LEVEL "max"
```

---

## 五、安装其他业务插件

完成上述环境配置后，安装你需要的业务插件：

### 5.1 查看可用插件

```bash
claude plugin list --from-marketplace liantian-cc-market
```

### 5.2 安装插件

```bash
# 安装企查查尽职调查工具包
claude plugin install qcc-due-diligence@liantian-cc-market
```

安装完成后，运行以下命令使插件生效：

```bash
claude plugin reload
```

通过以下命令验证插件已安装：

```bash
claude plugin list
```

---

## 六、验证完整环境

全部配置完成后，运行以下检查：

```bash
# 1. 验证工具链
python --version
pandoc --version
markitdown --version

# 2. 验证 API Key 已配置（使用本 skill 内置脚本列出所有环境变量）
python "${CLAUDE_PLUGIN_ROOT}/skills/liantian-env/scripts/set_env.py" list

# 3. 验证插件已安装
claude plugin list
```

全部检查通过，即为环境配置完成。

**注意**：`~/.claude/settings.json` 中的 `env` 字段仅在 Claude Code 会话中生效，不是操作系统级环境变量。如需在终端中直接使用这些变量（如测试 MCP 连接），可临时通过 `export`（macOS/Linux）或 `$env:`（PowerShell）设置。

---

## 七、markitdown 使用方法

`markitdown` 可将 PDF、DOCX、PPTX、XLSX、HTML、CSV、JSON、XML、ZIP、图片（OCR）等常见格式转换为 Markdown：

```bash
# 基本用法：将任意文件转换为 Markdown
markitdown path-to-file.pdf -o document.md

# 支持的格式示例
markitdown 报告.pdf    -o 报告.md     # PDF → Markdown
markitdown 数据.xlsx   -o 数据.md     # Excel → Markdown
markitdown 幻灯片.pptx -o 幻灯片.md    # PPT → Markdown
markitdown 页面.html   -o 页面.md     # HTML → Markdown
```

---

## 八、pandoc 使用方法

1. **首先生成完整的 Markdown 报告**（默认格式），保存为 `.md` 文件
2. **使用 pandoc 转换为目标格式**：

```bash
# Markdown → Word (.docx)
pandoc 报告.md -o 报告.docx --from markdown --to docx

# Markdown → PowerPoint (.pptx)
pandoc 报告.md -o 报告.pptx --from markdown --to pptx
```

3. **pandoc 转换规则**：
   - `--reference-doc`：可指定参考模板（如 `--reference-doc=模板.docx`）
   - 表格自动转换为对应格式的表格
   - Markdown 中的 `#` / `##` / `###` 分别映射为 Word 标题样式或 PPT 幻灯片标题
   - 代码块使用等宽字体渲染

---

## 九、故障排查

### 常见问题

| 问题                    | 原因                                               | 解决                                                                              |
| ----------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------- |
| `python` 命令找不到     | Python 未安装或未加入 PATH                         | 重新运行安装命令，安装时勾选"Add Python to PATH"                                  |
| `pandoc` 命令找不到     | Pandoc 未安装或未加入 PATH                         | 重新运行安装命令或手动将 Pandoc 安装目录加入系统 PATH                             |
| `markitdown` 命令找不到 | markitdown 未安装或 Python Scripts 目录未加入 PATH | 运行 `python -m pip install 'markitdown[all]'`                                    |
| `markitdown` 版本过旧   | pip 未升级到最新                                   | `python -m pip install --upgrade 'markitdown[all]'`                               |
| PDF 转换失败            | 缺少 OCR 依赖                                      | 确认已安装 `markitdown[all]`（包含 PDF/图片 OCR 支持）                            |
| API Key 不生效          | 配置在了系统环境变量而非 settings.json             | 使用本 skill 内置的 `set_env.py` 脚本写入 `~/.claude/settings.json` 的 `env` 字段 |
| MCP 返回 401 鉴权失败   | API Key 值无效或过期                               | 访问对应平台检查 API Key 是否正确或重新生成                                       |
| 插件未找到              | Marketplace 未添加或名称错误                       | 运行 `claude plugin marketplace list` 确认 marketplace 已添加                     |
| settings.json 配置丢失  | 手动编辑时 JSON 格式错误                           | 使用本 skill 内置的 `set_env.py` 脚本代替手动编辑，避免 JSON 格式错误             |

---

## 边界与免责

- 本 SKILL 仅负责工具链安装与环境验证，不执行具体的业务操作。实际业务请使用对应的业务 skill。
- 不同操作系统的包管理器版本可能滞后，如 winget/brew/apt 安装的版本不满足最低要求，请访问各工具官网下载最新版本。
- 第三方平台的 API Key 获取和费用由各平台独立管理，请参考各平台的官方文档。
- `~/.claude/settings.json` 中的 `env` 字段仅在 Claude Code 内部生效，不会影响操作系统环境变量。
