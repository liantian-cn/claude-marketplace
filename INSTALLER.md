# liantian cc market 环境配置指南

本指南用于 [liantian cc market](https://gitee.com/liantian-cn/claude-marketplace) 中所有插件的基础环境配置。首次使用该市场中的插件前，请按本文档完成环境初始化。

## 环境准备

1. 下载 https://raw.giteeusercontent.com/liantian-cn/cc-marketplace/raw/main/scripts/set_env.py

## 工作清单

- 逐项检测 API清单 内的API是否在 ~/.claude/settings.json 中已经配置。
  - 若未配置，提示用户获取。请用户访问对应网址获取API KEY后输入API KEY。
  - 若已配置则跳过。
- 安装本仓库到

```batch
claude plugin marketplace add https://gitee.com/liantian-cn/cc-marketplace.git
claude plugin install --scope user qcc-due-diligence@liantian-cc-market
claude plugin install --scope user essentials@liantian-cc-market


```

## API清单

### 企查查 API配置

- 此步不可跳过。
- API变量名 QCC_API_KEY

- 提示信息/获取方法：
  - 访问 https://agent.qcc.com/profile/api-key ，企查查扫码登录
  - 提示：APIkey是 qcc init --authorization "Bearer xxxxxx"其中xxx的部分。若有疑问，微信联系。
  - 需要充值

- 验证API：
  - KEY应该是MK开头的

### 阿里云 DashScope API Key

- 此步不可跳过。
- API变量名 DASHSCOPE_API_KEY

- 提示信息/获取方法：
  - 访问 https://bailian.console.aliyun.com/cn-beijing?tab=app#/mcp-market/detail/WebSearch ，支付宝扫码登录，点击立即开通
  - 然后访问 https://bailian.console.aliyun.com/cn-beijing?tab=app#/api-key ，创建API KEY，复制输入
  - 每月免费额度

- 验证API：
  - API KEY应该是sk-开头的

### Tavily Search API

- 此步可选
- API变量名 TAVILY_API_KEY

- 提示信息/获取方法：
  - 访问 https://app.tavily.com/home
  - 登录/注册 Tavily 账号
  - 在控制台创建或复制 API Key
  - 每月免费额度

- 验证API：
  - API KEY应该是tvly- 开头

### 博查（Bocha）搜索 API

- 此步可选
- API变量名 BOCHA_API_KEY

- 提示信息/获取方法：
  - 访问 https://open.bochaai.com/overview
  - 登录/注册博查开放平台账号
  - 在控制台创建或复制 API Key
  - 无免费额度，按次付费

- 验证API：
  - API KEY应该是sk- 开头

### 百度搜索 API（Baidu Web Search）

- 此步不可跳过。
- API变量名 BAIDU_API_KEY

- 提示信息/获取方法：
  - 访问 https://console.bce.baidu.com/qianfan/tools/toolsCenter，开通百度搜索服务
  - 访问 https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey，获取api key
  - 每月免费额度

- 验证API：
  - API KEY应该是bce-v3/ 开头
