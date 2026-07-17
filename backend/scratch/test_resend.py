import urllib.request
import urllib.error
import json

url = "https://api.resend.com/emails"
headers = {
    "Authorization": "Bearer re_hD2TKxKN_JY9eo6uZ13vC6uvYhBUsfatU",

    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


payload = {
    "from": "CODEXA Coding Club <onboarding@resend.dev>",
    "to": ["codexa@sitam.co.in"],
    "subject": "Test Resend API Key",
    "html": "<p>This is a test of the Resend API key configuration.</p>",
    "text": "This is a test of the Resend API key configuration."
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers=headers,
    method="POST"
)

try:
    print("Sending request to Resend API...")
    with urllib.request.urlopen(req, timeout=15) as response:
        print("Response Code:", response.code)
        print("Response Body:", response.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print("Error Details:", e.read().decode("utf-8"))
except Exception as e:
    print(f"Error: {e}")
