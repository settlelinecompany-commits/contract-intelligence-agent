#!/usr/bin/env python3
"""
Contract Intelligence Agent - Vercel Version
Exact copy of working local version
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
            text_length = len(result.get('raw_text', ''))
            print(f"🔍 DEBUG: OCR success, text length: {text_length}")
            return result
        else:
            error_msg = f"HTTP {response.status_code}: {response.text}"
            print(f"🔍 DEBUG: OCR failed: {error_msg}")
            return {"raw_text": "", "error": error_msg}
    except Exception as e:
        error_msg = f"OCR Exception: {str(e)}"
        print(f"🔍 DEBUG: OCR exception: {error_msg}")
        return {"raw_text": "", "error": error_msg}

def analyze_contract_ai(text: str) -> dict:
    """Analyze contract with OpenAI - exact copy from working local version"""
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
                        "inventory_present": true/false
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
                        "event_type": "rent_payment_due",
                        "title": "Rent Payment #1 Due",
                        "description": "Quarterly rent payment due",
                        "due_date": "2021-07-20",
                        "reminder_date": "2021-07-13",
                        "priority": "critical",
                        "amount": 12000.00,
                        "payment_number": 1,
                        "total_payments": 4,
                        "automated_actions": [
                            "📅 Add to Calendar",
                            "💬 Send WhatsApp Reminder",
                            "📷 Upload Cheque Image"
                        ]
                    }},
                    {{
                        "event_type": "move_out_checklist",
                        "title": "Move-out Checklist Due",
                        "description": "Collect final DEWA/telecom/chiller bills before deposit refund",
                        "due_date": "2022-07-19",
                        "reminder_date": "2022-07-12",
                        "priority": "high",
                        "checklist_items": [
                            "Final DEWA bill (Premise: 673-08258-0)",
                            "Final telecom bill",
                            "Final chiller bill",
                            "Property inspection",
                            "Key handover"
                        ],
                        "automated_actions": [
                            "📋 Generate Checklist",
                            "📧 Send Reminder Email",
                            "📱 WhatsApp Notification"
                        ]
                    }},
                    {{
                        "event_type": "deposit_return_followup",
                        "title": "Deposit Return Follow-up",
                        "description": "Follow up on deposit return of AED 4,000",
                        "due_date": "2022-08-02",
                        "reminder_date": "2022-08-02",
                        "priority": "medium",
                        "deposit_amount": 4000.00,
                        "automated_actions": [
                            "📧 Send Follow-up Email",
                            "📞 Schedule Call Reminder"
                        ]
                    }},
                    {{
                        "event_type": "renewal_window_start",
                        "title": "Renewal Window Opens (T-90)",
                        "description": "90-day renewal notice period begins",
                        "due_date": "2022-04-20",
                        "reminder_date": "2022-04-20",
                        "priority": "high",
                        "action_required": "Decide on renewal or give notice",
                        "automated_actions": [
                            "📧 Send Decision Reminder",
                            "📋 Generate Renewal Options"
                        ]
                    }},
                    {{
                        "event_type": "renewal_window_mid",
                        "title": "Renewal Decision Window (T-60)",
                        "description": "60 days before lease end - decision time",
                        "due_date": "2022-05-20",
                        "reminder_date": "2022-05-20",
                        "priority": "high",
                        "action_required": "Decide on renewal or give notice",
                        "automated_actions": [
                            "📧 Send Decision Reminder",
                            "📋 Generate Renewal Options"
                        ]
                    }},
                    {{
                        "event_type": "renewal_deadline",
                        "title": "Renewal Notice Deadline (T-30)",
                        "description": "30 days before lease end - final notice deadline",
                        "due_date": "2022-06-19",
                        "reminder_date": "2022-06-19",
                        "priority": "critical",
                        "action_required": "Give notice if not renewing",
                        "automated_actions": [
                            "🚨 Critical Deadline Alert",
                            "📧 Final Notice Reminder"
                        ]
                    }},
                    {{
                        "event_type": "inventory_signoff",
                        "title": "Inventory Sign-off Required",
                        "description": "Furnished property - inventory list needed",
                        "due_date": "2021-07-20",
                        "reminder_date": "2021-07-20",
                        "priority": "medium",
                        "action_required": "Complete inventory checklist",
                        "automated_actions": [
                            "📋 Generate Inventory Template",
                            "📧 Send Inventory Reminder"
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
                        "payment_method_details",
                        "viewing_access_protocol"
                    ],
                    "needs_confirmation": [
                        "ejari_registration_party_conflict",
                        "cheque_amounts_equal_split",
                        "maintenance_responsibility_clarity"
                    ],
                    "actionable_gaps": [
                        {{
                            "type": "upload",
                            "field": "ejari_number",
                            "label": "Upload Ejari PDF",
                            "description": "Ejari certificate required for legal compliance",
                            "priority": "critical",
                            "status": "missing",
                            "automated_action": "📄 Document Upload Interface"
                        }},
                        {{
                            "type": "contact",
                            "field": "tenant_phone",
                            "label": "Add Tenant Contact",
                            "description": "Tenant phone number missing",
                            "priority": "important",
                            "status": "missing",
                            "automated_action": "📱 Contact Form Interface"
                        }},
                        {{
                            "type": "upload",
                            "field": "cheque_images",
                            "label": "Upload Cheque Images",
                            "description": "Confirm payment dates and amounts",
                            "priority": "important",
                            "status": "missing",
                            "automated_action": "📷 Multi-file Upload Interface"
                        }},
                        {{
                            "type": "upload",
                            "field": "inventory_list",
                            "label": "Upload Inventory List",
                            "description": "Furnished property requires inventory",
                            "priority": "important",
                            "status": "missing",
                            "automated_action": "📋 Document Upload Interface"
                        }},
                        {{
                            "type": "confirmation",
                            "field": "ejari_registration_party",
                            "label": "Confirm Ejari Responsibility",
                            "description": "Contract has conflicting clauses on Ejari registration",
                            "priority": "important",
                            "status": "conflict",
                            "conflict_details": "Page 2: Landlord undertakes to register. Page 3: Tenant responsible.",
                            "automated_action": "✅ Conflict Resolution Interface"
                        }}
                    ],
                    "suggested_improvements": [
                        "Upload Ejari certificate for legal compliance",
                        "Add tenant contact number for communication",
                        "Upload cheque images to confirm payment schedule",
                        "Complete furnished property inventory checklist",
                        "Clarify Ejari registration responsibility"
                    ],
                    "validation_notes": "Contract has conflicting clauses on Ejari registration responsibility. Cheque dates need to be confirmed from actual cheques."
                }}
            }}
            
            For rental_events, generate ONLY events that are explicitly mentioned in the contract or can be logically derived:
            - Payment reminders based on actual cheque schedule and dates (include automated_actions: calendar, WhatsApp, upload)
            - Renewal window events (T-90, T-60, T-30 based on notice period) with decision reminders
            - Move-out checklist events based on lease end date and contract terms
            - Deposit return follow-up events (D+14 after lease end)
            - Maintenance events only if contract specifies (pest control, move-out utilities)
            - Inventory sign-off events for furnished properties
            - Compliance alerts (bounced cheques, early termination penalties)
            - Do NOT assume events not explicitly stated in the contract
            - Always include automated_actions array with relevant automation placeholders
            
            For completeness_analysis:
            - Score from 0-100 based on contract completeness
            - missing_critical: Essential fields missing (rent, dates, deposit, parties)
            - missing_important: Important but non-critical fields (utilities, maintenance details)
            - needs_confirmation: Data exists but needs verification (conflicting clauses, assumed values)
            - actionable_gaps: Array of gaps that can be resolved with specific actions
              - Each gap should have: type, field, label, description, priority, status, automated_action
              - Types: "upload", "contact", "confirmation"
              - Priorities: "critical", "important", "optional"
              - Status: "missing", "conflict", "incomplete"
              - automated_action: Description of future interface (e.g., "📄 Document Upload Interface")
            - Provide specific, actionable improvement suggestions
            - Note any data inconsistencies or validation issues
            
            Important:
            - Return ONLY the JSON object, no other text
            - Use null for missing information
            - Extract actual values from the contract text
            - Format currency as numbers (48000.00, not "AED 48,000")
            - Format dates as YYYY-MM-DD
            - Derive calculated fields (monthly rent = annual/12, cheque amount = annual/count)
            - If information is not clearly stated, use null
            - Do not make assumptions beyond what's explicitly in the contract
            """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert contract analyst. Return only valid JSON with comprehensive analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=3000
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
    """Main interface - exact copy from working local version"""
    html = """
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
                    
                    const response = await fetch('/api/analyze', {
                        method: 'POST',
                        body: formData
                    });
                    
                    clearInterval(progressInterval);
                    progressFill.style.width = '100%';
                    
                    if (response.ok) {
                        const result = await response.json();
                        statusMessage.innerHTML = '<div class="success">✅ Analysis complete!</div>';
                        resultsSection.style.display = 'block';
                        displayResults(result);
                    } else {
                        statusMessage.innerHTML = `<div class="error">❌ Analysis failed: ${response.statusText}</div>`;
                    }
                } catch (error) {
                    statusMessage.innerHTML = `<div class="error">❌ Connection error: ${error.message}</div>`;
                }
                
                progressBar.style.display = 'none';
            }
            
            function displayResults(result) {
                // Display contract data
                if (result.contract_data) {
                    const contractData = document.getElementById('contractData');
                    const data = result.contract_data;
                    
                    let contractHtml = `
                        <div class="contract-data">
                            <h4>📋 Contract Information</h4>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                                <div>
                                    <h5>🏢 Property Details</h5>
                                    <p><strong>Building:</strong> ${data.property?.building || 'N/A'}</p>
                                    <p><strong>Unit:</strong> ${data.property?.unit || 'N/A'}</p>
                                    <p><strong>Location:</strong> ${data.property?.location || 'N/A'}</p>
                                    <p><strong>Size:</strong> ${data.property?.size_sqm || 'N/A'} sqm</p>
                                    <p><strong>Type:</strong> ${data.property?.type || 'N/A'}</p>
                                </div>
                                <div>
                                    <h5>👥 Parties</h5>
                                    <p><strong>Landlord:</strong> ${data.parties?.landlord?.name || 'N/A'}</p>
                                    <p><strong>Tenant:</strong> ${data.parties?.tenant?.name || 'N/A'}</p>
                                    <p><strong>Agent:</strong> ${data.parties?.agent?.name || 'N/A'}</p>
                                </div>
                                <div>
                                    <h5>📅 Lease Terms</h5>
                                    <p><strong>Start Date:</strong> ${data.lease?.start_date || 'N/A'}</p>
                                    <p><strong>End Date:</strong> ${data.lease?.end_date || 'N/A'}</p>
                                    <p><strong>Duration:</strong> ${data.lease?.duration_months || 'N/A'} months</p>
                                </div>
                                <div>
                                    <h5>💰 Financial Details</h5>
                                    <p><strong>Annual Rent:</strong> AED ${data.rent?.annual_aed?.toLocaleString() || 'N/A'}</p>
                                    <p><strong>Monthly Rent:</strong> AED ${data.rent?.monthly_aed?.toLocaleString() || 'N/A'}</p>
                                    <p><strong>Deposit:</strong> AED ${data.deposit?.refundable_aed?.toLocaleString() || 'N/A'}</p>
                                    <p><strong>Cheques:</strong> ${data.rent?.cheques?.count || 'N/A'} cheques</p>
                                </div>
                            </div>
                        </div>
                    `;
                    contractData.innerHTML = contractHtml;
                }
                
                // Display completeness analysis
                if (result.completeness_analysis) {
                    const completenessAnalysis = document.getElementById('completenessAnalysis');
                    const completeness = result.completeness_analysis;
                    
                    let completenessHtml = `
                        <div class="completeness-section" style="margin: 15px 0; padding: 15px; border-radius: 5px; background: #f8f9fa; border: 1px solid #dee2e6;">
                            <h4>📊 Contract Completeness Analysis</h4>
                            <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 15px;">
                                <div style="font-size: 2em; font-weight: bold; color: ${completeness.completeness_score >= 80 ? '#28a745' : completeness.completeness_score >= 60 ? '#ffc107' : '#dc3545'};">
                                    ${completeness.completeness_score || 0}%
                                </div>
                                <div>
                                    <div style="font-weight: bold;">Completeness Score</div>
                                    <div style="color: #666; font-size: 0.9em;">${completeness.quality_status || 'Unknown'}</div>
                                </div>
                            </div>
                            
                            ${completeness.missing_critical && completeness.missing_critical.length > 0 ? `
                                <div style="margin-top: 10px;">
                                    <strong>🚨 Missing Critical:</strong>
                                    <ul style="margin: 5px 0; padding-left: 20px;">
                                        ${completeness.missing_critical.map(item => `
                                            <li style="color: #dc3545;">
                                                ${item}
                                            </li>
                                        `).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                            
                            ${completeness.missing_important && completeness.missing_important.length > 0 ? `
                                <div style="margin-top: 10px;">
                                    <strong>⚠️ Missing Important:</strong>
                                    <ul style="margin: 5px 0; padding-left: 20px;">
                                        ${completeness.missing_important.map(item => `
                                            <li style="color: #ffc107;">
                                                ${item}
                                            </li>
                                        `).join('')}
                                    </ul>
                                </div>
                            ` : ''}
                            
                            ${completeness.needs_confirmation && completeness.needs_confirmation.length > 0 ? `
                                <div style="margin-top: 10px;">
                                    <strong>❓ Needs Confirmation:</strong>
                                    <ul style="margin: 5px 0; padding-left: 20px;">
                                        ${completeness.needs_confirmation.map(item => `
                                            <li style="color: #17a2b8;">
                                                ${item}
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
                                    <div style="color: #666; font-size: 0.8em; margin-top: 8px;">
                                        <strong>Due:</strong> ${event.due_date || 'N/A'}
                                        ${event.reminder_date ? ` | <strong>Reminder:</strong> ${event.reminder_date}` : ''}
                                    </div>
                                </div>
                            </div>
                            
                            ${event.automated_actions && event.automated_actions.length > 0 ? `
                                <div class="automated-actions">
                                    <strong>🤖 Automated Actions (Future Features):</strong>
                                    <div class="action-tags">
                                        ${event.automated_actions.map(action => `
                                            <span class="action-tag">${action}</span>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                        </div>
                    `).join('');
                    
                    document.getElementById('rentalEvents').innerHTML = `
                        <div class="events-section" style="margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;">
                            <h4>📅 Rental Events & Reminders</h4>
                            ${eventsHtml}
                        </div>
                    `;
                } else {
                    document.getElementById('rentalEvents').innerHTML = `
                        <div class="events-section" style="margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; border: 1px solid #dee2e6;">
                            <h4>📅 Rental Events & Reminders</h4>
                            <div style="color: #666;">No rental events generated</div>
                        </div>
                    `;
                }
            }
            
            function getEventColor(eventType) {
                const colors = {
                    'rent_payment_due': '#dc3545',
                    'renewal_window_start': '#fd7e14',
                    'renewal_window_mid': '#ffc107',
                    'renewal_deadline': '#dc3545',
                    'move_out_checklist': '#17a2b8',
                    'deposit_return_followup': '#6c757d',
                    'inventory_signoff': '#28a745',
                    'maintenance_reminder': '#6f42c1',
                    'compliance_alert': '#dc3545'
                };
                return colors[eventType] || '#6c757d';
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
            
            if not ocr_result or not ocr_result.get('raw_text'):
                return JSONResponse(
                    status_code=400,
                    content={"detail": "OCR processing failed"}
                )
            
            # Step 2: AI Analysis
            analysis_result = analyze_contract_ai(ocr_result['raw_text'])
            
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