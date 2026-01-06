// i18n 国际化支持
const i18n = {
    currentLang: localStorage.getItem('language') || 'zh',
    
    translations: {
        zh: {
            // Header
            title: "EHR Agent - 电子病历辅助系统",
            subtitle: "智能问诊记录与病历生成系统",
            
            // Patient Info
            patientInfo: "患者基本信息",
            patientName: "患者姓名",
            patientNamePlaceholder: "请输入患者姓名",
            age: "年龄",
            agePlaceholder: "请输入年龄",
            gender: "性别",
            genderSelect: "请选择",
            genderMale: "男",
            genderFemale: "女",
            genderOther: "其他",
            medicalHistory: "既往史",
            medicalHistoryPlaceholder: "请输入既往史，无则填'无'",
            allergies: "过敏史",
            allergiesPlaceholder: "请输入过敏史，无则填'无'",
            currentMedications: "当前用药",
            currentMedicationsPlaceholder: "请输入当前用药，用逗号分隔，无则填'无'",
            
            // Consultation
            consultation: "问诊记录",
            startRecording: "开始录音",
            stopRecording: "停止录音",
            clearText: "清空",
            recordingStatus: "正在录音...",
            recordingStopped: "录音已停止",
            consultationPlaceholder: "点击'开始录音'进行语音输入，或直接在此输入问诊记录...",
            charCount: "字数",
            
            // Actions
            generateSOAP: "生成 SOAP 病历",
            recommendExams: "推荐检查项目",
            checkDrugs: "检查药物冲突",
            saveReport: "保存报告",
            
            // Loading
            processing: "处理中，请稍候...",
            
            // Results
            soapNote: "SOAP 病历",
            examRecommendations: "推荐检查项目",
            drugCheck: "药物冲突检查",
            
            // Messages
            pleaseEnterTranscript: "请先输入问诊记录",
            generateSOAPFailed: "生成 SOAP 病历失败",
            requestFailed: "请求失败",
            pleaseGenerateSOAP: "请先生成 SOAP 病历",
            recommendExamsFailed: "推荐检查项目失败",
            checkDrugsFailed: "检查药物冲突失败",
            saveReportSuccess: "报告已保存",
            saveReportFailed: "保存报告失败",
            clearConfirm: "确定要清空问诊记录吗？",
            noExamsRecommended: "未推荐检查项目",
            highPriority: "高优先级",
            mediumPriority: "中优先级",
            lowPriority: "低优先级",
            reason: "理由",
            detectedDrugs: "检测到的药物",
            overallAssessment: "总体评估",
            allergyWarnings: "过敏警告",
            drugInteractions: "药物相互作用",
            contraindications: "禁忌症",
            dosageWarnings: "剂量警告",
            recommendations: "建议",
            noConflicts: "未发现明显的药物冲突或安全风险。",
            
            // Speech Recognition
            speechNotSupported: "浏览器不支持语音识别",
            recordingError: "语音识别错误",
            startRecordingFailed: "启动录音失败，请检查麦克风权限",
            
            // Language
            language: "语言",
            chinese: "中文",
            english: "English"
        },
        
        en: {
            // Header
            title: "EHR Agent - Electronic Health Record Assistant",
            subtitle: "Intelligent Consultation Recording and Medical Record Generation System",
            
            // Patient Info
            patientInfo: "Patient Basic Information",
            patientName: "Patient Name",
            patientNamePlaceholder: "Please enter patient name",
            age: "Age",
            agePlaceholder: "Please enter age",
            gender: "Gender",
            genderSelect: "Please select",
            genderMale: "Male",
            genderFemale: "Female",
            genderOther: "Other",
            medicalHistory: "Medical History",
            medicalHistoryPlaceholder: "Please enter medical history, or 'None' if none",
            allergies: "Allergies",
            allergiesPlaceholder: "Please enter allergies, or 'None' if none",
            currentMedications: "Current Medications",
            currentMedicationsPlaceholder: "Please enter current medications, separated by commas, or 'None' if none",
            
            // Consultation
            consultation: "Consultation Record",
            startRecording: "Start Recording",
            stopRecording: "Stop Recording",
            clearText: "Clear",
            recordingStatus: "Recording...",
            recordingStopped: "Recording stopped",
            consultationPlaceholder: "Click 'Start Recording' for voice input, or type consultation record directly...",
            charCount: "Characters",
            
            // Actions
            generateSOAP: "Generate SOAP Note",
            recommendExams: "Recommend Examinations",
            checkDrugs: "Check Drug Conflicts",
            saveReport: "Save Report",
            
            // Loading
            processing: "Processing, please wait...",
            
            // Results
            soapNote: "SOAP Note",
            examRecommendations: "Recommended Examinations",
            drugCheck: "Drug Conflict Check",
            
            // Messages
            pleaseEnterTranscript: "Please enter consultation record first",
            generateSOAPFailed: "Failed to generate SOAP note",
            requestFailed: "Request failed",
            pleaseGenerateSOAP: "Please generate SOAP note first",
            recommendExamsFailed: "Failed to recommend examinations",
            checkDrugsFailed: "Failed to check drug conflicts",
            saveReportSuccess: "Report saved",
            saveReportFailed: "Failed to save report",
            clearConfirm: "Are you sure you want to clear the consultation record?",
            noExamsRecommended: "No examinations recommended",
            highPriority: "High Priority",
            mediumPriority: "Medium Priority",
            lowPriority: "Low Priority",
            reason: "Reason",
            detectedDrugs: "Detected Drugs",
            overallAssessment: "Overall Assessment",
            allergyWarnings: "Allergy Warnings",
            drugInteractions: "Drug Interactions",
            contraindications: "Contraindications",
            dosageWarnings: "Dosage Warnings",
            recommendations: "Recommendations",
            noConflicts: "No obvious drug conflicts or safety risks detected.",
            
            // Speech Recognition
            speechNotSupported: "Browser does not support speech recognition",
            recordingError: "Speech recognition error",
            startRecordingFailed: "Failed to start recording, please check microphone permissions",
            
            // Language
            language: "Language",
            chinese: "中文",
            english: "English"
        }
    },
    
    // 翻译函数
    t: function(key) {
        return this.translations[this.currentLang][key] || key;
    },
    
    // 设置语言
    setLanguage: function(lang) {
        if (this.translations[lang]) {
            this.currentLang = lang;
            localStorage.setItem('language', lang);
            this.updatePage();
        }
    },
    
    // 更新页面
    updatePage: function() {
        // 更新所有带有 data-i18n 属性的元素
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                if (element.hasAttribute('placeholder')) {
                    element.placeholder = translation;
                } else {
                    element.value = translation;
                }
            } else if (element.tagName === 'OPTION') {
                element.textContent = translation;
                // 更新选项的 value（如果是性别选择）
                if (key === 'genderMale') {
                    element.value = this.currentLang === 'zh' ? '男' : 'Male';
                } else if (key === 'genderFemale') {
                    element.value = this.currentLang === 'zh' ? '女' : 'Female';
                } else if (key === 'genderOther') {
                    element.value = this.currentLang === 'zh' ? '其他' : 'Other';
                } else if (key === 'genderSelect') {
                    element.value = this.currentLang === 'zh' ? '未提供' : 'Not provided';
                }
            } else {
                element.textContent = translation;
            }
        });
        
        // 更新 HTML lang 属性
        document.documentElement.lang = this.currentLang === 'zh' ? 'zh-CN' : 'en';
        
        // 更新页面标题
        document.title = this.t('title');
        
        // 更新语音识别语言
        if (typeof recognition !== 'undefined' && recognition) {
            recognition.lang = this.currentLang === 'zh' ? 'zh-CN' : 'en-US';
        }
        
        // 更新语言切换按钮状态
        document.querySelectorAll('.lang-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        const activeBtn = document.getElementById(`lang-${this.currentLang}`);
        if (activeBtn) {
            activeBtn.classList.add('active');
        }
    }
};

