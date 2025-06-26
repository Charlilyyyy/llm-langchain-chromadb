# LLM LangChain ChromaDB Chatbot

## Backend (Python)

1. Go to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key in `.env`:
   ```env
   OPENAI_API_KEY=your-openai-api-key-here
   ```
4. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

## Frontend (React)

1. Go to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the React app:
   ```bash
   npm start
   ```

The React app will connect to the FastAPI backend at `http://localhost:8000` by default. 