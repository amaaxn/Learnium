# 🚀 Deployment Guide for Learnium

## Production Readiness Checklist

### ✅ Current Status
- ✅ Multi-user support (user isolation with `@require_auth` on all routes)
- ✅ Environment variables properly configured (`.env` file, not committed)
- ✅ JWT authentication with secure token handling
- ✅ MongoDB database with user-scoped queries
- ✅ Error handling in API routes
- ✅ CORS configured (needs production origin restriction)

### ⚠️ Needs Attention Before Production

1. **CORS Configuration**
   - Currently allows all origins (`CORS(app, supports_credentials=True)`)
   - Should restrict to your production domain

2. **Environment Variables**
   - Must set in production environment (not `.env` file)
   - Required: `OPENAI_API_KEY`, `JWT_SECRET_KEY`, `MONGO_URI`, `MONGO_DB_NAME`

3. **MongoDB Connection**
   - Use MongoDB Atlas (cloud) instead of local MongoDB
   - Update `MONGO_URI` to Atlas connection string

4. **JWT Secret Key**
   - Generate a strong random secret (not the dev default)
   - Use: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

5. **OpenAI API Rate Limits**
   - Monitor usage and costs
   - Consider adding rate limiting per user

6. **Error Messages**
   - Some error messages may expose internal details
   - Review for production-safe error handling

---

## Recommended Deployment Platforms

### Option 1: Vercel (Frontend) + Railway/Render (Backend) ⭐ Recommended

**Frontend (Vercel):**
- Free tier available
- Automatic HTTPS
- Easy deployment from GitHub
- Great for React/Vite apps

**Backend (Railway or Render):**
- Free tier available (with limits)
- Easy environment variable setup
- Automatic HTTPS
- MongoDB Atlas integration

**Steps:**
1. Deploy backend to Railway/Render
2. Set environment variables
3. Deploy frontend to Vercel
4. Update frontend API URL to backend URL
5. Configure CORS on backend

### Option 2: AWS/GCP/Azure (Full Control)

**Pros:** Full control, scalable
**Cons:** More complex setup, costs can add up

### Option 3: DigitalOcean App Platform

**Pros:** Simple full-stack deployment
**Cons:** Costs more than free tiers

---

## Step-by-Step Deployment (Railway + Vercel)

### Backend Deployment (Railway)

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your Learnium repository
   - Select the `backend` folder as root

3. **Configure Environment Variables**
   ```
   OPENAI_API_KEY=sk-your-key-here
   JWT_SECRET_KEY=your-strong-random-secret
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/
   MONGO_DB_NAME=learnium_prod
   FLASK_ENV=production
   ```

4. **Update Railway Settings**
   - Set root directory to: `backend`
   - Set start command: `python app.py` (or use gunicorn for production)
   - Railway will auto-detect Python and install dependencies

5. **Use Production WSGI Server** (Recommended)
   - Add to `requirements.txt`: `gunicorn==21.2.0`
   - Update start command to: `gunicorn -w 4 -b 0.0.0.0:$PORT app:app`

6. **Get Backend URL**
   - Railway provides a public URL
   - Note this URL (e.g., `https://your-app.railway.app`)

### MongoDB Atlas Setup

1. **Create Atlas Account**
   - Go to https://www.mongodb.com/cloud/atlas
   - Create free cluster (M0)

2. **Create Database User**
   - Security → Database Access
   - Create user with password

3. **Whitelist IPs**
   - Network Access → Add IP Address
   - Add `0.0.0.0/0` for Railway (or specific Railway IPs)

4. **Get Connection String**
   - Clusters → Connect → Connect your application
   - Copy connection string
   - Replace `<password>` with your user password
   - Use format: `mongodb+srv://username:password@cluster.mongodb.net/learnium_prod`

### Frontend Deployment (Vercel)

1. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Set root directory to: `frontend`

3. **Configure Build Settings**
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Set Environment Variables**
   ```
   VITE_API_URL=https://your-app.railway.app
   ```

5. **Update API Client** (if needed)
   - Check `frontend/src/api/client.ts`
   - Ensure it uses `import.meta.env.VITE_API_URL` for production

6. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy

### Update CORS on Backend

After getting frontend URL, update `backend/app.py`:

```python
CORS(app, 
     origins=["https://your-app.vercel.app", "http://localhost:5173"],
     supports_credentials=True)
```

---

## Production Configuration Updates

### 1. Update `backend/app.py`

```python
# Add production checks
import os
from flask import Flask

app = Flask(__name__)

# Production CORS
if os.getenv("FLASK_ENV") == "production":
    from flask_cors import CORS
    frontend_url = os.getenv("FRONTEND_URL", "https://your-app.vercel.app")
    CORS(app, origins=[frontend_url], supports_credentials=True)
else:
    CORS(app, supports_credentials=True)  # Dev: allow all

# Production JWT secret (must be set in env)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
if not app.config["JWT_SECRET_KEY"]:
    raise ValueError("JWT_SECRET_KEY must be set in production")
```

### 2. Update `frontend/src/api/client.ts`

```typescript
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
});
```

### 3. Add `frontend/.env.production`

```
VITE_API_URL=https://your-backend.railway.app/api
```

---

## Security Checklist

- [ ] Change `JWT_SECRET_KEY` to strong random string
- [ ] Use MongoDB Atlas (not local)
- [ ] Restrict CORS to production domain only
- [ ] Set `FLASK_ENV=production`
- [ ] Use HTTPS only (automatic on Railway/Vercel)
- [ ] Review error messages for sensitive info
- [ ] Monitor OpenAI API usage and costs
- [ ] Set up logging/monitoring

---

## Testing Multi-User Support

Your app already supports multiple users:
- ✅ Each user has isolated data (filtered by `user_id`)
- ✅ All routes use `@require_auth` decorator
- ✅ Users cannot access other users' courses/materials/plans
- ✅ JWT tokens are user-specific

---

## Cost Estimates

**Free Tier Options:**
- Vercel: Free (up to 100GB bandwidth)
- Railway: $5/month free credit (usually enough for small apps)
- MongoDB Atlas: Free (512MB storage)
- OpenAI: Pay per use (~$0.001 per request with gpt-4o-mini)

**Estimated Monthly Cost:**
- Small app (<100 users): ~$5-10/month
- Medium app (100-1000 users): ~$20-50/month
- Large app: Custom pricing

---

## Monitoring & Maintenance

1. **Set up error tracking:**
   - Consider Sentry (free tier available)

2. **Monitor OpenAI costs:**
   - Set up billing alerts in OpenAI dashboard
   - Consider rate limiting per user

3. **Database backups:**
   - MongoDB Atlas has automatic backups (paid plans)
   - Or set up manual backup script

4. **Logs:**
   - Railway provides logs dashboard
   - Vercel provides build/deployment logs

---

## Quick Start Commands

```bash
# Generate JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Test production build locally
cd frontend && npm run build && npm run preview

# Test backend with gunicorn
cd backend && pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

---

## Need Help?

Common issues:
- CORS errors: Check frontend URL is in CORS origins
- Database connection: Verify MongoDB Atlas IP whitelist
- Environment variables: Double-check all are set in deployment platform
- Build errors: Check logs in Vercel/Railway dashboard
