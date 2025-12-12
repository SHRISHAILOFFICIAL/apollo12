# 🔑 Brevo API Key - Correct Setup

## ❌ The Problem

You copied an **SMTP key** (`xsmtpsib-...`) instead of an **API key** (`xkeysib-...`).

**Your current key starts with:** `xsmtpsib-` ❌  
**Should start with:** `xkeysib-` ✅

## ✅ How to Get the CORRECT API Key

### Step 1: Log in to Brevo
Go to: https://app.brevo.com

### Step 2: Navigate to API Keys
1. Click **Settings** (top right corner)
2. Click **SMTP & API** in the left menu
3. Click the **API Keys** tab (NOT SMTP tab!)

### Step 3: Generate New API Key
1. Click **"Generate a new API key"** button
2. Give it a name: `Apollo11 Backend`
3. **IMPORTANT:** Copy the key immediately - it starts with `xkeysib-`
4. Save it somewhere safe

### Step 4: Update Your .env File

Open `backend/.env` and update this line:

```env
# OLD (SMTP key - WRONG)
BREVO_API_KEY=xsmtpsib-dcd7bf69dd00cc7e3d412fc13ae05c626372efd507add157ed3fa16ccdeb826c-XaWLunHHIutaknUs

# NEW (API key - CORRECT)
BREVO_API_KEY=xkeysib-your-new-api-key-here
```

### Step 5: Revert Email Backend to Brevo

Since we switched to SMTP, we need to switch back to Brevo's Anymail backend.

I'll update the settings for you.

### Step 6: Test Email

```bash
python test_email.py
```

---

## 🔍 How to Tell the Difference

| Type | Prefix | Where to Find | Use For |
|------|--------|---------------|---------|
| **API Key** | `xkeysib-` | Settings → SMTP & API → **API Keys** tab | Django Anymail ✅ |
| **SMTP Key** | `xsmtpsib-` | Settings → SMTP & API → **SMTP** tab | Direct SMTP ❌ |

---

## 📋 Quick Checklist

- [ ] Log in to Brevo
- [ ] Go to Settings → SMTP & API → **API Keys** tab
- [ ] Generate new API key (starts with `xkeysib-`)
- [ ] Copy the key
- [ ] Update `backend/.env` with new key
- [ ] I'll update settings.py for you
- [ ] Test with `python test_email.py`

---

**The key difference:** You need the **API key** from the **API Keys tab**, not the SMTP password!
