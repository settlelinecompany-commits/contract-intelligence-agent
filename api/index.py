from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Contract Intelligence Agent</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 40px; text-align: center; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px; border-radius: 10px; margin-bottom: 20px; }
            .status { background: #e8f5e8; color: #2e7d32; padding: 20px; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 Contract Intelligence Agent</h1>
            <p>AI-powered rental contract analysis</p>
        </div>
        <div class="status">
            <h2>✅ Server is Running!</h2>
            <p>Your Vercel deployment is working correctly.</p>
            <p>Ready to process rental contracts with OCR and AI analysis.</p>
        </div>
    </body>
    </html>
    """)

@app.get("/api/health")
async def health():
    return {"status": "healthy", "message": "Contract Intelligence Agent is running"}

# For Vercel
handler = app