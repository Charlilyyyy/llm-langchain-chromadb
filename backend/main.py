import os
from fastapi import FastAPI, Request
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

class ChatRequest(BaseModel):
    user: str
    message: str

@app.get("/data")
async def get_data():
    # print("API KEY:", os.getenv("OPENAI_API_KEY"))
    return {"msg": "Hello"}

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    # Store user message in ChromaDB
    collection.add(
        documents=[req.message],
        metadatas=[{"user": req.user}],
        ids=[f"{req.user}_{len(collection.get()['ids'])}"]
    )
    # Get response from LLM
    response = conversation.predict(input=req.message)
    # Store bot response in ChromaDB
    collection.add(
        documents=[response],
        metadatas=[{"user": "bot"}],
        ids=[f"bot_{len(collection.get()['ids'])}"]
    )
    return {"response": response}

@app.get("/history/{user}")
async def get_history(user: str):
    # Retrieve all messages for the user
    results = collection.get()
    history = [
        {"user": meta["user"], "message": doc}
        for doc, meta in zip(results["documents"], results["metadatas"])
        if meta["user"] == user or meta["user"] == "bot"
    ]
    return {"history": history}

@app.get("/chroma/all")
async def get_all_chroma():
    results = collection.get()
    return results 