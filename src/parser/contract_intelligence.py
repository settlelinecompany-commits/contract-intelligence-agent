import os
from openai import OpenAI
from typing import Dict, List, Optional
import json
from datetime import datetime, timedelta
import re

class ContractIntelligence:
    """AI-powered contract parser that understands rental contract semantics"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"  # Cost-effective model for MVP
    
    def parse_contract(self, raw_text: str) -> Dict:
        """Parse contract text using OpenAI API to extract structured information, generate events, and validate completeness"""
        
        print("🧠 Using OpenAI API for comprehensive contract analysis...")
        
        try:
            # Create a comprehensive prompt for contract parsing, event generation, and completeness validation
            prompt = f"""
            You are an expert contract analyst specializing in Dubai rental agreements. 
            Analyze the following contract text and provide a comprehensive analysis in JSON format.
        
        Contract Text:
        {raw_text}
        
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
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert contract analyst. Return only valid JSON with comprehensive analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for consistent results
                max_tokens=3000  # Increased for comprehensive analysis
            )
            
            # Parse the response
            ai_response = response.choices[0].message.content.strip()
            print(f"🤖 OpenAI Response: {ai_response[:200]}...")
            
            # Clean the response - remove markdown formatting if present
            if ai_response.startswith('```json'):
                ai_response = ai_response.replace('```json', '').replace('```', '').strip()
            elif ai_response.startswith('```'):
                ai_response = ai_response.replace('```', '').strip()
            
            # Try to parse JSON response
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
    
    def _fallback_parsing(self, raw_text: str) -> Dict:
        """Fallback rule-based parsing when OpenAI API fails"""
        print("🧠 Using rule-based parsing (fallback mode)")
        
        try:
            # Extract data using simple rules
            contract_data = {
                "rent_amount": None,
                "monthly_rent": None, 
                "payment_schedule": None,
                "lease_start_date": None,
                "lease_end_date": None,
                "deposit_amount": None,
                "notice_period_days": None,
                "maintenance_responsibility": None,
                "maintenance_limit": None,
                "furnished": None,
                "agent_name": None,
                "property_type": None,
                "property_location": None,
                "utilities_included": None,
                "parking_spaces": None,
                "balcony": None,
                "gym": None,
                "pool": None,
                "ejari_number": None,
                "tenant_name": None,
                "landlord_name": None,
                "parsed_at": datetime.now().isoformat(),
                "ai_model": "rule_based_fallback",
                "confidence": "low",
                "rental_events": [],
                "completeness_analysis": {
                    "completeness_score": 0,
                    "quality_status": "poor",
                    "missing_critical_fields": ["rent_amount", "lease_dates", "deposit_amount"],
                    "missing_important_fields": ["payment_schedule", "notice_period"],
                    "suggested_improvements": ["Manual review required - AI parsing failed"],
                    "validation_notes": "Fallback parsing used - limited data extraction"
                }
            }
            
            # Try to extract some real data from text if available
            if "AED" in raw_text:
                # Look for rent amounts
                rent_matches = re.findall(r'AED\s*([0-9,]+)', raw_text)
                if rent_matches:
                    contract_data["rent_amount"] = f"AED {rent_matches[0]}"
                    print(f"✅ Extracted rent amount: {contract_data['rent_amount']}")
            
            if "cheque" in raw_text.lower():
                cheque_matches = re.findall(r'(\d+)\s*cheque', raw_text.lower())
                if cheque_matches:
                    contract_data["payment_schedule"] = f"{cheque_matches[0]} cheques"
                    print(f"✅ Extracted payment schedule: {contract_data['payment_schedule']}")
            
            # Look for dates
            date_matches = re.findall(r'(\d{4}-\d{2}-\d{2})', raw_text)
            if len(date_matches) >= 2:
                contract_data["lease_start_date"] = date_matches[0]
                contract_data["lease_end_date"] = date_matches[1]
                print(f"✅ Extracted dates: {date_matches[0]} to {date_matches[1]}")
            
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
                    "quality_status": "poor",
                    "missing_critical_fields": ["all"],
                    "missing_important_fields": ["all"],
                    "suggested_improvements": ["Manual review required - parsing failed"],
                    "validation_notes": "Parsing error occurred"
                }
            }
    
    def generate_contract_summary(self, contract_data: Dict) -> str:
        """Generate a human-readable summary of the contract"""
        
        summary = f"""
        📋 RENTAL CONTRACT SUMMARY
        
        🏠 Property: {contract_data.get('property_type', 'N/A')} in {contract_data.get('property_location', 'N/A')}
        💰 Annual Rent: {contract_data.get('rent_amount', 'N/A')} AED
        📅 Lease Period: {contract_data.get('lease_start_date', 'N/A')} to {contract_data.get('lease_end_date', 'N/A')}
        💳 Payment: {contract_data.get('payment_schedule', 'N/A')} cheques per year
        🔒 Deposit: {contract_data.get('deposit_amount', 'N/A')} AED
        📝 Notice Period: {contract_data.get('notice_period_days', 'N/A')} days
        
        🏠 Amenities:
        - Furnished: {contract_data.get('furnished', 'N/A')}
        - Parking: {contract_data.get('parking_spaces', 'N/A')} spaces
        - Balcony: {contract_data.get('balcony', 'N/A')}
        - Gym: {contract_data.get('gym', 'N/A')}
        - Pool: {contract_data.get('pool', 'N/A')}
        
        🔧 Maintenance: {contract_data.get('maintenance_responsibility', 'N/A')}
        💡 Utilities: {contract_data.get('utilities_included', 'N/A')}
        """
        
        return summary.strip()

# Test function
if __name__ == "__main__":
    parser = ContractIntelligence()
    print("Contract Intelligence AI initialized successfully!")
    print("Ready to parse rental contracts with AI!")