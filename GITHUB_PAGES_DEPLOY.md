# GitHub Pages 部署指南

本项目使用 **GitHub Pages** 部署前端，**Render** 部署后端。

## 快速开始

### 1. 启用 GitHub Pages

1. 进入 GitHub 仓库：https://github.com/Yuranz6/agent
2. 点击 **Settings** → **Pages**
3. 在 **Source** 部分：
   - 选择 **GitHub Actions**（不是 "Deploy from a branch"）
4. 保存设置

### 2. 配置后端 API URL（可选）

如果后端已部署到 Render，可以设置环境变量：

1. 进入仓库 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 添加：
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://your-render-backend-url.onrender.com/api`
   - 例如：`https://clone-i9i8.onrender.com/api`

如果不设置，前端会使用默认的 Render 后端 URL。

### 3. 推送代码触发部署

```bash
git add .
git commit -m "Configure GitHub Pages deployment"
git push origin main
```

推送后，GitHub Actions 会自动：
1. 构建 React 应用
2. 部署到 GitHub Pages

### 4. 查看部署状态

1. 进入仓库的 **Actions** 标签页
2. 查看最新的工作流运行状态
3. 部署成功后，访问：**https://yuranz6.github.io/agent**

## Render 后端部署

### 1. 登录 Render

访问 https://render.com 并使用 GitHub 账号登录

### 2. 创建 Web Service

1. 点击 **New** → **Web Service**
2. 连接 GitHub 仓库 `Yuranz6/agent`

### 3. 配置服务

- **Name**: `agent-backend`（或自定义）
- **Environment**: `Node`
- **Region**: 选择最近的区域
- **Branch**: `main`
- **Root Directory**: 留空
- **Build Command**: `npm install`
- **Start Command**: `node server/index.js`
- **Plan**: Free（或付费计划）

### 4. 配置环境变量

在 **Environment Variables** 部分添加：

```
NODE_ENV=production
PORT=10000
CLIENT_URL=https://yuranz6.github.io/agent
ELEVENLABS_API_KEY=your_elevenlabs_api_key
GOOGLE_AI_API_KEY=your_google_ai_api_key
ELEVENLABS_VOICE_ID=your_voice_id（可选）
```

### 5. 部署

点击 **Create Web Service**，Render 会自动开始部署。

部署完成后，你会获得后端 URL，例如：`https://agent-backend.onrender.com`

### 6. 更新前端 API 地址

获取 Render 后端 URL 后：

1. 在 GitHub 仓库 **Settings** → **Secrets and variables** → **Actions** 中
2. 更新或添加 `REACT_APP_API_URL` secret
3. 重新触发 GitHub Actions 部署（或推送新代码）

## 使用 render.yaml（推荐）

项目已包含 `render.yaml` 配置文件，可以：

1. 在 Render Dashboard 中点击 **New** → **Apply Manifest**
2. 选择仓库 `Yuranz6/agent`
3. 选择 `render.yaml` 文件
4. 手动添加环境变量（API keys）

## 验证部署

### 检查后端

```bash
curl https://your-render-backend-url.onrender.com/api/health
```

应该返回：`{"status":"ok","message":"Voice Clone API is running"}`

### 检查前端

1. 访问 https://yuranz6.github.io/agent
2. 打开浏览器开发者工具（F12）
3. 查看 Console 标签，确认 API 连接正常
4. 如果出现 CORS 错误，检查后端 `CLIENT_URL` 环境变量

## 常见问题

### CORS 错误

- 确保 Render 后端的 `CLIENT_URL` 环境变量设置为 `https://yuranz6.github.io/agent`
- 重启 Render 服务使配置生效

### 前端无法连接后端

- 检查 `REACT_APP_API_URL` 是否正确
- 确保后端 URL 以 `/api` 结尾
- 检查 Render 服务是否正在运行（Free 计划可能休眠）

### Render 服务休眠

- Free 计划的服务在 15 分钟无活动后会休眠
- 首次访问需要等待约 30 秒唤醒
- 可考虑使用付费计划或添加健康检查 ping

### GitHub Pages 404 错误

- 确保已启用 GitHub Pages（Settings → Pages）
- 选择 **GitHub Actions** 作为源
- 检查 GitHub Actions 工作流是否成功完成

## 项目结构

```
agent/
├── client/              # React 前端
│   ├── src/
│   └── package.json
├── server/              # Node.js 后端
│   ├── index.js
│   └── routes/
├── .github/
│   └── workflows/
│       └── deploy-frontend.yml  # GitHub Actions 工作流
├── render.yaml          # Render 部署配置
└── package.json
```

## 相关链接

- 前端地址：https://yuranz6.github.io/agent
- 后端地址：https://your-render-backend-url.onrender.com
- GitHub 仓库：https://github.com/Yuranz6/agent

