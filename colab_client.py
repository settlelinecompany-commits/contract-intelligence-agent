#!/usr/bin/env python3
"""
Colab OCR API Client
Calls the Google Colab Surya OCR API for GPU-accelerated processing
"""

import requests
import json
from pathlib import Path
from typing import Dict, Any, Optional
import base64

class ColabOCRClient:
    """Client to communicate with Colab Surya OCR API"""
    
    def __init__(self, colab_url: str):
        """
        Initialize Colab OCR client
        
        Args:
            colab_url: The ngrok URL from Colab (e.g., https://abc123.ngrok.io)
        """
        self.colab_url = colab_url.rstrip('/')
        self.health_endpoint = f"{self.colab_url}/health"
        self.ocr_endpoint = f"{self.colab_url}/ocr"
        self.ocr_base64_endpoint = f"{self.colab_url}/ocr-base64"
    
    def health_check(self) -> Dict[str, Any]:
        """Check if Colab API is healthy"""
        try:
            response = requests.get(self.health_endpoint, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """
        Process a PDF file using Colab OCR API
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            OCR results dictionary
        """
        try:
            print(f"🚀 Sending {file_path} to Colab OCR API...")
            
            # Check if file exists
            if not Path(file_path).exists():
                return {"error": f"File not found: {file_path}"}
            
            # Send file to Colab API
            with open(file_path, 'rb') as f:
                files = {'file': (Path(file_path).name, f, 'application/pdf')}
                response = requests.post(self.ocr_endpoint, files=files, timeout=120)
            
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Colab OCR completed: {result.get('text_length', 0)} characters")
            return result
            
        except Exception as e:
            print(f"❌ Colab API error: {e}")
            return {"error": str(e)}
    
    def process_file_base64(self, file_path: str) -> Dict[str, Any]:
        """
        Process a PDF file using base64 encoding (alternative method)
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            OCR results dictionary
        """
        try:
            print(f"🚀 Sending {file_path} to Colab OCR API (base64)...")
            
            # Read file and encode as base64
            with open(file_path, 'rb') as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Send to Colab API
            payload = {"file_data": file_data}
            response = requests.post(self.ocr_base64_endpoint, json=payload, timeout=120)
            
            response.raise_for_status()
            result = response.json()
            
            print(f"✅ Colab OCR completed: {result.get('text_length', 0)} characters")
            return result
            
        except Exception as e:
            print(f"❌ Colab API error: {e}")
            return {"error": str(e)}

def test_colab_api(colab_url: str, test_file: str = "Tenancy_Contract.pdf"):
    """Test the Colab API with a sample file"""
    print("="*60)
    print("🧪 TESTING COLAB OCR API")
    print("="*60)
    
    # Initialize client
    client = ColabOCRClient(colab_url)
    
    # Health check
    print("🔍 Checking API health...")
    health = client.health_check()
    print(f"Health Status: {health}")
    
    if health.get('status') != 'healthy':
        print("❌ API is not healthy. Check Colab connection.")
        return
    
    # Test file processing
    if Path(test_file).exists():
        print(f"\n📄 Testing with file: {test_file}")
        result = client.process_file(test_file)
        
        if result.get('extraction_status') == 'success':
            print(f"✅ Success! Extracted {result.get('text_length', 0)} characters")
            print(f"📊 Confidence: {result.get('average_confidence', 0):.1%}")
            print(f"📄 Pages: {result.get('pages_processed', 0)}")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
    else:
        print(f"❌ Test file not found: {test_file}")

if __name__ == "__main__":
    # Example usage
    COLAB_URL = "https://your-ngrok-url.ngrok.io"  # Replace with your actual ngrok URL
    
    print("🔧 Colab OCR API Client")
    print("="*40)
    print("1. Start the Colab API server")
    print("2. Copy the ngrok URL from Colab")
    print("3. Update COLAB_URL in this script")
    print("4. Run: python3 colab_client.py")
    print("="*40)
    
    # Uncomment to test:
    # test_colab_api(COLAB_URL)













