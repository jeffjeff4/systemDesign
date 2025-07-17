import requests
import sys

payment_id = sys.argv[1] if len(sys.argv) > 1 else None
if not payment_id:
    print("Usage: python simulate_gateway.py <payment_id>")
    exit()

res = requests.post("http://localhost:5000/webhook/payment_callback", json={
    "payment_id": payment_id,
    "success": True
})

print("Webhook sent:", res.status_code)
try:
    print("Response JSON:", res.json())
except Exception as e:
    print("Failed to decode JSON:", e)
    print("Raw response text:", res.text)
