---
name: 企业信息检索基本环境配置
description: 在企业信息检索场景中，当出现 Python/pandoc/markitdown 等工具未安装、版本不兼容、命令找不到等电脑环境问题时，使用本 skill 完成当前电脑的工具链安装与环境配置。也适用于首次使用企查查相关 skill 前的环境初始化，包括 QCC_API_KEY 环境变量的检查与配置。
version: "2026-06-03"
category: "企查查企业信息skills"
compatibility: "requires: python >= 3.12, pandoc >= 2.0"
mcp_servers: []
tags:
  - 环境配置
  - 工具安装
  - Python
  - Pandoc
  - markitdown
  - 文档转换
model: deepseek-v4-pro
---
# 企业信息检索基本环境配置
## SKILL 定位
本 SKILL 服务于企查查企业信息检索系列 skill 的基础环境配置需求。当其他 skill（如 KYB 尽调、UBO 穿透、信贷监控等）在执行过程中遇到工具链缺失（Python 未安装、pandoc 找不到、markitdown 命令失败等）时，引导用户通过本 skill 完成环境初始化。
**核心目标**：在当前电脑上完成 Python 3.12+、Pandoc 2.0+、markitdown 的安装与验证。
## 共享引用
- 本 skill 为其他企查查企业信息检索系列 skill 的基础依赖，其他 skill 在遇到环境问题时应在文件头引导用户访问本 skill。
## 环境准备
首次使用前，确认以下工具已安装。

### Windows（通过 winget）
```bash
# 安装 Python 3.12+
winget install -e --id Python.Python.3.12

# 安装 Pandoc
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

### QCC_API_KEY 环境变量
企查查 MCP 服务器（qcc-company、qcc-risk、qcc-ipr、qcc-operation、qcc-executive）均通过 `Authorization: Bearer ${QCC_API_KEY}` 进行鉴权，因此需要提前配置 `QCC_API_KEY` 环境变量。

**获取 API Key**：访问 [https://agent.qcc.com/profile/api-key](https://agent.qcc.com/profile/api-key) 登录企查查开放平台账号，在个人中心获取或创建 API Key。

**Windows（PowerShell）：**
```powershell
# 临时设置（当前会话）
$env:QCC_API_KEY = "your-api-key-here"

# 永久设置（用户级）
[System.Environment]::SetEnvironmentVariable('QCC_API_KEY', 'your-api-key-here', 'User')
```

**macOS / Linux（bash/zsh）：**
```bash
# 临时设置（当前会话）
export QCC_API_KEY="your-api-key-here"

# 永久设置（追加到 shell 配置文件）
echo 'export QCC_API_KEY="your-api-key-here"' >> ~/.bashrc   # bash
echo 'export QCC_API_KEY="your-api-key-here"' >> ~/.zshrc    # zsh
```

### 验证安装
安装完成后，运行以下命令验证：
```bash
python --version    # 应输出 3.12.x 或更高
pandoc --version    # 应输出 2.0 或更高
markitdown --version
```

**验证 QCC_API_KEY 环境变量：**
```bash
# Windows PowerShell
echo $env:QCC_API_KEY

# macOS / Linux
echo $QCC_API_KEY
```
若输出为你的 API Key 值，则配置成功；若为空，请先访问 [https://agent.qcc.com/profile/api-key](https://agent.qcc.com/profile/api-key) 获取 API Key，再按照上方"QCC_API_KEY 环境变量"章节完成设置。

全部四项检查均通过（Python、Pandoc、markitdown、QCC_API_KEY），即为环境配置完成。

## markitdown 使用方法
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

在企业信息检索工作流中的应用：当用户提供了 PDF/XLSX/DOCX 等非 Markdown 格式的输入文件时，先用 `markitdown` 将其转换为 Markdown，再进行分析处理。

## pandoc 使用方法
1. **首先生成完整的 Markdown 报告**（默认格式），保存为 `报告_[公司名].md`
2. **使用 pandoc 转换为目标格式**：
```bash
# Markdown → Word (.docx)
pandoc 报告_xxx.md -o 报告_xxx.docx --from markdown --to docx --reference-doc=模板.docx

# Markdown → PowerPoint (.pptx)
pandoc 报告_xxx.md -o 报告_xxx.pptx --from markdown --to pptx
```
3. **pandoc 转换规则**：
   - `--reference-doc`：如果同目录下存在 `assets/template.docx` 或 `assets/template.pptx`，自动作为参考模板使用
   - 表格自动转换为对应格式的表格
   - Markdown 中的 `#` / `##` / `###` 分别映射为 Word 标题样式或 PPT 幻灯片标题
   - 代码块使用等宽字体渲染
4. **依赖检查**：调用 pandoc 前先检查是否已安装（`pandoc --version`），若未安装则提示用户安装并仅输出 Markdown 文件。

## 故障排查
### 常见问题
| 问题 | 原因 | 解决 |
|------|------|------|
| `python` 命令找不到 | Python 未安装或未加入 PATH | 重新运行安装命令，安装时勾选"Add Python to PATH" |
| `pandoc` 命令找不到 | Pandoc 未安装或未加入 PATH | 重新运行安装命令或手动将 Pandoc 安装目录加入系统 PATH |
| `markitdown` 命令找不到 | markitdown 未安装或 Python Scripts 目录未加入 PATH | 运行 `python -m pip install 'markitdown[all]'` 升级到最新版 |
| `markitdown` 版本过旧 | pip 未升级到最新 | `python -m pip install --upgrade 'markitdown[all]'` |
| PDF 转换失败 | 缺少 OCR 依赖 | 确认已安装 `markitdown[all]`（包含 PDF/图片 OCR 支持） |
| QCC_API_KEY 未配置 | 未设置环境变量 | 访问 [https://agent.qcc.com/profile/api-key](https://agent.qcc.com/profile/api-key) 获取 API Key，按照上方"QCC_API_KEY 环境变量"章节设置，完成后重新打开终端 |
| MCP 返回 401 鉴权失败 | QCC_API_KEY 值无效或过期 | 访问 [https://agent.qcc.com/profile/api-key](https://agent.qcc.com/profile/api-key) 检查 API Key 是否正确或重新生成，确认企查查开放平台账号有效 |

## 边界与免责
本 SKILL 仅负责工具链安装与环境验证，不执行具体的企业信息检索操作。实际检索工作请使用对应的业务 skill（如 KYB 尽调、UBO 穿透等）。
不同操作系统的包管理器版本可能滞后，如 winget/brew/apt 安装的版本不满足最低要求，请访问各工具官网下载最新版本。
