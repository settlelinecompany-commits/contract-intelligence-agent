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
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{COLAB_URL}/ocr", files=files, timeout=60)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"text": "", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"text": "", "error": str(e)}

def analyze_contract_ai(text: str) -> dict:
    """Analyze contract with OpenAI"""
    try:
        prompt = f"""
Analyze this rental contract and return JSON with:
- property details (building, unit, location)
- parties (landlord, tenant names)
- lease terms (start_date, end_date)
- rent details (annual_aed, monthly_aed)
- deposit amount
- rental events (payment dates, renewal reminders)
- completeness analysis (missing fields)

Contract text: {text}

Return valid JSON only.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
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
            "contract_data": {"property": {"building": "Error", "unit": "Error"}},
            "rental_events": [],
            "completeness_analysis": {"completeness_score": 0}
        }

@app.get("/")
async def root():
    """Main interface"""
    html = """
<!DOCTYPE html>
<html>
<head>
    <title>Contract Intelligence Agent</title>
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
                
                document.getElementById('status').textContent = 'Analysis complete!';
                document.getElementById('content').innerHTML = formatResults(result);
                
            } catch (error) {
                document.getElementById('status').textContent = 'Error: ' + error.message;
            }
        }

        function formatResults(result) {
            let html = '';
            
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
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)