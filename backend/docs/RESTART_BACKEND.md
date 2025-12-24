# ⚠️ IMPORTANT: Restart Backend Server

## Why You're Getting 401 Error

The backend server is still using the **old API key** from when it started.

Django **does NOT auto-reload** environment variables from `.env` file!

## ✅ Solution: Restart Backend

**Stop the current backend server:**
- Press `Ctrl+C` in the terminal running `python manage.py runserver`

**Start it again:**
```bash
cd backend
python manage.py runserver
```

This will load the new Brevo API key from your updated `.env` file.

## 🧪 Test After Restart

1. Backend restarted with new API key ✅
2. Go to http://localhost:3000/auth/signup
3. Enter email
4. Click "Continue"
5. ✅ Should work now!

---

**Remember:** Whenever you change `.env` file, you must restart the server!
