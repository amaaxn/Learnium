# 🌐 Connect GoDaddy Domain (learnium.co) to Vercel

## Step-by-Step Guide

### Step 1: Add Domain in Vercel

1. **Go to Vercel Dashboard:**
   - Visit https://vercel.com/dashboard
   - Select your "learnium" project

2. **Add Custom Domain:**
   - Go to **Settings** → **Domains**
   - Click **"Add"** or **"Add Domain"**
   - Enter: `learnium.co`
   - Click **"Add"**

3. **Vercel will show you DNS configuration:**
   - After adding, Vercel will display what DNS records you need
   - Usually shows:
     - **A record** for root domain (`learnium.co`)
     - **CNAME record** for www (`www.learnium.co`)
   - **Note these values** - you'll need them for GoDaddy

---

### Step 2: Configure DNS in GoDaddy

#### Option A: Root Domain (learnium.co) - Recommended

1. **Log into GoDaddy:**
   - Go to https://dcc.godaddy.com/control/login
   - Log in to your account

2. **Go to DNS Management:**
   - Click **"My Products"**
   - Find **"learnium.co"** domain
   - Click **"DNS"** (or "Manage DNS")

3. **Add A Record:**
   - Scroll to **"Records"** section
   - Find **"A"** records section
   - Click **"Add"** or **"+"**
   - Configure:
     - **Type:** `A`
     - **Name:** `@` (or leave blank for root domain)
     - **Value:** `76.76.21.21` (Vercel's IP address - this is standard)
     - **TTL:** `600` (or 1 hour)
   - Click **"Save"**

4. **Add CNAME for www (Optional but recommended):**
   - Click **"Add"** again
   - Configure:
     - **Type:** `CNAME`
     - **Name:** `www`
     - **Value:** `cname.vercel-dns.com`
     - **TTL:** `600`
   - Click **"Save"**

#### Option B: If Vercel Gives You Different Values

Vercel might show you specific A record IPs or CNAME values. **Always use what Vercel shows you** in the Domains settings page, as they can vary.

---

### Step 3: Wait for DNS Propagation

1. **DNS Changes Take Time:**
   - Usually 5-60 minutes
   - Can take up to 24-48 hours (rare)
   - Most changes propagate within 1-2 hours

2. **Check Status in Vercel:**
   - Go back to Vercel → Settings → Domains
   - You'll see status:
     - ⏳ **"Pending"** = DNS not propagated yet
     - ⚠️ **"Invalid Configuration"** = DNS records incorrect
     - ✅ **"Valid Configuration"** = Everything working!
   - Once it shows "Valid Configuration", your domain is live!

---

### Step 4: Update Backend CORS

Once your domain is live:

1. **Get Your Live Domain:**
   - Your frontend will be: `https://learnium.co`

2. **Update Railway Environment:**
   - Go to Railway → Your backend service
   - Go to **Variables** tab
   - Update `FRONTEND_URL` to: `https://learnium.co`
   - Save (this triggers a redeploy)

3. **Verify:**
   - Visit `https://learnium.co`
   - Try logging in - should work!

---

## Quick Reference: GoDaddy DNS Records

For `learnium.co` pointing to Vercel:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | `76.76.21.21` | 600 |
| CNAME | www | `cname.vercel-dns.com` | 600 |

**Important:** The A record IP (`76.76.21.21`) is Vercel's standard IP. If Vercel shows you a different IP in their dashboard, use that instead.

---

## Troubleshooting

### Domain Shows "Invalid Configuration"

1. **Check DNS Records:**
   - Verify A record points to `76.76.21.21`
   - Verify CNAME for www points to `cname.vercel-dns.com`
   - Make sure there are no conflicting records

2. **Remove Conflicting Records:**
   - Delete any old A records pointing elsewhere
   - Delete any old CNAME records
   - Keep only the Vercel records

3. **Wait Longer:**
   - DNS changes can take time
   - Wait 1-2 hours and check again

### Domain Not Loading

1. **Check DNS Propagation:**
   - Use: https://dnschecker.org
   - Enter `learnium.co`
   - Check if A record shows `76.76.21.21` globally

2. **Clear Browser Cache:**
   - Try incognito/private mode
   - Clear DNS cache: `sudo dscacheutil -flushcache` (Mac) or restart router

3. **Verify in Vercel:**
   - Check Vercel dashboard shows "Valid Configuration"
   - Check deployment is successful

### SSL Certificate Issues

- Vercel automatically provisions SSL certificates
- This happens automatically after DNS is configured
- Can take 10-60 minutes after DNS propagates
- Your site will show "Not Secure" until SSL is ready (then automatically switches to HTTPS)

---

## Step-by-Step Screenshots Guide

### GoDaddy DNS Management:

1. **Access DNS:**
   - GoDaddy → My Products → learnium.co → DNS

2. **Add A Record:**
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   TTL: 600
   ```

3. **Add CNAME (optional):**
   ```
   Type: CNAME
   Name: www
   Value: cname.vercel-dns.com
   TTL: 600
   ```

4. **Save all records**

---

## Verify It's Working

### Test Your Domain:

1. **Visit:** `https://learnium.co`
   - Should load your Vercel deployment
   - Should show padlock (SSL certificate)

2. **Visit:** `https://www.learnium.co` (if you set up www)
   - Should redirect to or load `https://learnium.co`

3. **Test Login:**
   - Try creating an account
   - Should connect to Railway backend
   - Everything should work!

---

## Summary

✅ **What You Did:**
1. Added `learnium.co` in Vercel Domains
2. Added A record in GoDaddy: `@` → `76.76.21.21`
3. Added CNAME in GoDaddy: `www` → `cname.vercel-dns.com`
4. Updated Railway `FRONTEND_URL` to `https://learnium.co`
5. Waited for DNS propagation
6. Your domain is live! 🎉

---

## Important Notes

- **Always use HTTPS:** Vercel automatically provides SSL
- **Root vs www:** You can use either, but A record for root is recommended
- **DNS propagation:** Be patient - it can take time
- **Vercel values:** Always check Vercel's domain settings for the exact values they want

Your domain `learnium.co` will be live once DNS propagates! 🚀
