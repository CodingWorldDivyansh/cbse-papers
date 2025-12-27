# Deploy CBSE Papers App to Render (Free 24/7 Hosting)

## Step 1: Push Code to GitHub

### Option A: Create a new GitHub repository
1. Go to https://github.com/new
2. Name it `cbse-papers` (or any name you prefer)
3. Keep it public (required for free Render deployment)
4. Don't initialize with README (we already have code)
5. Click "Create repository"

### Option B: Use the commands below after creating the repo
```bash
cd /workspace/project
git remote add origin https://github.com/YOUR_USERNAME/cbse-papers.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Render

### Option A: One-Click Deploy (Recommended)
1. Go to https://render.com
2. Sign up/Login with your GitHub account
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render will auto-detect the `render.yaml` configuration
6. Click "Create Web Service"

### Option B: Manual Configuration
If auto-detection doesn't work:
- **Name**: cbse-papers
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`
- **Plan**: Free

## Step 3: Wait for Deployment
- Build takes 2-5 minutes
- Your app will be live at: `https://cbse-papers.onrender.com`

## Important Notes

### Free Tier Limitations
- App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- 750 hours/month free (enough for 24/7 for one service)

### Keep App Awake (Optional)
To prevent sleep, use a free cron service like:
- https://cron-job.org - Set up a ping every 14 minutes to your Render URL
- UptimeRobot (https://uptimerobot.com) - Free monitoring that also keeps app awake

## Files Created for Render

1. **render.yaml** - Render Blueprint configuration
2. **Procfile** - Gunicorn web server configuration  
3. **runtime.txt** - Python version specification
4. **requirements.txt** - Python dependencies

## Your App Features
- 2,376 CBSE papers (2015-2025)
- 6 subjects: Math, Accountancy, Economics, Business Studies, English, Data Science
- Direct PDF downloads with mirror fallback
- Bulk download as ZIP
- Filter by year, subject, type, region
- Mobile-responsive design
