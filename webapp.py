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
# API KEY
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

/* HIDE STREAMLIT DEFAULT */

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

[data-testid="stDecoration"] {
    display: none;
}

[data-testid="stStatusWidget"] {
    display: none;
}

.stDeployButton {
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
    font-size: 40px;
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
    font-size: 16px;
    padding: 12px;
}

/* CHAT */

.chat-container {
    max-width: 850px;
    margin: auto;
    padding-bottom: 120px;
}

.main-title {
    text-align: center;
    font-size: 70px;
    font-weight: bold;
    color: white;
    margin-top: 70px;
}

.sub-title {
    text-align: center;
    color: #cbd5e1;
    font-size: 28px;
    margin-bottom: 50px;
}

/* USER MESSAGE */

.user-message {
    background: #2563eb;
    padding: 16px 22px;
    border-radius: 22px;
    color: white;
    width: fit-content;
    max-width: 70%;
    margin-left: auto;
    margin-top: 18px;
    margin-bottom: 18px;
    font-size: 17px;
    box-shadow: 0 0 20px rgba(37,99,235,0.4);
}

/* AI MESSAGE */

.ai-message {
    background: #111827;
    padding: 18px 22px;
    border-radius: 22px;
    color: white;
    width: fit-content;
    max-width: 75%;
    margin-right: auto;
    margin-top: 18px;
    margin-bottom: 18px;
    font-size: 17px;
    border: 1px solid #1f2937;
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
    border: 1px solid #374151 !important;
    border-radius: 18px !important;
    padding: 18px !important;
    font-size: 16px !important;
}

/* MOBILE */

@media (max-width: 768px) {

    section[data-testid="stSidebar"] {
        width: 85vw !important;
    }

    .main-title {
        font-size: 52px;
        margin-top: 40px;
    }

    .sub-title {
        font-size: 22px;
    }

    .stChatInput {
        left: 10px !important;
        right: 10px !important;
        bottom: 10px !important;
    }

    .user-message,
    .ai-message {
        max-width: 90%;
        font-size: 16px;
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
# MAIN TITLE
# =========================

st.markdown(
    "<div class='chat-container'>",
    unsafe_allow_html=True
)

if len(st.session_state.messages) == 0:

    st.markdown(
        "<div class='main-title'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='sub-title'>Think Faster with Aashvi AI ⚡</div>",
        unsafe_allow_html=True
    )

# =========================
# SHOW CHAT
# =========================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"<div class='user-message'>{message['content']}</div>",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"<div class='ai-message'>{message['content']}</div>",
            unsafe_allow_html=True
        )

# =========================
# USER INPUT
# =========================

prompt = st.chat_input("Ask anything")

# =========================
# RESPONSE
# =========================

if prompt:

    # SAVE USER MESSAGE

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # GREETING SYSTEM

    greetings = [
        "hi",
        "hello",
        "hey",
        "hii",
        "helo"
    ]

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

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)