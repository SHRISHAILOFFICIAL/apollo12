import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

key_id = os.getenv('RAZORPAY_KEY_ID', '')
key_secret = os.getenv('RAZORPAY_KEY_SECRET', '')

print("=== Razorpay Keys Diagnostic ===")
print(f"Key ID length: {len(key_id)}")
print(f"Key ID starts with: {key_id[:10] if key_id else 'EMPTY'}")
print(f"Key Secret length: {len(key_secret)}")

if key_id:
    if not key_id.startswith('rzp_'):
        print("WARNING: Key ID should start with rzp_test_ or rzp_live_")
    else:
        print("Key ID format looks correct")
else:
    print("ERROR: Key ID is EMPTY!")

if key_secret:
    print("Key Secret is set")
else:
    print("ERROR: Key Secret is EMPTY!")
