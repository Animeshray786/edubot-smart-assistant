# 🌐 Ngrok Setup - Public Internet Access

## Make Your EduBot Accessible Worldwide in 10 Minutes!

---

## 📋 What is Ngrok?

Ngrok creates a **secure public tunnel** to your localhost. Perfect for:
- ✅ Showing your bot to remote evaluators
- ✅ Testing from anywhere (coffee shop, home, etc.)
- ✅ Quick demos without full deployment
- ✅ Mobile testing from anywhere

---

## 🚀 Quick Setup

### **Step 1: Install Ngrok**

#### Option A: Download & Extract
1. Go to https://ngrok.com/download
2. Download Windows version
3. Extract `ngrok.exe` to `C:\ngrok\` (or any folder)
4. Add to PATH (optional)

#### Option B: Using Chocolatey
```powershell
choco install ngrok
```

### **Step 2: Sign Up (Free)**

1. Go to https://dashboard.ngrok.com/signup
2. Sign up with Google/GitHub (quick!)
3. Get your **Auth Token**

### **Step 3: Authenticate**

```powershell
# Run this once (replace with your token)
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

Example:
```powershell
ngrok config add-authtoken 2abc123def456ghi789jkl
```

---

## 🎯 Two Ways to Use Ngrok

### **Method 1: Two Terminals (Recommended)**

**Terminal 1 - Start Flask:**
```powershell
cd "d:\ai chat-bot"
python app.py
```

Wait for Flask to start, then...

**Terminal 2 - Start Ngrok:**
```powershell
ngrok http 5000
```

✅ **You'll see:**
```
ngrok

Session Status    online
Account           Your Name (Plan: Free)
Version           3.x.x
Region            United States (us)
Latency           50ms
Web Interface     http://127.0.0.1:4040
Forwarding        https://abc123.ngrok-free.app -> http://localhost:5000

Connections       ttl     opn     rt1     rt5     p50     p90
                  0       0       0.00    0.00    0.00    0.00
```

📋 **Your Public URL**: `https://abc123.ngrok-free.app`

### **Method 2: Automated Script (Easier)**

Create `start_with_ngrok.py`:

```python
"""
Start EduBot with Ngrok
"""
from pyngrok import ngrok
import subprocess
import os
import sys

# Your ngrok auth token (get from https://dashboard.ngrok.com)
NGROK_AUTH_TOKEN = "YOUR_AUTH_TOKEN_HERE"

def main():
    # Set auth token
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    
    # Start ngrok tunnel
    print("Starting ngrok tunnel...")
    public_url = ngrok.connect(5000, bind_tls=True)
    
    print(f"""
╔══════════════════════════════════════════════════════╗
║           🎉 EDUBOT IS NOW PUBLIC! 🎉                ║
╠══════════════════════════════════════════════════════╣
║                                                       ║
║  🌍 Public URL (Share this worldwide):               ║
║  {public_url}                           ║
║                                                       ║
║  📱 Local URL:                                        ║
║  http://localhost:5000                               ║
║                                                       ║
╠══════════════════════════════════════════════════════╣
║  ✅ Share the public URL with ANYONE!                ║
║  ✅ Valid for 2 hours (free tier)                    ║
║  ✅ Press CTRL+C to stop                             ║
╚══════════════════════════════════════════════════════╝
    """)
    
    # Start Flask
    print("\nStarting Flask server...\n")
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()
```

**Install pyngrok:**
```powershell
pip install pyngrok
```

**Run it:**
```powershell
python start_with_ngrok.py
```

---

## 📱 Testing Your Public URL

1. **Copy the ngrok URL** (e.g., `https://abc123.ngrok-free.app`)
2. **Open on any device:**
   - Your phone (mobile data or WiFi)
   - Friend's computer
   - Tablet
   - Different network entirely!
3. **Share the link:**
   - WhatsApp: Send to project group
   - Email: Send to evaluator
   - SMS: Send to yourself for mobile testing

---

## ⚙️ Ngrok Web Interface

Open `http://127.0.0.1:4040` to see:
- 📊 Live traffic
- 📝 All requests
- 🔍 Request/response details
- 🐛 Debug issues

Perfect for monitoring demos!

---

## 🎓 Free Tier Limits

Ngrok Free includes:
- ✅ 1 online tunnel
- ✅ HTTPS support
- ✅ 40 connections/minute
- ⏰ 2 hour session timeout (just restart!)
- ✅ Random URL (changes each restart)

**Perfect for:**
- Demos & presentations
- Quick testing
- Remote access
- Mobile testing

---

## 🎯 Pro Tips

### **Keep Ngrok Running**

Free tier sessions last 2 hours, then auto-restart. Just leave it running during your demo!

### **Custom Subdomain** (Paid - $8/month)
```powershell
ngrok http 5000 --subdomain=edubot
# URL becomes: https://edubot.ngrok.io
```

### **Share with Warning Banner**

Free tier shows ngrok warning page first. Users click "Visit Site" to proceed. Normal behavior!

### **Check Status**
```powershell
# View active tunnels
curl http://localhost:4040/api/tunnels
```

---

## 🆘 Troubleshooting

### **Error: "command not found: ngrok"**

**Fix 1**: Use full path
```powershell
C:\ngrok\ngrok.exe http 5000
```

**Fix 2**: Add to PATH
1. Search Windows → "Environment Variables"
2. Edit PATH
3. Add `C:\ngrok\`
4. Restart PowerShell

### **Error: "Authentication failed"**

Run auth command again:
```powershell
ngrok config add-authtoken YOUR_TOKEN
```

### **Error: "Only one tunnel allowed"**

Free tier = 1 tunnel. Stop old ngrok instance:
```powershell
# Find process
tasklist | findstr ngrok

# Kill it
taskkill /F /IM ngrok.exe
```

### **Slow Connection**

Normal on free tier! Ngrok routes through their servers. Expect 100-300ms latency.

---

## 🔒 Security Notes

- ✅ Ngrok uses HTTPS (secure)
- ✅ Change SECRET_KEY in production
- ✅ Don't share URLs publicly (send directly to evaluators)
- ✅ Stop ngrok when done
- ⚠️ Free URLs are public - anyone with link can access

---

## 📊 Comparison: Ngrok vs Other Methods

| Feature | Ngrok | Local Network | Render Cloud |
|---------|-------|---------------|--------------|
| **Setup Time** | 10 min | 5 min | 30 min |
| **Access** | Worldwide | Same WiFi | Worldwide |
| **Uptime** | While running | While running | 24/7 |
| **URL Changes** | Every restart | Never | Never |
| **Best For** | Quick demos | Classroom | Final submission |

---

## 🎉 You're Ready!

**Start ngrok now:**

```powershell
# Terminal 1
cd "d:\ai chat-bot"
python app.py

# Terminal 2 (new window)
ngrok http 5000
```

**Copy the URL and share it!** 🌍

---

## 📝 For Your Demo

1. **Start ngrok 5 minutes before demo**
2. **Copy public URL**
3. **Test it once** on your phone
4. **Share with evaluator**
5. **Keep both terminals running**
6. **Watch ngrok dashboard** (http://127.0.0.1:4040)

**Good luck with your presentation!** 🎊
