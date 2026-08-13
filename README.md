# 🤖 Multi-Source AI Chatbot

An intelligent AI-powered chatbot that integrates multiple data sources into a single conversational interface. Users can chat with AI, summarize PDFs, summarize YouTube videos, and generate AI images—all from one application.

---

## 📖 Overview

Multi-Source AI Chatbot is a Streamlit-based application that combines the power of Large Language Models (LLMs) with document processing, video summarization, and AI image generation. Instead of relying on a single information source, the chatbot supports multiple content types to provide context-aware and accurate responses.

---

## ✨ Features

- 💬 AI-powered conversational chatbot
- 📄 PDF document summarization
- 🎥 YouTube video summarization using transcripts
- 🖼️ AI image generation from text prompts
- 🔐 User authentication (Login & Signup)
- 💾 Chat history stored using SQLite
- 🌐 Interactive Streamlit interface
- 🔒 Secure API key management using `.env`
- ⚠️ Error handling for invalid PDFs, broken YouTube links, and missing transcripts

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI Models & APIs
- Groq API (LLM)
- Hugging Face API (Image Generation)

### Database
- SQLite

### Libraries
- LangChain
- PyPDF2
- youtube-transcript-api
- python-dotenv
- Pillow
- Requests

---

## 📂 Project Structure

```text
MULTI_SOURCE_AI_CHATBOT/
│
├── app.py
├── auth.py
├── users.py
├── utils.py
├── database.db
├── requirements.txt
├── .env
├── generated_images/
├── outputs/
├── fonts/
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/MULTI_SOURCE_AI_CHATBOT.git
cd MULTI_SOURCE_AI_CHATBOT
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the environment

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
HF_API_KEY=your_huggingface_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

## Deploy

https://multisource.streamlit.app/

Open your browser and visit:

```
http://localhost:8501/
```

---

## 🚀 How It Works

1. User logs into the application.
2. Selects one of the available features:
   - AI Chat
   - PDF Summarization
   - YouTube Summarization
   - Image Generation
3. The application processes the input using the appropriate AI service.
4. The generated response is displayed to the user.
5. Chat history is stored securely in SQLite.

---

## 📸 Screenshots

### 🏠 Login Page

<img width="1893" height="780" alt="Screenshot 2026-07-14 111012" src="https://github.com/user-attachments/assets/8abb8221-bb3c-41bc-b25a-7f56f5d0d15b" />


---

### 💬 AI Chat

<img width="1906" height="883" alt="image" src="https://github.com/user-attachments/assets/b032dc81-093e-4b20-bb1b-08246b6d9681" />


---

### 📄 PDF Summarization

<img width="1897" height="890" alt="Screenshot 2026-07-14 111906" src="https://github.com/user-attachments/assets/34247d8e-0c04-43f9-ad75-e4b811cff067" />


---

### 🎥 YouTube Summarization

<img width="1907" height="897" alt="Screenshot 2026-07-14 111332" src="https://github.com/user-attachments/assets/640eecc6-58b9-44ab-924f-2f98e514900f" />


---

### 🖼️ Image Generation
<img width="1318" height="792" alt="Screenshot 2026-07-14 111618" src="https://github.com/user-attachments/assets/c83d5227-d59b-4580-9544-d3123cd7878d" />


---

## 📌 Future Enhancements

- Voice-based interaction
- Multi-language support
- RAG with vector databases
- Cloud deployment
- Conversation memory improvements

---

## 👩‍💻 Author

**Tejaswini Talapanti**

- GitHub: https://github.com/talapantitejaswini
- LinkedIn: www.linkedin.com/in/tejaswini-talapanti
