# 🔗 How to Find Your Railway Backend URL

## Quick Steps to Get Your Backend URL

### Option 1: From Railway Dashboard (Easiest)

1. **Go to Railway Dashboard:**
   - Visit https://railway.app/dashboard
   - Click on your project (e.g., "Learnium" or "wholesome-acceptance")

2. **Find Your Service:**
   - Click on your backend service

3. **Get the URL:**
   - Look at the top of the service page
   - You'll see a URL like: `https://your-app-name.up.railway.app`
   - Or go to "Settings" → "Networking" → "Public Domain"
   - **Copy this URL** - this is your backend URL

4. **Add `/api` for Frontend:**
   - Your frontend needs: `https://your-app-name.up.railway.app/api`
   - This is what you'll use in `VITE_API_URL`

---

### Option 2: From Deployments Tab

1. In your Railway service
2. Go to "Deployments" tab
3. Click on the latest successful deployment
4. Look for "Public URL" or "Domain" in the deployment details

---

### Option 3: From Settings → Networking

1. Go to your service → "Settings" tab
2. Click "Networking" in the sidebar (or find "Public Domain" section)
3. You'll see your public domain/URL there
4. Copy it!

---

## 🔧 Using the URL in Frontend

### For Vercel Deployment:

1. **Go to Vercel Dashboard:**
   - https://vercel.com/dashboard
   - Select your project

2. **Add Environment Variable:**
   - Go to "Settings" → "Environment Variables"
   - Add new variable:
     - **Key:** `VITE_API_URL`
     - **Value:** `https://your-app-name.up.railway.app/api`
     - Select all environments (Production, Preview, Development)
   - Click "Save"

3. **Redeploy Frontend:**
   - Go to "Deployments" tab
   - Click "..." on latest deployment
   - Select "Redeploy"
   - Or make a small change and push to trigger new deployment

---

### Verify Your Backend URL Works:

Test in your browser or with curl:

```bash
# Health check
curl https://your-app-name.up.railway.app/api/health

# Should return: {"status":"ok","environment":"production"}
```

Or open in browser:
```
https://your-app-name.up.railway.app/api/health
```

---

## 📝 Example Configuration

**Railway Backend URL:**
```
https://learnium-backend-production.up.railway.app
```

**Vercel Environment Variable:**
```
VITE_API_URL=https://learnium-backend-production.up.railway.app/api
```

**Frontend API Client:**
Your frontend code in `frontend/src/api/client.ts` will automatically use this:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";
```

---

## 🔒 Important Notes

1. **Always include `/api`** in the frontend URL
2. **Use HTTPS** (Railway provides SSL automatically)
3. **Update CORS** in backend if needed:
   - Make sure `FRONTEND_URL` in Railway points to your frontend domain
4. **Test the connection** before deploying frontend

---

## ❓ Troubleshooting

**If you can't find the URL:**
- Make sure your service is deployed and running
- Check "Deployments" tab for successful deployments
- Look in "Logs" to see if there are errors

**If URL doesn't work:**
- Verify service is running (green status)
- Check logs for errors
- Test the `/api/health` endpoint
