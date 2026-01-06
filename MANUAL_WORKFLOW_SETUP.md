# 手动创建 GitHub Actions Workflow 指南

由于当前 token 缺少 `workflow` 权限，请在 GitHub 网页上手动创建 workflow 文件。

## 步骤 1：创建 Workflow 文件

1. 访问：https://github.com/Yuranz6/agent/new/main
2. 在文件名输入框中输入：`.github/workflows/deploy-frontend.yml`
   - GitHub 会自动创建 `.github` 和 `workflows` 目录
3. 复制下面的完整内容并粘贴到编辑器中：

```yaml
name: Deploy Frontend to GitHub Pages

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build-and-deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: client/package-lock.json

      - name: Install root dependencies
        run: npm install

      - name: Install client dependencies
        working-directory: ./client
        run: npm install

      - name: Build React app
        working-directory: ./client
        env:
          REACT_APP_API_URL: ${{ secrets.REACT_APP_API_URL || 'https://clone-i9i8.onrender.com/api' }}
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './client/build'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

4. 滚动到底部，点击 **"Commit new file"** 按钮

## 步骤 2：启用 GitHub Pages

1. 访问：https://github.com/Yuranz6/agent/settings/pages
2. 在 **Source** 部分：
   - 选择 **"GitHub Actions"**（不是 "Deploy from a branch"）
3. 保存设置

## 步骤 3：配置后端 API URL（可选）

如果后端已部署到 Render：

1. 访问：https://github.com/Yuranz6/agent/settings/secrets/actions
2. 点击 **"New repository secret"**
3. 添加：
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://your-render-backend-url.onrender.com/api`
4. 点击 **"Add secret"**

## 步骤 4：触发部署

Workflow 会在以下情况自动运行：
- 推送到 `main` 分支时
- 手动触发：访问 Actions 标签页 → 选择 workflow → 点击 "Run workflow"

## 验证部署

1. 访问：https://github.com/Yuranz6/agent/actions
2. 查看最新的 workflow 运行状态
3. 部署成功后，访问：https://yuranz6.github.io/agent

## 故障排查

如果部署失败：
- 检查 Actions 标签页中的错误信息
- 确保已启用 GitHub Pages（Settings → Pages）
- 确保选择了 "GitHub Actions" 作为源

