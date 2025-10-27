# Contract Intelligence Backend

AI-powered contract analysis backend that extracts structured data from rental contracts using GPU-accelerated OCR and AI processing.

## Features

- **GPU-Accelerated OCR**: Uses RunPod serverless with Surya OCR for high-quality text extraction
- **AI-Powered Analysis**: GPT-4 for intelligent contract parsing and data extraction
- **Colab Integration**: Optional Google Colab OCR processing
- **Structured Data Extraction**: Converts contract text into organized JSON format
- **RunPod Deployment**: Serverless GPU processing for scalable OCR

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- RunPod account (for serverless deployment)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd contract-intelligence
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Local Development

**Run the FastAPI server:**
```bash
python3 api/index.py
```

**Access the API:**
- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### RunPod Deployment

1. **Build Docker image:**
   ```bash
   docker build -t contract-intelligence .
   ```

2. **Deploy to RunPod:**
   - Push image to RunPod registry
   - Create serverless endpoint
   - Configure environment variables

3. **Test RunPod endpoint:**
   ```bash
   curl -X POST "https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync" \
        -H "Authorization: Bearer YOUR_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"input": {"pdf_data": "base64_encoded_pdf"}}'
   ```

## Usage

### API Endpoints

- `POST /analyze` - Analyze uploaded contract PDF
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger UI)

### Request Format

```json
{
  "pdf_data": "base64_encoded_pdf_content"
}
```

### Response Format

```json
{
  "success": true,
  "ocr_text": "extracted text from PDF",
  "extracted_data": {
    "property": {...},
    "unit": {...},
    "landlord": {...},
    "tenant": {...},
    "lease": {...},
    "payments": [...],
    "documents": {...},
    "responsibilities": {...}
  }
}
```

## Architecture

- **Backend**: FastAPI with Python
- **OCR Processing**: RunPod serverless with Surya OCR (GPU-accelerated)
- **AI Analysis**: OpenAI GPT-4 for contract parsing
- **Deployment**: Docker containers on RunPod
- **Optional**: Google Colab integration for development

## File Structure

```
contract-intelligence/
├── api/
│   └── index.py                    # FastAPI application
├── rp_handler.py                   # RunPod serverless handler
├── colab_client.py                 # Colab OCR API client
├── colab_ocr_processor.ipynb       # Google Colab OCR notebook
├── src/
│   └── parser/
│       └── contract_intelligence.py # GPT-powered contract parser
├── Dockerfile                      # Docker configuration
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (create this)
└── README.md                      # This file
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |

## Integration with Frontend

This backend is designed to work with the `contract-dashboard` frontend:

1. **Frontend** uploads PDF to `/api/upload`
2. **Frontend** calls RunPod OCR endpoint
3. **Backend** processes OCR text with GPT-4
4. **Frontend** stores structured data in Supabase

## Development

### Local Testing

```bash
# Start FastAPI server
python3 api/index.py

# Test OCR processing
python3 -c "
import requests
import base64

# Read sample PDF
with open('Tenancy_Contract.pdf', 'rb') as f:
    pdf_data = base64.b64encode(f.read()).decode()

# Test API
response = requests.post('http://localhost:8000/analyze', 
                       json={'pdf_data': pdf_data})
print(response.json())
"
```

### RunPod Testing

```bash
# Test RunPod endpoint
python3 -c "
import requests
import base64

# Read sample PDF
with open('Tenancy_Contract.pdf', 'rb') as f:
    pdf_data = base64.b64encode(f.read()).decode()

# Test RunPod
response = requests.post('https://api.runpod.ai/v2/YOUR_ENDPOINT_ID/runsync',
                        headers={'Authorization': 'Bearer YOUR_API_KEY'},
                        json={'input': {'pdf_data': pdf_data}})
print(response.json())
"
```

## Troubleshooting

1. **RunPod OCR errors**: Check endpoint configuration and API key
2. **OpenAI API errors**: Check your API key and quota
3. **Docker build issues**: Ensure all dependencies are in requirements.txt
4. **Local server issues**: Check port availability and dependencies

## Contributing

This is the backend service for contract intelligence. The frontend dashboard is in a separate repository.

## License

[Add your license here]
