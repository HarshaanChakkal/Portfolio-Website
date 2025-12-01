from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import traceback
from dotenv import load_dotenv
from resend import Resend

load_dotenv()

app = FastAPI()

# Update this list with your frontend URL(s)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://portfolio-website-khaki-iota-54.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Resend client
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("WARNING: RESEND_API_KEY not set. Emails will fail until you set it.")
resend_client = Resend(API_KEY) if API_KEY else None

# Use a verified email (for testing, must match your Resend sandbox email)
SMTP_SENDER_DISPLAY = os.getenv("SMTP_SENDER")  # e.g., h895c959@ku.edu

@app.post("/contact")
async def contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    print("CONTACT REQUEST:", name, email)
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
                "to": [os.getenv("RECEIVER_EMAIL")],  # Your email for testing
                "subject": subject,
                "html": html,
                "reply_to": email
            }
        )
        print("Resend response:", resp)
        return JSONResponse(content={"message": "Email sent successfully"})

    except Exception as e:
        # Capture the exact Resend error (like unverified email/domain)
        error_msg = str(e)
        print("RESEND ERROR:", error_msg)
        if "only send testing emails" in error_msg:
            return JSONResponse(
                content={
                    "error": "Cannot send to this recipient in testing mode. "
                             "Use your verified email or verify a domain at resend.com."
                },
                status_code=400
            )
        return JSONResponse(content={"error": error_msg}, status_code=500)
