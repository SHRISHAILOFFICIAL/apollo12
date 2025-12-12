# Email Setup Guide - Brevo Configuration

Your backend already has email functionality built-in! You just need to configure it with your Brevo API key.

## 📧 What Email Features Are Available?

Your platform uses **Brevo** (formerly Sendinblue) to send:

1. **Signup OTP** - Email verification during user registration
2. **Password Reset OTP** - Secure password recovery via email

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Brevo Account

1. Go to **[https://www.brevo.com](https://www.brevo.com)**
2. Click **"Sign up free"**
3. Complete registration (Free plan includes **300 emails/day**)
4. Verify your email address

### Step 2: Get Your API Key

1. Log in to Brevo dashboard
2. Go to **Settings** (top right) → **SMTP & API**
3. Click on **API Keys** tab
4. Click **"Generate a new API key"**
5. Give it a name (e.g., "Apollo11 Backend")
6. **Copy the API key** (you won't see it again!)

### Step 3: Configure Your Backend

**Option A: Using .env file (Recommended)**

1. Open `backend/.env` file (or create from `.env.example`)
2. Add your Brevo API key:

```env
# Email Configuration (Brevo)
BREVO_API_KEY=xkeysib-your-actual-api-key-here
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

**Option B: Direct in settings.py (Not recommended for production)**

Edit `backend/config/settings.py`:

```python
ANYMAIL = {
    'BREVO_API_KEY': 'xkeysib-your-actual-api-key-here',
}

DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

### Step 4: Verify Sender Email (Important!)

Brevo requires you to verify the sender email address:

1. In Brevo dashboard, go to **Senders** → **Senders & IP**
2. Click **"Add a sender"**
3. Enter your email (e.g., `noreply@yourdomain.com`)
4. Verify the email by clicking the link sent to you

> **Note:** For testing, you can use your personal email as the sender.

### Step 5: Test Email Sending

Run this test script:

```bash
cd backend
python manage.py shell
```

Then in the Python shell:

```python
from users.email_service import send_otp_email

# Test sending OTP email
result = send_otp_email('your-email@example.com', '123456', purpose='signup')
print(f"Email sent: {result}")
```

Check your inbox! You should receive a beautifully formatted OTP email.

## 📋 Email Configuration Reference

### Current Settings (in `config/settings.py`)

```python
EMAIL_BACKEND = 'anymail.backends.brevo.EmailBackend'

ANYMAIL = {
    'BREVO_API_KEY': os.getenv('BREVO_API_KEY', ''),
}

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@apollo11.com')
```

### Email Templates

Your platform has two email templates (in `users/email_service.py`):

1. **Signup Verification Email**
   - Subject: "Verify Your Email - Apollo11 DCET Platform"
   - Contains: 6-digit OTP code
   - Expires: 10 minutes

2. **Password Reset Email**
   - Subject: "Password Reset Code - Apollo11 DCET Platform"
   - Contains: 6-digit OTP code
   - Expires: 10 minutes

## 🔧 API Endpoints Using Email

### 1. Send Signup OTP

```bash
POST /api/users/send-signup-otp/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "OTP sent successfully",
  "email": "user@example.com"
}
```

### 2. Verify Signup OTP

```bash
POST /api/users/verify-signup-otp/
Content-Type: application/json

{
  "email": "user@example.com",
  "otp": "123456"
}
```

### 3. Send Password Reset OTP

```bash
POST /api/users/send-password-reset-otp/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

### 4. Verify Password Reset OTP

```bash
POST /api/users/verify-password-reset-otp/
Content-Type: application/json

{
  "email": "user@example.com",
  "otp": "123456"
}
```

### 5. Reset Password

```bash
POST /api/users/reset-password/
Content-Type: application/json

{
  "email": "user@example.com",
  "otp": "123456",
  "new_password": "newpassword123"
}
```

## 🎨 Email Design

Your emails are professionally designed with:
- ✅ Responsive HTML layout
- ✅ Branded colors (Green for signup, Orange for password reset)
- ✅ Large, easy-to-read OTP codes
- ✅ Plain text fallback for email clients that don't support HTML
- ✅ Clear expiration warnings (10 minutes)

## 🐛 Troubleshooting

### "Failed to send OTP. Please try again."

**Possible causes:**

1. **Invalid API Key**
   - Check if `BREVO_API_KEY` is set correctly in `.env`
   - Verify the API key is active in Brevo dashboard

2. **Sender Email Not Verified**
   - Go to Brevo → Senders → Verify your sender email
   - Use the same email as `DEFAULT_FROM_EMAIL`

3. **Daily Limit Reached**
   - Free plan: 300 emails/day
   - Check usage in Brevo dashboard

4. **Django Anymail Not Installed**
   ```bash
   pip install django-anymail[brevo]
   ```

### Check Email Logs

Enable debug logging to see detailed error messages:

```python
# In settings.py, add:
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'anymail': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

### Test Email Configuration

Create a test script `test_email.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from users.email_service import send_otp_email

# Test email
email = input("Enter your email to test: ")
result = send_otp_email(email, '123456', purpose='signup')

if result:
    print("✅ Email sent successfully! Check your inbox.")
else:
    print("❌ Failed to send email. Check your configuration.")
```

Run it:
```bash
python test_email.py
```

## 📊 Brevo Free Plan Limits

- **300 emails/day** (perfect for testing and small deployments)
- Unlimited contacts
- Email templates
- Real-time statistics
- No credit card required

For production with more users, consider upgrading to a paid plan.

## 🔐 Security Best Practices

1. **Never commit API keys to Git**
   - Always use `.env` file
   - `.env` is in `.gitignore`

2. **Use environment variables**
   ```python
   BREVO_API_KEY = os.getenv('BREVO_API_KEY', '')
   ```

3. **Rotate API keys periodically**
   - Generate new keys every 3-6 months
   - Revoke old keys in Brevo dashboard

4. **Monitor email usage**
   - Check Brevo dashboard for suspicious activity
   - Set up alerts for high usage

## 📈 Production Deployment

For production, update your `.env`:

```env
# Production Email Settings
BREVO_API_KEY=xkeysib-your-production-api-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
DEBUG=False
```

And verify your domain in Brevo for better deliverability:
1. Go to Brevo → Senders → Domains
2. Add your domain
3. Add DNS records (SPF, DKIM)
4. Verify domain

## ✅ Verification Checklist

- [ ] Brevo account created
- [ ] API key generated
- [ ] API key added to `.env` file
- [ ] Sender email verified in Brevo
- [ ] Test email sent successfully
- [ ] OTP emails working for signup
- [ ] OTP emails working for password reset
- [ ] Email templates look good on mobile and desktop

## 🎯 Next Steps

1. ✅ Configure Brevo API key
2. ✅ Test email sending
3. 🔄 Integrate with frontend signup/login flows
4. 🔄 Monitor email delivery rates
5. 🔄 Customize email templates (optional)

---

**Setup Time:** ~5 minutes  
**Cost:** Free (300 emails/day)  
**Status:** Ready to use! 📧
