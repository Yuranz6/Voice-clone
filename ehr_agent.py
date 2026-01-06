"""
EHR Agent 主程序
整合语音录制、转录、SOAP生成、检查推荐、药物冲突检查等功能
"""
import os
import time
from datetime import datetime
from typing import Optional, Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.text import Text

from config import (
    GOOGLE_API_KEY, GEMINI_MODEL, RECORDINGS_DIR, OUTPUT_DIR,
    MICROPHONE_INDEX
)
from voice_recorder import VoiceRecorder
from speech_to_text import SpeechToText
from soap_generator import SOAPGenerator
from examination_recommender import ExaminationRecommender
from drug_checker import DrugChecker

console = Console()

class EHRAgent:
    """EHR Agent 主类"""
    
    def __init__(self):
        # 检查API密钥
        if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_google_api_key_here":
            console.print("\n[red]错误: 未设置有效的 GOOGLE_API_KEY[/red]")
            console.print("[yellow]请在 .env 文件中设置您的 Google API Key[/yellow]")
            console.print("[dim]获取 API Key: https://makersuite.google.com/app/apikey[/dim]")
            console.print("[dim]注意: Google API Key 是必需的，用于生成SOAP病历、检查推荐、药物冲突检查和语音识别[/dim]\n")
            raise ValueError("GOOGLE_API_KEY 未设置或无效")
        
        # 检查 API Key 是否可能泄露（简单检查）
        if "AIza" in GOOGLE_API_KEY and len(GOOGLE_API_KEY) < 50:
            console.print("[yellow]警告: API Key 格式可能不正确，请确认您的 API Key 完整有效[/yellow]")
        
        # 初始化组件
        self.voice_recorder = VoiceRecorder()
        self.speech_to_text = SpeechToText(google_api_key=GOOGLE_API_KEY)
        self.soap_generator = SOAPGenerator(GOOGLE_API_KEY, GEMINI_MODEL)
        self.exam_recommender = ExaminationRecommender(GOOGLE_API_KEY, GEMINI_MODEL)
        self.drug_checker = DrugChecker(GOOGLE_API_KEY, GEMINI_MODEL)
        
        # 问诊数据
        self.consultation_transcript = ""
        self.patient_info = {}
        self.soap_data = {}
        
        # 创建输出目录
        os.makedirs(RECORDINGS_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    def collect_patient_info(self) -> Dict:
        """收集患者基本信息"""
        console.print("\n[bold cyan]收集患者基本信息[/bold cyan]")
        info = {}
        
        info['name'] = Prompt.ask("患者姓名", default="未提供")
        info['age'] = Prompt.ask("年龄", default="未提供")
        info['gender'] = Prompt.ask("性别", choices=["男", "女", "其他"], default="未提供")
        info['medical_history'] = Prompt.ask("既往史", default="无")
        info['allergies'] = Prompt.ask("过敏史", default="无")
        info['current_medications'] = Prompt.ask("当前用药（用逗号分隔）", default="无")
        
        return info
    
    def record_consultation(self) -> str:
        """
        实时录制问诊过程并转文字
        
        Returns:
            问诊转录文本
        """
        console.print("\n[bold cyan]开始问诊录制[/bold cyan]")
        console.print("[yellow]提示: 说话后会自动转录，每段转录后可以选择继续或结束[/yellow]\n")
        
        transcript_parts = []
        
        try:
            while True:
                # 实时转录
                console.print("[dim]正在录音，请说话...[/dim]")
                text = self.speech_to_text.transcribe_realtime(MICROPHONE_INDEX)
                
                if text:
                    transcript_parts.append(text)
                    console.print(f"[green]✓ 转录:[/green] {text}\n")
                    
                    # 询问是否继续
                    if not Confirm.ask("继续录制下一段？", default=True):
                        break
                else:
                    console.print("[dim]未检测到语音[/dim]")
                    if not Confirm.ask("未检测到语音，是否重试？", default=True):
                        break
                    
        except KeyboardInterrupt:
            console.print("\n[yellow]录制中断[/yellow]")
        except Exception as e:
            console.print(f"[red]录制错误: {e}[/red]")
        
        full_transcript = " ".join(transcript_parts)
        self.consultation_transcript = full_transcript
        
        if full_transcript:
            console.print(f"\n[green]录制完成，共 {len(transcript_parts)} 段录音[/green]")
            console.print(f"[dim]完整转录文本:[/dim]\n{full_transcript}\n")
        else:
            console.print("\n[yellow]未获取到转录文本[/yellow]\n")
        
        return full_transcript
    
    def generate_soap_note(self) -> Dict:
        """生成SOAP病历"""
        console.print("\n[bold cyan]正在生成SOAP病历...[/bold cyan]")
        
        soap_data = self.soap_generator.generate_soap(
            self.consultation_transcript,
            self.patient_info
        )
        
        self.soap_data = soap_data
        
        # 显示SOAP病历
        soap_text = self.soap_generator.format_soap_text(soap_data)
        console.print(Panel(soap_text, title="SOAP 病历", border_style="cyan"))
        
        return soap_data
    
    def recommend_examinations(self) -> List[Dict]:
        """推荐检查项目"""
        console.print("\n[bold cyan]正在推荐检查项目...[/bold cyan]")
        
        examinations = self.exam_recommender.recommend_examinations(
            self.soap_data,
            self.consultation_transcript
        )
        
        # 显示推荐
        exam_text = self.exam_recommender.format_recommendations(examinations)
        console.print(Panel(exam_text, title="检查项目推荐", border_style="green"))
        
        return examinations
    
    def check_drug_conflicts(self) -> Dict:
        """检查药物冲突"""
        console.print("\n[bold cyan]正在检查药物冲突...[/bold cyan]")
        
        # 从SOAP计划中提取药物
        plan_text = self.soap_data.get('plan', '')
        prescribed_drugs = self.drug_checker.extract_drugs_from_plan(plan_text)
        
        if not prescribed_drugs:
            console.print("[yellow]未在治疗计划中发现药物，跳过药物冲突检查[/yellow]")
            return {}
        
        console.print(f"[dim]检测到药物: {', '.join(prescribed_drugs)}[/dim]")
        
        # 获取患者信息
        allergies = []
        if self.patient_info.get('allergies') and self.patient_info['allergies'] != '无':
            allergies = [a.strip() for a in self.patient_info['allergies'].split(',')]
        
        current_meds = []
        if self.patient_info.get('current_medications') and self.patient_info['current_medications'] != '无':
            current_meds = [m.strip() for m in self.patient_info['current_medications'].split(',')]
        
        # 执行检查
        check_results = self.drug_checker.check_drug_conflicts(
            prescribed_drugs=prescribed_drugs,
            patient_allergies=allergies if allergies else None,
            current_medications=current_meds if current_meds else None,
            medical_history=self.patient_info.get('medical_history')
        )
        
        # 显示结果
        check_text = self.drug_checker.format_check_results(check_results)
        console.print(Panel(check_text, title="药物冲突检查", border_style="yellow"))
        
        return check_results
    
    def save_results(self):
        """保存所有结果到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ehr_report_{timestamp}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("EHR Agent 问诊报告\n")
            f.write("="*60 + "\n\n")
            
            # 患者信息
            f.write("【患者信息】\n")
            for key, value in self.patient_info.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
            
            # 问诊记录
            f.write("【问诊记录】\n")
            f.write(self.consultation_transcript + "\n\n")
            
            # SOAP病历
            f.write(self.soap_generator.format_soap_text(self.soap_data))
            f.write("\n")
            
            # 检查推荐
            examinations = self.exam_recommender.recommend_examinations(
                self.soap_data, self.consultation_transcript
            )
            f.write(self.exam_recommender.format_recommendations(examinations))
            f.write("\n")
            
            # 药物冲突检查
            plan_text = self.soap_data.get('plan', '')
            prescribed_drugs = self.drug_checker.extract_drugs_from_plan(plan_text)
            if prescribed_drugs:
                allergies = []
                if self.patient_info.get('allergies') and self.patient_info['allergies'] != '无':
                    allergies = [a.strip() for a in self.patient_info['allergies'].split(',')]
                current_meds = []
                if self.patient_info.get('current_medications') and self.patient_info['current_medications'] != '无':
                    current_meds = [m.strip() for m in self.patient_info['current_medications'].split(',')]
                
                check_results = self.drug_checker.check_drug_conflicts(
                    prescribed_drugs=prescribed_drugs,
                    patient_allergies=allergies if allergies else None,
                    current_medications=current_meds if current_meds else None,
                    medical_history=self.patient_info.get('medical_history')
                )
                f.write(self.drug_checker.format_check_results(check_results))
        
        console.print(f"\n[green]报告已保存至: {filepath}[/green]")
        return filepath
    
    def run(self):
        """运行主流程"""
        console.print(Panel.fit(
            "[bold cyan]EHR Agent - 电子病历辅助系统[/bold cyan]\n\n"
            "功能：\n"
            "1. 实时语音转文字记录问诊\n"
            "2. 自动生成SOAP病历\n"
            "3. 推荐检查项目\n"
            "4. 药物冲突检查",
            border_style="cyan"
        ))
        
        try:
            # 1. 收集患者信息
            self.patient_info = self.collect_patient_info()
            
            # 2. 录制问诊（实时转文字）
            use_voice = Confirm.ask("是否使用语音输入？", default=True)
            
            if use_voice:
                transcript = self.record_consultation()
            else:
                console.print("\n[bold cyan]手动输入问诊记录[/bold cyan]")
                console.print("[yellow]提示: 输入问诊内容，输入空行结束[/yellow]\n")
                lines = []
                while True:
                    line = Prompt.ask("", default="", show_default=False)
                    if not line:
                        break
                    lines.append(line)
                transcript = "\n".join(lines)
                self.consultation_transcript = transcript
            
            if not transcript:
                console.print("[red]未获取到问诊记录，程序退出[/red]")
                return
            
            # 3. 生成SOAP病历
            self.generate_soap_note()
            
            # 4. 推荐检查项目
            self.recommend_examinations()
            
            # 5. 药物冲突检查
            self.check_drug_conflicts()
            
            # 6. 保存结果
            if Confirm.ask("\n是否保存报告到文件？"):
                self.save_results()
            
            console.print("\n[bold green]✓ 问诊流程完成！[/bold green]\n")
            
        except KeyboardInterrupt:
            console.print("\n[yellow]程序被用户中断[/yellow]")
        except Exception as e:
            console.print(f"\n[red]错误: {e}[/red]")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
        finally:
            self.voice_recorder.cleanup()

def main():
    """主函数"""
    agent = EHRAgent()
    agent.run()

if __name__ == "__main__":
    main()

