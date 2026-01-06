"""
药物冲突检查模块
"""
import google.generativeai as genai
from typing import List, Dict, Optional
import json

class DrugChecker:
    """药物冲突检查器"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.model_name = model
    
    def check_drug_conflicts(self, 
                            prescribed_drugs: List[str],
                            patient_allergies: Optional[List[str]] = None,
                            current_medications: Optional[List[str]] = None,
                            medical_history: Optional[str] = None) -> Dict:
        """
        检查药物冲突
        
        Args:
            prescribed_drugs: 处方药物列表
            patient_allergies: 患者过敏史（可选）
            current_medications: 患者当前用药（可选）
            medical_history: 患者病史（可选）
            
        Returns:
            包含冲突检查结果的字典
        """
        allergies_text = "无" if not patient_allergies else ", ".join(patient_allergies)
        current_meds_text = "无" if not current_medications else ", ".join(current_medications)
        history_text = medical_history or "无"
        
        prompt = f"""
你是一位经验丰富的临床药师。请检查以下处方药物的安全性。

处方药物：
{', '.join(prescribed_drugs)}

患者信息：
- 过敏史：{allergies_text}
- 当前用药：{current_meds_text}
- 病史：{history_text}

请检查以下内容：
1. 药物过敏风险：处方药物是否与患者过敏史冲突
2. 药物相互作用：处方药物之间是否存在相互作用
3. 药物与当前用药冲突：处方药物是否与患者当前用药冲突
4. 药物与疾病冲突：处方药物是否与患者病史冲突
5. 剂量合理性：药物剂量是否合理

请以JSON格式返回，包含：
- has_conflicts: 是否存在冲突（布尔值）
- allergy_warnings: 过敏警告列表
- drug_interactions: 药物相互作用列表（包含药物对和说明）
- contraindications: 禁忌症列表
- dosage_warnings: 剂量警告列表
- recommendations: 建议列表
- severity: 总体严重程度（高/中/低/无）
"""
        
        try:
            full_prompt = f"""你是一位专业的临床药师，擅长识别药物冲突和用药安全风险。

{prompt}

请确保返回有效的JSON格式。"""
            
            generation_config = {
                "temperature": 0.2,
                "response_mime_type": "application/json",
            }
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            result = json.loads(response.text)
            return result
            
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg or "leaked" in error_msg.lower() or "API key" in error_msg:
                print(f"❌ API Key 错误: {error_msg}")
                print("   请检查您的 Google API Key 是否有效，或需要更换新的 API Key")
                print("   获取新 API Key: https://makersuite.google.com/app/apikey")
            else:
                print(f"药物冲突检查错误: {e}")
            return {
                "error": error_msg,
                "has_conflicts": False,
                "allergy_warnings": [],
                "drug_interactions": [],
                "contraindications": [],
                "dosage_warnings": [],
                "recommendations": [],
                "severity": "未知"
            }
    
    def extract_drugs_from_plan(self, plan_text: str) -> List[str]:
        """
        从治疗计划中提取药物名称
        
        Args:
            plan_text: 治疗计划文本
            
        Returns:
            药物名称列表
        """
        prompt = f"""
请从以下治疗计划中提取所有提到的药物名称。

治疗计划：
{plan_text}

请以JSON格式返回，包含一个drugs数组，每个元素是药物名称。
只提取明确的药物名称，不包括检查项目或其他非药物内容。
"""
        
        try:
            full_prompt = f"""你擅长从医疗文本中准确提取药物名称。

{prompt}

请确保返回有效的JSON格式。"""
            
            generation_config = {
                "temperature": 0.1,
                "response_mime_type": "application/json",
            }
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            result = json.loads(response.text)
            return result.get('drugs', [])
            
        except Exception as e:
            error_msg = str(e)
            if "403" in error_msg or "leaked" in error_msg.lower() or "API key" in error_msg:
                print(f"❌ API Key 错误: {error_msg}")
                print("   请检查您的 Google API Key 是否有效，或需要更换新的 API Key")
            else:
                print(f"提取药物名称错误: {e}")
            return []
    
    def format_check_results(self, check_results: Dict) -> str:
        """
        格式化药物冲突检查结果
        
        Args:
            check_results: 检查结果字典
            
        Returns:
            格式化的文本
        """
        if "error" in check_results:
            return f"错误: {check_results['error']}"
        
        text = "\n【药物冲突检查结果】\n"
        text += "="*60 + "\n\n"
        
        severity = check_results.get('severity', '未知')
        has_conflicts = check_results.get('has_conflicts', False)
        
        # 严重程度指示
        severity_icons = {
            '高': '⚠️ 高风险',
            '中': '⚡ 中等风险',
            '低': 'ℹ️ 低风险',
            '无': '✅ 无风险'
        }
        text += f"总体评估: {severity_icons.get(severity, severity)}\n\n"
        
        # 过敏警告
        allergy_warnings = check_results.get('allergy_warnings', [])
        if allergy_warnings:
            text += "【过敏警告】\n"
            for warning in allergy_warnings:
                text += f"⚠️ {warning}\n"
            text += "\n"
        
        # 药物相互作用
        drug_interactions = check_results.get('drug_interactions', [])
        if drug_interactions:
            text += "【药物相互作用】\n"
            for interaction in drug_interactions:
                if isinstance(interaction, dict):
                    drugs = interaction.get('drugs', '未知')
                    description = interaction.get('description', '未提供')
                    text += f"⚠️ {drugs}: {description}\n"
                else:
                    text += f"⚠️ {interaction}\n"
            text += "\n"
        
        # 禁忌症
        contraindications = check_results.get('contraindications', [])
        if contraindications:
            text += "【禁忌症】\n"
            for contra in contraindications:
                text += f"🚫 {contra}\n"
            text += "\n"
        
        # 剂量警告
        dosage_warnings = check_results.get('dosage_warnings', [])
        if dosage_warnings:
            text += "【剂量警告】\n"
            for warning in dosage_warnings:
                text += f"⚠️ {warning}\n"
            text += "\n"
        
        # 建议
        recommendations = check_results.get('recommendations', [])
        if recommendations:
            text += "【建议】\n"
            for rec in recommendations:
                text += f"💡 {rec}\n"
            text += "\n"
        
        if not has_conflicts and not allergy_warnings and not drug_interactions:
            text += "✅ 未发现明显的药物冲突或安全风险。\n"
        
        return text

