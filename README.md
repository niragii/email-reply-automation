# email-reply-automation
Automates Gmail replies using AI with secure credential handling and policy-based context retrieval,  using Google Gemini, LangChain, and RAG for professional, context-aware replies.

## 🚀 Features

- Automated replies to unread Gmail messages  
- AI-generated responses using Google Gemini  
- Policy-aware replies using vector-based document retrieval (RAG)  
- Secure handling of API keys and OAuth credentials  
- Filters promotional and no-reply emails  
- Clean, modular Python codebase  

---

## 🧠 How It Works

1. **Document Embedding**
   - Internal policy documents are converted into embeddings
   - Stored in a Chroma vector database for semantic search

2. **Email Processing**
   - Fetches unread Gmail messages using Gmail API
   - Extracts email content and sender details

3. **Context Retrieval (RAG)**
   - Relevant policy context is retrieved based on email content
   - Context is injected into the AI prompt

4. **AI Reply Generation**
   - Google Gemini generates a professional, human-like reply
   - Replies are sent automatically and emails are marked as read

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
 bash
git clone https://github.com/your-username/email-reply-automation.git
cd email-reply-automation 
### 2. Create Virtual Environment
bash
Copy code
python3 -m venv venv
source venv/bin/activate
### 3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
### 4. Configure Environment Variables
Create a .env file using the example:

bash
Copy code
cp .env.example .env
Add your Gemini API key:

env
Copy code
GOOGLE_API_KEY=your_api_key_here
## 📧 Gmail API Setup
Enable Gmail API in Google Cloud Console

Create OAuth credentials

Download credentials.json

Place it in the project root (ignored by git)

## 📄 Embed Policy Document
Place your policy document in the project root (ignored by git) and run:

bash
Copy code
python database.py
This creates a vector database used for context retrieval.

## ▶️ Run Email Automation
bash
Copy code
python emailagent.py
The script will:

Read unread emails

Generate AI replies

Send responses automatically

Mark emails as read

