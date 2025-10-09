#!/usr/bin/env python3
"""
Contract Intelligence Agent - Simple Vercel Version
"""

import os
import json
import tempfile
import requests
from datetime import datetime
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
import openai

# Initialize FastAPI app
app = FastAPI(title="Contract Intelligence Agent")

# Configuration
COLAB_URL = os.getenv('COLAB_OCR_URL', 'https://snaillike-russel-snodly.ngrok-free.dev')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

def process_ocr(file_path: str) -> dict:
    """Process file with Colab OCR"""
    try:
        print(f"🔍 DEBUG: Attempting OCR with URL: {COLAB_URL}/ocr")
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{COLAB_URL}/ocr", files=files, timeout=60)
        
        print(f"🔍 DEBUG: OCR response status: {response.status_code}")
        print(f"🔍 DEBUG: OCR response content: {response.text[:200]}...")
        
        if response.status_code == 200:
            result = response.json()
            print(f"🔍 DEBUG: OCR success, text length: {len(result.get('text', ''))}")
            return result
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            print(f"🔍 DEBUG: OCR failed: {error_msg}")
            return {"text": "", "error": error_msg}
    except Exception as e:
        error_msg = f"OCR Exception: {str(e)}"
        print(f"🔍 DEBUG: OCR exception: {error_msg}")
        return {"text": "", "error": error_msg}

def analyze_contract_ai(text: str) -> dict:
    """Analyze contract with OpenAI"""
    try:
        prompt = f"""
You are an expert contract analyst specializing in Dubai rental agreements. 
Analyze the following contract text and provide a comprehensive analysis in JSON format.

Contract Text:
{text}

Return ONLY a valid JSON object with the following structure:
{{
    "contract_data": {{
        "property": {{
            "building": "Building name (e.g., 'Resortz Residence Block 2')",
            "unit": "Unit number (e.g., 'Apt 113')",
            "location": "Full location (e.g., 'Arjan, Al Barsha South Third, Dubai')",
            "size_sqm": 85.42,
            "type": "Property type (Residential, Commercial, etc.)"
        }},
        "parties": {{
            "landlord": {{
                "name": "Full landlord name",
                "passport_no": "Passport number if mentioned",
                "phone_primary": "Primary phone number",
                "phone_alt": "Alternative phone number if mentioned",
                "email": "Email address if mentioned"
            }},
            "tenant": {{
                "name": "Full tenant name",
                "passport_no": "Passport number if mentioned",
                "phone_primary": "Primary phone number if mentioned",
                "email": "Email address if mentioned"
            }},
            "agent": {{
                "name": "Real estate agent or company name",
                "email": "Agent email if mentioned",
                "phone": "Agent phone if mentioned"
            }}
        }},
        "identifiers": {{
            "dewa_premise_no": "DEWA premise number if mentioned",
            "plot_no": "Plot number if mentioned",
            "ejari_number": "Ejari registration number if mentioned"
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
                "amounts": [12000.00, 12000.00, 12000.00, 12000.00],
                "dates": ["2021-07-20", "2021-10-20", "2022-01-20", "2022-04-20"]
            }}
        }},
        "deposit": {{
            "refundable_aed": 4000.00,
            "type": "Security deposit"
        }},
        "furnishing": {{
            "status": "Fully furnished/Unfurnished/Partially furnished",
            "inventory_present": true
        }},
        "responsibilities": {{
            "service_charges": {{
                "party": "Landlord/Tenant",
                "amount": "Amount if specified"
            }},
            "dewa": {{
                "party": "Landlord/Tenant"
            }},
            "chiller": {{
                "party": "Landlord/Tenant",
                "amount": "Amount if specified"
            }},
            "maintenance": {{
                "major_party": "Landlord/Tenant",
                "minor_party": "Landlord/Tenant",
                "minor_cap_aed": 500.00
            }},
            "ejari_registration": {{
                "party": "Landlord/Tenant",
                "conflict_notes": "Any conflicting clauses"
            }}
        }},
        "terms": {{
            "pets_allowed": false,
            "subletting_allowed": false,
            "early_termination": {{
                "notice_days": 30,
                "penalty": "Penalty description"
            }},
            "renewal": {{
                "notice_days": 90,
                "broker_fee": "Broker fee if mentioned"
            }}
        }}
    }},
    "rental_events": [
        {{
            "event_type": "payment_due",
            "title": "Rent Payment Due",
            "description": "Monthly rent payment due",
            "due_date": "2021-08-20",
            "priority": "high",
            "automated_action": "Send WhatsApp Reminder"
        }},
        {{
            "event_type": "renewal_window_start",
            "title": "Renewal Window Opens",
            "description": "90-day renewal notice period begins",
            "due_date": "2022-04-20",
            "priority": "medium",
            "automated_action": "Add to Calendar"
        }}
    ],
    "completeness_analysis": {{
        "completeness_score": 85,
        "missing_critical": ["ejari_number", "tenant_phone"],
        "missing_important": ["cheque_dates", "inventory_list"],
        "needs_confirmation": ["ejari_registration_party"],
        "suggested_improvements": [
            "Upload Ejari certificate",
            "Add tenant contact details"
        ],
        "actionable_gaps": [
            {{
                "type": "missing_document",
                "field": "ejari_certificate",
                "label": "Ejari Certificate",
                "description": "Ejari registration certificate not found",
                "priority": "high",
                "status": "missing",
                "automated_action": "Request Upload"
            }}
        ]
    }}
}}

IMPORTANT INSTRUCTIONS:
1. Extract ONLY information explicitly stated in the contract text
2. Do NOT make assumptions or derive values not clearly mentioned
3. Use null for missing information, not placeholder text
4. Format dates as YYYY-MM-DD
5. Format currency amounts as numbers (e.g., 48000.00)
6. Return ONLY the JSON object, no additional text or explanations
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=3000,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        
        # Clean JSON response
        if result.startswith('```json'):
            result = result.replace('```json', '').replace('```', '').strip()
        elif result.startswith('```'):
            result = result.replace('```', '').strip()
        
        return json.loads(result)
        
    except Exception as e:
        return {
            "error": str(e),
            "contract_data": {
                "property": {"building": "Error", "unit": "Error", "location": "Error"},
                "parties": {"landlord": {"name": "Error"}, "tenant": {"name": "Error"}},
                "rent": {"annual_aed": 0, "monthly_aed": 0},
                "deposit": {"refundable_aed": 0}
            },
            "rental_events": [],
            "completeness_analysis": {"completeness_score": 0, "missing_critical": [], "actionable_gaps": []}
        }

@app.get("/")
async def root():
    """Main interface"""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Contract Intelligence Agent - Debug v321d13e</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        .header { text-align: center; margin-bottom: 30px; }
        .upload-section { border: 2px dashed #ddd; padding: 30px; text-align: center; margin-bottom: 30px; border-radius: 8px; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .results { margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 5px; }
        .metric { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Contract Intelligence Agent</h1>
            <p>AI-powered rental contract analysis</p>
        </div>
        
        <div class="upload-section">
            <h3>📄 Upload Contract PDF</h3>
            <input type="file" id="fileInput" accept=".pdf" style="margin: 10px;">
            <br>
            <button class="btn" onclick="analyzeContract()">🚀 Analyze Contract</button>
        </div>
        
        <div id="results" class="results" style="display: none;">
            <h3>📊 Analysis Results</h3>
            <div id="status">Processing...</div>
            <div id="content"></div>
        </div>
    </div>

    <script>
        async function analyzeContract() {
            const file = document.getElementById('fileInput').files[0];
            if (!file) {
                alert('Please select a PDF file');
                return;
            }

            document.getElementById('results').style.display = 'block';
            document.getElementById('status').textContent = 'Processing...';

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                
                // Debug: Log the result structure
                console.log('🔍 Full result:', result);
                console.log('🔍 Contract data:', result.contract_data);
                console.log('🔍 Rental events:', result.rental_events);
                console.log('🔍 Completeness analysis:', result.completeness_analysis);
                
                document.getElementById('status').textContent = 'Analysis complete!';
                document.getElementById('content').innerHTML = formatResults(result);
                
            } catch (error) {
                document.getElementById('status').textContent = 'Error: ' + error.message;
            }
        }

        function formatResults(result) {
            let html = '';
            
            // Debug: Show raw result structure
            html += '<div class="metric" style="background: #f0f0f0; border-left: 4px solid #ff6b6b;">';
            html += '<h4>🔍 Debug Info</h4>';
            html += `<strong>Result keys:</strong> ${Object.keys(result).join(', ')}<br>`;
            if (result.contract_data) {
                html += `<strong>Contract data keys:</strong> ${Object.keys(result.contract_data).join(', ')}<br>`;
            }
            html += '</div>';
            
            if (result.contract_data) {
                html += '<div class="metric">';
                html += '<h4>📋 Contract Data</h4>';
                html += `<strong>Property:</strong> ${result.contract_data.property?.building || 'N/A'}<br>`;
                html += `<strong>Unit:</strong> ${result.contract_data.property?.unit || 'N/A'}<br>`;
                html += `<strong>Location:</strong> ${result.contract_data.property?.location || 'N/A'}<br>`;
                html += `<strong>Annual Rent:</strong> AED ${result.contract_data.rent?.annual_aed || 'N/A'}<br>`;
                html += `<strong>Monthly Rent:</strong> AED ${result.contract_data.rent?.monthly_aed || 'N/A'}<br>`;
                html += `<strong>Deposit:</strong> AED ${result.contract_data.deposit?.refundable_aed || 'N/A'}<br>`;
                html += '</div>';
            }

            if (result.rental_events && result.rental_events.length > 0) {
                html += '<div class="metric">';
                html += '<h4>📅 Rental Events</h4>';
                result.rental_events.forEach(event => {
                    html += `<div style="margin: 10px 0; padding: 10px; background: #fff; border-radius: 5px;">`;
                    html += `<strong>${event.title || event.event_type}</strong><br>`;
                    html += `${event.description || ''}<br>`;
                    html += `<small>Due: ${event.due_date || 'N/A'}</small>`;
                    html += '</div>';
                });
                html += '</div>';
            }

            if (result.completeness_analysis) {
                html += '<div class="metric">';
                html += '<h4>✅ Completeness Analysis</h4>';
                html += `<strong>Score:</strong> ${result.completeness_analysis.completeness_score || 0}%<br>`;
                if (result.completeness_analysis.missing_critical) {
                    html += `<strong>Missing Critical:</strong> ${result.completeness_analysis.missing_critical.join(', ')}<br>`;
                }
                html += '</div>';
            }

            return html;
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html)

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
            ocr_result = process_ocr(temp_file_path)
            
            if not ocr_result or not ocr_result.get('text'):
                return JSONResponse(
                    status_code=400,
                    content={"detail": "OCR processing failed"}
                )
            
            # Step 2: AI Analysis
            analysis_result = analyze_contract_ai(ocr_result['text'])
            
            # Debug: Log the structure being returned
            print(f"🔍 DEBUG: Analysis result keys: {list(analysis_result.keys())}")
            if 'contract_data' in analysis_result:
                print(f"🔍 DEBUG: Contract data keys: {list(analysis_result['contract_data'].keys())}")
            if 'rental_events' in analysis_result:
                print(f"🔍 DEBUG: Rental events count: {len(analysis_result['rental_events'])}")
            
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

@app.get("/api/test-ai")
async def test_ai():
    """Test AI function with sample text"""
    sample_text = "This is a rental contract for Resortz Residence Block 2, Apt 113. Annual rent is AED 48,000. Tenant is John Doe."
    result = analyze_contract_ai(sample_text)
    return JSONResponse(content={
        "test_result": result,
        "keys": list(result.keys()) if isinstance(result, dict) else "Not a dict"
    })

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        colab_status = "healthy" if COLAB_URL else "unhealthy"
        openai_status = "healthy" if OPENAI_API_KEY else "unhealthy"
        
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

# For Vercel - app is the main instance
# Force deployment update - commit 78b3162
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)