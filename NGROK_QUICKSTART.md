# 🌐 Quick Ngrok Setup - Get Your EduBot Online in 5 Steps!

## ⚡ Super Quick Start

### **Step 1: Install pyngrok**
```powershell
pip install pyngrok
```

### **Step 2: Get Ngrok Auth Token** (Optional but recommended)
1. Go to: https://dashboard.ngrok.com/signup
2. Sign up (free, takes 30 seconds)
3. Copy your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken

### **Step 3: Add Your Token** (Optional)
Open `start_with_ngrok.py` and replace:
```python
NGROK_AUTH_TOKEN = "YOUR_AUTH_TOKEN_HERE"
```
With:
```python
NGROK_AUTH_TOKEN = "your_actual_token_2abc123def456"
```

### **Step 4: Run It!**
```powershell
python start_with_ngrok.py
```

### **Step 5: Share the URL!**
You'll see a public URL like: `https://abc123.ngrok-free.app`

**Share this with ANYONE worldwide!** 🌍

---

## 🎯 Alternative: Manual Method (Two Terminals)

If you prefer manual control:

### **Terminal 1 - Start Flask:**
```powershell
cd "d:\ai chat-bot"
python app.py
```

### **Terminal 2 - Start Ngrok:**

#### Option A: Using pyngrok Python
```powershell
python -c "from pyngrok import ngrok; print(ngrok.connect(5000))"
```

#### Option B: Using ngrok.exe directly
```powershell
# If ngrok is installed
ngrok http 5000

# Or with full path
C:\ngrok\ngrok.exe http 5000
```

---

## 📊 Monitor Your Traffic

Open in browser: **http://127.0.0.1:4040**

You'll see:
- 📈 Live request/response logs
- 🔍 Request details
- 📊 Traffic statistics
- 🐛 Debug information

Perfect for monitoring during demos!

---

## 🔧 Troubleshooting

### **Error: "pyngrok not installed"**
```powershell
pip install pyngrok
```

### **Error: "authentication failed"**
Get token from: https://dashboard.ngrok.com/get-started/your-authtoken

### **Want to use ngrok.exe directly?**

Download from: https://ngrok.com/download

Then run:
```powershell
# Start Flask first
python app.py

# In another terminal
ngrok http 5000
```

---

## ✅ Success Checklist

After running, you should see:
- ✅ Public URL displayed (https://something.ngrok-free.app)
- ✅ Flask server running
- ✅ Dashboard available at http://127.0.0.1:4040
- ✅ Can access bot from any device worldwide

---

## 🎓 For Your Demo

**Before Demo:**
1. Run `python start_with_ngrok.py`
2. Copy the public URL
3. Test it once on your phone

**During Demo:**
1. Share the public URL
2. Show it working on different devices
3. Monitor dashboard for live traffic

**Pro Tip:** Start ngrok 5 minutes before your presentation!

---

## ⏰ Session Limits (Free Tier)

- ⏱️ 2 hour sessions (auto-reconnects)
- 🔄 URL changes each restart
- 📊 40 connections/minute
- ✅ Unlimited tunnels per day

**Good enough for any demo or presentation!**

---

## 🆘 Need Help?

Check the full guide: **NGROK_SETUP.md**

Or just ask me! 💬
