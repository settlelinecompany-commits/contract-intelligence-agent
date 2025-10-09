#!/usr/bin/env python3
"""
Contract Intelligence Agent - Single File Vercel Solution
AI-powered contract analysis with OCR and automated event generation
"""

import os
import json
import tempfile
import requests
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import openai

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
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.colab_url}/ocr", files=files, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                return {"text": "", "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            return {"text": "", "error": str(e)}

class ContractIntelligence:
    """AI-powered contract analysis"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.model = "gpt-4o-mini"
    
    def parse_contract(self, raw_text: str) -> dict:
        """Parse contract text using OpenAI API"""
        
        try:
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
                "name": "Full landlord name",
                "passport_no": "Passport number",
                "phone_primary": "Primary phone",
                "email": "Email address"
            }},
            "tenant": {{
                "name": "Full tenant name",
                "passport_no": "Passport number", 
                "phone_primary": "Primary phone",
                "email": "Email address"
            }}
        }},
        "lease": {{
            "start_date": "2021-07-20",
            "end_date": "2022-07-19",
            "duration_months": 12
        }},
        "rent": {{
            "annual_aed": 48000.00,
            "monthly_aed": 4000.00,
            "cheques": {{
                "count": 4,
                "amounts": [12000.00, 12000.00, 12000.00, 12000.00]
            }}
        }},
        "deposit": {{
            "refundable_aed": 4000.00
        }},
        "furnishing": {{
            "status": "Fully furnished"
        }}
    }},
    "rental_events": [
        {{
            "event_type": "rent_payment",
            "title": "Rent Payment Due",
            "description": "Monthly rent payment",
            "due_date": "2021-08-20",
            "priority": "high",
            "automated_actions": [
                "📅 Add to Calendar",
                "📧 Send Reminder"
            ]
        }}
    ],
    "completeness_analysis": {{
        "completeness_score": 85,
        "quality_status": "good",
        "missing_critical": ["ejari_number"],
        "actionable_gaps": [
            {{
                "type": "upload",
                "field": "ejari_number",
                "label": "Upload Ejari PDF",
                "description": "Ejari certificate required",
                "priority": "critical",
                "automated_action": "📄 Request Document Upload"
            }}
        ]
    }}
}}

IMPORTANT: 
- Extract ONLY information explicitly stated in the contract
- Use null for missing information, don't make assumptions
- Format dates as YYYY-MM-DD
- Format currency as numbers (e.g., 48000.00)
- Return valid JSON only, no markdown formatting
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.1
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Clean up response if it has markdown formatting
            if ai_response.startswith('```json'):
                ai_response = ai_response.replace('```json', '').replace('```', '').strip()
            elif ai_response.startswith('```'):
                ai_response = ai_response.replace('```', '').strip()
            
            # Parse JSON response
            analysis_result = json.loads(ai_response)
            
            # Extract contract data and add metadata
            contract_data = analysis_result.get("contract_data", {})
            contract_data["parsed_at"] = datetime.now().isoformat()
            contract_data["ai_model"] = self.model
            contract_data["confidence"] = "high"
            
            # Add events and completeness analysis to the result
            contract_data["rental_events"] = analysis_result.get("rental_events", [])
            contract_data["completeness_analysis"] = analysis_result.get("completeness_analysis", {})
            
            return contract_data
            
        except Exception as e:
            return self._fallback_parsing(raw_text)
    
    def _fallback_parsing(self, raw_text: str) -> dict:
        """Fallback parsing if AI fails"""
        return {
            "contract_data": {
                "property": {"building": "Unknown", "unit": "Unknown", "location": "Unknown"},
                "parties": {"landlord": {"name": "Unknown"}, "tenant": {"name": "Unknown"}},
                "lease": {"start_date": "Unknown", "end_date": "Unknown"},
                "rent": {"annual_aed": 0, "monthly_aed": 0},
                "parsed_at": datetime.now().isoformat(),
                "ai_model": "fallback",
                "confidence": "low"
            },
            "rental_events": [],
            "completeness_analysis": {
                "completeness_score": 0,
                "quality_status": "failed",
                "missing_critical": ["all_fields"],
                "actionable_gaps": []
            }
        }

# Initialize components
colab_client = ColabOCRClient(COLAB_URL)
contract_intelligence = ContractIntelligence()

@app.get("/")
async def root():
    """Main web interface"""
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Contract Intelligence Agent</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .upload-section { border: 2px dashed #ddd; padding: 30px; text-align: center; margin-bottom: 30px; border-radius: 8px; }
        .upload-section:hover { border-color: #007bff; }
        .results-section { display: none; }
        .metric-card { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
        .contract-data { background: #e8f5e8; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .btn:hover { background: #0056b3; }
        .progress-bar { width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; margin: 10px 0; }
        .progress-fill { height: 100%; background: #007bff; width: 0%; transition: width 0.3s ease; }
        .event-card { background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px 0; }
        .event-high { border-left: 4px solid #dc3545; }
        .event-medium { border-left: 4px solid #ffc107; }
        .event-low { border-left: 4px solid #28a745; }
        .completeness-section { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .gap-item { background: #fff; border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 5px 0; }
        .gap-critical { border-left: 4px solid #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Contract Intelligence Agent</h1>
            <p>AI-powered rental contract analysis with OCR and automated event generation</p>
        </div>

        <div class="upload-section">
            <h3>📄 Upload Contract PDF</h3>
            <input type="file" id="fileInput" accept=".pdf" style="margin: 10px;">
            <br>
            <button class="btn" onclick="analyzeContract()">🚀 Analyze Contract</button>
        </div>

        <div class="results-section" id="resultsSection">
            <h3>📊 Analysis Results</h3>
            <div class="progress-bar">
                <div class="progress-fill" id="progressFill"></div>
            </div>
            <div id="statusMessage">Processing...</div>
            
            <div id="contractData" class="contract-data" style="display: none;">
                <h4>📋 Contract Data</h4>
                <div id="contractDetails"></div>
            </div>

            <div id="rentalEvents" style="display: none;">
                <h4>📅 Rental Events</h4>
                <div id="eventsList"></div>
            </div>

            <div id="completenessAnalysis" class="completeness-section" style="display: none;">
                <h4>✅ Completeness Analysis</h4>
                <div id="completenessDetails"></div>
            </div>
        </div>
    </div>

    <script>
        async function analyzeContract() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Please select a PDF file');
                return;
            }

            const resultsSection = document.getElementById('resultsSection');
            const progressFill = document.getElementById('progressFill');
            const statusMessage = document.getElementById('statusMessage');
            
            resultsSection.style.display = 'block';
            progressFill.style.width = '0%';
            statusMessage.textContent = 'Uploading file...';

            const formData = new FormData();
            formData.append('file', file);

            try {
                progressFill.style.width = '25%';
                statusMessage.textContent = 'Processing with OCR...';

                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    body: formData
                });

                progressFill.style.width = '75%';
                statusMessage.textContent = 'Analyzing with AI...';

                const result = await response.json();
                
                progressFill.style.width = '100%';
                statusMessage.textContent = 'Analysis complete!';

                displayResults(result);
                
            } catch (error) {
                statusMessage.textContent = 'Error: ' + error.message;
                progressFill.style.width = '0%';
            }
        }

        function displayResults(result) {
            // Display contract data
            if (result.contract_data) {
                document.getElementById('contractData').style.display = 'block';
                document.getElementById('contractDetails').innerHTML = formatContractData(result.contract_data);
            }

            // Display rental events
            if (result.rental_events && result.rental_events.length > 0) {
                document.getElementById('rentalEvents').style.display = 'block';
                document.getElementById('eventsList').innerHTML = formatEvents(result.rental_events);
            }

            // Display completeness analysis
            if (result.completeness_analysis) {
                document.getElementById('completenessAnalysis').style.display = 'block';
                document.getElementById('completenessDetails').innerHTML = formatCompleteness(result.completeness_analysis);
            }
        }

        function formatContractData(data) {
            let html = '<div class="metric-card">';
            html += `<strong>Property:</strong> ${data.property?.building || 'N/A'} - ${data.property?.unit || 'N/A'}<br>`;
            html += `<strong>Location:</strong> ${data.property?.location || 'N/A'}<br>`;
            html += `<strong>Annual Rent:</strong> AED ${data.rent?.annual_aed || 'N/A'}<br>`;
            html += `<strong>Monthly Rent:</strong> AED ${data.rent?.monthly_aed || 'N/A'}<br>`;
            html += `<strong>Lease Period:</strong> ${data.lease?.start_date || 'N/A'} to ${data.lease?.end_date || 'N/A'}<br>`;
            html += `<strong>Deposit:</strong> AED ${data.deposit?.refundable_aed || 'N/A'}<br>`;
            html += '</div>';
            return html;
        }

        function formatEvents(events) {
            let html = '';
            events.forEach(event => {
                const priorityClass = event.priority === 'high' ? 'event-high' : 
                                    event.priority === 'medium' ? 'event-medium' : 'event-low';
                html += `<div class="event-card ${priorityClass}">`;
                html += `<strong>${event.title}</strong><br>`;
                html += `${event.description}<br>`;
                html += `<small>Due: ${event.due_date}</small>`;
                if (event.automated_actions) {
                    html += '<br><small>Actions: ' + event.automated_actions.join(', ') + '</small>';
                }
                html += '</div>';
            });
            return html;
        }

        function formatCompleteness(analysis) {
            let html = `<div class="metric-card">Completeness Score: ${analysis.completeness_score}%</div>`;
            
            if (analysis.actionable_gaps && analysis.actionable_gaps.length > 0) {
                html += '<h5>Actionable Gaps:</h5>';
                analysis.actionable_gaps.forEach(gap => {
                    const priorityClass = gap.priority === 'critical' ? 'gap-critical' : 'gap-important';
                    html += `<div class="gap-item ${priorityClass}">`;
                    html += `<strong>${gap.label}</strong><br>`;
                    html += `${gap.description}<br>`;
                    html += `<small>Action: ${gap.automated_action}</small>`;
                    html += '</div>';
                });
            }
            
            return html;
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
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Step 1: OCR Processing
            ocr_result = colab_client.process_contract(temp_file_path)
            
            if not ocr_result or not ocr_result.get('text'):
                return JSONResponse(
                    status_code=400,
                    content={"detail": "OCR processing failed - no text extracted"}
                )
            
            # Step 2: AI Analysis
            analysis_result = contract_intelligence.parse_contract(ocr_result['text'])
            
            return JSONResponse(content=analysis_result)
            
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
                
    except Exception as e:
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
        openai_status = "✅ OpenAI API key present" if OPENAI_API_KEY else "❌ OpenAI API key missing"
        
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