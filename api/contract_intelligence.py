#!/usr/bin/env python3
"""
Contract Intelligence Parser for Vercel
AI-powered contract analysis
"""

import os
import json
from datetime import datetime
from typing import Dict
import openai

class ContractIntelligence:
    """AI-powered contract analysis"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o-mini"
    
    def parse_contract(self, raw_text: str) -> Dict:
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
                "phone_alt": "Alternative phone",
                "email": "Email address"
            }},
            "tenant": {{
                "name": "Full tenant name",
                "passport_no": "Passport number", 
                "phone_primary": "Primary phone",
                "email": "Email address"
            }}
        }},
        "identifiers": {{
            "ejari_number": "Ejari registration number",
            "dewa_premise_no": "DEWA premise number",
            "plot_no": "Plot number"
        }},
        "lease": {{
            "start_date": "2021-07-20",
            "end_date": "2022-07-19",
            "duration_months": 12,
            "renewal_notice_days": 90
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
            "security_deposit": 4000.00
        }},
        "furnishing": {{
            "status": "Fully furnished",
            "inventory_list": "List of furnished items"
        }},
        "responsibilities": {{
            "service_charges": "Landlord",
            "dewa": "Tenant", 
            "chiller": "Tenant",
            "maintenance_major": "Landlord",
            "maintenance_minor": "Tenant",
            "maintenance_minor_cap": 500.00
        }},
        "terms": {{
            "pets_allowed": false,
            "subletting_allowed": false,
            "early_termination_notice": 30,
            "early_termination_penalty": "2 months rent + AED 1,000",
            "governing_law": "Dubai laws"
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
        "missing_important": ["inventory_list"],
        "needs_confirmation": ["cheque_dates"],
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
                max_tokens=3000,
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
            
        except json.JSONDecodeError as e:
            return self._fallback_parsing(raw_text)
        except Exception as e:
            return self._fallback_parsing(raw_text)
    
    def _fallback_parsing(self, raw_text: str) -> Dict:
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
