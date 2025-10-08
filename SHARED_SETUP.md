# Shared Colab Setup Instructions

## For Team Members

### Super Quick Setup (Pre-configured!)

1. **Just update your `.env` file:**
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```
2. **Run the app:**
   ```bash
   python3 contract_intelligence_agent.py
   ```

**That's it!** The Colab OCR URL is already hardcoded in the application.

### For the Colab Owner

**To share your Colab setup:**

1. **Keep your Colab notebook running** (`colab_ocr_processor.ipynb`)
2. **Share your ngrok URL** with team members
3. **Restart Colab if needed** (runtime disconnects happen)

**Current ngrok URL format:**
```
https://[random-string].ngrok-free.dev
```

### Benefits of Shared Setup

- ✅ **Faster onboarding** - no need to set up individual Colab accounts
- ✅ **Shared GPU resources** - more efficient use of Colab Pro
- ✅ **Consistent API** - same endpoint for all team members
- ✅ **Easy maintenance** - one person manages the Colab setup

### Troubleshooting

**If OCR stops working:**
- Ask the Colab owner to restart their notebook
- Check if the ngrok URL has changed
- Verify the Colab notebook is still running

**If you want your own setup:**
- Follow the "Option B" instructions in README.md
- You'll need your own Google Colab account and ngrok account
