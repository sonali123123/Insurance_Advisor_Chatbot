# utils.py

from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from gtts import gTTS
import whisper
import os

def load_multiple_pdfs(file_paths):
    all_docs = []
    for file_path in file_paths:
        loader = PyMuPDFLoader(file_path=file_path)
        docs = loader.load()
        all_docs.extend(docs)
    return all_docs

def split_docs(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=20,
        length_function=len
    )
    return text_splitter.split_documents(documents=documents)

def generate_audio_from_response(response, lang):
    tts = gTTS(text=response, lang=lang)
    audio_path = os.path.join(RESPONSE_AUDIO_DIR, f"response_{lang}.mp3")
    tts.save(audio_path)
    return audio_path, response

def transcribe_audio(audio_path):
    whisper_model = whisper.load_model(WHISPER_MODEL_NAME)
    result = whisper_model.transcribe(audio_path, language='en')
    return result.get("text", "").strip()