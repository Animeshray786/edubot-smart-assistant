# 🚀 Quick Start - Make EduBot Live NOW!

## ⚡ Fastest Method: Local Network (5 Minutes)

### Your bot is **already configured** for network access!

### **Step 1: Start the Server**

```powershell
cd "d:\ai chat-bot"
python app.py
```

### **Step 2: Get Your URLs**

The app will show:
```
╔═══════════════════════════════════════════════════════╗
║          EduBot - Smart Student Assistant             ║
╠═══════════════════════════════════════════════════════╣
║  Local Access:    http://localhost:5000               ║
║  Network Access:  http://192.168.X.X:5000             ║
╠═══════════════════════════════════════════════════════╣
║  Share the Network URL with anyone on the same WiFi   ║
║  to test your chatbot!                                ║
╚═══════════════════════════════════════════════════════╝
```

### **Step 3: Share & Test**

✅ **On your computer**: Open `http://localhost:5000`

✅ **On other devices** (same WiFi): 
- Open phone/tablet browser
- Go to the **Network Access** URL shown
- Test the chatbot!

### **Step 4: Allow Firewall (If Needed)**

If others can't connect, run as **Administrator**:

```powershell
# Allow Python through firewall
netsh advfirewall firewall add rule name="EduBot Flask" dir=in action=allow protocol=TCP localport=5000
```

---

## 🌍 For Public Internet Access

Choose one:

### **Option A: Ngrok (10 minutes)**
See `NGROK_SETUP.md` for detailed instructions

### **Option B: Render.com Cloud (30 minutes)**
See `DEPLOYMENT.md` for step-by-step guide

---

## 🎯 Which Method to Use?

| Scenario | Method | Time |
|----------|--------|------|
| **Demo to classmates in college** | Local Network | 5 min |
| **Show to evaluators remotely** | Ngrok | 10 min |
| **Final submission / Portfolio** | Render.com | 30 min |
| **Testing on your phone** | Local Network | 5 min |

---

## ✅ Quick Test Checklist

After going live:
- [ ] Open the URL
- [ ] Chat works (try "hello")
- [ ] Quick actions work (click buttons)
- [ ] Guest mode works
- [ ] Can create account
- [ ] Login works
- [ ] Voice button visible

---

## 🆘 Troubleshooting

**Others can't access on network?**
→ Check Windows Firewall (run command above)

**Server won't start?**
→ Make sure no other app is using port 5000

**Want to change port?**
→ Edit `app.py`, change `port=5000` to another number

---

**Ready to go live? Run `python app.py` now!** 🚀
