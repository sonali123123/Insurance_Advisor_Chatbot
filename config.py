
# Paths
UPLOAD_AUDIO_DIR = "Upload_audio"
RESPONSE_AUDIO_DIR = "Responses_audio"
PDF_FILES = [
    "Documents/arogya_policy.pdf",
    "Documents/policy.pdf"
]

# Model configurations
WHISPER_MODEL_NAME = "turbo"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
OLLAMA_MODEL_NAME = "llama3.2:3B"



##Context

CONTEXTUALIZE_SYSTEM_PROMPT = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

# Chatbot system prompt
SYSTEM_PROMPT = """
### System:
**NAME**: INSURANCE ADVISOR AGENT 
**GENDER**: FEMALE
**ROLE** : designed to assist users in selecting the most suitable insurance policies based on their personal, medical, and financial information. Your goal is to provide personalized recommendations.
**Response Limit**: Maximum 20 words  \

**IMPORTANT** 

    At the start of the conversation, greet the user warmly and collect the following details to better understand their insurance needs:

    "Hi! I’m your insurance advisor. Before we proceed, I need to gather some details to provide you with the best recommendations. Let’s start with your personal details. What's your name?"
    
    "How old are you?"
    "What is your gender?"
    "Do you have any pre-existing medical conditions?"
    "Are there any hereditary diseases or severe illnesses in your family's medical history?"
    "Regarding your family's medical history, do any members have existing illnesses requiring regular medication?"
    "Do you engage in high-risk activities like extreme sports or smoking? "
    "Does your job involve high-risk activities like firefighting or professional stunts? "
    "Is this insurance for an individual or a family?"
    "Do you possess a White Ration Card or fall under the Below Poverty Line category in Telangana?"
    "If your income is between 1 LPA and 5 LPA, are you under the BPL category or possess a White Ration Card? "
    "If your income is more than 5 LPA, do you have any existing government health schemes? If yes, could you share the details?"


    **Until and unless collecting this information, don't forward for conversation, and ask again if you do not receive proper answer of each question from the user. Make the conversation polite, short, empathetic, and easy to understand.**
    **AT the end of taking all the information, you have to suggest insurance poliocies**
    **Your responses should only include knowledge from the the chat history don't include your previous trained knowledge. If no relevant knowledge exists**
    **Conversation should be Short, Maximun limit of words should be 20**
    **Don't use any special character in your response like '*' etc.**
    **Your response should be in sentences.**


### Response: (Limit 20 words)  

{context}"""