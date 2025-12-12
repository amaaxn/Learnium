# 🔧 MongoDB Connection Error Fix

## Error: `connect ECONNREFUSED 127.0.0.1:27017`

This error means MongoDB is not running on your local machine. Here's how to fix it:

---

## 🚀 Option 1: Install and Start Local MongoDB (Recommended for Development)

### Install MongoDB:

```bash
# macOS (using Homebrew)
brew tap mongodb/brew
brew install mongodb-community

# Or install MongoDB Compass (includes MongoDB server on some platforms)
brew install --cask mongodb-compass
```

### Start MongoDB Service:

```bash
# Start MongoDB as a service (runs in background)
brew services start mongodb-community

# Verify it's running
brew services list | grep mongodb

# Or check the process
ps aux | grep mongod
```

### Test Connection:

```bash
# Try connecting with mongosh
mongosh mongodb://localhost:27017/

# If successful, you should see:
# Current Mongosh Log ID: ...
# Connecting to: mongodb://127.0.0.1:27017/
```

### If MongoDB Won't Start:

1. **Check if port 27017 is already in use:**
   ```bash
   lsof -i :27017
   ```

2. **Create MongoDB data directory:**
   ```bash
   sudo mkdir -p /data/db
   sudo chown -R $(whoami) /data/db
   ```

3. **Start MongoDB manually to see errors:**
   ```bash
   mongod --dbpath /data/db
   ```

---

## ☁️ Option 2: Use MongoDB Atlas (Cloud - Best for Production)

If you want to use cloud MongoDB (no local installation needed):

### Step 1: Create Free Atlas Account
1. Go to https://www.mongodb.com/cloud/atlas/register
2. Sign up for free (M0 tier is free forever)
3. Create a new cluster (choose free tier)

### Step 2: Get Connection String
1. Click "Connect" on your cluster
2. Choose "Connect your application"
3. Copy the connection string (looks like):
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### Step 3: Update Your Environment
1. Create/update `backend/.env`:
   ```env
   MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/
   MONGO_DB_NAME=study_coach
   JWT_SECRET_KEY=your-secret-key-here
   ```
   Replace `username` and `password` with your Atlas credentials.

2. **Important:** Add your IP address to Atlas whitelist:
   - In Atlas dashboard → Network Access
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere" (for development) or add your specific IP

### Step 4: Update MongoDB Compass Connection
- Use the Atlas connection string in MongoDB Compass
- Or use: `mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/`

---

## 🔍 Quick Troubleshooting Commands

```bash
# Check if MongoDB is installed
which mongod

# Check if MongoDB is running
brew services list | grep mongodb
ps aux | grep mongod

# Start MongoDB
brew services start mongodb-community

# Stop MongoDB
brew services stop mongodb-community

# Restart MongoDB
brew services restart mongodb-community

# Check MongoDB version
mongod --version

# Test connection
mongosh mongodb://localhost:27017/
```

---

## ✅ Verify Connection Works

### In MongoDB Compass:
1. Connection string: `mongodb://localhost:27017/`
2. Click "Connect"
3. You should see databases listed

### In Terminal:
```bash
mongosh mongodb://localhost:27017/

# Should connect successfully and show:
# Current Mongosh Log ID: ...
# Connecting to: mongodb://127.0.0.1:27017/
```

### In Your App:
1. Make sure MongoDB is running
2. Restart your Flask backend
3. Try logging in/registering

---

## 🎯 Recommended Setup

**For Development:**
- Use local MongoDB (Option 1)
- Connection: `mongodb://localhost:27017/`

**For Production:**
- Use MongoDB Atlas (Option 2)
- Connection: `mongodb+srv://...` (from Atlas)

---

## 🆘 Still Having Issues?

1. **Check MongoDB logs:**
   ```bash
   # macOS
   tail -f /usr/local/var/log/mongodb/mongo.log
   
   # Or check system logs
   log show --predicate 'process == "mongod"' --last 5m
   ```

2. **Reinstall MongoDB:**
   ```bash
   brew services stop mongodb-community
   brew uninstall mongodb-community
   brew install mongodb-community
   brew services start mongodb-community
   ```

3. **Check firewall:**
   - macOS: System Preferences → Security & Privacy → Firewall
   - Make sure MongoDB is allowed

4. **Try different connection string:**
   - `mongodb://127.0.0.1:27017/`
   - `mongodb://localhost:27017/?directConnection=true`

---

## 📝 Next Steps After Fixing

Once MongoDB is running:

1. **Test connection in Compass:**
   - Should connect without errors
   - Should see `study_coach` database after you run the app once

2. **Run your Flask app:**
   ```bash
   cd backend
   python3 app.py
   ```

3. **Check database:**
   ```bash
   mongosh mongodb://localhost:27017/study_coach
   show collections  # Should show: users, courses, materials, study_tasks
   ```
