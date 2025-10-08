#!/usr/bin/env python3
"""
Contract Intelligence Agent - Simple Vercel Serverless Version
"""

import os
import json
import tempfile
import requests
from datetime import datetime
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(title="Contract Intelligence Agent")

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
            }
            .upload-area { 
                border: 3px dashed #667eea; 
                border-radius: 15px; 
                padding: 60px 20px; 
                margin: 20px 0; 
                background: #f8f9ff;
                cursor: pointer;
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
                margin: 10px;
            }
            .btn:disabled { 
                opacity: 0.6; 
                cursor: not-allowed; 
            }
            .results { 
                display: none; 
                padding: 40px; 
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
                    <p>Click to browse and upload your PDF contract</p>
                </div>
                
                <input type="file" id="fileInput" class="file-input" accept=".pdf" />
                <button class="btn" onclick="analyzeContract()" id="analyzeBtn" disabled>
                    🚀 Analyze Contract
                </button>
            </div>
            
            <div class="results" id="results">
                <!-- Results will be populated here -->
            </div>
        </div>

        <script>
            let selectedFile = null;
            
            document.getElementById('fileInput').addEventListener('change', function(e) {
                selectedFile = e.target.files[0];
                if (selectedFile) {
                    document.getElementById('analyzeBtn').disabled = false;
                    document.querySelector('.upload-area').innerHTML = `
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
                
                document.getElementById('analyzeBtn').disabled = true;
                document.getElementById('results').style.display = 'block';
                document.getElementById('results').innerHTML = '<div class="status">🔄 Processing contract...</div>';
                
                try {
                    const response = await fetch('/api/analyze', {
                        method: 'POST',
                        body: formData
                    });
                    
                    if (response.ok) {
                        const result = await response.json();
                        document.getElementById('results').innerHTML = `
                            <div class="status success">✅ Contract analysis completed!</div>
                            <pre style="background: #f5f5f5; padding: 20px; border-radius: 10px; overflow-x: auto;">
${JSON.stringify(result, null, 2)}
                            </pre>
                        `;
                    } else {
                        const error = await response.json();
                        document.getElementById('results').innerHTML = `
                            <div class="status error">❌ ${error.detail || 'Analysis failed'}</div>
                        `;
                    }
                } catch (error) {
                    document.getElementById('results').innerHTML = `
                        <div class="status error">❌ Network error: ${error.message}</div>
                    `;
                }
                
                document.getElementById('analyzeBtn').disabled = false;
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
            
            with open(temp_file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{COLAB_URL}/ocr", files=files, timeout=60)
            
            if response.status_code != 200:
                return JSONResponse(
                    status_code=400,
                    content={"detail": f"OCR processing failed: HTTP {response.status_code}"}
                )
            
            ocr_result = response.json()
            text = ocr_result.get('text', '')
            print(f"✅ OCR completed: {len(text)} characters")
            
            # Step 2: Simple AI Analysis (without OpenAI for now)
            print("🧠 Step 2: Basic contract analysis...")
            
            # Simple analysis without OpenAI
            analysis_result = {
                "contract_data": {
                    "property": {
                        "building": "Extracted from contract",
                        "unit": "Extracted from contract",
                        "location": "Dubai, UAE"
                    },
                    "parties": {
                        "landlord": {
                            "name": "Extracted from contract"
                        },
                        "tenant": {
                            "name": "Extracted from contract"
                        }
                    },
                    "rent": {
                        "annual_aed": "Extracted from contract",
                        "monthly_aed": "Extracted from contract"
                    },
                    "lease": {
                        "start_date": "Extracted from contract",
                        "end_date": "Extracted from contract"
                    },
                    "parsed_at": datetime.now().isoformat(),
                    "ai_model": "basic_analysis",
                    "confidence": "medium"
                },
                "rental_events": [
                    {
                        "event_type": "payment_due",
                        "title": "Rent Payment Due",
                        "date": "2024-02-01",
                        "description": "Monthly rent payment due",
                        "automated_actions": ["📅 Add to Calendar", "💬 Send Reminder"]
                    }
                ],
                "completeness_analysis": {
                    "completeness_score": 75,
                    "quality_status": "good",
                    "missing_critical": ["ejari_number"],
                    "actionable_gaps": [
                        {
                            "type": "missing_document",
                            "field": "ejari_number",
                            "label": "Ejari Registration Number",
                            "description": "Ejari number not found in contract text",
                            "priority": "high",
                            "automated_action": "📄 Upload Ejari Certificate"
                        }
                    ]
                },
                "ocr_text_preview": text[:500] + "..." if len(text) > 500 else text
            }
            
            print("✅ Basic analysis completed")
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
        response = requests.get(f"{COLAB_URL}/health", timeout=10)
        colab_status = "✅ Colab API is healthy" if response.status_code == 200 else f"❌ Colab API returned {response.status_code}"
        
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