# 🚀 EduBot Quick Start Guide

## ✅ Server is Already Running!

Your server is **LIVE** at:
- **Local:** http://localhost:5000
- **Network:** http://10.222.58.180:5000

---

## 📖 How to Use

### Method 1: Simple Start (Recommended)
Just run the Python app directly:
```bash
python app.py
```

### Method 2: With Health Check
Use the startup scripts that include automatic health checks:

**Windows (PowerShell):**
```powershell
.\start.ps1
```

**Windows (CMD):**
```cmd
start.bat
```

### Method 3: Manual Health Check
Run health check separately before starting:
```bash
python healthcheck.py
python app.py
```

---

## 🔧 Common Issues & Fixes

### Issue 1: "Configuration warnings"
**These are safe to ignore!** They're just optional features.

To hide warnings completely, add to `.env`:
```env
SHOW_CONFIG_WARNINGS=False
```

### Issue 2: Port 5000 already in use
**Solution:** Another instance is running. Either:
1. Use that running instance (it's working!)
2. Or stop it first: Press `Ctrl+C` in the terminal

### Issue 3: Missing packages
**Solution:** Install required packages:
```bash
pip install -r requirements.txt
```

---

## 📁 What Do All These Files Do?

| File | Purpose |
|------|---------|
| `app.py` | **Main server** - Run this to start! |
| `healthcheck.py` | Pre-flight checks & auto-fixes |
| `start.bat` | Windows startup script (CMD) |
| `start.ps1` | Windows startup script (PowerShell) |
| `.env` | Configuration file (edit this for settings) |
| `requirements.txt` | Python packages needed |

---

## ⚙️ Configuration

All settings are in `.env` file. Key settings:

```env
# Required (already set)
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-key
CSRF_SECRET_KEY=your-csrf-key

# Optional (has defaults)
LOG_LEVEL=INFO
REDIS_ENABLED=False

# Optional (only if using email)
# MAIL_SERVER=smtp.gmail.com
# MAIL_USERNAME=your-email
# MAIL_PASSWORD=your-password
```

---

## 🎯 Features Available

Once server is running, access:

| Feature | URL |
|---------|-----|
| **Main Chat** | http://localhost:5000 |
| **API Docs** | http://localhost:5000/api/docs |
| **Admin Dashboard** | http://localhost:5000/admin |
| **Lecture Notes** | http://localhost:5000/admin/lecture-notes |

---

## 🐛 Debugging

### View Logs
```bash
# Real-time logs
Get-Content logs\edubot.log -Wait

# Error logs only
Get-Content logs\edubot.error.log
```

### Check What's Running
```bash
# Check if server is running
netstat -ano | findstr :5000

# Kill process on port 5000 (if needed)
taskkill /F /PID <process_id>
```

### Reset Everything
```bash
# Clear all caches and sessions
Remove-Item -Recurse -Force flask_session, __pycache__, logs
python app.py
```

---

## 💡 Pro Tips

1. **Always Running?** The server auto-restarts when you edit code files (in DEBUG mode)

2. **Clean Startup:** Use `start.ps1` or `start.bat` - they auto-create missing folders

3. **No Warnings:** Set `SHOW_CONFIG_WARNINGS=False` in `.env`

4. **Network Access:** Share the network URL with others on same WiFi

5. **Production Mode:** Change `FLASK_ENV=production` in `.env` (disables auto-restart)

---

## 📞 Need Help?

1. **Check server is running:** Look for "Running on http://127.0.0.1:5000" message
2. **Check logs:** Open `logs/edubot.log`
3. **Run health check:** `python healthcheck.py`
4. **Restart server:** Press `Ctrl+C` then `python app.py`

---

## ✨ Next Steps

Your server is ready! Now you can:

1. **Open the chat interface:** http://localhost:5000
2. **Explore features:** Try "what can you do" in chat
3. **Access admin panel:** http://localhost:5000/admin (login: admin/admin123)
4. **Read API docs:** http://localhost:5000/api/docs

---

**Happy Chatting! 🎓🤖**
