# ✅ Brevo Setup - Final Steps

## What I've Done

✅ **Updated `config/settings.py`** to use Brevo Anymail backend:
```python
EMAIL_BACKEND = 'anymail.backends.brevo.EmailBackend'
ANYMAIL = {
    'BREVO_API_KEY': os.getenv('BREVO_API_KEY', ''),
}
```

## What You Need to Do

### 1. Update Your .env File

Open `backend/.env` and update the `BREVO_API_KEY` line with your new key:

```env
# Replace this line:
BREVO_API_KEY=xsmtpsib-old-smtp-key...

# With your new API key (starts with xkeysib-):
BREVO_API_KEY=xkeysib-your-new-api-key-here
```

**IMPORTANT:** 
- The key should start with `xkeysib-` (not `xsmtpsib-`)
- Keep it on ONE line (no line breaks)
- Also update `DEFAULT_FROM_EMAIL` if needed

### 2. Verify Sender Email in Brevo

Make sure your sender email is verified:
1. Go to Brevo Dashboard
2. Settings → Senders
3. Add and verify `shrishailkone.21@gmail.com` (or your email)

### 3. Test Email

```bash
python test_email.py
```

Enter your test email and check your inbox!

---

## ✅ Checklist

- [ ] Got correct API key from Brevo (starts with `xkeysib-`)
- [ ] Updated `BREVO_API_KEY` in `.env` file
- [ ] Verified sender email in Brevo dashboard
- [ ] Tested with `python test_email.py`
- [ ] Received test email successfully

---

## 🔍 Quick Verification

After updating `.env`, verify it's loaded correctly:

```bash
python check_config.py
```

This will show if your API key is being read properly.

---

**Once you update the .env file, run the test and you should be good to go!** 🚀
