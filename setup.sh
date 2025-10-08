#!/bin/bash

# Contract Intelligence Agent Setup Script

echo "🤖 Setting up Contract Intelligence Agent..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8+ first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cat > .env << EOF
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Colab OCR Configuration (optional - pre-configured in code)
# COLAB_OCR_URL=your_colab_ngrok_url_here
EOF
    echo "✅ Created .env file. Please update it with your API keys."
else
    echo "✅ .env file already exists."
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your OpenAI API key"
echo "2. Run: python3 contract_intelligence_agent.py"
echo "3. Open: http://localhost:8002"
echo ""
echo "Note: Colab OCR is pre-configured - no additional setup needed!"
echo ""
echo "For detailed instructions, see README.md"
