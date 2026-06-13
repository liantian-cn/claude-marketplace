# liantian cc market 环境配置指南

本指南供 **Claude Code agent** 阅读并引导用户逐步完成 [liantian cc market](https://gitee.com/liantian-cn/cc-marketplace) 中所有插件的基础环境配置。

> **用户使用方式：** 对 Claude 说 "请按 https://gitee.com/liantian-cn/cc-marketplace/blob/main/INSTALLER.md 帮我安装环境。"

## Agent 行为准则

- **逐步执行：** 按本文档顺序执行，每完成一个步骤必须等待用户确认后再继续下一步。
- **先检测再行动：** 每一步都先检查当前状态，若已配置则告知用户并跳过，避免重复操作。
- **明确提示：** 需要用户输入时，给出清晰的提示信息（包括获取 API Key 的网址和步骤）。
- **错误处理：** 若命令执行失败，告知用户失败原因和建议的解决方式，等待用户指示后继续。
- **幂等性：** 本指南可重复执行，已完成的配置会被自动检测并跳过。

---

## Phase 0: 准备工具脚本

> **目标：** 下载 `set_env.py`，该脚本用于安全读写 `~/.claude/settings.json` 中的环境变量。

### Step 0.1: 检测 Python 环境

运行以下命令确认 Python 可用：

```bash
python --version
```

- **成功：** 报告 Python 版本，进入 Step 0.2。
- **失败：** 提示用户 "需要安装 Python 3.8+，请访问 https://www.python.org/downloads/ 下载安装。" 等待用户安装完成后重新检测。

### Step 0.2: 下载 set_env.py

```bash
curl -o set_env.py https://raw.giteeusercontent.com/liantian-cn/cc-marketplace/raw/main/scripts/set_env.py
```

- **成功：** 报告 "✅ set_env.py 下载完成"，进入 Step 0.3。
- **失败：** 提示用户 "下载失败，请检查网络连接。可尝试手动下载：https://raw.giteeusercontent.com/liantian-cn/cc-marketplace/raw/main/scripts/set_env.py"。

### Step 0.3: 验证 set_env.py 可运行

```bash
python set_env.py list
```

- **成功：** 报告输出结果（当前可能显示无环境变量），进入 Step 0.4。
- **失败：** 报告错误并等待用户排查。

### Step 0.4: 确认

向用户报告：
> "Phase 0 完成。工具脚本已就绪。当前已配置的环境变量：[从上述命令获取的列表]。是否继续进入 Phase 1（必选 API 设置）？"

等待用户确认后进入 Phase 1。

---

## Phase 1: 必选 API 设置

> **目标：** 配置 3 个必选 API Key。这些 API 是插件运行的基础依赖，**不可跳过**。

---

### 1.1 QCC_API_KEY（企查查数据 API）

**用途：** 企查查商业数据库查询——公司信息、风险扫描、知识产权、经营状况、高管信息等。
**必选/可选：** 🔴 必选，不可跳过
**变量名：** `QCC_API_KEY`

#### Step 1: 检测是否已配置

```bash
python set_env.py get QCC_API_KEY
```

- **已配置 →** 报告 "✅ QCC_API_KEY 已配置" 并显示当前值（脱敏），跳到 Step 5 确认。
- **未配置 →** 进入 Step 2。

#### Step 2: 提示用户获取

向用户输出：

> "### 配置 QCC_API_KEY（企查查 API）
>
> 企查查 API 是尽职调查插件的核心依赖，用于查询企业工商信息、风险数据、知识产权、经营状况等。
>
> **获取方式：**
> 1. 访问 https://agent.qcc.com/profile/api-key
> 2. 使用企查查扫码登录
> 3. 复制 API Key（格式：`MK` 开头的一串字符）
> 4. 💡 提示：API Key 是 `qcc init --authorization "Bearer xxxxxx"` 命令中 `xxxxxx` 的部分
> 5. ⚠️ 需要充值才能使用
>
> **请输入你的 QCC_API_KEY：**"

等待用户输入。

#### Step 3: 设置 API Key

用户输入后，运行：

```bash
python set_env.py set QCC_API_KEY <用户输入的值>
```

- **成功：** 报告 "已写入 QCC_API_KEY"。
- **失败：** 报告错误信息，等待用户指示。

#### Step 4: 验证格式

检查用户输入的值：
- 是否以 `MK` 开头？
- **是 →** 报告 "✅ 格式正确"。
- **否 →** 警告用户 "⚠️ QCC_API_KEY 通常以 `MK` 开头，你输入的值可能不正确。是否继续？" 等待用户确认。

#### Step 5: 确认

报告 "✅ QCC_API_KEY 配置完成"，等待用户确认后进入 1.2。

---

### 1.2 DASHSCOPE_API_KEY（阿里云百炼搜索 API）

**用途：** 阿里云 DashScope 百炼 WebSearch MCP 服务，提供中文搜索引擎能力。
**必选/可选：** 🔴 必选，不可跳过
**变量名：** `DASHSCOPE_API_KEY`

#### Step 1: 检测是否已配置

```bash
python set_env.py get DASHSCOPE_API_KEY
```

- **已配置 →** 报告 "✅ DASHSCOPE_API_KEY 已配置"，跳到 Step 5。
- **未配置 →** 进入 Step 2。

#### Step 2: 提示用户获取

向用户输出：

> "### 配置 DASHSCOPE_API_KEY（阿里云百炼搜索）
>
> 阿里云百炼 WebSearch 提供中文网络搜索能力。
>
> **获取方式：**
> 1. 访问 https://bailian.console.aliyun.com/cn-beijing?tab=app#/mcp-market/detail/WebSearch
> 2. 使用支付宝扫码登录
> 3. 点击「立即开通」开通百炼服务
> 4. 访问 https://bailian.console.aliyun.com/cn-beijing?tab=app#/api-key
> 5. 创建 API Key 并复制
> 6. 💡 每月有免费额度
>
> **请输入你的 DASHSCOPE_API_KEY（应以 `sk-` 开头）：**"

等待用户输入。

#### Step 3: 设置 API Key

```bash
python set_env.py set DASHSCOPE_API_KEY <用户输入的值>
```

#### Step 4: 验证格式

- 是否以 `sk-` 开头？
- **是 →** 报告 "✅ 格式正确"。
- **否 →** 警告用户 "⚠️ DASHSCOPE_API_KEY 通常以 `sk-` 开头，你输入的值可能不正确。是否继续？"

#### Step 5: 确认

报告 "✅ DASHSCOPE_API_KEY 配置完成"，等待用户确认后进入 1.3。

---

### 1.3 BAIDU_API_KEY（百度搜索 API）

**用途：** 百度 AI 搜索 MCP 服务，提供百度搜索结果。
**必选/可选：** 🔴 必选，不可跳过
**变量名：** `BAIDU_API_KEY`

#### Step 1: 检测是否已配置

```bash
python set_env.py get BAIDU_API_KEY
```

- **已配置 →** 报告 "✅ BAIDU_API_KEY 已配置"，跳到 Step 5。
- **未配置 →** 进入 Step 2。

#### Step 2: 提示用户获取

向用户输出：

> "### 配置 BAIDU_API_KEY（百度 AI 搜索）
>
> 百度 AI 搜索提供基于百度搜索引擎的网络搜索能力。
>
> **获取方式：**
> 1. 访问 https://console.bce.baidu.com/qianfan/tools/toolsCenter，开通百度搜索服务
> 2. 访问 https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey
> 3. 获取 API Key 并复制
> 4. 💡 每月有免费额度
>
> **请输入你的 BAIDU_API_KEY（应以 `bce-v3/` 开头）：**"

等待用户输入。

#### Step 3: 设置 API Key

```bash
python set_env.py set BAIDU_API_KEY <用户输入的值>
```

#### Step 4: 验证格式

- 是否以 `bce-v3/` 开头？
- **是 →** 报告 "✅ 格式正确"。
- **否 →** 警告用户 "⚠️ BAIDU_API_KEY 通常以 `bce-v3/` 开头，你输入的值可能不正确。是否继续？"

#### Step 5: 确认

报告 "✅ BAIDU_API_KEY 配置完成"，等待用户确认后进入 Phase 2。

---

## Phase 2: 可选 API 设置

> **目标：** 配置 2 个可选 API Key。这些 API 可增强搜索能力，但**可以跳过**。

在 Phase 2 开始时告知用户：
> "接下来是 2 个可选 API 的设置。它们可以增强搜索能力，但不是必须的。你随时可以说「跳过」来跳过当前 API，或「全部跳过」跳过所有可选 API。"

---

### 2.1 TAVILY_API_KEY（Tavily 搜索 API）

**用途：** Tavily 搜索引擎，擅长英文内容的深度搜索。
**必选/可选：** 🟡 可选，可跳过
**变量名：** `TAVILY_API_KEY`

#### Step 1: 检测是否已配置

```bash
python set_env.py get TAVILY_API_KEY
```

- **已配置 →** 报告 "✅ TAVILY_API_KEY 已配置"，跳到 Step 5。
- **未配置 →** 进入 Step 2。

#### Step 2: 提示用户获取或跳过

向用户输出：

> "### 配置 TAVILY_API_KEY（Tavily 搜索 — 可选）
>
> Tavily 提供面向 AI 的搜索引擎，擅长英文内容深度搜索。
>
> **获取方式：**
> 1. 访问 https://app.tavily.com/home
> 2. 登录/注册 Tavily 账号
> 3. 在控制台创建或复制 API Key
> 4. 💡 每月有免费额度
> 5. 📋 格式：`tvly-` 开头
>
> **请输入你的 TAVILY_API_KEY，或回复「跳过」：**"

等待用户输入。

- 若用户说「跳过」→ 报告 "⏭️ 已跳过 TAVILY_API_KEY"，进入 2.2。
- 若用户输入 API Key → 进入 Step 3。

#### Step 3: 设置 API Key

```bash
python set_env.py set TAVILY_API_KEY <用户输入的值>
```

#### Step 4: 验证格式

- 是否以 `tvly-` 开头？
- **是 →** 报告 "✅ 格式正确"。
- **否 →** 警告用户但继续。

#### Step 5: 确认

报告 "✅ TAVILY_API_KEY 配置完成"（或 "⏭️ 已跳过"），等待用户确认后进入 2.2。

---

### 2.2 BOCHA_API_KEY（博查搜索 API）

**用途：** 博查开放平台搜索 API，提供中文互联网搜索能力。
**必选/可选：** 🟡 可选，可跳过
**变量名：** `BOCHA_API_KEY`

#### Step 1: 检测是否已配置

```bash
python set_env.py get BOCHA_API_KEY
```

- **已配置 →** 报告 "✅ BOCHA_API_KEY 已配置"，跳到 Step 5。
- **未配置 →** 进入 Step 2。

#### Step 2: 提示用户获取或跳过

向用户输出：

> "### 配置 BOCHA_API_KEY（博查搜索 — 可选）
>
> 博查开放平台提供中文互联网搜索能力。
>
> **获取方式：**
> 1. 访问 https://open.bochaai.com/overview
> 2. 登录/注册博查开放平台账号
> 3. 在控制台创建或复制 API Key
> 4. ⚠️ 无免费额度，按次付费
> 5. 📋 格式：`sk-` 开头
>
> **请输入你的 BOCHA_API_KEY，或回复「跳过」：**"

等待用户输入。

- 若用户说「跳过」→ 报告 "⏭️ 已跳过 BOCHA_API_KEY"，进入 Phase 3。
- 若用户输入 API Key → 进入 Step 3。

#### Step 3: 设置 API Key

```bash
python set_env.py set BOCHA_API_KEY <用户输入的值>
```

#### Step 4: 验证格式

- 是否以 `sk-` 开头？
- **是 →** 报告 "✅ 格式正确"。
- **否 →** 警告用户但继续。

#### Step 5: 确认

报告 "✅ BOCHA_API_KEY 配置完成"（或 "⏭️ 已跳过"），等待用户确认后进入 Phase 3。

---

## Phase 3: 安装插件市场与插件

> **目标：** 添加 liantian-cc-market 市场源并安装插件。

---

### 3.1 添加市场源

#### Step 1: 检测是否已添加

```bash
claude plugin marketplace list
```

检查输出中是否包含 `liantian-cc-market`。

- **已添加 →** 报告 "✅ 市场源 liantian-cc-market 已添加"，跳到 Step 4。
- **未添加 →** 进入 Step 2。

#### Step 2: 添加市场源

```bash
claude plugin marketplace add https://gitee.com/liantian-cn/cc-marketplace.git
```

- **成功：** 报告 "✅ 市场源添加成功"。
- **失败：** 报告错误信息，提示用户检查网络和 Git 配置，等待用户指示。

#### Step 3: 验证

```bash
claude plugin marketplace list
```

确认 `liantian-cc-market` 出现在列表中。

#### Step 4: 确认

报告 "✅ 市场源 liantian-cc-market 已就绪"，等待用户确认后进入 3.2。

---

### 3.2 安装 essentials 插件

> **说明：** `essentials` 是其他插件的基础依赖，**必须先安装**。

#### Step 1: 检测是否已安装

```bash
claude plugin list
```

检查输出中是否包含 `essentials@liantian-cc-market`。

- **已安装 →** 报告 "✅ essentials 已安装"，跳到 Step 4。
- **未安装 →** 进入 Step 2。

#### Step 2: 安装插件

```bash
claude plugin install --scope user essentials@liantian-cc-market
```

- **成功：** 报告 "✅ essentials 安装成功"。
- **失败：** 报告错误信息，等待用户指示。

#### Step 3: 验证

```bash
claude plugin list
```

确认 `essentials@liantian-cc-market` 出现在列表中且状态为 enabled。

#### Step 4: 确认

报告 "✅ essentials 插件已就绪"，等待用户确认后进入 3.3。

---

### 3.3 安装 qcc-due-diligence 插件

#### Step 1: 检测是否已安装

```bash
claude plugin list
```

检查输出中是否包含 `qcc-due-diligence@liantian-cc-market`。

- **已安装 →** 报告 "✅ qcc-due-diligence 已安装"，跳到 Step 4。
- **未安装 →** 进入 Step 2。

#### Step 2: 安装插件

```bash
claude plugin install --scope user qcc-due-diligence@liantian-cc-market
```

- **成功：** 报告 "✅ qcc-due-diligence 安装成功"。
- **失败：** 报告错误信息，等待用户指示。

#### Step 3: 验证

```bash
claude plugin list
```

确认 `qcc-due-diligence@liantian-cc-market` 出现在列表中且状态为 enabled。

#### Step 4: 确认

报告 "✅ qcc-due-diligence 插件已就绪"，等待用户确认后进入 Phase 4。

---

## Phase 4: 验证与总结

> **目标：** 确认所有配置正确，输出完整的环境摘要。

### Step 4.1: 列出所有环境变量

```bash
python set_env.py list
```

### Step 4.2: 列出所有已安装插件

```bash
claude plugin list
```

### Step 4.3: 输出配置摘要

根据上述命令的输出，向用户呈现以下格式的摘要表：

```markdown
## 🎉 环境配置完成！

### API 配置状态

| API | 变量名 | 状态 |
|-----|--------|------|
| 企查查数据 API | QCC_API_KEY | ✅ 已配置 / ❌ 未配置 |
| 阿里云百炼搜索 | DASHSCOPE_API_KEY | ✅ 已配置 / ❌ 未配置 |
| 百度 AI 搜索 | BAIDU_API_KEY | ✅ 已配置 / ❌ 未配置 |
| Tavily 搜索 | TAVILY_API_KEY | ✅ 已配置 / ⏭️ 已跳过 / ❌ 未配置 |
| 博查搜索 | BOCHA_API_KEY | ✅ 已配置 / ⏭️ 已跳过 / ❌ 未配置 |

### 插件安装状态

| 插件 | 来源 | 状态 |
|------|------|------|
| essentials | liantian-cc-market | ✅ 已安装 / ❌ 未安装 |
| qcc-due-diligence | liantian-cc-market | ✅ 已安装 / ❌ 未安装 |

### 下一步

- 若所有必选 API 和插件均为 ✅：环境配置完成，可以开始使用插件。
- 若存在未配置的必选项：请重新运行对应的 Phase 完成配置。
- 若可选 API 被跳过：随时可以重新运行 Phase 2 来补充配置。
```

---

## 附录：API 获取详情参考

以下为各 API 的详细获取信息，供 agent 在用户遇到问题时提供额外帮助。

### 企查查 API Key（QCC_API_KEY）

- **获取地址：** https://agent.qcc.com/profile/api-key
- **登录方式：** 企查查扫码登录
- **提示：** API Key 是 `qcc init --authorization "Bearer xxxxxx"` 命令中 `xxxxxx` 的部分
- **费用：** 需要充值
- **格式：** `MK` 开头

### 阿里云 DashScope API Key（DASHSCOPE_API_KEY）

- **开通地址：** https://bailian.console.aliyun.com/cn-beijing?tab=app#/mcp-market/detail/WebSearch
- **API Key 管理：** https://bailian.console.aliyun.com/cn-beijing?tab=app#/api-key
- **登录方式：** 支付宝扫码登录
- **步骤：** 先点击「立即开通」，再创建 API Key
- **费用：** 每月免费额度
- **格式：** `sk-` 开头

### Tavily Search API Key（TAVILY_API_KEY）

- **获取地址：** https://app.tavily.com/home
- **登录方式：** 注册/登录 Tavily 账号
- **费用：** 每月免费额度
- **格式：** `tvly-` 开头

### 博查搜索 API Key（BOCHA_API_KEY）

- **获取地址：** https://open.bochaai.com/overview
- **登录方式：** 注册/登录博查开放平台账号
- **费用：** 无免费额度，按次付费
- **格式：** `sk-` 开头

### 百度搜索 API Key（BAIDU_API_KEY）

- **服务开通：** https://console.bce.baidu.com/qianfan/tools/toolsCenter
- **API Key 管理：** https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey
- **费用：** 每月免费额度
- **格式：** `bce-v3/` 开头
