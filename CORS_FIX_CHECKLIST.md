# CORS Error Fix Checklist

## ✅ Code is Fixed
The backend code now has explicit CORS header handling that should work.

## ⚠️ CRITICAL: Check Railway Environment Variable

The CORS error happens because Railway backend doesn't know which frontend origin to allow.

### Step 1: Verify FRONTEND_URL in Railway
1. Go to Railway Dashboard
2. Click your Backend Service
3. Go to **"Variables"** tab
4. Find `FRONTEND_URL`
5. **It MUST be set to:** `https://www.learnium.co` (with `https://` and `www`)

### Step 2: If FRONTEND_URL is Missing or Wrong
1. Click **"New Variable"** or **Edit** existing
2. **Key:** `FRONTEND_URL`
3. **Value:** `https://www.learnium.co`
4. **Save**
5. Railway will auto-redeploy (wait 2-3 minutes)

### Step 3: Verify Deployment
After Railway redeploys, check the logs. You should see:
```
🔧 FRONTEND_URL: https://www.learnium.co
✅ CORS configured for: ['https://www.learnium.co', ...]
```

### Step 4: Test
1. Refresh your frontend site
2. Try logging in
3. Check browser console - CORS errors should be gone

## If Still Not Working

1. **Check Railway Logs** - Look for CORS configuration messages
2. **Verify Container is Running** - Make sure backend stays up (not restarting)
3. **Check Browser Console** - Look for the actual error message
4. **Test OPTIONS Request** - In browser console, run:
   ```javascript
   fetch('https://learnium-production.up.railway.app/api/auth/login', {
     method: 'OPTIONS',
     headers: { 'Origin': 'https://www.learnium.co' }
   }).then(r => console.log('Status:', r.status, 'Headers:', [...r.headers.entries()]))
   ```

## Quick Test
After Railway redeploys, check Railway logs for:
- `🔍 OPTIONS preflight from origin: https://www.learnium.co`
- `✅ CORS Allow-Origin header set to: https://www.learnium.co`

If you see these, CORS is working!
