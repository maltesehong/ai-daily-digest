# 📝 GitHub 部署完整指南

> 一步步教你如何在GitHub上部署这个AI日报系统

## 🎯 目标

- ✅ 创建GitHub仓库
- ✅ 上传所有项目文件
- ✅ 配置Gmail推送
- ✅ 启动自动化工作流

---

## 📋 你需要准备什么

1. **GitHub账户** - 已有（你说过创建好了✓）
2. **Gmail账户** - 用于发送日报邮件
3. **所有项目文件** - 已为你生成好

---

## 🚀 详细步骤

### 第1步：完成GitHub仓库创建

你现在在GitHub的"创建新仓库"页面，这样配置：

| 字段 | 值 |
|------|-----|
| Repository name | `ai-daily-digest` |
| Description | `Daily AI industry news digest for product managers` |
| Public/Private | **Public** ✓ |
| Add a README file | ✓ 勾选 |
| Add .gitignore | Python |
| Choose a license | MIT |

✅ 点击 **"Create repository"** 按钮

---

### 第2步：添加项目文件到仓库

创建好仓库后，你会看到仓库首页。有两种方式上传文件：

#### 方式A：在网页上直接上传（推荐新手）

1. **创建目录结构**：
   - 点击 "Add file" → "Create new file"
   - 输入文件名：`.github/workflows/daily-digest.yml`
   - 这样会自动创建 `.github/workflows/` 目录
   - 粘贴下面的 daily-digest.yml 内容
   - 点击 "Commit changes"

2. **重复上传其他文件**：
   - `src/main.py` → 粘贴 main.py 内容
   - `src/collector.py` → 粘贴 collector.py 内容
   - `src/processor.py` → 粘贴 processor.py 内容
   - `src/sender.py` → 粘贴 sender.py 内容
   - `config/sources.json` → 粘贴 sources.json 内容
   - `config/categories.json` → 粘贴 categories.json 内容
   - `requirements.txt` → 粘贴 requirements.txt 内容
   - `.env.example` → 粘贴 .env.example 内容

#### 方式B：用Git命令行（高级用户）

```bash
# 克隆仓库到本地
git clone https://github.com/yourusername/ai-daily-digest.git
cd ai-daily-digest

# 删除自动生成的README
rm README.md

# 创建目录结构
mkdir -p .github/workflows
mkdir -p src
mkdir -p config

# 复制所有文件到相应目录
# (假设你把生成的文件放在当前目录)
cp main.py ./
cp collector.py src/
cp processor.py src/
cp sender.py src/
cp sources.json config/
cp categories.json config/
cp requirements.txt ./
cp .env.example ./
cp daily-digest.yml .github/workflows/
cp README.md ./
cp GITHUB_SETUP_GUIDE.md ./

# 创建 __init__.py (Python包标记)
touch src/__init__.py

# 提交所有文件
git add .
git commit -m "Initial commit: Add AI Daily Digest system"
git push origin main
```

---

### 第3步：配置Gmail应用密码

⚠️ **这一步非常重要！不能跳过！**

#### 3.1 打开Google账户安全设置

1. 访问：https://myaccount.google.com/security
2. 用你的Gmail账户登录
3. 向下滚动找到 **"您的安全"** 部分

#### 3.2 启用两步验证（如果还未启用）

1. 找到 **"两步验证"** 选项
2. 如果显示 "未启用"，点击启用
3. 按照Google提示完成设置（需要用手机确认）

#### 3.3 创建应用密码

1. 回到 https://myaccount.google.com/security
2. 向下滚动，找到 **"应用专用密码"**
3. 如果看不到这个选项，说明你的账户可能需要更多安全配置
4. 点击 "应用专用密码"
5. **选择：** 
   - 应用：**Mail** ✓
   - 设备：**Windows PC**（或你正在用的设备）
6. 点击 **"生成"**
7. Google会生成一个16字符的密码，形如：`xxxx xxxx xxxx xxxx`
8. **复制这个密码** - 稍后需要用

---

### 第4步：设置GitHub Secrets

1. **进入仓库设置**：
   - 打开你的仓库：https://github.com/yourusername/ai-daily-digest
   - 点击上方 **"Settings"** 标签

2. **找到 Secrets**：
   - 左侧菜单 → **"Secrets and variables"** → **"Actions"**

3. **添加4个Secret**：

   **Secret 1: GMAIL_SENDER**
   - 点击 "New repository secret"
   - Name: `GMAIL_SENDER`
   - Value: `your-email@gmail.com` （你的Gmail地址）
   - 点击 "Add secret"

   **Secret 2: GMAIL_PASSWORD**
   - 点击 "New repository secret"
   - Name: `GMAIL_PASSWORD`
   - Value: `xxxx xxxx xxxx xxxx` （刚才从Google复制的16字符密码）
   - 点击 "Add secret"

   **Secret 3: RECIPIENT_EMAIL**
   - 点击 "New repository secret"
   - Name: `RECIPIENT_EMAIL`
   - Value: `your-email@gmail.com` （收件人邮箱，可以和发件人相同）
   - 点击 "Add secret"

   **Secret 4: NEWSAPI_KEY（可选）**
   - 如果你想使用NewsAPI，先去 https://newsapi.org 免费注册
   - 获得API Key后：
   - 点击 "New repository secret"
   - Name: `NEWSAPI_KEY`
   - Value: `your_newsapi_key_here`
   - 点击 "Add secret"

✅ 完成后，应该有4个Secrets显示在列表中

---

### 第5步：验证工作流正常工作

1. **进入 Actions 标签页**：
   - 打开仓库主页
   - 点击上方 **"Actions"** 标签

2. **找到 "AI Daily Digest" 工作流**：
   - 左侧菜单应该显示 "AI Daily Digest"

3. **手动触发运行**：
   - 点击 "AI Daily Digest"
   - 点击 "Run workflow" 按钮
   - 选择 "Run workflow"
   - 等待30秒左右

4. **查看运行日志**：
   - 点击最新的运行记录
   - 点击 "generate-digest" 任务
   - 查看详细日志（应该显示 ✅ 成功）

5. **检查邮箱**：
   - 检查你的收件邮箱（通常1-2分钟内收到）
   - 应该看到一封来自你Gmail的邮件，主题为 "🤖 AI 行业日报"

---

## 📅 自动运行设置

一切正常后，系统会：

✅ **每天早上9点自动运行**
- 采集最新AI新闻
- 分类整理
- 发送邮件到你的邮箱

你什么都不需要做，完全自动化！

---

## 🔍 如何查看运行历史

1. 进入仓库的 **Actions** 标签页
2. 可以看到所有运行记录（成功✓或失败✗）
3. 点击任意记录查看详细日志
4. 可以看到每个步骤的执行情况

---

## ❌ 常见问题排查

### Q1: 收不到邮件

**可能原因：**
- ❌ 使用了Gmail账户密码而非应用密码
- ❌ Secret配置错误（有空格或多余字符）
- ❌ Gmail账户被Google认为有安全风险

**解决方案：**
1. 重新检查 `GMAIL_PASSWORD` 是否为 `xxxx xxxx xxxx xxxx` 格式
2. 删除Secret，重新添加（注意没有前后空格）
3. 访问 https://myaccount.google.com/security/checkup 查看账户安全状态
4. 如果显示有异常登录，按提示处理

### Q2: Actions 运行失败

**查看错误信息：**
1. 进入 Actions → 点击失败的运行
2. 点击 "generate-digest" 任务
3. 查看日志中的错误信息
4. 常见错误：
   - `SMTPAuthenticationError` → Gmail密码错误
   - `Connection refused` → 网络问题
   - `Module not found` → 依赖安装失败

### Q3: 采集不到新闻

**原因：**
- RSS源已失效或被封
- 网络连接问题
- 关键词过于严格

**解决方案：**
1. 可以修改 `config/sources.json` 中的源
2. 调整 `config/categories.json` 中的关键词
3. 提交修改后，重新运行工作流

---

## 🎉 完成！

恭喜！现在你的AI日报系统已经成功部署了！

**从现在开始：**
- ⏰ 每天早上9点，系统自动采集新闻
- 📧 自动整理分类后发送到你的邮箱
- 📊 你可以随时在仓库的 Actions 页面查看运行状态

---

## 💡 后续优化建议

1. **定制化分类**：修改 `categories.json` 中的关键词，适应你的需求
2. **添加更多源**：在 `sources.json` 中添加你喜欢的信息源
3. **修改推送时间**：编辑 `.github/workflows/daily-digest.yml` 中的 cron 表达式
4. **监控运行状态**：定期检查 Actions 日志，确保没有失败

---

**有问题？** 检查仓库中的 README.md 和代码注释，或提交 Issue！

祝你使用愉快！🚀

