 # 🤖Multi-source-AI-Chatbot
 
## 📌 Problem Statement

Existing chatbots are often limited to a single data source and fail to provide comprehensive and accurate responses.An intelligent Multiple Source AI Chatbot that integrates data from various sources such as user queries, PDFs, YouTube videos, and AI image generation models. The system provides accurate, context-aware responses through a single conversational interface using modern AI technologies.

**🎯Goal:To design and develop a Multiple Source AI Chatbot that intelligently retrieves, integrates, and presents information from multiple data sources, providing accurate, context-aware, and user-friendly conversational responses.**

## 💡 Solution Approach

The proposed solution involves designing a Multiple Source AI Chatbot that integrates data from various sources such as documents, databases, and web APIs. User queries are first processed using Natural Language Processing (NLP) techniques to understand intent and extract key information. Based on the query, relevant data is retrieved from multiple sources simultaneously.

The retrieved information is then filtered, combined, and passed to an AI language model to generate a unified, context-aware response. The chatbot interface allows users to interact in natural language, while the backend ensures efficient data retrieval, response generation, and context management. This approach improves accuracy, scalability, and usability compared to single-source chatbots.

## 🚀 Project Features

💬Text Chat with AI (multi-turn conversation) 
🖼️Image Generation from Prompt 
🎥YouTube Video Summarization (using transcript) 
📄PDF Summarization (upload PDF and get summary) 
🔐 User authentication (Login & Signup)
🗃️ Chat history storage using SQLite
🌐 Interactive Streamlit-based UI
✅ Clean UI with tabs/sections 
✅ Environment variables for API keys (safe and professional) 
✅ Error handling (no transcript, invalid links, empty PDF, etc.)

## 📁 Repository Structure
│
├── .venv/                         # Python virtual environment
│
├── chatbot/
│   └── Chatbot/
│       ├── __pycache__/           # Python cache files
│       │
│       ├── fonts/                 # Custom fonts
│       │   └── DejaVuSans.ttf
│       │
│       ├── generated_images/      # AI-generated images
│       │   └── image.png
│       │
│       ├── outputs/               # Output files (summaries, logs, etc.)
│       │
│       ├── .env                   # Environment variables (API keys)
│       │
│       ├── app.py                 # Main Streamlit application
│       ├── auth.py                # User authentication (login/signup)
│       ├── users.py               # User management & database operations
│       ├── utils.py               # Core AI utilities and integrations
│       ├── database.db            # SQLite database (users & chat history)
│       │
│       └── generated_image.png    # Sample/generated image
│
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation


## ▶️ Steps to Run the Application
1️⃣ Clone the Repository
git clone <repository_url>
cd MULTI_SOURCE_AI_CHATBOT

2️⃣ Create and Activate Virtual Environment
python -m venv .venv
.venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables
Create a .env file inside chatbot/Chatbot/ and add:
GROQ_API_KEY=your_groq_api_key
HF_API_KEY=your_huggingface_api_key

5️⃣ Run the Application
cd chatbot/Chatbot
streamlit run app.py

6️⃣ Open in Browser
http://localhost:8502
Step 1: Open project folder cd multi_purpose_ai_chatbot Step 2: Create & activate virtual environment

Windows (CMD)

python -m venv .venv ..venv\Scripts\activate Step 4: Add API keys in .env

Create a file named .env in the project root:

GROQ_API_KEY=your_groq_key_here HF_API_KEY=your_huggingface_key_here Step 5: Run Streamlit app streamlit run app.py

## Access the app
Local URL:http://localhost:8502#

🧑‍🎓 Author

👩‍💻Tejaswini Talapanti
Capstone Project - Multi Source AI Chatbot
Training Program | January 2026
🔗Github:https://github.com/talapantitejaswini 
🔗Linkedin:www.linkedin.com/in/tejaswini-talapanti

