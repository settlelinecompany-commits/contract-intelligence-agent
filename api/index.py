def handler(request):
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Contract Intelligence Agent</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    padding: 40px; 
                    text-align: center; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    margin: 0;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .container {
                    background: white;
                    color: #333;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    max-width: 600px;
                }
                .header { 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; 
                    padding: 30px; 
                    border-radius: 15px; 
                    margin-bottom: 20px; 
                }
                .status { 
                    background: #e8f5e8; 
                    color: #2e7d32; 
                    padding: 20px; 
                    border-radius: 10px; 
                    border: 1px solid #4caf50;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🤖 Contract Intelligence Agent</h1>
                    <p>AI-powered rental contract analysis</p>
                </div>
                <div class="status">
                    <h2>✅ Server is Running!</h2>
                    <p>Your Vercel deployment is working correctly.</p>
                    <p>Ready to process rental contracts with OCR and AI analysis.</p>
                    <p><strong>Status:</strong> All systems operational</p>
                </div>
            </div>
        </body>
        </html>
        '''
    }