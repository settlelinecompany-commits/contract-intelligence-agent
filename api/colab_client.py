#!/usr/bin/env python3
"""
Colab OCR Client for Vercel
Lightweight client for Colab OCR API
"""

import requests
from typing import Dict, Any

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
