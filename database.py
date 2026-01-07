import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load API key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set")

#narendra bhai testing mode

# Load the PDF 
doc_path = "policy.pdf"
loader = PyPDFLoader(doc_path)
documents = loader.load()

# Split document
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# Create vector DB
embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

vectordb = Chroma.from_documents(
    chunks,
    embedding,
    persist_directory="policy_db"
)

vectordb.persist()
print("✅ Document embedded and stored successfully.")
