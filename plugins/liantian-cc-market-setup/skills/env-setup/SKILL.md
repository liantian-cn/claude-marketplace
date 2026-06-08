---
name: liantian cc market 环境配置
description: "MANUAL_ONLY: 此技能仅通过 /env-setup 手动调用，不会被自动触发。用于 liantian cc market 插件的初始环境配置。"
version: "2026-06-08"
category: "环境配置"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers: []
tags:
  - 环境配置
  - 工具安装
  - Python
  - Pandoc
  - markitdown
  - API Key
  - 初始化
model: deepseek-v4-pro
---
# liantian cc market 环境配置

## SKILL 定位

本 SKILL 服务于 [liantian cc market](https://gitee.com/liantian-cn/claude-marketplace) 中所有插件的基础环境配置需求。当用户首次使用该市场中的插件，或插件在执行过程中遇到工具链缺失时，引导用户通过本 skill 完成环境初始化。

**核心目标**：在当前电脑上完成 Python 3.12+、Pandoc 2.0+、markitdown 的安装与验证，注册各第三方平台账号并获取 API Key，将 API Key 配置到 Claude Code 的 `~/.claude/settings.json` 中。

## 共享引用

- 本 skill 为 liantian cc market 中所有插件的基础依赖。
- 本 skill 仅通过用户手动执行 `/env-setup` 或明确要求"环境配置"时触发，不会被自动调用。

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

### 3.1 企查查（QCC）开放平台

**适用插件**：`qcc-due-diligence`

1. 访问 [https://agent.qcc.com/profile/api-key](https://agent.qcc.com/profile/api-key)
2. 登录/注册企查查开放平台账号
3. 在个人中心创建或复制 API Key

**配置方式**（写入 `~/.claude/settings.json` 的 `env` 字段，**不是操作系统环境变量**）：

```bash
# 使用 Claude Code 的配置命令
claude config set env.QCC_API_KEY "your-api-key-here"
```

或手动编辑 `~/.claude/settings.json`，在 `env` 对象中添加：

```json
{
  "env": {
    "QCC_API_KEY": "your-api-key-here"
  }
}
```

### 3.2 DeepSeek API（ Anthropic 兼容接口）

**说明**：liantian cc market 默认使用 DeepSeek API 作为模型后端（兼容 Anthropic 接口）。

1. 访问 [https://platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys)
2. 登录/注册 DeepSeek 账号
3. 创建 API Key

**配置方式**：

```bash
claude config set env.ANTHROPIC_AUTH_TOKEN "sk-your-deepseek-api-key"
claude config set env.ANTHROPIC_BASE_URL "https://api.deepseek.com/anthropic"
claude config set env.ANTHROPIC_MODEL "deepseek-v4-pro[1m]"
claude config set env.ANTHROPIC_DEFAULT_OPUS_MODEL "deepseek-v4-pro[1m]"
claude config set env.ANTHROPIC_DEFAULT_SONNET_MODEL "deepseek-v4-pro[1m]"
claude config set env.ANTHROPIC_DEFAULT_HAIKU_MODEL "deepseek-v4-flash"
```

或手动编辑 `~/.claude/settings.json`：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-your-deepseek-api-key",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash"
  }
}
```

### 3.3 阿里云 DashScope API Key

**适用场景**：部分插件可能需要阿里云的模型能力。

1. 访问 [https://dashscope.console.aliyun.com/apiKey](https://dashscope.console.aliyun.com/apiKey)
2. 登录阿里云账号
3. 创建 API Key

**配置方式**：

```bash
claude config set env.DASHSCOPE_API_KEY "sk-your-dashscope-key"
```

### 3.4 Tavily Search API

**适用场景**：插件中涉及网络搜索的功能。

1. 访问 [https://tavily.com/](https://tavily.com/)
2. 注册账号并获取 API Key

**配置方式**：

```bash
claude config set env.TAVILY_API_KEY "tvly-your-tavily-key"
```

---

## 四、配置 Claude Code Subagent 模型（可选）

```bash
claude config set env.CLAUDE_CODE_SUBAGENT_MODEL "deepseek-v4-flash"
claude config set env.CLAUDE_CODE_EFFORT_LEVEL "max"
```

---

## 五、添加 Marketplace 并安装插件

### 5.1 添加 liantian cc market

```bash
claude plugin marketplace add https://gitee.com/liantian-cn/claude-marketplace.git
```

### 5.2 查看可用插件

```bash
claude plugin list --from-marketplace liantian-cc-market
```

### 5.3 安装插件

```bash
# 安装企查查尽职调查工具包
claude plugin install qcc-due-diligence@liantian-cc-market

# 安装环境配置工具包
claude plugin install liantian-cc-market-setup@liantian-cc-market
```

安装完成后，运行以下命令使插件生效：

```bash
claude plugin reload
```

---

## 六、验证完整环境

全部配置完成后，运行以下检查：

```bash
# 1. 验证工具链
python --version
pandoc --version
markitdown --version

# 2. 验证 API Key 已配置（查看 settings.json 中的 env 字段）
cat ~/.claude/settings.json

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

| 问题 | 原因 | 解决 |
|------|------|------|
| `python` 命令找不到 | Python 未安装或未加入 PATH | 重新运行安装命令，安装时勾选"Add Python to PATH" |
| `pandoc` 命令找不到 | Pandoc 未安装或未加入 PATH | 重新运行安装命令或手动将 Pandoc 安装目录加入系统 PATH |
| `markitdown` 命令找不到 | markitdown 未安装或 Python Scripts 目录未加入 PATH | 运行 `python -m pip install 'markitdown[all]'` |
| `markitdown` 版本过旧 | pip 未升级到最新 | `python -m pip install --upgrade 'markitdown[all]'` |
| PDF 转换失败 | 缺少 OCR 依赖 | 确认已安装 `markitdown[all]`（包含 PDF/图片 OCR 支持） |
| API Key 不生效 | 配置在了系统环境变量而非 settings.json | 确认使用 `claude config set env.XXX` 或手动编辑 `~/.claude/settings.json` 的 `env` 字段 |
| MCP 返回 401 鉴权失败 | API Key 值无效或过期 | 访问对应平台检查 API Key 是否正确或重新生成 |
| 插件未找到 | Marketplace 未添加或名称错误 | 运行 `claude plugin marketplace list` 确认 marketplace 已添加 |
| settings.json 配置丢失 | 手动编辑时 JSON 格式错误 | 使用 `claude config set` 命令代替手动编辑，或用 `python -m json.tool` 验证 JSON 格式 |

---

## 边界与免责

- 本 SKILL 仅负责工具链安装与环境验证，不执行具体的业务操作。实际业务请使用对应的业务 skill。
- 不同操作系统的包管理器版本可能滞后，如 winget/brew/apt 安装的版本不满足最低要求，请访问各工具官网下载最新版本。
- 第三方平台的 API Key 获取和费用由各平台独立管理，请参考各平台的官方文档。
- `~/.claude/settings.json` 中的 `env` 字段仅在 Claude Code 内部生效，不会影响操作系统环境变量。
