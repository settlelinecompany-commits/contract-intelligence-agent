#!/usr/bin/env python3
"""
Contract Intelligence Agent
Combines Colab GPU OCR + OpenAI API for intelligent contract parsing
"""

import os
import sys
from datetime import datetime
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from colab_client import ColabOCRClient
from src.parser.contract_intelligence import ContractIntelligence
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Contract Intelligence Agent")

# Initialize components
COLAB_URL = os.getenv('COLAB_OCR_URL', 'https://snaillike-russel-snodly.ngrok-free.dev')
colab_client = None
contract_parser = None

def get_colab_client():
    """Get or create Colab client"""
    global colab_client
    if colab_client is None:
        colab_client = ColabOCRClient(COLAB_URL)
    return colab_client

def get_contract_parser():
    """Get or create contract parser"""
    global contract_parser
    if contract_parser is None:
        contract_parser = ContractIntelligence()
    return contract_parser


@app.get("/", response_class=HTMLResponse)
async def get_agent_interface():
    return """
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
            .progress-fill { height: 100%; background: #28a745; transition: width 0.3s; }
            .error { color: #dc3545; background: #f8d7da; padding: 10px; border-radius: 5px; margin: 10px 0; }
            .success { color: #155724; background: #d4edda; padding: 10px; border-radius: 5px; margin: 10px 0; }
            .agent-badge { background: #6f42c1; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; margin-left: 10px; }
            .ai-badge { background: #fd7e14; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; margin-left: 5px; }
            .step { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #17a2b8; }
            .priority-badge { font-size: 0.7em; font-weight: bold; text-transform: uppercase; padding: 2px 8px; border-radius: 12px; }
            .priority-badge.critical { background: #dc3545; color: white; }
            .priority-badge.high { background: #fd7e14; color: white; }
            .priority-badge.medium { background: #ffc107; color: black; }
            .priority-badge.low { background: #6c757d; color: white; }
            .automated-actions { margin-top: 15px; padding: 12px; background: #e9ecef; border-radius: 6px; border-left: 3px solid #6c757d; }
            .action-tags { display: flex; flex-wrap: wrap; gap: 6px; }
            .action-tag { background: #f8f9fa; color: #495057; padding: 4px 10px; border-radius: 15px; font-size: 0.8em; border: 1px dashed #6c757d; }
            .gap-chips { display: flex; flex-direction: column; gap: 10px; }
            .gap-chip { display: flex; align-items: center; padding: 15px; border-radius: 8px; border-left: 4px solid; }
            .gap-chip.critical { background: #f8d7da; border-left-color: #dc3545; }
            .gap-chip.important { background: #fff3cd; border-left-color: #ffc107; }
            .gap-chip.conflict { background: #d1ecf1; border-left-color: #17a2b8; }
            .gap-content { flex: 1; }
            .gap-label { font-weight: bold; display: block; margin-bottom: 5px; }
            .gap-description { color: #666; font-size: 0.9em; display: block; margin-bottom: 5px; }
            .automated-action { font-size: 0.8em; color: #6c757d; font-style: italic; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 Contract Intelligence Agent</h1>
                <p>AI-Powered Contract Analysis & Data Extraction</p>
                <span class="agent-badge">Intelligent Agent</span>
                <span class="ai-badge">OpenAI GPT</span>
            </div>
            
            <div class="upload-section">
                <h3>📄 Upload Rental Contract</h3>
                <p>Upload your rental contract PDF for intelligent analysis</p>
                <input type="file" id="fileInput" accept=".pdf" style="margin: 10px;">
                <br>
                <button class="btn" onclick="processContract()">🤖 Analyze Contract with AI</button>
                <div class="progress-bar" id="progressBar" style="display: none;">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div id="statusMessage"></div>
            </div>
            
            <div class="results-section" id="resultsSection">
                <h3>📊 Contract Analysis Results</h3>
                <div id="processingSteps"></div>
                <div id="contractData"></div>
                <div id="completenessAnalysis"></div>
                <div id="actionableGaps"></div>
                <div id="rentalEvents"></div>
                <div id="rawTextOutput"></div>
            </div>
        </div>

        <script>
            async function processContract() {
                const fileInput = document.getElementById('fileInput');
                const file = fileInput.files[0];
                
                if (!file) {
                    alert('Please select a PDF file');
                    return;
                }
                
                const progressBar = document.getElementById('progressBar');
                const progressFill = document.getElementById('progressFill');
                const statusMessage = document.getElementById('statusMessage');
                const resultsSection = document.getElementById('resultsSection');
                const processingSteps = document.getElementById('processingSteps');
                
                // Show progress
                progressBar.style.display = 'block';
                progressFill.style.width = '0%';
                statusMessage.innerHTML = '<div class="success">🤖 Starting AI analysis...</div>';
                
                // Show processing steps
                processingSteps.innerHTML = `
                    <div class="step">🚀 Step 1: Uploading to Colab GPU OCR...</div>
                    <div class="step">🧠 Step 2: AI Contract Analysis with OpenAI...</div>
                    <div class="step">📅 Step 3: Generating rental events and reminders...</div>
                `;
                
                const formData = new FormData();
                formData.append('file', file);
                
                try {
                    // Simulate progress
                    let progress = 0;
                    const progressInterval = setInterval(() => {
                        progress += Math.random() * 15;
                        if (progress > 90) progress = 90;
                        progressFill.style.width = progress + '%';
                    }, 2000);
                    
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        body: formData
                    });
                    
                    clearInterval(progressInterval);
                    progressFill.style.width = '100%';
                    
                    if (response.ok) {
                        const result = await response.json();
                        displayResults(result);
                        statusMessage.innerHTML = '<div class="success">✅ AI analysis completed successfully!</div>';
                    } else {
                        const error = await response.json();
                        statusMessage.innerHTML = `<div class="error">❌ Error: ${error.detail}</div>`;
                    }
                } catch (error) {
                    statusMessage.innerHTML = `<div class="error">❌ Connection error: ${error.message}</div>`;
                }
                
                progressBar.style.display = 'none';
            }
            
            function displayResults(result) {
                const resultsSection = document.getElementById('resultsSection');
                const contractData = document.getElementById('contractData');
                const completenessAnalysis = document.getElementById('completenessAnalysis');
                const rentalEvents = document.getElementById('rentalEvents');
                const rawTextOutput = document.getElementById('rawTextOutput');
                
                // Show results section
                resultsSection.style.display = 'block';
                
                // Display contract data
                if (result.contract_data) {
                    const data = result.contract_data;
                    
                    // Build structured display
                    let contractHtml = `
                        <div class="contract-data">
                            <h4>🏠 Extracted Contract Information</h4>
                    `;
                    
                    // Property Information
                    if (data.property) {
                        contractHtml += `
                            <div style="margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 5px;">
                                <h5>🏢 Property Details</h5>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                                    <div><strong>Building:</strong> ${data.property.building || 'N/A'}</div>
                                    <div><strong>Unit:</strong> ${data.property.unit || 'N/A'}</div>
                                    <div><strong>Location:</strong> ${data.property.location || 'N/A'}</div>
                                    <div><strong>Size:</strong> ${data.property.size_sqm || 'N/A'} sqm</div>
                                    <div><strong>Type:</strong> ${data.property.type || 'N/A'}</div>
                                </div>
                            </div>
                        `;
                    }
                    
                    // Parties Information
                    if (data.parties) {
                        contractHtml += `
                            <div style="margin: 15px 0; padding: 15px; background: #e8f5e8; border-radius: 5px;">
                                <h5>👥 Parties</h5>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                                    <div>
                                        <strong>Landlord:</strong><br>
                                        ${data.parties.landlord?.name || 'N/A'}<br>
                                        ${data.parties.landlord?.phone_primary || ''}<br>
                                        ${data.parties.landlord?.email || ''}
                                    </div>
                                    <div>
                                        <strong>Tenant:</strong><br>
                                        ${data.parties.tenant?.name || 'N/A'}<br>
                                        ${data.parties.tenant?.phone_primary || ''}<br>
                                        ${data.parties.tenant?.email || ''}
                                    </div>
                                </div>
                                ${data.parties.agent?.name ? `
                                    <div style="margin-top: 10px;">
                                        <strong>Agent:</strong> ${data.parties.agent.name}
                                        ${data.parties.agent.email ? `<br>Email: ${data.parties.agent.email}` : ''}
                                    </div>
                                ` : ''}
                            </div>
                        `;
                    }
                    
                    // Lease & Financial Information
                    if (data.lease || data.rent || data.deposit) {
                        contractHtml += `
                            <div style="margin: 15px 0; padding: 15px; background: #fff3cd; border-radius: 5px;">
                                <h5>💰 Lease & Financial Details</h5>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                                    <div><strong>Lease Period:</strong> ${data.lease?.start_date || 'N/A'} to ${data.lease?.end_date || 'N/A'}</div>
                                    <div><strong>Annual Rent:</strong> AED ${data.rent?.annual_aed || 'N/A'}</div>
                                    <div><strong>Monthly Rent:</strong> AED ${data.rent?.monthly_aed || 'N/A'}</div>
                                    <div><strong>Payment Schedule:</strong> ${data.rent?.cheques?.count || 'N/A'} cheques</div>
                                    <div><strong>Deposit:</strong> AED ${data.deposit?.refundable_aed || 'N/A'}</div>
                                    <div><strong>Furnished:</strong> ${data.furnishing?.status || 'N/A'}</div>
                                </div>
                                ${data.rent?.cheques?.dates && data.rent.cheques.dates.length > 0 ? `
                                    <div style="margin-top: 10px;">
                                        <strong>Payment Dates:</strong><br>
                                        ${data.rent.cheques.dates.map((date, index) => 
                                            `Cheque ${index + 1}: ${date} (AED ${data.rent.cheques.amounts?.[index] || 'N/A'})`
                                        ).join('<br>')}
                                    </div>
                                ` : ''}
                            </div>
                        `;
                    }
                    
                    // Responsibilities
                    if (data.responsibilities) {
                        contractHtml += `
                            <div style="margin: 15px 0; padding: 15px; background: #d1ecf1; border-radius: 5px;">
                                <h5>🔧 Responsibilities</h5>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                                    <div><strong>Service Charges:</strong> ${data.responsibilities.service_charges?.party || 'N/A'}</div>
                                    <div><strong>DEWA:</strong> ${data.responsibilities.dewa?.party || 'N/A'}</div>
                                    <div><strong>Chiller:</strong> ${data.responsibilities.chiller?.party || 'N/A'}</div>
                                    <div><strong>Maintenance (Major):</strong> ${data.responsibilities.maintenance?.major_party || 'N/A'}</div>
                                    <div><strong>Maintenance (Minor):</strong> ${data.responsibilities.maintenance?.minor_party || 'N/A'}</div>
                                    <div><strong>Minor Cap:</strong> AED ${data.responsibilities.maintenance?.minor_cap_aed || 'N/A'}</div>
                                </div>
                                ${data.responsibilities.ejari_registration?.conflict_notes ? `
                                    <div style="margin-top: 10px; padding: 10px; background: #f8d7da; border-radius: 3px;">
                                        <strong>⚠️ Ejari Registration Conflict:</strong> ${data.responsibilities.ejari_registration.conflict_notes}
                                    </div>
                                ` : ''}
                            </div>
                        `;
                    }
                    
                    // Terms & Conditions
                    if (data.terms) {
                        contractHtml += `
                            <div style="margin: 15px 0; padding: 15px; background: #e2e3e5; border-radius: 5px;">
                                <h5>📋 Terms & Conditions</h5>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                                    <div><strong>Pets Allowed:</strong> ${data.terms.pets_allowed !== null ? data.terms.pets_allowed : 'N/A'}</div>
                                    <div><strong>Subletting:</strong> ${data.terms.subletting_allowed !== null ? data.terms.subletting_allowed : 'N/A'}</div>
                                    <div><strong>Early Termination Notice:</strong> ${data.terms.early_termination?.notice_days || 'N/A'} days</div>
                                    <div><strong>Renewal Notice:</strong> ${data.terms.renewal?.notice_days || 'N/A'} days</div>
                                </div>
                                ${data.terms.early_termination?.penalty ? `
                                    <div style="margin-top: 10px;">
                                        <strong>Early Termination Penalty:</strong> ${data.terms.early_termination.penalty}
                                    </div>
                                ` : ''}
                            </div>
                        `;
                    }
                    
                    // Identifiers
                    if (data.identifiers) {
                        contractHtml += `
                            <div style="margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 5px;">
                                <h5>🆔 Identifiers</h5>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                                    <div><strong>DEWA Premise No:</strong> ${data.identifiers.dewa_premise_no || 'N/A'}</div>
                                    <div><strong>Plot No:</strong> ${data.identifiers.plot_no || 'N/A'}</div>
                                    <div><strong>Ejari No:</strong> ${data.identifiers.ejari_number || 'N/A'}</div>
                                </div>
                            </div>
                        `;
                    }
                    
                    contractHtml += `
                            <div style="margin-top: 15px; padding: 10px; background: #f8f9fa; border-radius: 5px;">
                                <strong>AI Model:</strong> ${data.ai_model || 'N/A'} | 
                                <strong>Confidence:</strong> ${data.confidence || 'N/A'} | 
                                <strong>Parsed:</strong> ${data.parsed_at ? new Date(data.parsed_at).toLocaleString() : 'N/A'}
                            </div>
                        </div>
                    `;
                    
                    contractData.innerHTML = contractHtml;
                    
                    
                }
                
                // Display completeness analysis
                if (result.completeness_analysis) {
                    const completeness = result.completeness_analysis;
                    const completenessHtml = `
                        <div class="completeness-section" style="margin: 15px 0; padding: 15px; border-radius: 5px; background: #e3f2fd; border: 1px solid #bbdefb;">
                            <h4>📋 Contract Completeness Analysis</h4>
                            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                <div style="flex: 1;">
                                    <strong>Completeness Score:</strong> ${completeness.completeness_score || 0}%
                                </div>
                                <div style="color: ${completeness.quality_status === 'excellent' ? '#4caf50' : completeness.quality_status === 'good' ? '#ff9800' : completeness.quality_status === 'fair' ? '#ff5722' : '#f44336'};">
                                    ${completeness.quality_status === 'excellent' ? '✅ Excellent' : 
                                      completeness.quality_status === 'good' ? '⚠️ Good' : 
                                      completeness.quality_status === 'fair' ? '⚠️ Fair' : '❌ Poor'}
                                </div>
                            </div>
                            
                            ${completeness.missing_critical && completeness.missing_critical.length > 0 ? `
                                <div style="margin-top: 10px;">
                                    <strong>❌ Missing Critical Fields:</strong>
                                    <ul style="margin: 5px 0; padding-left: 20px;">
                                        ${completeness.missing_critical.map(field => `
                                            <li style="color: #d32f2f;">
                                                ${field.replace(/_/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase())}
                                            </li>
                                        `).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                            
                            ${completeness.missing_important && completeness.missing_important.length > 0 ? `
                                <div style="margin-top: 10px;">
                                    <strong>⚠️ Missing Important Fields:</strong>
                                    <ul style="margin: 5px 0; padding-left: 20px;">
                                        ${completeness.missing_important.map(field => `
                                            <li style="color: #ff9800;">
                                                ${field.replace(/_/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase())}
                                            </li>
                                        `).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                            
                            ${completeness.needs_confirmation && completeness.needs_confirmation.length > 0 ? `
                                <div style="margin-top: 10px;">
                                    <strong>🔍 Needs Confirmation:</strong>
                                    <ul style="margin: 5px 0; padding-left: 20px;">
                                        ${completeness.needs_confirmation.map(field => `
                                            <li style="color: #1976d2;">
                                                ${field.replace(/_/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase())}
                                            </li>
                                        `).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                            
                            ${completeness.suggested_improvements && completeness.suggested_improvements.length > 0 ? `
                                <div style="margin-top: 10px;">
                                    <strong>💡 Suggested Improvements:</strong>
                                    <ul style="margin: 5px 0; padding-left: 20px;">
                                        ${completeness.suggested_improvements.map(improvement => `
                                            <li style="color: #1976d2;">
                                                ${improvement}
                                            </li>
                                        `).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                            
                            ${completeness.validation_notes ? `
                                <div style="margin-top: 10px; padding: 10px; background: #fff3cd; border-radius: 3px; border: 1px solid #ffeaa7;">
                                    <strong>📝 Validation Notes:</strong>
                                    <div style="color: #856404; margin-top: 5px;">${completeness.validation_notes}</div>
                                </div>
                            ` : ''}
                        </div>
                    `;
                    completenessAnalysis.innerHTML = completenessHtml;
                } else {
                    completenessAnalysis.innerHTML = `
                        <div class="completeness-section" style="margin: 15px 0; padding: 15px; border-radius: 5px; background: #f8f9fa; border: 1px solid #dee2e6;">
                            <h4>📋 Contract Completeness Analysis</h4>
                            <div style="color: #666;">No completeness analysis available</div>
                        </div>
                    `;
                }
                
                // Display actionable gaps
                if (result.completeness_analysis && result.completeness_analysis.actionable_gaps && result.completeness_analysis.actionable_gaps.length > 0) {
                    const gaps = result.completeness_analysis.actionable_gaps;
                    const gapsHtml = `
                        <div class="gaps-section" style="margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;">
                            <h4>🔧 Action Required (Future Features)</h4>
                            <div class="gap-chips">
                                ${gaps.map(gap => `
                                    <div class="gap-chip ${gap.priority}" style="display: flex; align-items: flex-start; padding: 15px; border-radius: 8px; border-left: 4px solid;">
                                        <span class="gap-icon" style="font-size: 1.5em; margin-right: 15px; margin-top: 2px;">
                                            ${gap.type === 'upload' ? '📄' : gap.type === 'contact' ? '📱' : gap.type === 'confirmation' ? '⚠️' : '🔧'}
                                        </span>
                                        <div class="gap-content" style="flex: 1;">
                                            <span class="gap-label" style="font-weight: bold; display: block; margin-bottom: 5px; font-size: 1.1em;">
                                                ${gap.label}
                                            </span>
                                            <span class="gap-description" style="color: #666; font-size: 0.9em; display: block; margin-bottom: 8px;">
                                                ${gap.description}
                                            </span>
                                            ${gap.conflict_details ? `
                                                <div style="background: #fff3cd; padding: 8px; border-radius: 4px; margin-bottom: 8px; font-size: 0.85em;">
                                                    <strong>Conflict Details:</strong> ${gap.conflict_details}
                                                </div>
                                            ` : ''}
                                            <span class="automated-action" style="font-size: 0.8em; color: #6c757d; font-style: italic; display: block;">
                                                🤖 ${gap.automated_action}
                                            </span>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    `;
                    document.getElementById('actionableGaps').innerHTML = gapsHtml;
                } else {
                    document.getElementById('actionableGaps').innerHTML = `
                        <div class="gaps-section" style="margin: 20px 0; padding: 20px; background: #d4edda; border-radius: 8px; border: 1px solid #c3e6cb;">
                            <h4>✅ No Action Required</h4>
                            <div style="color: #155724;">All contract information is complete and up to date!</div>
                        </div>
                    `;
                }
                
                // Display rental events
                if (result.rental_events && result.rental_events.length > 0) {
                    const events = result.rental_events;
                    const eventsHtml = events.map(event => `
                        <div class="event-item" style="border-left: 4px solid ${getEventColor(event.event_type)}; padding: 15px; margin: 15px 0; background: #f8f9fa; border-radius: 8px;">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                                <div style="flex: 1;">
                                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
                                        <strong style="font-size: 1.1em;">${event.title}</strong>
                                        <span class="priority-badge ${event.priority}" style="padding: 2px 8px; border-radius: 12px; font-size: 0.7em; font-weight: bold; text-transform: uppercase;">
                                            ${event.priority}
                                        </span>
                                    </div>
                                    <div style="color: #666; font-size: 0.9em; margin-bottom: 8px;">${event.description}</div>
                                    ${event.amount ? `<div style="color: #28a745; font-weight: bold;">Amount: AED ${event.amount.toLocaleString()}</div>` : ''}
                                    ${event.checklist_items ? `
                                        <div style="margin-top: 8px;">
                                            <strong>Checklist Items:</strong>
                                            <ul style="margin: 5px 0; padding-left: 20px; font-size: 0.9em;">
                                                ${event.checklist_items.map(item => `<li>${item}</li>`).join('')}
                                            </ul>
                                        </div>
                                    ` : ''}
                                </div>
                                <div style="text-align: right; min-width: 120px;">
                                    <div style="font-weight: bold; color: ${getEventColor(event.event_type)}; font-size: 1.1em;">${event.due_date || 'N/A'}</div>
                                    <div style="font-size: 0.8em; color: #666;">${event.event_type.replace(/_/g, ' ')}</div>
                                </div>
                            </div>
                            ${event.automated_actions && event.automated_actions.length > 0 ? `
                                <div class="automated-actions" style="margin-top: 15px; padding: 12px; background: #e9ecef; border-radius: 6px; border-left: 3px solid #6c757d;">
                                    <h5 style="margin: 0 0 8px 0; color: #495057; font-size: 0.9em;">🤖 Automated Actions (Future Features):</h5>
                                    <div class="action-tags" style="display: flex; flex-wrap: wrap; gap: 6px;">
                                        ${event.automated_actions.map(action => `
                                            <span class="action-tag" style="background: #f8f9fa; color: #495057; padding: 4px 10px; border-radius: 15px; font-size: 0.8em; border: 1px dashed #6c757d;">
                                                ${action}
                                            </span>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                        </div>
                    `).join('');
                    
                    rentalEvents.innerHTML = `
                        <div class="events-data">
                            <h4>📅 Generated Rental Events & Reminders</h4>
                            <div style="margin-bottom: 15px; color: #666;">
                                Found ${events.length} actionable events from contract analysis
                            </div>
                            ${eventsHtml}
                        </div>
                    `;
                } else {
                    rentalEvents.innerHTML = `
                        <div class="events-data">
                            <h4>📅 Generated Rental Events & Reminders</h4>
                            <div style="color: #666;">No events generated from contract data</div>
                        </div>
                    `;
                }
                
                // Display raw text
                rawTextOutput.innerHTML = `
                    <h4>📄 OCR Extracted Text</h4>
                    <div class="text-output">${result.ocr_result?.raw_text || 'No text extracted'}</div>
                `;
            }
            
            function getEventColor(eventType) {
                const colors = {
                    'rent_payment_reminder': '#dc3545',
                    'renewal_window_start': '#ffc107',
                    'renewal_window_mid': '#fd7e14',
                    'renewal_deadline': '#dc3545',
                    'notice_deadline': '#dc3545',
                    'maintenance_reminder': '#17a2b8',
                    'deposit_return_reminder': '#6c757d',
                    'compliance_alert': '#e83e8c',
                    'pest_control_reminder': '#20c997',
                    'move_out_utilities': '#6f42c1',
                    'default': '#6c757d'
                };
                return colors[eventType] || colors.default;
            }
        </script>
    </body>
    </html>
    """

@app.post("/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    """Analyze contract using Colab OCR + OpenAI API"""
    
    try:
        print(f"🤖 Starting contract analysis for {file.filename}")
        
        # Save uploaded file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Step 1: OCR with Colab GPU
        print("🚀 Step 1: Processing with Colab GPU OCR...")
        client = get_colab_client()
        ocr_result = client.process_file(temp_path)
        
        if ocr_result.get('extraction_status') != 'success':
            raise Exception(f"OCR failed: {ocr_result.get('error', 'Unknown error')}")
        
        print(f"✅ OCR completed: {ocr_result.get('text_length', 0)} characters")
        
        # Step 2: AI Contract Analysis (includes event generation and completeness validation)
        print("🧠 Step 2: Comprehensive AI analysis with OpenAI API...")
        parser = get_contract_parser()
        contract_data = parser.parse_contract(ocr_result['raw_text'])
        
        if 'error' in contract_data:
            raise Exception(f"AI parsing failed: {contract_data['error']}")
        
        # Extract events and completeness analysis from the contract data
        rental_events = contract_data.get('rental_events', [])
        completeness_analysis = contract_data.get('completeness_analysis', {})
        
        print(f"✅ AI analysis completed - Generated {len(rental_events)} events, Completeness: {completeness_analysis.get('completeness_score', 0)}%")
        
        # Clean up temp file
        os.unlink(temp_path)
        
        return {
            "status": "success",
            "ocr_result": ocr_result,
            "contract_data": contract_data,
            "rental_events": rental_events,
            "completeness_analysis": completeness_analysis,
            "analysis_time": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Contract analysis error: {e}")
        return {"error": str(e), "status": "failed"}

@app.get("/health")
async def health_check():
    """Check system health"""
    try:
        # Check Colab API
        client = get_colab_client()
        colab_health = client.health_check()
        
        # Check OpenAI API
        parser = get_contract_parser()
        openai_health = {"status": "healthy", "model": parser.model}
        
        return {
            "status": "healthy",
            "colab_api": colab_health,
            "openai_api": openai_health,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

if __name__ == "__main__":
    print("🤖 Starting Contract Intelligence Agent...")
    print(f"📡 Colab URL: {COLAB_URL}")
    print("📱 Open your browser to: http://localhost:8002")
    
    # Test connections
    try:
        client = get_colab_client()
        health = client.health_check()
        if health.get('status') == 'healthy':
            print("✅ Colab API is healthy and ready!")
        else:
            print("⚠️ Colab API not healthy - check connection")
    except Exception as e:
        print(f"❌ Colab connection error: {e}")
    
    try:
        parser = get_contract_parser()
        print("✅ OpenAI API initialized successfully!")
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
    
    uvicorn.run(app, host="0.0.0.0", port=8002)
    