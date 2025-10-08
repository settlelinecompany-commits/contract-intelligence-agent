@echo off
REM Contract Intelligence Agent Setup Script for Windows

echo 🤖 Setting up Contract Intelligence Agent...

REM Check if Python 3 is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3 is required but not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo ⚙️ Creating .env file...
    (
        echo # OpenAI API Configuration
        echo OPENAI_API_KEY=your_openai_api_key_here
        echo.
        echo # Colab OCR Configuration (optional - pre-configured in code)
        echo # COLAB_OCR_URL=your_colab_ngrok_url_here
    ) > .env
    echo ✅ Created .env file. Please update it with your API keys.
) else (
    echo ✅ .env file already exists.
)

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Update .env file with your OpenAI API key
echo 2. Run: python contract_intelligence_agent.py
echo 3. Open: http://localhost:8002
echo.
echo Note: Colab OCR is pre-configured - no additional setup needed!
echo.
echo For detailed instructions, see README.md
pause
