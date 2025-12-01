
import os
import resend
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Initialize Resend
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
resend.api_key = RESEND_API_KEY

# FastAPI app
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
class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.get("/")
def root():
    return {"status": "Backend is running"}

@app.post("/contact")
async def contact(form: ContactForm):
    print("CONTACT REQUEST:", form.name, form.email)
    print("RESEND_API_KEY set?:", bool(RESEND_API_KEY))

    if not RESEND_API_KEY:
        raise HTTPException(status_code=500, detail="Resend API key not configured")

    # Validate sender email domain (.com or .edu)
    if not (form.email.endswith(".com") or form.email.endswith(".edu")):
        raise HTTPException(status_code=400, detail="Email domain must be .com or .edu")

    try:
        # Send email using Resend
        response = resend.Emails.send(
            {
                "from": "Portfolio Contact <contact@ku.edu>",
                "to": ["h895c959@ku.edu"],  # your receiving email
                "subject": f"New Contact Request - {form.name}",
                "html": f"""
                    <h2>New Contact Form Submission</h2>
                    <p><strong>Name:</strong> {form.name}</p>
                    <p><strong>Email:</strong> {form.email}</p>
                    <p><strong>Message:</strong></p>
                    <p>{form.message}</p>
                """,
            }
        )

        print("EMAIL SENT:", response)
        return {"status": "success", "message": "Email sent"}

    except Exception as e:
        print("RESEND ERROR:", e)
        raise HTTPException(status_code=500, detail="Failed to send email")