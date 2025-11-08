# Deployment Guide

## Prerequisites
- GitHub account
- Vercel account (sign up at vercel.com)
- Git installed locally

## Git Setup (Completed)
✅ Repository initialized
✅ .gitignore created
✅ Initial commit made

## Next Steps

### 1. Push to GitHub

You need to create a GitHub repository first:

1. Go to https://github.com/new
2. Create a new repository (e.g., "ai-hr-assistant")
3. Copy the repository URL

Then run these commands:
```bash
git remote add origin YOUR_GITHUB_REPO_URL
git branch -M main
git push -u origin main
```

Example:
```bash
git remote add origin https://github.com/yourusername/ai-hr-assistant.git
git branch -M main
git push -u origin main
```

### 2. Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard (Recommended)
1. Go to https://vercel.com
2. Sign in with your GitHub account
3. Click "Add New Project"
4. Import your GitHub repository
5. Configure the project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - Add environment variables:
     - `NEXT_PUBLIC_API_URL`: Your backend API URL
6. Click "Deploy"

#### Option B: Deploy via Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### 3. Environment Variables

#### Frontend (.env.local)
Create in `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
```

#### Backend (.env)
Create in `backend/.env`:
```
GROQ_API_KEY=your_groq_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=hr-assistant
```

### 4. Backend Deployment Notes

The Python backend may need additional configuration for Vercel:
- Ensure `requirements.txt` is up to date
- Vercel Python runtime has size limitations
- Consider using Vercel Serverless Functions or deploying backend separately (Railway, Render, etc.)

### Alternative Backend Deployment Options:
- **Railway**: https://railway.app
- **Render**: https://render.com
- **Heroku**: https://heroku.com
- **AWS Lambda**: For serverless deployment

## Deployment Checklist
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Set up Vercel account
- [ ] Import repository to Vercel
- [ ] Configure environment variables
- [ ] Deploy frontend
- [ ] Deploy backend (consider separate service)
- [ ] Update frontend API URL
- [ ] Test deployed application

## Support
For issues, check:
- Vercel deployment logs
- GitHub Actions (if configured)
- Environment variable configuration
