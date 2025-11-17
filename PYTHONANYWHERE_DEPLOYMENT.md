# 🚀 EduBot - PythonAnywhere Deployment Guide

## ✅ Step-by-Step Deployment

### **Step 1: Create PythonAnywhere Account (5 min)**

1. Go to: **https://www.pythonanywhere.com**
2. Click **"Pricing & signup"**
3. Choose **"Create a Beginner account"** (FREE)
4. Fill in:
   - Username (remember this!)
   - Email
   - Password
5. Verify your email
6. Login to PythonAnywhere

---

### **Step 2: Upload Your Code via GitHub (10 min)**

#### **2a. Create GitHub Repository**

Open PowerShell and run:

```powershell
cd "d:\ai chat-bot"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "EduBot ready for PythonAnywhere deployment"

# Create repo on GitHub:
# 1. Go to https://github.com/new
# 2. Repository name: edubot-smart-assistant
# 3. Public
# 4. Don't add README (we have one)
# 5. Click "Create repository"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/edubot-smart-assistant.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### **2b. Clone to PythonAnywhere**

1. In PythonAnywhere dashboard, click **"Consoles"** tab
2. Click **"$ Bash"** to start a console
3. Run these commands:

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/edubot-smart-assistant.git

# Navigate into folder
cd edubot-smart-assistant

# Install dependencies
pip3.10 install --user -r requirements.txt

# This will take 2-3 minutes
```

---

### **Step 3: Create Web App (5 min)**

1. Click **"Web"** tab in PythonAnywhere
2. Click **"Add a new web app"**
3. Click **"Next"** (accept default domain for now)
4. Select **"Manual configuration"**
5. Choose **"Python 3.10"**
6. Click **"Next"**

---

### **Step 4: Configure WSGI File (5 min)**

1. In the **Web** tab, scroll to **"Code"** section
2. Click on the WSGI configuration file link (looks like: `/var/www/yourusername_pythonanywhere_com_wsgi.py`)
3. **DELETE ALL** existing code
4. **PASTE THIS CODE:**

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/edubot-smart-assistant'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['FLASK_APP'] = 'app.py'

# Import your Flask application
from app import app as application

# For debugging (optional - remove in production)
application.debug = False
```

**⚠️ IMPORTANT:** Replace `YOUR_USERNAME` with your actual PythonAnywhere username!

5. Click **"Save"** (top right)

---

### **Step 5: Configure Virtualenv & Static Files (5 min)**

#### **In the Web tab:**

**1. Source code:**
```
/home/YOUR_USERNAME/edubot-smart-assistant
```

**2. Working directory:**
```
/home/YOUR_USERNAME/edubot-smart-assistant
```

**3. Static files:**
Click **"Add a new static files mapping"**

```
URL: /static/
Directory: /home/YOUR_USERNAME/edubot-smart-assistant/static
```

**4. Virtualenv (Optional but Recommended):**

Skip this for now - we installed packages with `--user` flag.

---

### **Step 6: Initialize Database (5 min)**

1. Go back to **"Consoles"** tab
2. Open your Bash console
3. Run:

```bash
cd edubot-smart-assistant

# Initialize database
python3.10 -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"

# Create admin user (optional)
python3.10 -c "
from app import app, db
from database.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = User(
        username='admin',
        email='admin@edubot.com',
        password_hash=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    print('Admin user created!')
"
```

---

### **Step 7: Reload Web App (1 min)**

1. Go back to **"Web"** tab
2. Scroll to top
3. Click the big green **"Reload yourusername.pythonanywhere.com"** button
4. Wait 10-20 seconds

---

### **Step 8: Test Your Live Site! 🎉**

1. Click the link at top: `https://yourusername.pythonanywhere.com`
2. Your EduBot is now LIVE! ✅
3. Test all features:
   - Chat interface
   - Study planner
   - All 30+ features
   - Login/Register

---

## 🌐 Connect Your Hostinger Domain (Optional)

### **In PythonAnywhere:**

1. **Web** tab → **"CNAME Setup"** section
2. Note your domain: `yourusername.pythonanywhere.com`

### **In Hostinger:**

1. Login to Hostinger
2. **Domains** → Your domain → **DNS**
3. Click **"Add Record"**

**For subdomain (edubot.yourdomain.com):**
```
Type: CNAME
Name: edubot
Points to: yourusername.pythonanywhere.com
TTL: 3600
```

4. Click **"Add Record"**
5. Wait 30-60 minutes for DNS propagation
6. Visit: `https://edubot.yourdomain.com`

---

## 🔧 Troubleshooting

### **Issue: Error log shows "No module named 'app'"**

**Solution:**
1. Check WSGI file has correct path
2. Make sure `app.py` exists in `/home/YOUR_USERNAME/edubot-smart-assistant`

### **Issue: 500 Internal Server Error**

**Solution:**
1. Go to **Web** tab
2. Click **"Error log"** link
3. Read the error message
4. Fix the issue
5. Click **"Reload"**

### **Issue: Static files not loading (no CSS)**

**Solution:**
1. Check static files mapping in Web tab
2. Make sure path is: `/home/YOUR_USERNAME/edubot-smart-assistant/static`
3. Click **"Reload"**

### **Issue: Database errors**

**Solution:**
```bash
cd edubot-smart-assistant
python3.10 -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

## 📱 Your Live URLs

**Free subdomain:** `https://yourusername.pythonanywhere.com`

**Custom domain (after DNS setup):** `https://edubot.yourdomain.com`

---

## 🔄 How to Update Your Site

When you make changes locally:

```powershell
# On your computer
cd "d:\ai chat-bot"
git add .
git commit -m "Updated features"
git push
```

Then in PythonAnywhere Bash console:

```bash
cd edubot-smart-assistant
git pull
# Reload via Web tab
```

---

## 📊 Free Tier Limits

✅ **1 web app** - Perfect for EduBot
✅ **512 MB storage** - Plenty for your app
✅ **100k hits/day** - ~3M requests/month
✅ **Always online** - No sleep mode
✅ **Free forever** - No expiration

---

## 🎓 Success Checklist

- [ ] PythonAnywhere account created
- [ ] Code uploaded via GitHub
- [ ] Web app created
- [ ] WSGI file configured
- [ ] Static files mapped
- [ ] Database initialized
- [ ] Web app reloaded
- [ ] Site tested and working
- [ ] Custom domain added (optional)
- [ ] SSL certificate active

---

## 🆘 Need Help?

1. Check **Error log** in Web tab
2. Check **Server log** in Web tab
3. PythonAnywhere forums: https://www.pythonanywhere.com/forums/
4. PythonAnywhere help: https://help.pythonanywhere.com/

---

**Your EduBot is now live 24/7 for FREE! 🎉**

Total deployment time: ~30 minutes
Cost: $0.00 forever!
