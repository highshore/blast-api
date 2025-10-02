# BLAST API for GammaFold

FastAPI service that provides BLAST functionality using Biopython.

## Quick Deploy to Railway

1. **Push to GitHub:**
   ```bash
   cd /Users/nespresso/Desktop/blast-api
   git init
   git add .
   git commit -m "BLAST API service"
   gh repo create blast-api --public --source=. --push
   ```

2. **Deploy on Railway:**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your `blast-api` repository
   - Railway will auto-detect Python and deploy

3. **Add Environment Variable:**
   - In Railway dashboard, go to your service
   - Click "Variables" tab
   - Add: `NCBI_API_KEY` = `e62a5f1dcd925f307a6b5027aa57e5ec0508`

4. **Get Your URL:**
   - Railway will give you a URL like: `https://blast-api-production-xxxx.up.railway.app`
   - Copy this URL

## Update GammaFold Frontend

In your GammaFold `.env`:
```
VITE_PYTHON_BLAST_API=https://your-railway-url.up.railway.app
```

## Local Development

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export NCBI_API_KEY=e62a5f1dcd925f307a6b5027aa57e5ec0508
uvicorn main:app --reload --port 8000
```

Then in GammaFold `.env`:
```
VITE_PYTHON_BLAST_API=http://localhost:8000
```

## Alternative: Deploy to Render

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repo
4. Settings:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `NCBI_API_KEY`

## Endpoints

- `GET /` - Service status
- `POST /blast-submit` - Submit BLAST search
- `GET /health` - Health check

