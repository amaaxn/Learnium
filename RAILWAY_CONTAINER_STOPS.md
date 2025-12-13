# Railway Container Keeps Stopping - Troubleshooting

## Issue
Container starts successfully, health check passes (200 OK), but Railway sends SIGTERM and stops the container.

## Possible Causes

### 1. Railway Health Check Configuration
Railway might be expecting a different health check response format or timing.

**Fix:** Check Railway dashboard → Your Service → Settings → Health Checks
- Ensure health check path is: `/api/health`
- Health check timeout: 10-30 seconds
- Health check interval: 10-30 seconds

### 2. Railway Service Configuration
Check if there are any service-level settings causing restarts:
- Railway → Your Service → Settings
- Look for "Auto Deploy", "Restart Policy", etc.

### 3. Resource Limits
Railway might be killing the container due to resource constraints:
- Check Railway → Your Service → Metrics
- Look for memory/CPU spikes
- Consider upgrading your Railway plan if hitting limits

### 4. Port Configuration
Ensure the port is correctly configured:
- Railway automatically sets `$PORT` environment variable
- The app should bind to `0.0.0.0:$PORT`
- Check Railway logs for port binding confirmation

## Quick Fixes to Try

### Option 1: Simplify Health Check (Already Done)
The health check endpoint now returns minimal response for faster Railway verification.

### Option 2: Check Railway Service Settings
1. Go to Railway → Your Backend Service
2. Click "Settings" tab
3. Scroll to "Health Checks" section
4. Verify:
   - Path: `/api/health`
   - Timeout: 10 seconds
   - Interval: 10 seconds

### Option 3: Check Railway Deployment Settings
1. Railway → Your Service → Settings → Deployments
2. Look for any auto-restart or deployment policies

### Option 4: Monitor Railway Metrics
1. Railway → Your Service → Metrics
2. Watch for memory/CPU usage spikes
3. Check if container is being killed due to resource limits

## Test After Changes

After Railway redeploys:
1. Watch the logs - container should stay running
2. Check if you see repeated "Stopping Container" messages
3. Test login/register - should work if container stays up

## If Still Stopping

Share:
1. Railway dashboard → Service → Metrics (screenshot)
2. Railway dashboard → Service → Settings → Health Checks (screenshot)
3. Any error messages in Railway logs after the stop
