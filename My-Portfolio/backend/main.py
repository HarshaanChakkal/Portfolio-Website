
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
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
if not RESEND_API_KEY:
    print("WARNING: RESEND_API_KEY not set. Email will fail until you set it.")
resend_client = Resend(RESEND_API_KEY) if RESEND_API_KEY else None

SMTP_SENDER_DISPLAY = "Portfolio Contact <onboarding@resend.dev>"
  # change to your verified sender

@app.post("/contact")
async def contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    # debug logs (appear in Render logs)
    print("CONTACT REQUEST:", name, email)
    print("RESEND_API_KEY set?:", bool(RESEND_API_KEY))

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
