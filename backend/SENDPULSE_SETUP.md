# SendPulse Email Setup Guide

## Why SendPulse?

- ✅ **Free tier: 12,000 emails/month** (vs Brevo's 300/day)
- ✅ **Easy SMTP setup** - No API key complications
- ✅ **Reliable delivery**
- ✅ **Simple configuration**

## 🚀 Quick Setup (5 minutes)

### Step 1: Create SendPulse Account

1. Go to **[https://sendpulse.com](https://sendpulse.com)**
2. Click **"Sign Up Free"**
3. Complete registration
4. Verify your email

### Step 2: Get SMTP Credentials

1. Log in to SendPulse dashboard
2. Go to **Settings** → **SMTP**
3. Click **"Generate SMTP password"**
4. Copy the credentials:
   - **SMTP Server:** `smtp-pulse.com`
   - **Port:** `465` (SSL) or `587` (TLS)
   - **Username:** Your SendPulse email
   - **Password:** Generated SMTP password

### Step 3: Update Django Settings

I'll create a new settings configuration for you.

### Step 4: Update .env File

Add these to your `.env`:

```env
# Email Configuration (SendPulse)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp-pulse.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-sendpulse-email@example.com
EMAIL_HOST_PASSWORD=your-generated-smtp-password
DEFAULT_FROM_EMAIL=your-sendpulse-email@example.com
```

## 📋 Complete Setup Instructions

I'll create the configuration files for you now...
