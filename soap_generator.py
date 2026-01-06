"""
SOAP病历生成模块
"""
import google.generativeai as genai
from typing import Dict, Optional
import json
from datetime import datetime

class SOAPGenerator:
    """SOAP病历生成器"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.model_name = model
    
    def generate_soap(self, consultation_transcript: str, patient_info: Optional[Dict] = None) -> Dict:
        """
        根据问诊记录生成SOAP病历
        
        Args:
            consultation_transcript: 问诊转录文本
            patient_info: 患者基本信息（可选）
            
        Returns:
            包含SOAP各部分的字典
        """
        patient_context = ""
        if patient_info:
            patient_context = f"""
患者基本信息：
- 姓名：{patient_info.get('name', '未知')}
- 年龄：{patient_info.get('age', '未知')}
- 性别：{patient_info.get('gender', '未知')}
- 既往史：{patient_info.get('medical_history', '无')}
- 过敏史：{patient_info.get('allergies', '无')}
"""
        
        prompt = f"""
你是一位经验丰富的临床医生。请根据以下问诊记录，生成一份完整的SOAP格式病历。

{patient_context}

问诊记录：
{consultation_transcript}

请按照SOAP格式生成病历，包括：
1. S (Subjective - 主观资料)：患者主诉、现病史、既往史、个人史等
2. O (Objective - 客观资料)：体格检查发现、生命体征等
3. A (Assessment - 评估)：初步诊断、鉴别诊断等
4. P (Plan - 计划)：治疗方案、检查计划、用药计划、随访计划等

请以JSON格式返回，包含以下字段：
- subjective: 主观资料
- objective: 客观资料  
- assessment: 评估
- plan: 计划
- chief_complaint: 主诉（简要）
- preliminary_diagnosis: 初步诊断（列表）

确保内容专业、准确、完整。
"""
        
        try:
            full_prompt = f"""你是一位专业的临床医生，擅长撰写规范的SOAP病历。

{prompt}

请确保返回有效的JSON格式。"""
            
            generation_config = {
                "temperature": 0.3,
                "response_mime_type": "application/json",
            }
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            result = json.loads(response.text)
            result['generated_at'] = datetime.now().isoformat()
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg or "leaked" in error_msg.lower() or "API key" in error_msg:
                print(f"❌ API Key 错误: {error_msg}")
                print("   请检查您的 Google API Key 是否有效，或需要更换新的 API Key")
                print("   获取新 API Key: https://makersuite.google.com/app/apikey")
            else:
                print(f"生成SOAP病历错误: {e}")
            return {
                "error": error_msg,
                "subjective": "",
                "objective": "",
                "assessment": "",
                "plan": "",
                "chief_complaint": "",
                "preliminary_diagnosis": []
            }
    
    def format_soap_text(self, soap_data: Dict) -> str:
        """
        将SOAP数据格式化为文本
        
        Args:
            soap_data: SOAP数据字典
            
        Returns:
            格式化的文本
        """
        if "error" in soap_data:
            return f"错误: {soap_data['error']}"
        
        text = f"""
{'='*60}
SOAP 病历
{'='*60}

【主诉】
{soap_data.get('chief_complaint', '未提供')}

【主观资料 (S - Subjective)】
{soap_data.get('subjective', '')}

【客观资料 (O - Objective)】
{soap_data.get('objective', '')}

【评估 (A - Assessment)】
{soap_data.get('assessment', '')}

【计划 (P - Plan)】
{soap_data.get('plan', '')}

【初步诊断】
{', '.join(soap_data.get('preliminary_diagnosis', []))}

生成时间: {soap_data.get('generated_at', '')}
{'='*60}
"""
        return text

