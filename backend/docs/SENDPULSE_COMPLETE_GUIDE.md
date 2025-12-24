# 📧 SendPulse Email Setup - Complete Guide

## ✅ Why SendPulse is Better

| Feature | SendPulse | Brevo |
|---------|-----------|-------|
| **Free Emails/Month** | 12,000 | 9,000 (300/day) |
| **Setup Complexity** | Simple SMTP | API Key issues |
| **Reliability** | Excellent | Good |
| **Configuration** | 5 minutes | 10+ minutes |

## 🚀 Complete Setup (5 Minutes)

### Step 1: Create SendPulse Account

1. Go to **[https://sendpulse.com/register](https://sendpulse.com/register)**
2. Sign up with your email
3. Verify your email address
4. Log in to dashboard

### Step 2: Get SMTP Credentials

1. In SendPulse dashboard, click your profile (top right)
2. Go to **Settings** → **SMTP**
3. Click **"Generate SMTP password"** button
4. **IMPORTANT:** Copy and save these credentials:
   ```
   SMTP Server: smtp-pulse.com
   Port: 587 (TLS) or 465 (SSL)
   Username: [Your SendPulse email]
   Password: [Generated password - save this!]
   ```

### Step 3: Verify Sender Email (Important!)

1. In SendPulse, go to **Settings** → **Sender Addresses**
2. Click **"Add sender address"**
3. Enter your email (e.g., `shrishailkone.21@gmail.com`)
4. Click the verification link sent to your email
5. ✅ Email verified!

### Step 4: Update Your .env File

**Option A: Copy the template (Easiest)**
```powershell
Copy-Item .env.sendpulse .env -Force
```

**Option B: Manual edit**

Open your `.env` file and replace the email section with:

```env
# Email Configuration (SendPulse SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-pulse.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=your-sendpulse-email@example.com
EMAIL_HOST_PASSWORD=your-generated-smtp-password
DEFAULT_FROM_EMAIL=your-sendpulse-email@example.com
```

**Replace:**
- `your-sendpulse-email@example.com` → Your SendPulse account email
- `your-generated-smtp-password` → The password from Step 2

### Step 5: Test Email!

```bash
python test_email.py
```

Enter your test email and check your inbox! 🎉

## 📋 Example .env Configuration

Here's a complete example:

```env
# Email Configuration (SendPulse SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-pulse.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
EMAIL_HOST_USER=shrishailkone.21@gmail.com
EMAIL_HOST_PASSWORD=Abc123XyzGeneratedPassword
DEFAULT_FROM_EMAIL=shrishailkone.21@gmail.com
```

## 🔧 Alternative: Use Gmail (Quick Test)

If you want to test with Gmail first:

1. **Enable 2-Step Verification** in your Google Account
2. **Generate App Password**:
   - Go to [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Select "Mail" and "Other (Custom name)"
   - Copy the 16-character password
3. **Update .env**:
   ```env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-gmail@gmail.com
   EMAIL_HOST_PASSWORD=your-16-char-app-password
   DEFAULT_FROM_EMAIL=your-gmail@gmail.com
   ```

## ✅ Verification Checklist

- [ ] SendPulse account created
- [ ] SMTP password generated
- [ ] Sender email verified in SendPulse
- [ ] `.env` file updated with credentials
- [ ] `python test_email.py` runs successfully
- [ ] Test email received in inbox

## 🐛 Troubleshooting

### "Authentication failed"
- Check EMAIL_HOST_USER is your SendPulse email
- Verify EMAIL_HOST_PASSWORD is the SMTP password (not your account password)
- Make sure you generated the SMTP password in SendPulse

### "Sender not verified"
- Go to SendPulse → Settings → Sender Addresses
- Add and verify your email address

### "Connection refused"
- Check EMAIL_PORT is 587
- Verify EMAIL_USE_TLS is True
- Make sure EMAIL_HOST is smtp-pulse.com

## 📊 SendPulse Free Plan Limits

- ✅ **12,000 emails/month**
- ✅ **500 subscribers**
- ✅ **Unlimited sender addresses**
- ✅ **Email templates**
- ✅ **Real-time statistics**
- ✅ **No credit card required**

## 🎯 What Changed in Your Backend

I've updated `settings.py` to use **standard SMTP** instead of Brevo's Anymail:

**Before:**
```python
EMAIL_BACKEND = 'anymail.backends.brevo.EmailBackend'
```

**After:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp-pulse.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
# ... more SMTP settings
```

This means you can now use **any SMTP provider** (SendPulse, Gmail, Mailgun, etc.) just by changing the .env file!

## 🚀 Next Steps

1. ✅ Set up SendPulse account (5 min)
2. ✅ Update .env with credentials
3. ✅ Test with `python test_email.py`
4. 🔄 Integrate with frontend signup/login
5. 🔄 Monitor email delivery in SendPulse dashboard

---

**SendPulse is much simpler than Brevo and has a better free tier!** 🎉
