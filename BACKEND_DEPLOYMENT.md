# Backend Deployment Guide (Render.com)

## Why Render.com?
- Free tier available
- Native Python/FastAPI support
- Easy environment variable management
- Automatic deployments from GitHub
- Better suited for long-running processes than Vercel

## Deployment Steps

### 1. Push Backend Files to GitHub

The following files have been created for deployment:
- `backend/Procfile` - Tells Render how to run the app
- `backend/runtime.txt` - Specifies Python version
- `backend/build.sh` - Build script for dependencies
- `render.yaml` - Render configuration file

### 2. Sign Up for Render

1. Go to https://render.com
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### 3. Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `dinhsst/ai-hr-assistant`
3. Configure the service:

   **Settings:**
   - **Name**: `ai-hr-assistant-backend`
   - **Region**: Oregon (US West) or closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

### 4. Add Environment Variables

In the Render dashboard, add these environment variables:

**Required:**
```
GROQ_API_KEY=your_groq_api_key_here
```

**Optional (for LangChain tracing):**
```
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=hr-assistant
```

### 5. Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Start the FastAPI server
3. Wait for deployment to complete (5-10 minutes)
4. Your backend URL will be: `https://ai-hr-assistant-backend.onrender.com`

### 6. Update Frontend Environment Variable

Once backend is deployed, update your Vercel frontend:

```bash
# Add the backend URL to Vercel
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://ai-hr-assistant-backend.onrender.com
```

Then redeploy the frontend:
```bash
cd frontend
vercel --prod
```

## Alternative: Deploy Backend to Railway.app

If you prefer Railway:

1. Go to https://railway.app
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select `dinhsst/ai-hr-assistant`
5. Set root directory to `backend`
6. Add environment variables
7. Railway will auto-detect Python and deploy

Your backend URL: `https://your-app.railway.app`

## Alternative: Deploy Backend to Vercel (Serverless)

While not ideal for FastAPI, you can try:

1. Create `backend/vercel.json`:
```json
{
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

2. Deploy:
```bash
cd backend
vercel --prod
```

**Note**: Vercel serverless functions have 10-second timeout on free tier.

## Testing Your Deployment

After backend is deployed, test it:

```bash
# Health check
curl https://your-backend-url.onrender.com/api/health

# Test chat endpoint
curl -X POST https://your-backend-url.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the remote work policy?"}'
```

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Ensure all dependencies in `requirements.txt` are compatible
- Verify Python version in `runtime.txt`

### Application Crashes
- Check application logs in Render
- Verify environment variables are set correctly
- Check that GROQ_API_KEY is valid

### Slow Response (Free Tier)
- Free tier apps spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Upgrade to paid tier for always-on service

## Post-Deployment Checklist

- [ ] Backend deployed successfully on Render
- [ ] Health endpoint returns 200 OK
- [ ] Environment variables configured
- [ ] Frontend updated with backend URL
- [ ] Frontend redeployed to Vercel
- [ ] End-to-end chat tested
- [ ] CV upload feature tested

## URLs Summary

**Frontend (Vercel)**: https://frontend-lsa3we58y-dinhssts-projects.vercel.app
**Backend (Render)**: https://ai-hr-assistant-backend.onrender.com (after deployment)
**GitHub Repo**: https://github.com/dinhsst/ai-hr-assistant

## Support

For issues:
- Render docs: https://render.com/docs
- Railway docs: https://docs.railway.app
- FastAPI deployment: https://fastapi.tiangolo.com/deployment/
