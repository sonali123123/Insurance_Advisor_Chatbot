# chatbot.py

from fastapi import FastAPI, File, UploadFile, BackgroundTasks, Body, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from langchain_ollama import ChatOllama
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
from config import PDF_FILES, UPLOAD_AUDIO_DIR, RESPONSE_AUDIO_DIR, SYSTEM_PROMPT, WHISPER_MODEL_NAME, EMBEDDING_MODEL_NAME, OLLAMA_MODEL_NAME,CONTEXTUALIZE_SYSTEM_PROMPT 
from utils import load_multiple_pdfs, split_docs, generate_audio_from_response, transcribe_audio
import os

app = FastAPI()

# Load and split documents
docs = load_multiple_pdfs(file_paths=PDF_FILES)
splits = split_docs(documents=docs)

# Initialize models
llm = ChatOllama(model=OLLAMA_MODEL_NAME, temperature=0)
embedding_function = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)
vectorstore = Chroma.from_documents(
    collection_name='my_collection',
    documents=splits,
    embedding=embedding_function,
    persist_directory="./chroma_db"
)
retriever = vectorstore.as_retriever(k=3)

# Chat history store
store = {}

# Chatbot chains
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", CONTEXTUALIZE_SYSTEM_PROMPT ),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

# FastAPI endpoints
@app.post("/whisper")
async def whisper_endpoint(language: str, file: UploadFile = File(...)):
    try:
        temp_filename = f"{file.filename}"
        file_path = os.path.join(UPLOAD_AUDIO_DIR, temp_filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        transcription_text = transcribe_audio(file_path)
        os.remove(file_path)
        return JSONResponse(content={"transcription": transcription_text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to transcribe audio: {e}")

@app.post("/ask")
async def ask(lang: str, query: dict = Body(...), background_tasks: BackgroundTasks = None):
    try:
        query_text = query.get("query", "")
        if not query_text:
            return JSONResponse(status_code=400, content={"error": "Query text is missing"})
        
        session_id = "default_session"
        response = conversational_rag_chain.invoke(
            {"input": query_text},
            config={"configurable": {"session_id": session_id}}
        )
        response_audio_path, translated_response = generate_audio_from_response(response["answer"], lang)
        audio_url = f"http://10.7.0.28:5505/static/{os.path.basename(response_audio_path)}"
        return JSONResponse(content={"response": translated_response, "audio_url": audio_url})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

app.mount("/static", StaticFiles(directory="audio_files"), name="static")