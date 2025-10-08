#!/usr/bin/env python3
"""
Contract Intelligence Agent - Standalone Vercel Serverless Version
AI-powered contract analysis with OCR and automated event generation
"""

import os
import sys
import json
import tempfile
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Contract Intelligence Agent",
    description="AI-powered rental contract analysis with OCR and automated event generation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
COLAB_URL = os.getenv('COLAB_OCR_URL', 'https://snaillike-russel-snodly.ngrok-free.dev')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

class ColabOCRClient:
    """Client for Colab OCR API"""
    
    def __init__(self, colab_url: str):
        self.colab_url = colab_url.rstrip('/')
    
    async def health_check(self) -> str:
        """Check if Colab OCR API is healthy"""
        try:
            response = requests.get(f"{self.colab_url}/health", timeout=10)
            if response.status_code == 200:
                return "✅ Colab API is healthy"
            else:
                return f"❌ Colab API returned {response.status_code}"
        except Exception as e:
            return f"❌ Colab API error: {str(e)}"
    
    def process_contract(self, file_path: str) -> dict:
        """Process contract file with Colab OCR"""
        try:
            print(f"🚀 Sending {os.path.basename(file_path)} to Colab OCR API...")
            
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.colab_url}/ocr", files=files, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Colab OCR completed: {len(result.get('text', ''))} characters")
                return result
            else:
                print(f"❌ Colab OCR failed: {response.status_code}")
                return {"text": "", "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Colab OCR error: {str(e)}")
            return {"text": "", "error": str(e)}

class ContractIntelligence:
    """AI-powered contract analysis"""
    
    def __init__(self, openai_api_key: str):
        self.openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None
        self.model = "gpt-4o-mini"
    
    def parse_contract(self, raw_text: str) -> dict:
        """Parse contract text using OpenAI API"""
        
        if not self.openai_client:
            return self._fallback_parsing(raw_text)
        
        print("🧠 Using OpenAI API for comprehensive contract analysis...")
        
        try:
            # Create a comprehensive prompt for contract parsing
            prompt = f"""
            You are an expert contract analyst specializing in Dubai rental agreements. 
            Analyze the following contract text and provide a comprehensive analysis in JSON format.

            Contract Text:
            {raw_text}

            Return ONLY a valid JSON object with the following structure:
            {{
                "contract_data": {{
                    "property": {{
                        "building": "Building name",
                        "unit": "Unit number", 
                        "location": "Full location",
                        "size_sqm": 85.42,
                        "type": "Property type"
                    }},
                    "parties": {{
                        "landlord": {{
                            "name": "Landlord name",
                            "passport_no": "Passport number",
                            "phone_primary": "Primary phone",
                            "phone_alt": "Alternative phone",
                            "email": "Email address"
                        }},
                        "tenant": {{
                            "name": "Tenant name",
                            "passport_no": "Passport number", 
                            "phone_primary": "Primary phone",
                            "phone_alt": "Alternative phone",
                            "email": "Email address"
                        }}
                    }},
                    "lease": {{
                        "start_date": "2021-07-20",
                        "end_date": "2022-07-19",
                        "duration_months": 12,
                        "notice_period_days": 30
                    }},
                    "rent": {{
                        "annual_aed": 48000.00,
                        "monthly_aed": 4000.00,
                        "cheques": {{
                            "count": 4,
                            "amount_per_cheque": 12000.00,
                            "dates": ["2021-07-20", "2021-10-20", "2022-01-20", "2022-04-20"]
                        }}
                    }},
                    "deposit": {{
                        "refundable_aed": 4000.00,
                        "security_deposit": 4000.00
                    }},
                    "furnishing": {{
                        "status": "Fully furnished",
                        "inventory_present": true
                    }},
                    "responsibilities": {{
                        "service_charges": "Landlord",
                        "dewa": "Tenant", 
                        "chiller": "Tenant",
                        "ejari_registration": "Tenant",
                        "maintenance_major": "Landlord",
                        "maintenance_minor": "Tenant",
                        "maintenance_minor_cap": 500.00
                    }},
                    "terms": {{
                        "pets_allowed": false,
                        "subletting_allowed": false,
                        "early_termination_penalty": "2 months rent + AED 1,000",
                        "renewal_notice_days": 90,
                        "governing_law": "Dubai laws"
                    }},
                    "identifiers": {{
                        "ejari_number": "Ejari registration number",
                        "dewa_premise_no": "DEWA premise number",
                        "plot_no": "Plot number"
                    }}
                }},
                "rental_events": [
                    {{
                        "event_type": "payment_due",
                        "title": "Rent Payment Due",
                        "date": "2021-10-20",
                        "description": "Second rent payment of AED 12,000 due",
                        "automated_actions": [
                            "📅 Add to Calendar",
                            "💬 Send WhatsApp Reminder",
                            "📧 Send Email Reminder"
                        ]
                    }},
                    {{
                        "event_type": "renewal_window_start",
                        "title": "Renewal Window Opens",
                        "date": "2022-04-20",
                        "description": "90-day renewal notice period begins",
                        "automated_actions": [
                            "📅 Add to Calendar",
                            "💬 Send WhatsApp Reminder",
                            "📧 Send Email Reminder"
                        ]
                    }}
                ],
                "completeness_analysis": {{
                    "completeness_score": 85,
                    "quality_status": "good",
                    "missing_critical": [
                        "ejari_number",
                        "cheque_dates",
                        "tenant_phone"
                    ],
                    "missing_important": [
                        "inventory_list",
                        "landlord_email",
                        "maintenance_cap"
                    ],
                    "needs_confirmation": [
                        "service_charges_responsibility",
                        "chiller_responsibility"
                    ],
                    "actionable_gaps": [
                        {{
                            "type": "missing_document",
                            "field": "ejari_number",
                            "label": "Ejari Registration Number",
                            "description": "Ejari number not found in contract text",
                            "priority": "high",
                            "status": "missing",
                            "automated_action": "📄 Upload Ejari Certificate"
                        }},
                        {{
                            "type": "missing_contact",
                            "field": "tenant_phone",
                            "label": "Tenant Phone Number",
                            "description": "Tenant contact number not found",
                            "priority": "medium", 
                            "status": "missing",
                            "automated_action": "📱 Add Tenant Contact"
                        }}
                    ],
                    "validation_notes": [
                        "Contract appears to be a standard Dubai tenancy agreement",
                        "Most key terms are present and clearly defined",
                        "Some contact information and document references are missing"
                    ]
                }}
            }}

            IMPORTANT INSTRUCTIONS:
            1. Extract ONLY information explicitly stated in the contract text
            2. Do NOT make assumptions or add information not present
            3. If information is not found, use null or empty string
            4. Format dates as YYYY-MM-DD
            5. Format currency amounts as numbers (e.g., 48000.00)
            6. Return ONLY the JSON object, no additional text
            7. Ensure the JSON is valid and properly formatted
            """

            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert contract analyst. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=3000,
                temperature=0.1
            )
            
            ai_response = response.choices[0].message.content.strip()
            print(f"🤖 OpenAI Response: {ai_response[:100]}...")
            
            # Clean up response (remove markdown code blocks if present)
            if ai_response.startswith("```json"):
                ai_response = ai_response[7:]
            if ai_response.endswith("```"):
                ai_response = ai_response[:-3]
            ai_response = ai_response.strip()
            
            # Parse JSON response
            try:
                analysis_result = json.loads(ai_response)
                
                # Extract contract data and add metadata
                contract_data = analysis_result.get("contract_data", {})
                contract_data["parsed_at"] = datetime.now().isoformat()
                contract_data["ai_model"] = self.model
                contract_data["confidence"] = "high"
                
                # Add events and completeness analysis to the result
                contract_data["rental_events"] = analysis_result.get("rental_events", [])
                contract_data["completeness_analysis"] = analysis_result.get("completeness_analysis", {})
                
                print("✅ Comprehensive contract analysis completed with OpenAI API")
                return contract_data
                
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parsing failed, falling back to rule-based extraction: {e}")
                return self._fallback_parsing(raw_text)
                
        except Exception as e:
            print(f"❌ OpenAI API error: {e}")
            print("🔄 Falling back to rule-based parsing...")
            return self._fallback_parsing(raw_text)
    
    def _fallback_parsing(self, raw_text: str) -> dict:
        """Fallback rule-based parsing when OpenAI API fails"""
        print("🧠 Using rule-based parsing (fallback mode)")
        
        try:
            # Extract data using simple rules
            contract_data = {
                "property": {
                    "building": None,
                    "unit": None,
                    "location": None,
                    "size_sqm": None,
                    "type": "Residential"
                },
                "parties": {
                    "landlord": {
                        "name": None,
                        "passport_no": None,
                        "phone_primary": None,
                        "phone_alt": None,
                        "email": None
                    },
                    "tenant": {
                        "name": None,
                        "passport_no": None,
                        "phone_primary": None,
                        "phone_alt": None,
                        "email": None
                    }
                },
                "lease": {
                    "start_date": None,
                    "end_date": None,
                    "duration_months": None,
                    "notice_period_days": None
                },
                "rent": {
                    "annual_aed": None,
                    "monthly_aed": None,
                    "cheques": {
                        "count": None,
                        "amount_per_cheque": None,
                        "dates": []
                    }
                },
                "deposit": {
                    "refundable_aed": None,
                    "security_deposit": None
                },
                "furnishing": {
                    "status": None,
                    "inventory_present": None
                },
                "responsibilities": {
                    "service_charges": None,
                    "dewa": None,
                    "chiller": None,
                    "ejari_registration": None,
                    "maintenance_major": None,
                    "maintenance_minor": None,
                    "maintenance_minor_cap": None
                },
                "terms": {
                    "pets_allowed": None,
                    "subletting_allowed": None,
                    "early_termination_penalty": None,
                    "renewal_notice_days": None,
                    "governing_law": None
                },
                "identifiers": {
                    "ejari_number": None,
                    "dewa_premise_no": None,
                    "plot_no": None
                },
                "parsed_at": datetime.now().isoformat(),
                "ai_model": "fallback",
                "confidence": "low",
                "rental_events": [],
                "completeness_analysis": {
                    "completeness_score": 0,
                    "quality_status": "incomplete",
                    "missing_critical": ["all_fields"],
                    "missing_important": [],
                    "needs_confirmation": [],
                    "actionable_gaps": [],
                    "validation_notes": ["Fallback parsing used - limited data extracted"]
                }
            }
            
            print("✅ Fallback parsing completed")
            return contract_data
            
        except Exception as e:
            print(f"Error in fallback parsing: {e}")
            return {
                "error": str(e), 
                "parsed_at": datetime.now().isoformat(),
                "rental_events": [],
                "completeness_analysis": {
                    "completeness_score": 0,
                    "quality_status": "error",
                    "missing_critical": ["all_fields"],
                    "missing_important": [],
                    "needs_confirmation": [],
                    "actionable_gaps": [],
                    "validation_notes": [f"Error in parsing: {str(e)}"]
                }
            }

# Initialize services
colab_client = ColabOCRClient(COLAB_URL)
contract_intelligence = ContractIntelligence(OPENAI_API_KEY)

@app.get("/")
async def root():
    """Serve the main web interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Contract Intelligence Agent</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: white; 
                border-radius: 20px; 
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .header { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 40px; 
                text-align: center; 
            }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .header p { font-size: 1.2em; opacity: 0.9; }
            .upload-section { 
                padding: 40px; 
                text-align: center; 
                border-bottom: 1px solid #eee;
            }
            .upload-area { 
                border: 3px dashed #667eea; 
                border-radius: 15px; 
                padding: 60px 20px; 
                margin: 20px 0; 
                background: #f8f9ff;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .upload-area:hover { 
                border-color: #764ba2; 
                background: #f0f2ff; 
            }
            .upload-area.dragover { 
                border-color: #764ba2; 
                background: #e8ebff; 
                transform: scale(1.02);
            }
            .upload-icon { 
                font-size: 4em; 
                color: #667eea; 
                margin-bottom: 20px; 
            }
            .file-input { 
                display: none; 
            }
            .btn { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                border: none; 
                padding: 15px 30px; 
                border-radius: 50px; 
                font-size: 1.1em; 
                cursor: pointer; 
                transition: all 0.3s ease;
                margin: 10px;
            }
            .btn:hover { 
                transform: translateY(-2px); 
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            .btn:disabled { 
                opacity: 0.6; 
                cursor: not-allowed; 
                transform: none;
            }
            .progress { 
                display: none; 
                margin: 20px 0; 
            }
            .progress-bar { 
                width: 100%; 
                height: 8px; 
                background: #f0f0f0; 
                border-radius: 4px; 
                overflow: hidden; 
            }
            .progress-fill { 
                height: 100%; 
                background: linear-gradient(90deg, #667eea, #764ba2); 
                width: 0%; 
                transition: width 0.3s ease; 
            }
            .results { 
                display: none; 
                padding: 40px; 
            }
            .section { 
                margin: 30px 0; 
                padding: 25px; 
                background: #f8f9ff; 
                border-radius: 15px; 
                border-left: 5px solid #667eea;
            }
            .section h3 { 
                color: #333; 
                margin-bottom: 15px; 
                font-size: 1.3em;
            }
            .field { 
                display: flex; 
                justify-content: space-between; 
                padding: 8px 0; 
                border-bottom: 1px solid #eee; 
            }
            .field:last-child { 
                border-bottom: none; 
            }
            .field-label { 
                font-weight: 600; 
                color: #555; 
            }
            .field-value { 
                color: #333; 
                text-align: right; 
            }
            .events { 
                display: grid; 
                gap: 15px; 
                margin-top: 20px; 
            }
            .event { 
                padding: 20px; 
                border-radius: 10px; 
                border-left: 5px solid; 
                background: white;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .event.payment_due { border-left-color: #4CAF50; }
            .event.renewal_window_start { border-left-color: #FF9800; }
            .event.renewal_window_mid { border-left-color: #FF9800; }
            .event.renewal_deadline { border-left-color: #F44336; }
            .event.notice_deadline { border-left-color: #E91E63; }
            .event.maintenance_reminder { border-left-color: #00BCD4; }
            .event.deposit_return_reminder { border-left-color: #8BC34A; }
            .event.compliance_alert { border-left-color: #FFC107; }
            .event.pest_control_reminder { border-left-color: #795548; }
            .event.move_out_utilities { border-left-color: #9E9E9E; }
            .event-title { 
                font-weight: 600; 
                margin-bottom: 8px; 
                color: #333;
            }
            .event-date { 
                color: #666; 
                font-size: 0.9em; 
                margin-bottom: 8px;
            }
            .event-description { 
                color: #555; 
                margin-bottom: 10px;
            }
            .automated-actions { 
                display: flex; 
                flex-wrap: wrap; 
                gap: 8px; 
                margin-top: 10px;
            }
            .action-chip { 
                background: #e3f2fd; 
                color: #1976d2; 
                padding: 4px 12px; 
                border-radius: 20px; 
                font-size: 0.8em; 
                border: 1px solid #bbdefb;
            }
            .completeness-analysis { 
                margin-top: 20px; 
            }
            .gap-item { 
                padding: 15px; 
                margin: 10px 0; 
                background: white; 
                border-radius: 10px; 
                border-left: 4px solid #ff9800;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .gap-title { 
                font-weight: 600; 
                color: #333; 
                margin-bottom: 5px;
            }
            .gap-description { 
                color: #666; 
                margin-bottom: 10px;
            }
            .gap-actions { 
                display: flex; 
                flex-wrap: wrap; 
                gap: 8px;
            }
            .gap-action { 
                background: #fff3e0; 
                color: #f57c00; 
                padding: 4px 12px; 
                border-radius: 20px; 
                font-size: 0.8em; 
                border: 1px solid #ffcc02;
            }
            .status { 
                padding: 20px; 
                text-align: center; 
                border-radius: 10px; 
                margin: 20px 0; 
            }
            .status.success { 
                background: #e8f5e8; 
                color: #2e7d32; 
                border: 1px solid #4caf50; 
            }
            .status.error { 
                background: #ffebee; 
                color: #c62828; 
                border: 1px solid #f44336; 
            }
            .status.info { 
                background: #e3f2fd; 
                color: #1565c0; 
                border: 1px solid #2196f3; 
            }
            @media (max-width: 768px) {
                .container { margin: 10px; border-radius: 15px; }
                .header { padding: 30px 20px; }
                .header h1 { font-size: 2em; }
                .upload-section, .results { padding: 30px 20px; }
                .field { flex-direction: column; text-align: left; }
                .field-value { text-align: left; margin-top: 5px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Contract Intelligence Agent</h1>
                <p>AI-powered rental contract analysis with OCR and automated event generation</p>
            </div>
            
            <div class="upload-section">
                <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                    <div class="upload-icon">📄</div>
                    <h3>Upload Rental Contract</h3>
                    <p>Drag & drop your PDF contract here or click to browse</p>
                    <p style="color: #666; font-size: 0.9em; margin-top: 10px;">
                        Supports PDF files up to 10MB
                    </p>
                </div>
                
                <input type="file" id="fileInput" class="file-input" accept=".pdf" />
                <button class="btn" onclick="analyzeContract()" id="analyzeBtn" disabled>
                    🚀 Analyze Contract
                </button>
                
                <div class="progress" id="progress">
                    <div class="progress-bar">
                        <div class="progress-fill" id="progressFill"></div>
                    </div>
                    <p id="progressText">Processing...</p>
                </div>
            </div>
            
            <div class="results" id="results">
                <!-- Results will be populated here -->
            </div>
        </div>

        <script>
            let selectedFile = null;
            
            // File input handling
            document.getElementById('fileInput').addEventListener('change', function(e) {
                selectedFile = e.target.files[0];
                if (selectedFile) {
                    document.getElementById('analyzeBtn').disabled = false;
                    document.querySelector('.upload-area').style.borderColor = '#4CAF50';
                    document.querySelector('.upload-area').innerHTML = `
                        <div class="upload-icon">✅</div>
                        <h3>File Selected</h3>
                        <p>${selectedFile.name}</p>
                        <p style="color: #666; font-size: 0.9em;">Click "Analyze Contract" to proceed</p>
                    `;
                }
            });
            
            // Drag and drop handling
            const uploadArea = document.querySelector('.upload-area');
            
            uploadArea.addEventListener('dragover', function(e) {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });
            
            uploadArea.addEventListener('dragleave', function(e) {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
            });
            
            uploadArea.addEventListener('drop', function(e) {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    selectedFile = files[0];
                    document.getElementById('fileInput').files = files;
                    document.getElementById('analyzeBtn').disabled = false;
                    uploadArea.style.borderColor = '#4CAF50';
                    uploadArea.innerHTML = `
                        <div class="upload-icon">✅</div>
                        <h3>File Selected</h3>
                        <p>${selectedFile.name}</p>
                        <p style="color: #666; font-size: 0.9em;">Click "Analyze Contract" to proceed</p>
                    `;
                }
            });
            
            async function analyzeContract() {
                if (!selectedFile) return;
                
                const formData = new FormData();
                formData.append('file', selectedFile);
                
                // Show progress
                document.getElementById('progress').style.display = 'block';
                document.getElementById('analyzeBtn').disabled = true;
                document.getElementById('results').style.display = 'none';
                
                // Simulate progress
                let progress = 0;
                const progressInterval = setInterval(() => {
                    progress += Math.random() * 15;
                    if (progress > 90) progress = 90;
                    document.getElementById('progressFill').style.width = progress + '%';
                    document.getElementById('progressText').textContent = 
                        progress < 30 ? 'Uploading file...' :
                        progress < 60 ? 'Processing with OCR...' :
                        progress < 90 ? 'Analyzing with AI...' : 'Finalizing results...';
                }, 500);
                
                try {
                    const response = await fetch('/api/analyze', {
                        method: 'POST',
                        body: formData
                    });
                    
                    clearInterval(progressInterval);
                    document.getElementById('progressFill').style.width = '100%';
                    document.getElementById('progressText').textContent = 'Complete!';
                    
                    if (response.ok) {
                        const result = await response.json();
                        displayResults(result);
                    } else {
                        const error = await response.json();
                        showError(error.detail || 'Analysis failed');
                    }
                } catch (error) {
                    clearInterval(progressInterval);
                    showError('Network error: ' + error.message);
                }
                
                document.getElementById('progress').style.display = 'none';
                document.getElementById('analyzeBtn').disabled = false;
            }
            
            function displayResults(result) {
                const resultsDiv = document.getElementById('results');
                resultsDiv.style.display = 'block';
                
                let html = '<div class="status success">✅ Contract analysis completed successfully!</div>';
                
                // Contract Data
                if (result.contract_data) {
                    html += '<div class="section"><h3>📋 Contract Information</h3>';
                    
                    const contractData = result.contract_data;
                    
                    // Property Information
                    if (contractData.property) {
                        html += '<h4>🏠 Property</h4>';
                        Object.entries(contractData.property).forEach(([key, value]) => {
                            if (value) {
                                html += `<div class="field">
                                    <span class="field-label">${formatLabel(key)}</span>
                                    <span class="field-value">${value}</span>
                                </div>`;
                            }
                        });
                    }
                    
                    // Parties Information
                    if (contractData.parties) {
                        html += '<h4>👥 Parties</h4>';
                        if (contractData.parties.landlord) {
                            html += '<h5>Landlord</h5>';
                            Object.entries(contractData.parties.landlord).forEach(([key, value]) => {
                                if (value) {
                                    html += `<div class="field">
                                        <span class="field-label">${formatLabel(key)}</span>
                                        <span class="field-value">${value}</span>
                                    </div>`;
                                }
                            });
                        }
                        if (contractData.parties.tenant) {
                            html += '<h5>Tenant</h5>';
                            Object.entries(contractData.parties.tenant).forEach(([key, value]) => {
                                if (value) {
                                    html += `<div class="field">
                                        <span class="field-label">${formatLabel(key)}</span>
                                        <span class="field-value">${value}</span>
                                    </div>`;
                                }
                            });
                        }
                    }
                    
                    // Financial Information
                    if (contractData.rent || contractData.deposit) {
                        html += '<h4>💰 Financial</h4>';
                        if (contractData.rent) {
                            Object.entries(contractData.rent).forEach(([key, value]) => {
                                if (value) {
                                    html += `<div class="field">
                                        <span class="field-label">${formatLabel(key)}</span>
                                        <span class="field-value">${value}</span>
                                    </div>`;
                                }
                            });
                        }
                        if (contractData.deposit) {
                            Object.entries(contractData.deposit).forEach(([key, value]) => {
                                if (value) {
                                    html += `<div class="field">
                                        <span class="field-label">${formatLabel(key)}</span>
                                        <span class="field-value">${value}</span>
                                    </div>`;
                                }
                            });
                        }
                    }
                    
                    html += '</div>';
                }
                
                // Events
                if (result.rental_events && result.rental_events.length > 0) {
                    html += '<div class="section"><h3>📅 Rental Events</h3><div class="events">';
                    
                    result.rental_events.forEach(event => {
                        html += `<div class="event ${event.event_type}">
                            <div class="event-title">${event.title}</div>
                            <div class="event-date">📅 ${event.date}</div>
                            <div class="event-description">${event.description}</div>`;
                        
                        if (event.automated_actions && event.automated_actions.length > 0) {
                            html += '<div class="automated-actions">';
                            event.automated_actions.forEach(action => {
                                html += `<span class="action-chip">${action}</span>`;
                            });
                            html += '</div>';
                        }
                        
                        html += '</div>';
                    });
                    
                    html += '</div></div>';
                }
                
                // Completeness Analysis
                if (result.completeness_analysis) {
                    html += '<div class="section"><h3>🔍 Completeness Analysis</h3>';
                    
                    const analysis = result.completeness_analysis;
                    
                    if (analysis.actionable_gaps && analysis.actionable_gaps.length > 0) {
                        html += '<div class="completeness-analysis">';
                        analysis.actionable_gaps.forEach(gap => {
                            html += `<div class="gap-item">
                                <div class="gap-title">${gap.label}</div>
                                <div class="gap-description">${gap.description}</div>`;
                            
                            if (gap.automated_action) {
                                html += `<div class="gap-actions">
                                    <span class="gap-action">${gap.automated_action}</span>
                                </div>`;
                            }
                            
                            html += '</div>';
                        });
                        html += '</div>';
                    }
                    
                    html += '</div>';
                }
                
                resultsDiv.innerHTML = html;
                
                // Scroll to results
                resultsDiv.scrollIntoView({ behavior: 'smooth' });
            }
            
            function formatLabel(key) {
                return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            }
            
            function showError(message) {
                const resultsDiv = document.getElementById('results');
                resultsDiv.style.display = 'block';
                resultsDiv.innerHTML = `<div class="status error">❌ ${message}</div>`;
                resultsDiv.scrollIntoView({ behavior: 'smooth' });
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/api/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    """Analyze uploaded contract"""
    try:
        print(f"🤖 Starting contract analysis for {file.filename}")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Step 1: OCR Processing
            print("🚀 Step 1: Processing with Colab GPU OCR...")
            ocr_result = colab_client.process_contract(temp_file_path)
            
            if not ocr_result or not ocr_result.get('text'):
                return JSONResponse(
                    status_code=400,
                    content={"detail": "OCR processing failed - no text extracted"}
                )
            
            print(f"✅ OCR completed: {len(ocr_result['text'])} characters")
            
            # Step 2: AI Analysis
            print("🧠 Step 2: Comprehensive AI analysis with OpenAI API...")
            analysis_result = contract_intelligence.parse_contract(ocr_result['text'])
            
            print(f"✅ AI analysis completed - Generated {len(analysis_result.get('rental_events', []))} events, Completeness: {analysis_result.get('completeness_analysis', {}).get('completeness_score', 'N/A')}%")
            
            return JSONResponse(content=analysis_result)
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Analysis failed: {str(e)}"}
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check Colab API
        colab_status = await colab_client.health_check()
        
        # Check OpenAI API
        openai_status = "✅ OpenAI API initialized" if OPENAI_API_KEY else "❌ OpenAI API key missing"
        
        return JSONResponse(content={
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "colab_ocr": colab_status,
                "openai": openai_status
            }
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "error": str(e)}
        )

# For Vercel
handler = app