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

-.venv/ – Contains the Python virtual environment and installed dependencies for the project.
-chatbot/ – Root directory that holds all chatbot-related source code and resources.
-Chatbot/ – Main application module containing backend logic, UI, and configurations.
-__pycache__/ – Stores compiled Python bytecode files for faster execution.
-fonts/ – Contains custom font files used for UI or PDF/image rendering.
-generated_images/ – Stores AI-generated images created by the chatbot.
-outputs/ – Holds generated outputs such as summaries, logs, and processed files.
-.env – Stores sensitive environment variables like API keys securely.
-app.py – Entry point of the application that runs the Streamlit interface.
-auth.py – Handles user authentication including login and signup functionality.
-users.py – Manages user data, chat history, and database operations.
-utils.py – Contains core AI functions such as chat response generation, summarization, and image generation.
-database.db – SQLite database used to store user credentials and chat history.
-requirements.txt – Lists all Python packages required to run the project.
-README.md – Provides project overview, setup instructions, and usage details.


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

