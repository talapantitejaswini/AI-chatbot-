 # AI-chatbot-Multi-source-AI-Chatbot
 
## 📌 Problem Statement

Existing chatbots are often limited to a single data source and fail to provide comprehensive and accurate responses. This project aims to develop a Multiple Source AI Chatbot that integrates information from various sources and delivers intelligent, context-aware responses through a unified conversational interface.

**Goal: Build one simple chatbot app where a user can do all these tasks from a single UI.**

## 💡 Solution Approach
We build a Streamlit web app that acts as the front-end interface. Behind the scenes, a utils.py module handles all AI functions:

LLM Chat → via Groq API

Image generation → via HuggingFace (Inference API) OR Diffusers (local)

YouTube summarization → transcript → summarize with LLM

PDF summarization → extract text → summarize with LLM

This modular approach makes the code easy to maintain and upgrade.

## 🚀 Project Features
✅ Text Chat with AI (multi-turn conversation) ✅ Image Generation from Prompt ✅ YouTube Video Summarization (using transcript) ✅ PDF Summarization (upload PDF and get summary) ✅ Clean UI with tabs/sections ✅ Environment variables for API keys (safe and professional) ✅ Error handling (no transcript, invalid links, empty PDF, etc.)

## 📁 Folder structure
MULTI SOURCE AI CHATBOT │ ├── .venv/ # Virtual environment │ ├── chatbot/ │ └── Chatbot/ │ │ │ ├── pycache/ # Python cache files │ │ │ ├── fonts/ # Custom fonts │ │ └── DejaVuSans.ttf │ │ │ ├── generated_images/ # AI generated images folder │ │ └── image.png │ │ │ ├── outputs/ # Output files (summaries, logs, etc.) │ │ │ ├── .env # Environment variables (API keys) │ │ │ ├── app.py # Main Streamlit application │ │ │ ├── auth.py # Authentication logic (login/signup) │ │ │ ├── users.py # User management (DB operations) │ │ │ ├── utils.py # Core AI utilities (chat, summarize, image) │ │ │ ├── database.db # SQLite database (users + chat history) │ │ │ └── generated_image.png # Sample/generated image │ ├── requirements.txt # Python dependencies └── README.md # Project documentation

## 📂 File Descriptions
app.py

Main Streamlit application

Builds UI (chat input, tabs, upload, buttons)

Calls functions from utils.py

Stores chat history in st.session_state

utils.py

Contains all helper logic:

chat_with_llm(prompt) → sends prompt to Groq and returns response

generate_image(prompt) → generates image using HF or Diffusers

summarize_youtube(url) → fetches transcript and summarizes

summarize_pdf(pdf_file) → extracts text and summarizes

requirements.txt

All required Python packages.

.env

Stores API keys:

GROQ_API_KEY=

HF_API_KEY=

README.md

Project explanation (this content).

## Steps to Run the Project
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

