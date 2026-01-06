"""
EHR Agent Web 应用
Flask 后端服务器
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime
from config import GOOGLE_API_KEY, GEMINI_MODEL
from soap_generator import SOAPGenerator
from examination_recommender import ExaminationRecommender
from drug_checker import DrugChecker

# 获取应用根目录
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
CORS(app)

# 延迟初始化组件（避免启动时出错）
soap_generator = None
exam_recommender = None
drug_checker = None

def init_components():
    """初始化 AI 组件"""
    global soap_generator, exam_recommender, drug_checker
    if soap_generator is None:
        try:
            print("正在初始化 AI 组件...")
            soap_generator = SOAPGenerator(GOOGLE_API_KEY, GEMINI_MODEL)
            exam_recommender = ExaminationRecommender(GOOGLE_API_KEY, GEMINI_MODEL)
            drug_checker = DrugChecker(GOOGLE_API_KEY, GEMINI_MODEL)
            print("✅ AI 组件初始化成功")
        except Exception as e:
            print(f"⚠️  AI 组件初始化失败: {e}")
            print("   应用仍可运行，但 AI 功能可能不可用")
            # 不抛出异常，让应用继续运行

@app.route('/')
def index():
    """主页面"""
    try:
        import os
        template_path = os.path.join(app.template_folder, 'index.html')
        if not os.path.exists(template_path):
            return f"错误: 模板文件不存在 - {template_path}<br>当前工作目录: {os.getcwd()}<br>模板文件夹: {app.template_folder}", 500
        return render_template('index.html')
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        return f"错误: 无法加载模板 - {str(e)}<br><pre>{error_detail}</pre>", 500

@app.route('/health')
def health():
    """健康检查端点"""
    return jsonify({
        'status': 'ok',
        'message': 'EHR Agent API is running'
    })

@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({
        'error': '页面未找到',
        'message': '请访问 http://localhost:5000/',
        'available_routes': [
            '/',
            '/api/generate-soap',
            '/api/recommend-examinations',
            '/api/check-drug-conflicts',
            '/api/save-report'
        ]
    }), 404

@app.route('/api/generate-soap', methods=['POST'])
def generate_soap():
    """生成 SOAP 病历"""
    try:
        init_components()
        if soap_generator is None:
            return jsonify({'error': 'AI 组件未初始化，请检查 API Key 配置'}), 500
        
        data = request.json
        consultation_transcript = data.get('transcript', '')
        patient_info = data.get('patient_info', {})
        
        if not consultation_transcript:
            return jsonify({'error': '问诊记录不能为空'}), 400
        
        # 生成 SOAP 病历
        soap_data = soap_generator.generate_soap(consultation_transcript, patient_info)
        
        return jsonify({
            'success': True,
            'data': soap_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recommend-examinations', methods=['POST'])
def recommend_examinations():
    """推荐检查项目"""
    try:
        init_components()
        if exam_recommender is None:
            return jsonify({'error': 'AI 组件未初始化，请检查 API Key 配置'}), 500
        
        data = request.json
        soap_data = data.get('soap_data', {})
        consultation_transcript = data.get('transcript', '')
        
        if not soap_data:
            return jsonify({'error': 'SOAP 数据不能为空'}), 400
        
        # 推荐检查项目
        examinations = exam_recommender.recommend_examinations(soap_data, consultation_transcript)
        
        return jsonify({
            'success': True,
            'data': examinations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/check-drug-conflicts', methods=['POST'])
def check_drug_conflicts():
    """检查药物冲突"""
    try:
        init_components()
        if drug_checker is None:
            return jsonify({'error': 'AI 组件未初始化，请检查 API Key 配置'}), 500
        
        data = request.json
        plan_text = data.get('plan_text', '')
        patient_info = data.get('patient_info', {})
        
        if not plan_text:
            return jsonify({'error': '治疗计划不能为空'}), 400
        
        # 提取药物
        prescribed_drugs = drug_checker.extract_drugs_from_plan(plan_text)
        
        if not prescribed_drugs:
            return jsonify({
                'success': True,
                'data': {
                    'has_conflicts': False,
                    'message': '未在治疗计划中发现药物'
                }
            })
        
        # 获取患者信息
        allergies = []
        if patient_info.get('allergies') and patient_info['allergies'] != '无':
            allergies = [a.strip() for a in patient_info['allergies'].split(',')]
        
        current_meds = []
        if patient_info.get('current_medications') and patient_info['current_medications'] != '无':
            current_meds = [m.strip() for m in patient_info['current_medications'].split(',')]
        
        # 检查药物冲突
        check_results = drug_checker.check_drug_conflicts(
            prescribed_drugs=prescribed_drugs,
            patient_allergies=allergies if allergies else None,
            current_medications=current_meds if current_meds else None,
            medical_history=patient_info.get('medical_history')
        )
        
        return jsonify({
            'success': True,
            'data': check_results,
            'prescribed_drugs': prescribed_drugs
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/save-report', methods=['POST'])
def save_report():
    """保存报告"""
    try:
        data = request.json
        report_content = data.get('content', '')
        
        if not report_content:
            return jsonify({'error': '报告内容不能为空'}), 400
        
        # 确保输出目录存在
        os.makedirs('output', exist_ok=True)
        
        # 保存文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ehr_report_{timestamp}.txt"
        filepath = os.path.join('output', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': filepath
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # 检查 API Key
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_google_api_key_here":
        print("⚠️  警告: 未设置有效的 GOOGLE_API_KEY")
        print("   请在 .env 文件中设置您的 Google API Key")
        print("   应用仍可启动，但 AI 功能将不可用")
    else:
        # 尝试初始化组件
        try:
            init_components()
        except Exception as e:
            print(f"⚠️  AI 组件初始化失败: {e}")
            print("   应用仍可启动，但 AI 功能将不可用")
    
    # 检查文件是否存在
    import os
    if not os.path.exists('templates/index.html'):
        print("错误: templates/index.html 不存在")
        exit(1)
    if not os.path.exists('static/css/style.css'):
        print("错误: static/css/style.css 不存在")
        exit(1)
    if not os.path.exists('static/js/app.js'):
        print("错误: static/js/app.js 不存在")
        exit(1)
    
    print("=" * 60)
    print("EHR Agent Web 应用启动中...")
    print("=" * 60)
    print(f"✅ 模板文件夹: {app.template_folder}")
    print(f"✅ 静态文件夹: {app.static_folder}")
    print(f"")
    print(f"🌐 访问地址: http://localhost:5000 (如果端口被占用会自动切换)")
    print(f"")
    print(f"按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    # 自动查找可用端口
    import socket
    
    def find_free_port(start_port=5000, max_attempts=10):
        """查找可用端口"""
        # 跳过已知被占用的端口（Datadog 使用 5000, 5001, 5002）
        skip_ports = [5000, 5001, 5002]
        
        for port in range(start_port, start_port + max_attempts):
            if port in skip_ports:
                continue
            try:
                # 先尝试连接，检查是否真的可用
                test_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_sock.settimeout(0.1)
                result = test_sock.connect_ex(('localhost', port))
                test_sock.close()
                
                if result == 0:
                    # 端口已被占用，跳过
                    continue
                
                # 尝试绑定
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(('', port))
                sock.close()
                return port
            except (OSError, socket.error):
                continue
        return None
    
    # 优先使用环境变量 PORT（Render 等平台会设置）
    port = os.getenv('PORT')
    if port:
        try:
            port = int(port)
        except ValueError:
            port = None
    
    # 如果没有环境变量，则查找可用端口
    if not port:
        port = find_free_port(5000)
        if port is None:
            print(f"\n❌ 错误: 无法找到可用端口 (5000-5009)")
            print(f"请关闭占用端口的程序:")
            print(f"  lsof -ti:5000 | xargs kill -9")
            exit(1)
        
        if port != 5000:
            print(f"\n⚠️  端口 5000 被占用，使用端口 {port}")
        else:
            print(f"\n✅ 使用端口 {port}")
    else:
        print(f"\n✅ 使用环境变量端口: {port}")
    
    print(f"\n📋 应用信息:")
    print(f"   模板文件夹: {app.template_folder}")
    print(f"   静态文件夹: {app.static_folder}")
    print(f"   模板文件存在: {os.path.exists(os.path.join(app.template_folder, 'index.html'))}")
    print(f"\n🌐 访问地址: http://localhost:{port}")
    print(f"💡 健康检查: http://localhost:{port}/health")
    print("=" * 60)
    print("按 Ctrl+C 停止服务器")
    print("=" * 60)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ 错误: 端口 {port} 已被占用")
            print(f"请关闭占用端口的程序:")
            print(f"  lsof -ti:{port} | xargs kill -9")
        else:
            raise

