# Contract Intelligence OCR API - User Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Working Code (with debugging)
```python
import base64
import requests

def ocr_pdf(pdf_file_path):
    # Convert PDF to base64
    with open(pdf_file_path, 'rb') as f:
        pdf_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    # Call OCR API
    response = requests.post(
        'https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync',
        headers={'Authorization': 'Bearer YOUR_RUNPOD_API_KEY'},
        json={'input': {'pdf_data': pdf_base64}}
    )
    
    result = response.json()
    
    # DEBUG: Print the full response
    print("Status Code:", response.status_code)
    print("Full Response:", result)
    
    return result

# Usage
result = ocr_pdf('your_document.pdf')
print("Keys in response:", list(result.keys()))

# Access the OCR text (adjust key name based on actual response)
if 'ocr_text' in result:
    print(result['ocr_text'])
else:
    print("Available keys:", list(result.keys()))
```

### 3. API Details
- **Endpoint**: `https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync`
- **Method**: POST
- **Auth**: Bearer token (set YOUR_RUNPOD_API_KEY in environment variables)
- **Input**: PDF file path
- **Output**: JSON with extracted text

### 4. Troubleshooting
- If you get `KeyError`, check what keys are actually in the response
- The debug code will show you the exact response structure
- Adjust the key name based on what's actually returned

## Features
- ✅ Arabic & English OCR
- ✅ High accuracy text extraction
- ✅ Simple integration
- ✅ Debugging included

## Example Usage
```python
# Process a PDF document
result = ocr_pdf('contract.pdf')
print(result['ocr_text'])  # Print extracted text
```

## Support
For issues or questions, contact the API administrator.