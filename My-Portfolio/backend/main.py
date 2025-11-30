from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import smtplib
import os
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://portfolio-website-khaki-iota-54.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the contact endpoint
@app.post('/contact')
async def contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    # configure the email parameters
    sender_email = os.getenv('SMTP_SENDER')
    sender_password = os.getenv('SMTP_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL')

    # declare the email content
    subject = f'New Message from {name}'
    body = f'From: {name} <{email}>\n\n{message}'
    msg = f'Subject: {subject}\n\n{body}'

    try:
        # send the email and return a success response
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, receiver_email, msg)
        return JSONResponse(content={'message': 'Email sent successfully'})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    