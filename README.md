# EHR Agent - 电子病历辅助系统

智能电子病历辅助系统，支持实时语音转文字、自动生成SOAP病历、检查项目推荐和药物冲突检查。

## 功能特性

### 1. 实时语音转文字 ✓
- 问诊过程中实时录制语音
- 自动转换为文字记录
- 支持中文语音识别

### 2. 自动生成SOAP病历 ✓
- 根据问诊记录自动生成完整的SOAP格式病历
- 包含：主观资料(S)、客观资料(O)、评估(A)、计划(P)
- 自动提取主诉和初步诊断

### 3. 检查项目推荐 ✓
- 基于SOAP病历和问诊记录智能推荐检查项目
- 按优先级分类（高/中/低）
- 提供推荐理由

### 4. 药物冲突检查 ✓
- 自动从治疗计划中提取药物
- 检查药物过敏风险
- 检查药物相互作用
- 检查禁忌症和剂量合理性

## 安装

### 1. 克隆或下载项目

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**注意**: 在 macOS 上安装 `pyaudio` 可能需要先安装 PortAudio：

```bash
brew install portaudio
pip install pyaudio
```

### 3. 配置环境变量

创建 `.env` 文件并填入你的 Google API 密钥：

```bash
# 创建 .env 文件
cat > .env << EOF
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-pro
EOF
```

编辑 `.env` 文件，设置您的 Google API Key：

```
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

**注意**: 可用的模型包括：
- `gemini-2.5-flash` (推荐，快速且经济)
- `gemini-2.5-pro` (更强大，适合复杂任务)

**获取 Google API Key**: https://makersuite.google.com/app/apikey

## 使用方法

### 方式一：Web 应用（推荐）

启动 Web 应用，在浏览器中使用图形界面：

```bash
python run_web.py
```

然后在浏览器中访问：http://localhost:5000

**详细说明请参考**：[WEB_APP_README.md](WEB_APP_README.md)

### 方式二：命令行程序

运行命令行版本：

```bash
python ehr_agent.py
```

### 使用流程

1. **收集患者信息**
   - 输入患者姓名、年龄、性别等基本信息
   - 输入既往史、过敏史、当前用药

2. **问诊录制**
   - 系统开始实时语音识别
   - 说话内容会自动转换为文字
   - 按 Enter 键结束录制（或等待自动结束）

3. **自动生成结果**
   - SOAP病历草案
   - 推荐检查项目
   - 药物冲突检查结果

4. **保存报告**
   - 选择是否保存完整报告到文件
   - 报告保存在 `output/` 目录

## 项目结构

```
EHR agent/
├── app.py                    # Flask Web 应用后端
├── run_web.py               # Web 应用启动脚本
├── ehr_agent.py             # 命令行主程序
├── voice_recorder.py        # 语音录制模块
├── speech_to_text.py       # 语音转文字模块
├── soap_generator.py        # SOAP病历生成模块
├── examination_recommender.py # 检查项目推荐模块
├── drug_checker.py         # 药物冲突检查模块
├── config.py                # 配置文件
├── requirements.txt         # 依赖包
├── templates/               # Web 应用模板
│   └── index.html          # 前端页面
├── static/                  # 静态资源
│   ├── css/
│   │   └── style.css       # 样式文件
│   └── js/
│       └── app.js          # 前端 JavaScript
├── .env.example            # 环境变量示例
├── README.md               # 说明文档
├── WEB_APP_README.md       # Web 应用使用指南
├── recordings/             # 录音文件目录（自动创建）
└── output/                 # 输出报告目录（自动创建）
```

## 模块说明

### voice_recorder.py
实时语音录制功能，使用 PyAudio 进行音频采集。

### speech_to_text.py
语音转文字功能，使用 Google Speech Recognition API（需要网络连接）。

### soap_generator.py
使用 Google Gemini AI 模型根据问诊记录生成规范的 SOAP 格式病历。

### examination_recommender.py
基于病情和诊断推荐合适的检查项目，包括常规检查、生化检查、影像学检查等。

### drug_checker.py
使用 Google Gemini AI 检查处方药物的安全性，包括：
- 过敏风险检查
- 药物相互作用检查
- 禁忌症检查
- 剂量合理性检查

## 注意事项

1. **API 密钥**: 需要有效的 Google API 密钥才能使用 Gemini AI 功能（用于生成SOAP病历、检查推荐、药物冲突检查）
   - 如果遇到 `403 Your API key was reported as leaked` 错误，请参考 [API_KEY_SETUP.md](API_KEY_SETUP.md) 获取帮助
   - **重要**: 永远不要将 API Key 提交到 Git 仓库，`.env` 文件已在 `.gitignore` 中
2. **网络连接**: 语音识别和 AI 功能都需要网络连接
3. **麦克风权限**: 需要授予程序麦克风访问权限
4. **语音识别**: 使用 Google Speech Recognition API
5. **AI 模型**: 使用 Google Gemini 2.5 Flash/Pro 模型进行医疗文本生成和分析
6. **医疗建议**: 本系统生成的病历和建议仅供参考，不能替代专业医疗判断

## 改进建议

- [ ] 支持离线语音识别（使用本地模型）
- [ ] 添加 GUI 界面
- [ ] 支持多语言
- [ ] 集成真实的药物数据库
- [ ] 添加病历模板自定义
- [ ] 支持导出为 PDF/Word 格式
- [ ] 添加病历历史记录和检索功能

## 许可证

本项目仅供学习和研究使用。
