#!/usr/bin/env python3
"""
Contract Intelligence Agent - Vercel Serverless
AI-powered contract analysis with OCR and automated event generation
"""

import os
import json
import tempfile
from datetime import datetime
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Import our modular components
from .colab_client import ColabOCRClient
from .contract_intelligence import ContractIntelligence

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
        .text-output { background: #f8f9fa; padding: 20px; border-radius: 5px; max-height: 400px; overflow-y: auto; font-family: monospace; white-space: pre-wrap; }
        .contract-data { background: #e8f5e8; padding: 20px; border-radius: 5px; margin: 20px 0; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
        .btn:hover { background: #0056b3; }
        .btn-success { background: #28a745; }
        .btn-warning { background: #ffc107; color: black; }
        .progress-bar { width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; overflow: hidden; margin: 10px 0; }
        .progress-fill { height: 100%; background: #007bff; width: 0%; transition: width 0.3s ease; }
        .event-card { background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px 0; }
        .event-high { border-left: 4px solid #dc3545; }
        .event-medium { border-left: 4px solid #ffc107; }
        .event-low { border-left: 4px solid #28a745; }
        .completeness-section { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .gap-item { background: #fff; border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 5px 0; }
        .gap-critical { border-left: 4px solid #dc3545; }
        .gap-important { border-left: 4px solid #ffc107; }
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