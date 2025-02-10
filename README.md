

# Insurance Advisor Chatbot

The **Insurance Advisor Chatbot** is a conversational AI application designed to assist users in selecting the most suitable insurance policies based on their personal, medical, and financial information. The chatbot uses natural language processing (NLP) and retrieval-augmented generation (RAG) to provide personalized recommendations.

---

## Features

- **PDF Document Processing**: Loads and processes insurance policy documents from PDF files.
- **Conversational AI**: Uses a language model (LLM) to generate responses to user queries.
- **Audio Support**: Transcribes user audio inputs and generates audio responses.
- **Multi-language Support**: Translates queries and responses into the user's preferred language.
- **Session Management**: Maintains chat history for each user session.

---

## Prerequisites

Before running the application, ensure you have the following installed:

1. **Docker**: Install Docker from [here](https://docs.docker.com/get-docker/).
2. **Docker Compose** (optional): Install Docker Compose from [here](https://docs.docker.com/compose/install/).

---

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/insurance-advisor-chatbot.git
cd insurance-advisor-chatbot
```

### 2. Build the Docker Image

Build the Docker image for the application:

```bash
docker build -t insurance-advisor-chatbot .
```

### 3. Run the Application

Run the Docker container:

```bash
docker run -p 5505:5505 insurance-advisor-chatbot
```

Alternatively, use Docker Compose:

```bash
docker-compose up -d
```

The application will be accessible at `http://localhost:5505`.

---

## Usage

### Endpoints

1. **Transcribe Audio**:
   - **Endpoint**: `POST /whisper`
   - **Description**: Transcribes an audio file into text.
   - **Parameters**:
     - `language`: The language of the audio file (e.g., `en` for English).
     - `file`: The audio file to transcribe.
   - **Example**:
     ```bash
     curl -X POST -F "file=@audio.mp3" -F "language=en" http://localhost:5505/whisper
     ```

2. **Ask a Question**:
   - **Endpoint**: `POST /ask`
   - **Description**: Generates a response to a user query.
   - **Parameters**:
     - `lang`: The language for the response (e.g., `en` for English).
     - `query`: The user's query in JSON format.
   - **Example**:
     ```bash
     curl -X POST -H "Content-Type: application/json" -d '{"query": "What is the best insurance policy for me?"}' http://localhost:5505/ask?lang=en
     ```

---



## Configuration

### Environment Variables

The following environment variables can be configured:

- `UPLOAD_AUDIO_DIR`: Directory for storing uploaded audio files (default: `Upload_audio`).
- `RESPONSE_AUDIO_DIR`: Directory for storing generated audio responses (default: `Responses_audio`).
- `WHISPER_MODEL_NAME`: Whisper model for audio transcription (default: `turbo`).
- `EMBEDDING_MODEL_NAME`: Sentence Transformer model for embeddings (default: `all-MiniLM-L6-v2`).
- `OLLAMA_MODEL_NAME`: Ollama language model for chat (default: `llama3.2:3B`).

---

## Troubleshooting

1. **Docker Container Fails to Start**:
   - Ensure Docker is installed and running.
   - Check the logs for errors:
     ```bash
     docker logs <container_id>
     ```

2. **File Upload Issues**:
   - Ensure the `Upload_audio` and `Responses_audio` directories exist and have proper permissions.

3. **Missing Dependencies**:
   - Rebuild the Docker image to ensure all dependencies are installed:
     ```bash
     docker build -t insurance-advisor-chatbot .
     ```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contact

For questions or feedback, please contact:

- **Name**: Sonali
- **Email**: sonalithakur196@gmail.com
- **GitHub**: https://github.com/sonali123123

---

This `README.md` provides a comprehensive guide for setting up, using, and contributing to the `insurance-advisor-chatbot` application. Let me know if you need further customization!
