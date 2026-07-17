import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "kanthivardhan264@gmail.com"
SMTP_PASSWORD = "kufj litc xpnj fpnd"
SMTP_FROM_EMAIL = "kanthivardhan264@gmail.com"

msg = MIMEMultipart()
msg["From"] = f"CODEXA Coding Club <{SMTP_FROM_EMAIL}>"
msg["To"] = "codexa@sitam.co.in"
msg["Subject"] = "Test SMTP OTP Delivery"
msg.attach(MIMEText("This is a test to verify your Gmail SMTP credentials. Your OTP is: 123456", "plain"))

try:
    print("Connecting to SMTP server...")
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        print("Logging in...")
        server.login(SMTP_USER, SMTP_PASSWORD)
        print("Sending mail...")
        server.sendmail(SMTP_FROM_EMAIL, "codexa@sitam.co.in", msg.as_string())
    print("SUCCESS: SMTP connection and mail delivery succeeded!")
except Exception as e:
    print(f"FAILED to send email: {e}")
