# 🔧 Railway Backend Build Troubleshooting

## Common Build Failure Issues & Fixes

### ✅ 1. Root Directory Configuration

**Problem:** Railway doesn't know where your backend code is.

**Solution:**
1. In Railway dashboard, go to your service
2. Click "Settings" → "Root Directory"
3. Set to: `backend`
4. Save and redeploy

---

### ✅ 2. Python Version

**Problem:** Railway might use wrong Python version.

**Solution:**
Create `backend/runtime.txt` with:
```
python-3.11.0
```

Or in Railway:
1. Go to "Variables" tab
2. Add: `PYTHON_VERSION=3.11`

---

### ✅ 3. Start Command Issues

**Problem:** Gunicorn not found or wrong command.

**Current command:**
```
gunicorn -w 4 --bind 0.0.0.0:$PORT --timeout 120 app:app
```

**Alternative if gunicorn fails:**
```
python app.py
```

**Better gunicorn command:**
```
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app
```

---

### ✅ 4. Missing Dependencies

**Problem:** Dependencies not installing.

**Check:**
- Make sure `requirements.txt` is in `backend/` folder
- All dependencies are listed correctly
- No syntax errors in requirements.txt

**Fix:**
1. Check build logs in Railway
2. Look for "ModuleNotFoundError" or similar
3. Add missing package to `requirements.txt`

---

### ✅ 5. Environment Variables

**Problem:** Build succeeds but app crashes on startup.

**Required Environment Variables:**
```
ENVIRONMENT=production
FLASK_ENV=production
OPENAI_API_KEY=sk-your-key
JWT_SECRET_KEY=your-secret-here
MONGO_URI=mongodb+srv://...
MONGO_DB_NAME=learnium_prod
FRONTEND_URL=https://yourdomain.com
PORT=5000
```

**Note:** Railway sets `PORT` automatically, but you can override it.

---

### ✅ 6. Import Errors

**Problem:** Python can't find modules.

**Check build logs for:**
- `ModuleNotFoundError: No module named '...'`
- `ImportError: ...`

**Common fixes:**
- Make sure all `__init__.py` files exist in folders
- Check imports are correct (no typos)
- Verify all dependencies in requirements.txt

---

### ✅ 7. Build Log Analysis

**How to check logs:**
1. In Railway, click on your service
2. Go to "Deployments" tab
3. Click on the failed deployment
4. Check "Build Logs" and "Deploy Logs"

**Look for:**
- Red error messages
- "ModuleNotFoundError"
- "ImportError"
- "SyntaxError"
- Missing files

---

## Quick Fix Checklist

- [ ] Root directory set to `backend`
- [ ] `runtime.txt` exists with Python version
- [ ] `requirements.txt` is correct
- [ ] Start command is correct
- [ ] All environment variables set
- [ ] Check build logs for specific errors

---

## Step-by-Step Fix

1. **Check Root Directory:**
   - Settings → Root Directory → `backend`

2. **Verify Start Command:**
   - Settings → Deploy → Custom Start Command
   - Use: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 app:app`

3. **Check Environment Variables:**
   - Variables tab
   - Make sure all required vars are set

4. **Check Build Logs:**
   - Deployments → Latest → Build Logs
   - Look for error messages

5. **Test Locally:**
   ```bash
   cd backend
   pip install -r requirements.txt
   gunicorn --bind 0.0.0.0:5001 app:app
   ```

---

## Alternative: Use Python Directly

If gunicorn keeps failing, use Python directly (temporary fix):

**Start Command:**
```
python app.py
```

**Update app.py to handle PORT:**
```python
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    app.run(debug=False, port=port, host="0.0.0.0")
```

---

## Still Not Working?

1. **Check Railway Status:** https://status.railway.app
2. **View Detailed Logs:** Railway → Service → Logs tab
3. **Try Minimal Start:** Use `python app.py` temporarily
4. **Contact Support:** Railway support if issue persists

---

## Example Working Configuration

**Root Directory:** `backend`

**Start Command:**
```
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app
```

**Environment Variables:**
```
ENVIRONMENT=production
FLASK_ENV=production
PORT=5000
OPENAI_API_KEY=...
JWT_SECRET_KEY=...
MONGO_URI=...
MONGO_DB_NAME=learnium_prod
FRONTEND_URL=https://yourdomain.com
```
