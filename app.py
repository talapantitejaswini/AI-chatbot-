import streamlit as st
from auth import create_user, login_user, save_chat, load_chats, delete_chat
from utils import chat_with_llm, generate_image, summarize_youtube, summarize_pdf

st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")

SYSTEM_PROMPT = {"role": "system", "content": "You are a helpful, friendly AI assistant."}

st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("messages", [])
st.session_state.setdefault("chat_id", None)
st.session_state.setdefault("chat_title", "New Chat")

# =========================
# AUTH PAGE
# =========================
if not st.session_state.logged_in:
    left, right = st.columns([1.3, 1])

    with left:
        st.markdown("## 🤖 AI Multi-Tool Chatbot")
        st.markdown("""
### 📌 Project Description
AI Chatbot is an intelligent multi-tool assistant that can chat naturally, summarize YouTube videos and PDFs, and generate AI images. It remembers conversations across tools, providing a seamless ChatGPT-like experience in one unified interface.

### 👥 Team Members
- Sahithi Malladi
- Tejaswini Talapanti
- Malleswari Bandaru
""")

    with right:
        st.markdown("## 🔐 Login / Sign Up")
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", use_container_width=True):
                if login_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.messages = [SYSTEM_PROMPT]
                    st.session_state.chat_id = None
                    st.session_state.chat_title = "My Chat"
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        with tab2:
            new_user = st.text_input("Choose Username", key="signup_user")
            new_pass = st.text_input("Choose Password", type="password", key="signup_pass")
            if st.button("Create Account", use_container_width=True):
                if create_user(new_user, new_pass):
                    st.success("Account created! Please login 🔐")
                else:
                    st.error("Username already exists")

    st.stop()

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown(f"👤 **{st.session_state.username}**")

if st.sidebar.button("➕ New Chat"):
    st.session_state.messages = [SYSTEM_PROMPT]
    st.session_state.chat_id = None
    st.session_state.chat_title = "New Chat"
    st.rerun()

if st.sidebar.button("🗑 Clear Current Chat"):
    st.session_state.messages = [SYSTEM_PROMPT]
    st.session_state.chat_id = None
    st.session_state.chat_title = "New Chat"
    st.rerun()

st.sidebar.divider()
st.sidebar.subheader("💬 Chat History")

user_chats = load_chats(st.session_state.username, grouped=True) or {}
for chat_id, chat in user_chats.items():
    c1, c2 = st.sidebar.columns([4, 1])
    if c1.button(chat["title"], key=f"open_{chat_id}"):
        st.session_state.chat_id = chat_id
        st.session_state.chat_title = chat["title"]
        st.session_state.messages = chat["messages"]
        st.rerun()
    if c2.button("🗑", key=f"del_{chat_id}"):
        delete_chat(chat_id)
        if st.session_state.chat_id == chat_id:
            st.session_state.messages = [SYSTEM_PROMPT]
            st.session_state.chat_id = None
            st.session_state.chat_title = "New Chat"
        st.rerun()

st.sidebar.divider()
tool = st.sidebar.radio("🛠 Tools", ["Chat", "YouTube Summary", "PDF Summary", "Image Generation"])

st.sidebar.divider()
summary_language = st.sidebar.radio("🌐 Summary Language", ["English", "Telugu"], index=0)

if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

# =========================
# MAIN
# =========================
st.title(f"🤖 {st.session_state.chat_title}")

# Render chat history (ChatGPT-like memory across tools)
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        if msg.get("type") == "image":
            st.image(msg["content"])
        else:
            st.markdown(msg["content"])

# =========================
# TOOL: CHAT
# =========================
if tool == "Chat":
    prompt = st.chat_input("Ask anything...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_id = save_chat(st.session_state.username, st.session_state.chat_id, "user", prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_with_llm(st.session_state.messages)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
        save_chat(st.session_state.username, st.session_state.chat_id, "assistant", response)

# =========================
# TOOL: YOUTUBE SUMMARY
# =========================
elif tool == "YouTube Summary":
    yt_url = st.text_input("Paste YouTube URL")

    if st.button("Summarize Video"):
        if not yt_url:
            st.warning("Please paste a YouTube URL first.")
        else:
            with st.spinner("Summarizing video..."):
                summary = summarize_youtube(yt_url, summary_language)

            st.markdown(summary)

            st.session_state.messages.append({
                "role": "assistant",
                "content": f"📺 **YouTube Summary:**\n\n{summary}"
            })
            save_chat(st.session_state.username, st.session_state.chat_id, "assistant", f"YouTube Summary:\n{summary}")

# =========================
# TOOL: PDF SUMMARY
# =========================
elif tool == "PDF Summary":
    uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded_pdf and st.button("Summarize PDF"):
        with st.spinner("Reading PDF..."):
            summary = summarize_pdf(uploaded_pdf)

        st.markdown(summary)

        st.session_state.messages.append({
            "role": "assistant",
            "content": f"📄 **PDF Summary:**\n\n{summary}"
        })
        save_chat(st.session_state.username, st.session_state.chat_id, "assistant", f"PDF Summary:\n{summary}")

# =========================
# TOOL: IMAGE GENERATION
# =========================
elif tool == "Image Generation":
    img_prompt = st.chat_input("Describe the image...")
    if img_prompt:
        st.session_state.messages.append({"role": "user", "content": img_prompt})
        save_chat(st.session_state.username, st.session_state.chat_id, "user", img_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Generating image..."):
                result = generate_image(img_prompt)

                if isinstance(result, str) and result.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                    st.image(result)
                    st.session_state.messages.append({"role": "assistant", "type": "image", "content": result})
                    save_chat(st.session_state.username, st.session_state.chat_id, "assistant", f"Image generated: {img_prompt}")
                else:
                    st.error(result)
                    st.session_state.messages.append({"role": "assistant", "content": result})
                    save_chat(st.session_state.username, st.session_state.chat_id, "assistant", result)
