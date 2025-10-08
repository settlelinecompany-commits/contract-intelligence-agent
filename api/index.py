#!/usr/bin/env python3
"""
Contract Intelligence Agent - Vercel Serverless Version
AI-powered contract analysis with OCR and automated event generation
"""

import os
import sys
import json
import tempfile
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from colab_client import ColabOCRClient
from src.parser.contract_intelligence import ContractIntelligence
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
            .event.payment { border-left-color: #4CAF50; }
            .event.renewal { border-left-color: #FF9800; }
            .event.maintenance { border-left-color: #2196F3; }
            .event.deposit { border-left-color: #9C27B0; }
            .event.inventory { border-left-color: #607D8B; }
            .event.renewal_window_start { border-left-color: #FF5722; }
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
            
            print(f"✅ AI analysis completed - Generated {len(analysis_result.get('rental_events', []))} events, Completeness: {analysis_result.get('completeness_analysis', {}).get('completeness_percentage', 'N/A')}%")
            
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
