# "https://portfolio-website-khaki-iota-54.vercel.app"
# backend/main.py
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import traceback
from dotenv import load_dotenv
from resend import Resend

load_dotenv()

app = FastAPI()

# Update this list with your actual frontend URL(s)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://portfolio-website-khaki-iota-54.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Resend client (reads API key from env)
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("WARNING: RESEND_API_KEY not set. Email will fail until you set it.")
resend_client = Resend(API_KEY) if API_KEY else None

# Replace these with the 'from' address you want emails to appear from.
# Resend requires the sending identity. Use a verified address or a resend-provided onboarding one.
SMTP_SENDER_DISPLAY = "harshaanchakkal@gmail.com"  # change to your verified sender

@app.post("/contact")
async def contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    # debug logs (appear in Render logs)
    print("CONTACT REQUEST:", name, email)
    print("API KEY set?:", bool(os.getenv("API_KEY")))

    if resend_client is None:
        return JSONResponse(content={"error": "Email service not configured"}, status_code=500)

    subject = f"New message from {name}"
    html = f"""
      <p><strong>From:</strong> {name} &lt;{email}&gt;</p>
      <p><strong>Message:</strong></p>
      <p>{message.replace('<', '&lt;').replace('>', '&gt;').replace('\n','<br/>')}</p>
    """

    try:
        resp = resend_client.emails.send(
            {
                "from": SMTP_SENDER_DISPLAY,
                "to": [os.getenv("RECEIVER_EMAIL")],
                "subject": subject,
                "html": html,
                # set reply-to so you can reply directly to the user
                "reply_to": email
            }
        )
        print("Resend response:", resp)
        return JSONResponse(content={"message": "Email sent successfully"})
    except Exception as e:
        print("RESEND ERROR:")
        traceback.print_exc()
        return JSONResponse(content={"error": str(e)}, status_code=500)
