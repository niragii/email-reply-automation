import os
import base64
import re
import google.generativeai as genai
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# ================= CONFIG =================
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
VECTORSTORE_DIR = "policy_db"
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set")

genai.configure(api_key=GEMINI_API_KEY)

retriever = Chroma(
    persist_directory=VECTORSTORE_DIR,
    embedding_function=GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GEMINI_API_KEY
    )
).as_retriever()

# ================= HELPERS =================
def is_no_reply(sender):
    return re.search(r'no[-_]?reply|noreply|donotreply', sender, re.I)

def is_promotional_email(body):
    keywords = [
        "unsubscribe", "promotion", "sale", "discount",
        "newsletter", "webinar", "marketing"
    ]
    body_lower = body.lower()
    return sum(1 for k in keywords if k in body_lower) >= 3

def clean_reply(text):
    return text.strip()

# ================= AI REPLY =================
def generate_reply(body, sender_name="there"):
    if is_promotional_email(body):
        return "NO_REPLY_NEEDED"

    model = genai.GenerativeModel("gemini-1.5-flash")

    context_docs = retriever.invoke(body)
    context_text = "\n\n".join(d.page_content for d in context_docs[:3])

    prompt = f"""
You are an AI email assistant.

Email:
{body}

Relevant company policy context:
{context_text}

Write a professional, polite, human-sounding reply.
"""

    response = model.generate_content(prompt)
    return clean_reply(response.text)

# ================= GMAIL =================
def authenticate():
    if not os.path.exists("credentials.json"):
        raise FileNotFoundError("Missing credentials.json")

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)
