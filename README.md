# Contract Intelligence Agent

AI-powered contract analysis system that extracts structured data from rental contracts, generates automated events, and provides completeness validation.

## Features

- **GPU-Accelerated OCR**: Uses Google Colab with Surya OCR for high-quality text extraction
- **AI-Powered Analysis**: GPT-4o-mini for intelligent contract parsing and data extraction
- **Automated Event Generation**: Creates rental events with automated action placeholders
- **Completeness Validation**: Identifies missing information and actionable gaps
- **Beautiful Web UI**: Clean, organized interface with visual elements

## Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Access to Colab OCR API (shared ngrok URL from team member)

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
   
   **Note:** Colab OCR URL is pre-configured in the code. No need to set `COLAB_OCR_URL` unless you want to use a different endpoint.

5. **Colab OCR is pre-configured!**
   
   The system uses a shared Colab OCR endpoint that's already configured in the code. No additional setup needed!
   
   **If you want to use your own Colab:**
   - Open `colab_ocr_processor.ipynb` in Google Colab
   - Run all cells to start the OCR API server
   - Set `COLAB_OCR_URL` in your `.env` file with your ngrok URL

6. **Run the application:**
   ```bash
   python3 contract_intelligence_agent.py
   ```

7. **Access the web interface:**
   Open your browser to `http://localhost:8002`

## Usage

1. **Upload a rental contract PDF** using the web interface
2. **View extracted contract data** organized by sections (Property, Parties, Financial, etc.)
3. **Review generated events** with automated action placeholders
4. **Check completeness analysis** for missing information and actionable gaps

## Architecture

- **Frontend**: FastAPI with HTML/JavaScript web interface
- **OCR Processing**: Google Colab with Surya OCR (GPU-accelerated)
- **AI Analysis**: OpenAI GPT-4o-mini for contract parsing
- **Data Structure**: Structured JSON with property, parties, lease, and responsibilities

## File Structure

```
contract-intelligence/
├── contract_intelligence_agent.py    # Main FastAPI application
├── colab_client.py                   # Colab OCR API client
├── colab_ocr_processor.ipynb         # Google Colab OCR notebook
├── src/
│   └── parser/
│       └── contract_intelligence.py  # GPT-powered contract parser
├── requirements.txt                  # Python dependencies
├── .env                             # Environment variables (create this)
└── README.md                        # This file
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `COLAB_OCR_URL` | ngrok URL from Colab OCR server | No (pre-configured) |

## API Endpoints

- `GET /` - Web interface
- `POST /analyze` - Analyze uploaded contract
- `GET /health` - Health check

## Future Features (Visual Placeholders)

The system shows visual placeholders for future automation features:

- **Automated Actions**: Calendar integration, WhatsApp reminders, document uploads
- **Actionable Gaps**: Upload interfaces, contact forms, conflict resolution
- **Smart Notifications**: Email/SMS reminders, deadline alerts

## Troubleshooting

1. **Colab OCR not working**: 
   - If using shared setup: Ask team member to restart their Colab notebook
   - If using your own: Ensure the Colab notebook is running and ngrok URL is correct
2. **OpenAI API errors**: Check your API key and quota
3. **Port already in use**: Kill existing processes or change the port in the code

## Contributing

This is a prototype system for contract intelligence. The visual elements show planned features for discussion and development.

## License

[Add your license here]
