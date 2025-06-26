import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from langchain_openai import OpenAI
# from openai import OpenAI
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from chromadb import Client as ChromaClient
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ChromaDB setup
chroma_client = ChromaClient()
collection = chroma_client.get_or_create_collection("chat_history")

# print("API KEY:", os.getenv("OPENAI_API_KEY"))

# LangChain setup
llm = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

HARDCODED_USER = "admin"
HARDCODED_PASS = "password123"

USERS = {
    "admin": "password123",
    "alice": "alicepass"
}

class ChatRequest(BaseModel):
    user: str
    message: str

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/data")
async def get_data():
    # print("API KEY:", os.getenv("OPENAI_API_KEY"))
    return {"msg": "Hello"}

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # Store user message in ChromaDB with user-specific ID
    user_msg_id = f"{req.user}_user_{len(collection.get(where={"user": req.user})['ids'])}"
    collection.add(
        documents=[req.message],
        metadatas=[{"user": req.user, "role": "user"}],
        ids=[user_msg_id]
    )
    # Get response from LLM
    response = conversation.predict(input=req.message)
    # Store bot response in ChromaDB with user-specific ID
    bot_msg_id = f"{req.user}_bot_{len(collection.get(where={"user": req.user})['ids'])}"
    collection.add(
        documents=[response],
        metadatas=[{"user": req.user, "role": "bot"}],
        ids=[bot_msg_id]
    )
    return {"response": response}

@app.get("/history/{user}")
async def get_history(user: str):
    # Retrieve all messages for the user only
    results = collection.get(where={"user": user})
    history = [
        {"user": meta["user"], "role": meta.get("role", "user"), "message": doc}
        for doc, meta in zip(results["documents"], results["metadatas"])
    ]
    return {"history": history}

@app.get("/chroma/all")
async def get_all_chroma():
    results = collection.get()
    return results

@app.post("/login")
async def login(req: LoginRequest):
    if req.username in USERS and req.password == USERS[req.username]:
        return {"success": True, "username": req.username}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials") 