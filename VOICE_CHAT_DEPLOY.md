# Voice Clone Chat 部署指南

本指南将帮助你将 Voice Clone Chat 前端和后端部署到 Render 和 GitHub Pages。

## 架构说明

- **前端**: React 应用，部署到 GitHub Pages
- **后端**: Node.js Express 应用，部署到 Render

## 步骤 1: 部署后端到 Render

### 方式一：使用 render-voice-chat.yaml（推荐）

1. **登录 Render**
   - 访问 https://render.com
   - 使用 GitHub 账号登录

2. **创建新服务**
   - 点击 "New" → "Blueprint"
   - 连接 GitHub 仓库 `Yuranz6/agent`
   - 选择 `render-voice-chat.yaml` 文件

3. **配置环境变量**
   - 在服务设置中找到 "Environment Variables"
   - 添加以下环境变量：
     ```
     ELEVENLABS_API_KEY=你的ElevenLabs_API_Key
     GOOGLE_AI_API_KEY=你的Google_AI_API_Key
     CLIENT_URL=https://yuranz6.github.io/agent
     ```
   - 注意：`ELEVENLABS_API_KEY` 和 `GOOGLE_AI_API_KEY` 需要手动设置

4. **部署**
   - 点击 "Apply" 开始部署
   - 等待部署完成（约 5-10 分钟）
   - 记录后端 URL，例如：`https://voice-clone-chat-backend.onrender.com`

### 方式二：手动创建 Web Service

1. **登录 Render**
   - 访问 https://render.com
   - 使用 GitHub 账号登录

2. **创建 Web Service**
   - 点击 "New" → "Web Service"
   - 连接 GitHub 仓库 `Yuranz6/agent`

3. **配置服务**
   - **Name**: `voice-clone-chat-backend`（或自定义）
   - **Environment**: `Node`
   - **Region**: 选择最近的区域（如 Singapore）
   - **Branch**: `main`
   - **Root Directory**: 留空（使用项目根目录）
   - **Build Command**: `npm install`
   - **Start Command**: `node server/index.js`
   - **Plan**: Free（或根据需要选择付费计划）

4. **配置环境变量**
   在 "Environment Variables" 部分添加：
   ```
   NODE_ENV=production
   PORT=10000
   CLIENT_URL=https://yuranz6.github.io/agent
   ELEVENLABS_API_KEY=你的ElevenLabs_API_Key
   GOOGLE_AI_API_KEY=你的Google_AI_API_Key
   ELEVENLABS_VOICE_ID=你的Voice_ID（可选）
   ```

5. **部署**
   - 点击 "Create Web Service"
   - Render 会自动开始部署
   - 部署完成后会获得后端 URL

## 步骤 2: 配置前端连接到后端

### 方式一：使用 GitHub Secrets（推荐）

1. **在 GitHub 仓库中设置 Secret**
   - 进入仓库 Settings → Secrets and variables → Actions
   - 点击 "New repository secret"
   - 添加：
     - **Name**: `REACT_APP_API_URL`
     - **Value**: `https://你的后端URL.onrender.com/api`
     - 例如：`https://voice-clone-chat-backend.onrender.com/api`

2. **推送代码触发部署**
   ```bash
   git push origin main
   ```
   - GitHub Actions 会自动使用 Secret 中的 API URL 构建前端

### 方式二：直接修改配置文件

1. **更新 `client/src/config.js`**
   ```javascript
   let apiUrl = process.env.REACT_APP_API_URL || 'https://你的后端URL.onrender.com/api';
   ```

2. **更新 `.github/workflows/deploy-frontend.yml`**
   ```yaml
   REACT_APP_API_URL: ${{ secrets.REACT_APP_API_URL || 'https://你的后端URL.onrender.com/api' }}
   ```

3. **提交并推送**
   ```bash
   git add client/src/config.js .github/workflows/deploy-frontend.yml
   git commit -m "Update Voice Clone Chat API URL"
   git push origin main
   ```

## 步骤 3: 启用 GitHub Pages

1. **在 GitHub 仓库中启用 Pages**
   - 进入仓库 Settings → Pages
   - Source 选择 "GitHub Actions"（不是 "Deploy from a branch"）
   - 保存设置

2. **触发部署**
   - 推送代码到 main 分支
   - GitHub Actions 会自动构建并部署前端
   - 部署完成后，前端地址为：`https://yuranz6.github.io/agent`

## 验证部署

### 1. 检查后端健康状态

```bash
curl https://你的后端URL.onrender.com/api/health
```

应该返回：
```json
{
  "status": "ok",
  "message": "Voice Clone API is running"
}
```

### 2. 访问前端

打开浏览器访问：`https://yuranz6.github.io/agent`

### 3. 测试功能

1. **克隆声音**
   - 上传音频文件
   - 等待克隆完成

2. **开始聊天**
   - 选择克隆的声音
   - 发送消息
   - 验证 AI 是否使用克隆的声音回复

## 故障排除

### 后端无法访问

1. **检查 CORS 配置**
   - 确保 `CLIENT_URL` 环境变量包含前端 URL
   - 格式：`https://yuranz6.github.io/agent`

2. **检查 API Key**
   - 确认 `ELEVENLABS_API_KEY` 和 `GOOGLE_AI_API_KEY` 已正确设置
   - 在 Render Dashboard 中验证环境变量

### 前端无法连接后端

1. **检查 API URL**
   - 打开浏览器开发者工具（F12）
   - 查看 Console 中的 "API Base URL" 日志
   - 确认 URL 正确

2. **检查网络请求**
   - 在 Network 标签页查看 API 请求
   - 确认请求 URL 正确
   - 检查是否有 CORS 错误

### 部署失败

1. **查看构建日志**
   - 在 Render Dashboard 中查看构建日志
   - 在 GitHub Actions 中查看部署日志

2. **检查依赖**
   - 确认 `package.json` 中的依赖正确
   - 确认 Node.js 版本兼容

## 更新部署

当你推送新代码到 GitHub 时：
- **后端**: Render 会自动检测并重新部署
- **前端**: GitHub Actions 会自动构建并部署到 GitHub Pages

## 获取帮助

如果遇到问题：
1. 查看 Render Dashboard 中的日志
2. 查看 GitHub Actions 中的部署日志
3. 检查 [Render 文档](https://render.com/docs)
4. 检查 [GitHub Pages 文档](https://docs.github.com/en/pages)

