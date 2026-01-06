# EHR Agent Web 应用使用指南

## 功能特性

Web 版本的 EHR Agent 提供了友好的图形界面，包含以下功能：

1. **患者信息录入** - 填写患者基本信息
2. **实时语音转文字** - 使用浏览器内置的 Web Speech API 进行语音识别
3. **SOAP 病历生成** - 自动生成完整的 SOAP 格式病历
4. **检查项目推荐** - 智能推荐必要的检查项目
5. **药物冲突检查** - 检查处方药物的安全性
6. **报告保存** - 将完整报告保存为文本文件

## 安装和启动

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

确保 `.env` 文件中已配置 Google API Key：

```
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

### 3. 启动 Web 应用

有两种方式启动：

**方式一：使用启动脚本（推荐）**
```bash
python run_web.py
```

**方式二：直接运行 Flask 应用**
```bash
python app.py
```

### 4. 访问应用

启动后，在浏览器中访问：
```
http://localhost:5000
```

## 使用流程

1. **填写患者信息**
   - 输入患者姓名、年龄、性别等基本信息
   - 填写既往史、过敏史、当前用药

2. **录入问诊记录**
   - 方式一：点击"开始录音"按钮，使用语音输入（需要浏览器支持并授予麦克风权限）
   - 方式二：直接在文本框中手动输入问诊记录

3. **生成 SOAP 病历**
   - 点击"生成 SOAP 病历"按钮
   - 系统会自动生成完整的 SOAP 格式病历

4. **推荐检查项目**
   - 在生成 SOAP 病历后，点击"推荐检查项目"
   - 系统会根据病情推荐合适的检查项目，并按优先级分类

5. **检查药物冲突**
   - 点击"检查药物冲突"按钮
   - 系统会从治疗计划中提取药物，并检查安全性

6. **保存报告**
   - 点击"保存报告"按钮
   - 完整的问诊报告会保存到 `output/` 目录

## 浏览器要求

- **推荐浏览器**：Chrome、Edge（最新版本）
- **语音识别**：需要支持 Web Speech API
  - Chrome/Edge: ✅ 完全支持
  - Firefox: ⚠️ 部分支持
  - Safari: ❌ 不支持

## 技术栈

- **后端**：Flask (Python)
- **前端**：HTML5 + CSS3 + JavaScript (原生)
- **语音识别**：Web Speech API（浏览器内置）
- **AI 模型**：Google Gemini 2.5 Flash

## 目录结构

```
EHR agent/
├── app.py                 # Flask 后端应用
├── run_web.py             # 启动脚本
├── templates/
│   └── index.html        # 前端 HTML
├── static/
│   ├── css/
│   │   └── style.css     # 样式文件
│   └── js/
│       └── app.js        # 前端 JavaScript
└── output/               # 报告输出目录
```

## 故障排除

### 1. 404 页面未找到

**问题**: 访问 http://localhost:5000 显示 404 错误

**解决方案**:
- 确认应用已正确启动（查看终端输出）
- 确认访问的 URL 是 `http://localhost:5000/`（注意末尾的斜杠）
- 检查是否有其他程序占用 5000 端口
- 使用启动脚本：`./start_web.sh` 或 `bash start_web.sh`
- 运行测试脚本检查：`python test_app.py`

### 2. 语音识别不工作

- 确保使用 Chrome 或 Edge 浏览器
- 检查浏览器是否授予了麦克风权限
- 在浏览器设置中允许麦克风访问
- 查看浏览器控制台是否有错误信息

### 3. API 请求失败

- 检查 `.env` 文件中的 API Key 是否正确
- 确认网络连接正常
- 查看浏览器控制台的错误信息
- 检查后端终端是否有错误输出

### 4. 端口被占用

如果 5000 端口被占用，可以修改 `app.py` 或 `run_web.py` 中的端口号：

```python
app.run(debug=True, host='0.0.0.0', port=8080)  # 改为其他端口
```

或者查找并关闭占用端口的进程：

```bash
# macOS/Linux
lsof -ti:5000 | xargs kill -9

# 或使用其他端口启动
```

### 5. 模板文件未找到

如果提示模板文件不存在：
- 确认 `templates/index.html` 文件存在
- 确认 `static/css/style.css` 文件存在
- 确认 `static/js/app.js` 文件存在
- 检查当前工作目录是否正确

## 安全注意事项

- Web 应用默认运行在本地（localhost），仅本机可访问
- 如需部署到服务器，请配置 HTTPS 和适当的身份验证
- API Key 存储在服务器端，不会暴露给前端
- `.env` 文件包含敏感信息，不要提交到版本控制

## 与命令行版本的区别

- **Web 版本**：图形界面，更易用，支持浏览器语音识别
- **命令行版本**：适合脚本化和自动化场景

两个版本共享相同的核心功能模块，可以根据需要选择使用。

