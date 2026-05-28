import streamlit as st
import os
from groq import Groq

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Aashvi AI",
    page_icon="🌸",
    layout="wide"
)

# =========================
# GROQ API
# =========================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* HIDE STREAMLIT */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    display: none;
}

/* APP */

.stApp {
    background: linear-gradient(to bottom, #020617, #020b1f);
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #0b1120;
    border-right: 1px solid #1e293b;
    width: 260px !important;
}

.sidebar-title {
    font-size: 38px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
    margin-bottom: 20px;
}

.new-chat-btn button {
    width: 100%;
    border-radius: 14px;
    background: #2563eb;
    color: white;
    border: none;
    padding: 12px;
    font-size: 16px;
}

/* MAIN */

.main-title {
    text-align: center;
    font-size: 72px;
    font-weight: bold;
    margin-top: 35px;
    color: white;
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    font-size: 24px;
    margin-bottom: 50px;
}

/* CHAT AREA */

.chat-container {
    max-width: 900px;
    margin: auto;
    padding-bottom: 120px;
}

/* USER MESSAGE */

.user-msg {
    background: #2563eb;
    padding: 14px 20px;
    border-radius: 22px;
    width: fit-content;
    max-width: 70%;
    margin-left: auto;
    margin-top: 18px;
    margin-bottom: 18px;
    color: white;
    font-size: 16px;
    box-shadow: 0 0 18px rgba(37,99,235,0.3);
}

/* AI MESSAGE */

.ai-msg {
    background: #111827;
    padding: 14px 20px;
    border-radius: 22px;
    width: fit-content;
    max-width: 70%;
    margin-right: auto;
    margin-top: 18px;
    margin-bottom: 18px;
    color: white;
    border: 1px solid #1f2937;
    font-size: 16px;
}

/* INPUT */

.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 320px;
    right: 40px;
}

.stChatInput input {
    background: #111827 !important;
    color: white !important;
    border-radius: 18px !important;
    border: 1px solid #374151 !important;
    padding: 18px !important;
    font-size: 16px !important;
}

/* MOBILE */

@media (max-width: 768px) {

    section[data-testid="stSidebar"] {
        width: 80vw !important;
    }

    .main-title {
        font-size: 50px;
        margin-top: 20px;
    }

    .sub-title {
        font-size: 20px;
    }

    .stChatInput {
        left: 10px !important;
        right: 10px !important;
        bottom: 10px !important;
    }

    .user-msg,
    .ai-msg {
        max-width: 90%;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown(
        "<div class='sidebar-title'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='new-chat-btn'>", unsafe_allow_html=True)

    if st.button("➕ New Chat"):

        st.session_state.messages = []
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# TITLE ALWAYS VISIBLE
# =========================

st.markdown(
    "<div class='main-title'>🌸 Aashvi AI</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Think Faster with Aashvi AI ⚡</div>",
    unsafe_allow_html=True
)

# =========================
# CHAT AREA
# =========================

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"<div class='user-msg'>{message['content']}</div>",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"<div class='ai-msg'>{message['content']}</div>",
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# USER INPUT
# =========================

prompt = st.chat_input("Ask anything")

# =========================
# RESPONSE
# =========================

if prompt:

    # SAVE USER MESSAGE

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    greetings = [
        "hi",
        "hello",
        "hey",
        "hii",
        "helo"
    ]

    # GREETING RESPONSE

    if prompt.lower().strip() in greetings:

        reply = "Hello 👋 How can I help you today?"

    else:

        try:

            completion = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=st.session_state.messages,

                temperature=0.7,
                max_tokens=1024
            )

            reply = completion.choices[0].message.content

        except Exception as e:

            reply = f"Error: {e}"

    # SAVE AI RESPONSE

    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })

    st.rerun()