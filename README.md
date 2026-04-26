# 🤖 AI Daily Digest - AI行业日报系统

为AI产品经理量身定制的自动化日报系统，每天早上9点自动采集、整理、分类AI行业最新动态，通过邮件推送。

## 📋 功能特性

✅ **多源采集** - RSS、API、网页爬虫多渠道信息聚合
✅ **智能分类** - 针对AI PM设计的9大分类体系
✅ **自动化处理** - 去重、分类、排序自动完成
✅ **邮件推送** - 每天早上9点自动发送格式精美的HTML邮件
✅ **零成本部署** - 使用GitHub Actions免费托管运行

## 📊 分类体系（AI产品经理视角）

| 分类 | 说明 | 关键词示例 |
|------|------|----------|
| 🔬 基础模型突破 | 新模型发布、SOTA刷新、能力提升 | GPT-5、Gemini、性能突破 |
| 💼 商业化进展 | API开放、定价策略、商业模式 | 价格调整、企业方案 |
| 🚀 产品应用 | 垂直应用、行业解决方案 | Copilot、自动化工具 |
| 💰 融资并购 | 融资轮次、估值、并购信息 | Series C、IPO |
| ⚖️ 政策监管 | 法规变化、安全要求、合规 | AI Act、监管指南 |
| 🔧 技术创新 | 微调、量化、推理优化 | 开源模型、RAG技术 |
| 🏢 企业战略 | 大厂组织调整、产品路线 | 战略转向、新产品发布 |
| 📊 市场竞争 | 竞品对标、生态布局 | 市场份额、合作伙伴 |
| 🛠️ 开发者工具 | 框架、库、SDK、工具链 | PyTorch、LangChain |

## 🚀 快速开始

### 前置要求

- GitHub 账户
- Gmail 账户（或其他支持SMTP的邮箱）
- Python 3.11+（本地测试用，GitHub Actions自动配置）

### 步骤1：创建GitHub仓库

1. 访问 [GitHub](https://github.com/new)
2. 创建新仓库，命名为 `ai-daily-digest`
3. 选择 Public（便于分享）
4. 勾选 "Add a README file"

### 步骤2：上传项目文件

将以下文件上传到仓库：

```
ai-daily-digest/
├── .github/workflows/
│   └── daily-digest.yml          # GitHub Actions配置
├── src/
│   ├── __init__.py
│   ├── collector.py              # 新闻采集
│   ├── processor.py              # 内容处理
│   └── sender.py                 # 邮件发送
├── config/
│   ├── sources.json              # 信息源配置
│   └── categories.json           # 分类配置
├── main.py                       # 主程序入口
├── requirements.txt              # Python依赖
├── .env.example                  # 环境变量示例
└── README.md                     # 本文件
```

### 步骤3：配置Gmail应用密码

⚠️ **不能使用Gmail账户密码！必须使用应用密码**

#### 3.1 启用两步验证
1. 访问 [Google账户安全设置](https://myaccount.google.com/security)
2. 左侧导航找到 "安全性"
3. 向下滚动到 "您的Google设备"，启用两步验证（如未启用）

#### 3.2 创建应用密码
1. 回到 [Google账户安全设置](https://myaccount.google.com/security)
2. 向下滚动到 "应用专用密码"
3. 选择应用：Mail
4. 选择设备：Windows电脑（或其他）
5. 点击生成，Google会给你一个16字符的密码（形如 `xxxx xxxx xxxx xxxx`）
6. **复制这个密码（不是你的Gmail密码）**

### 步骤4：设置GitHub Secrets

1. 进入仓库的 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"，添加以下4个密钥：

| 密钥名 | 值 | 示例 |
|--------|-----|-----|
| `GMAIL_SENDER` | 你的Gmail地址 | `your-email@gmail.com` |
| `GMAIL_PASSWORD` | Gmail应用密码 | `xxxx xxxx xxxx xxxx` |
| `RECIPIENT_EMAIL` | 收件人邮箱 | `your-email@gmail.com` |
| `NEWSAPI_KEY` | NewsAPI密钥（可选） | 从[newsapi.org](https://newsapi.org)获取 |

### 步骤5：验证工作流

1. 进入仓库的 Actions 标签页
2. 找到 "AI Daily Digest" 工作流
3. 点击 "Run workflow" → "Run workflow"
4. 等待几分钟，检查邮箱是否收到日报

✅ 如果成功，每天早上9点你都会自动收到日报！

## 📧 邮件示例

```
🤖 AI 行业日报 - 2024年04月26日

📊 今日共收集 42 条相关新闻

🔬 基础模型突破
  1. OpenAI 发布 GPT-5 新功能...
  2. Google Gemini 能力更新...

💼 商业化进展
  1. Claude API 降价30%...
  2. LLaMA 商业许可发布...

[更多分类...]
```

## 🔧 本地测试

想在本地先测试一下？

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/ai-daily-digest.git
cd ai-daily-digest

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置环境变量
cp .env.example .env
# 编辑.env，填入你的Gmail配置

# 5. 运行主程序
python main.py
```

## ⚙️ 自定义配置

### 修改推送时间

编辑 `.github/workflows/daily-digest.yml`：

```yaml
on:
  schedule:
    # 格式: 分 小时 * * *
    # 例如：每天下午3点 = "0 7 * * *" (15 - 8 = 7 UTC)
    - cron: '0 1 * * *'  # 目前是早上9点
```

### 添加/修改信息源

编辑 `config/sources.json`：

```json
{
  "rss_feeds": [
    {
      "name": "你的源名称",
      "url": "RSS_URL",
      "keywords": ["关键词1", "关键词2"]
    }
  ]
}
```

### 调整分类规则

编辑 `config/categories.json`，修改关键词或添加新分类

## 🐛 故障排除

### ❌ 无法接收邮件

**原因可能：**
- Gmail应用密码配置错误
- 环境变量未正确设置
- Gmail账户被认为有风险

**解决方案：**
1. 检查 `GMAIL_PASSWORD` 是否为16字符应用密码
2. 在 [Google安全性检查页面](https://myaccount.google.com/security) 确认账户安全
3. 检查 GitHub Actions 日志：Actions → 运行记录 → 查看日志

### ❌ 采集不到新闻

**原因可能：**
- RSS源已失效
- 关键词过于严格
- 网络连接问题

**解决方案：**
1. 验证 `config/sources.json` 中的URL是否有效
2. 降低关键词匹配的严格程度
3. 运行本地测试查看详细日志

## 📈 进阶功能（后续版本）

- [ ] 支持多语言
- [ ] 支持微信、Telegram推送
- [ ] 网页看板展示
- [ ] 用户自定义订阅偏好
- [ ] AI摘要总结
- [ ] 热点排行榜

## 📄 许可证

MIT License - 自由使用和修改

## 💬 反馈和建议

如有问题或建议，欢迎提交 Issue 或 Pull Request！

---

**更新日志：**
- 2024-04-26: 初始版本发布，支持9大分类、Gmail推送、GitHub Actions自动运行

