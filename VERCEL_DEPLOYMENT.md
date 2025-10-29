# Vercel Deployment Guide

## Quick Deploy to Vercel

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub** (already done!)
2. **Go to [vercel.com](https://vercel.com)** and sign in
3. **Click "New Project"**
4. **Import your GitHub repository**: `settlelinecompany-commits/contract-intelligence-agent`
5. **Configure environment variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `COLAB_OCR_URL`: `https://snaillike-russel-snodly.ngrok-free.dev` (already set)
6. **Click "Deploy"**

### Option 2: Deploy with Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy from your project directory
cd /Users/admin/rental-tech/contract-intelligence
vercel

# Set environment variables
vercel env add OPENAI_API_KEY
# Enter your OpenAI API key when prompted

# Redeploy with environment variables
vercel --prod
```

## Important Notes

### ⚠️ **Limitations for Vercel Deployment:**

1. **File Upload Size**: Vercel has a 4.5MB limit for serverless functions
2. **Execution Time**: 10-second timeout for Hobby plan, 60 seconds for Pro
3. **Colab Dependency**: Your Colab OCR must stay running
4. **Cold Starts**: First request might be slower

### 🔧 **Optimizations Made:**

- ✅ **Serverless-optimized** FastAPI app in `/api/index.py`
- ✅ **Minimal dependencies** in `requirements-vercel.txt`
- ✅ **Vercel configuration** in `vercel.json`
- ✅ **Environment variables** pre-configured
- ✅ **Error handling** for serverless environment

### 📱 **After Deployment:**

Your app will be available at:
- **Production URL**: `https://your-project-name.vercel.app`
- **API Endpoints**: 
  - `GET /` - Web interface
  - `POST /api/analyze` - Contract analysis
  - `GET /api/health` - Health check

### 🚀 **Alternative: Railway/Render**

If Vercel doesn't work well for your use case, consider:

- **Railway**: Better for long-running processes
- **Render**: Good for Python apps with file uploads
- **Heroku**: Traditional PaaS option

### 💡 **Pro Tips:**

1. **Keep Colab running** - The OCR service needs to stay active
2. **Monitor usage** - Vercel has usage limits on free tier
3. **Test thoroughly** - Serverless environments behave differently
4. **Consider Pro plan** - For higher limits and better performance

## Troubleshooting

### Common Issues:

1. **"Function timeout"**: Reduce file size or optimize processing
2. **"Module not found"**: Check `requirements-vercel.txt`
3. **"Environment variable missing"**: Set in Vercel dashboard
4. **"Colab OCR failed"**: Ensure your Colab notebook is running

### Debug Commands:

```bash
# Check Vercel logs
vercel logs

# Test locally with Vercel
vercel dev

# Check environment variables
vercel env ls
```




