# Environment Variables Documentation

Complete reference for all environment variables used in the DCET Platform.

## Django Backend (.env)

### Core Django Settings

#### `SECRET_KEY` (Required)
- **Description**: Django secret key for cryptographic signing
- **Security**: CRITICAL - Must be unique and kept secret
- **Generate**: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- **Example**: `SECRET_KEY=django-insecure-abc123xyz...`

#### `DEBUG` (Required)
- **Description**: Enable/disable debug mode
- **Production**: Must be `False`
- **Development**: Can be `True`
- **Default**: `False`
- **Example**: `DEBUG=False`

#### `ALLOWED_HOSTS` (Required)
- **Description**: Comma-separated list of allowed host/domain names
- **Production**: Your server IP or domain
- **Format**: Comma-separated, no spaces
- **Example**: `ALLOWED_HOSTS=192.168.1.18,localhost,127.0.0.1`

---

### Database Configuration

#### `DB_ENGINE` (Optional)
- **Description**: Django database backend
- **Default**: `django.db.backends.mysql`
- **Example**: `DB_ENGINE=django.db.backends.mysql`

#### `DB_NAME` (Required)
- **Description**: Database name
- **Default**: `dcet_platform`
- **Example**: `DB_NAME=dcet_platform`

#### `DB_USER` (Required)
- **Description**: Database username
- **Default**: `root`
- **Production**: Use dedicated user
- **Example**: `DB_USER=dcet_user`

#### `DB_PASSWORD` (Required)
- **Description**: Database password
- **Security**: Use strong password in production
- **Example**: `DB_PASSWORD=your_strong_password_here`

#### `DB_HOST` (Optional)
- **Description**: Database server host
- **Default**: `localhost`
- **Example**: `DB_HOST=localhost`

#### `DB_PORT` (Optional)
- **Description**: Database server port
- **Default**: `3306`
- **Example**: `DB_PORT=3306`

---

### Redis Cache Configuration

#### `REDIS_URL` (Optional)
- **Description**: Redis connection URL
- **Default**: `redis://127.0.0.1:6379/1`
- **Format**: `redis://host:port/db`
- **Example**: `REDIS_URL=redis://127.0.0.1:6379/1`

---

### CORS Configuration

#### `CORS_ALLOWED_ORIGINS` (Required)
- **Description**: Comma-separated list of allowed origins for CORS
- **Format**: Full URLs with protocol, comma-separated
- **Example**: `CORS_ALLOWED_ORIGINS=http://192.168.1.18,http://localhost:3000`

---

### Email Configuration (Brevo)

#### `BREVO_API_KEY` (Required for email)
- **Description**: Brevo (formerly Sendinblue) API key
- **Get Key**: https://app.brevo.com/settings/keys/api
- **Format**: Starts with `xkeysib-` (NOT `xsmtpsib-`)
- **Example**: `BREVO_API_KEY=xkeysib-abc123...`

#### `DEFAULT_FROM_EMAIL` (Optional)
- **Description**: Default sender email address
- **Default**: `noreply@apollo11.com`
- **Example**: `DEFAULT_FROM_EMAIL=noreply@yourdomain.com`

---

### Payment Gateway (Razorpay)

#### `RAZORPAY_KEY_ID` (Required for payments)
- **Description**: Razorpay API key ID
- **Get Key**: https://dashboard.razorpay.com/app/keys
- **Format**: Starts with `rzp_test_` or `rzp_live_`
- **Example**: `RAZORPAY_KEY_ID=rzp_test_abc123...`

#### `RAZORPAY_KEY_SECRET` (Required for payments)
- **Description**: Razorpay API key secret
- **Security**: CRITICAL - Keep secret
- **Example**: `RAZORPAY_KEY_SECRET=your_secret_here`

#### `RAZORPAY_WEBHOOK_SECRET` (Required for webhooks)
- **Description**: Razorpay webhook secret for signature verification
- **Get Secret**: Razorpay Dashboard > Webhooks
- **Example**: `RAZORPAY_WEBHOOK_SECRET=your_webhook_secret`

---

### Deployment Settings

#### `STATIC_ROOT` (Optional)
- **Description**: Absolute path where static files will be collected
- **Default**: `{BASE_DIR}/staticfiles`
- **Production**: `/var/www/dcet-platform/backend/staticfiles`
- **Example**: `STATIC_ROOT=/var/www/dcet-platform/backend/staticfiles`

#### `MEDIA_ROOT` (Optional)
- **Description**: Absolute path where media files will be stored
- **Default**: `{BASE_DIR}/media`
- **Production**: `/var/www/dcet-platform/backend/media`
- **Example**: `MEDIA_ROOT=/var/www/dcet-platform/backend/media`

---

## Frontend (.env.production)

### API Configuration

#### `NEXT_PUBLIC_API_URL` (Required)
- **Description**: Backend API base URL
- **Format**: Full URL with protocol, ending with `/api`
- **Development**: `http://localhost:8000/api`
- **Production**: `http://192.168.1.18/api` or `https://yourdomain.com/api`
- **Example**: `NEXT_PUBLIC_API_URL=http://192.168.1.18/api`

#### `NEXT_PUBLIC_DEBUG` (Optional)
- **Description**: Enable debug mode in frontend
- **Production**: `false`
- **Development**: `true`
- **Default**: `false`
- **Example**: `NEXT_PUBLIC_DEBUG=false`

---

## Security Best Practices

### Critical Variables (Never Commit)
- `SECRET_KEY`
- `DB_PASSWORD`
- `BREVO_API_KEY`
- `RAZORPAY_KEY_SECRET`
- `RAZORPAY_WEBHOOK_SECRET`

### Production Checklist
- [ ] Generate new `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Use strong `DB_PASSWORD`
- [ ] Update `ALLOWED_HOSTS` with actual domain/IP
- [ ] Update `CORS_ALLOWED_ORIGINS` with actual frontend URL
- [ ] Use production Razorpay keys (not test keys)
- [ ] Verify `.env` is in `.gitignore`

---

## Example Production .env File

```bash
# Django Core
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=192.168.1.18,yourdomain.com

# Database
DB_NAME=dcet_platform
DB_USER=dcet_user
DB_PASSWORD=strong_password_here
DB_HOST=localhost
DB_PORT=3306

# Redis
REDIS_URL=redis://127.0.0.1:6379/1

# CORS
CORS_ALLOWED_ORIGINS=http://192.168.1.18,https://yourdomain.com

# Email
BREVO_API_KEY=xkeysib-your-actual-key
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Payments
RAZORPAY_KEY_ID=rzp_live_your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret

# Deployment
STATIC_ROOT=/var/www/dcet-platform/backend/staticfiles
MEDIA_ROOT=/var/www/dcet-platform/backend/media
```
