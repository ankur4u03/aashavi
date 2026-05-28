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
# API
# =========================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_title" not in st.session_state:
    st.session_state.chat_title = "New Chat"

# =========================
# CSS
# =========================

st.markdown("""
<style>

/* =========================
HIDE STREAMLIT
========================= */

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

/* =========================
APP
========================= */

.stApp {
    background-color: #212121;
    color: white;
    overflow: hidden;
}

/* =========================
SIDEBAR
========================= */

section[data-testid="stSidebar"] {
    background-color: #171717;
    border-right: 1px solid #2d2d2d;
    width: 260px !important;
}

/* =========================
LOGO
========================= */

.logo {
    font-size: 42px;
    font-weight: bold;
    margin-top: 15px;
    margin-bottom: 35px;
    color: white;
}

/* =========================
BUTTONS
========================= */

.stButton button {
    width: 100%;
    background: transparent;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 14px;
    text-align: left;
    font-size: 16px;
    transition: 0.2s;
}

.stButton button:hover {
    background-color: #2b2b2b;
}

/* =========================
RECENT CHAT
========================= */

.chat-item {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
    color: white;
    font-size: 15px;
    background-color: transparent;
    transition: 0.2s;
}

.chat-item:hover {
    background-color: #2a2a2a;
    cursor: pointer;
}

/* =========================
TITLE
========================= */

.main-title {
    text-align: center;
    font-size: 72px;
    font-weight: 800;
    color: white;
    margin-top: 70px;
}

.sub-title {
    text-align: center;
    color: #b4b4b4;
    font-size: 26px;
    margin-bottom: 60px;
}

/* =========================
CHATGPT STYLE CHAT
========================= */

.user-message {
    max-width: 850px;
    margin: auto;
    background-color: #303030;
    padding: 18px 22px;
    border-radius: 18px;
    margin-top: 20px;
    margin-bottom: 20px;
    font-size: 17px;
    color: white;
}

.ai-message {
    max-width: 850px;
    margin: auto;
    padding: 10px 5px;
    margin-bottom: 25px;
    font-size: 17px;
    line-height: 1.8;
    color: white;
}

/* =========================
INPUT
========================= */

.stChatInput {
    position: fixed;
    bottom: 18px;
    left: 320px;
    right: 40px;
}

.stChatInput input {
    background-color: #2b2b2b !important;
    color: white !important;
    border: 1px solid #444 !important;
    border-radius: 18px !important;
    padding: 20px !important;
    font-size: 17px !important;
}

/* =========================
SCROLL
========================= */

::-webkit-scrollbar {
    width: 7px;
}

::-webkit-scrollbar-thumb {
    background: #444;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown(
        "<div class='logo'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    if st.button("➕ New Chat"):

        st.session_state.messages = []
        st.session_state.chat_title = "New Chat"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        "<div style='color:#9e9e9e;font-size:14px;margin-bottom:15px;'>Recent Chats</div>",
        unsafe_allow_html=True
    )

    # AUTO TITLE LIKE CHATGPT

    if len(st.session_state.messages) > 0:

        first_msg = st.session_state.messages[0]["content"][:28]

        st.session_state.chat_title = first_msg

    st.markdown(
        f"<div class='chat-item'>💬 {st.session_state.chat_title}</div>",
        unsafe_allow_html=True
    )

# =========================
# TITLE
# =========================

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
# CHAT HISTORY
# =========================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class='user-message'>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class='ai-message'>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# INPUT
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

    # SHOW USER MESSAGE

    st.markdown(
        f"""
        <div class='user-message'>
            {prompt}
        </div>
        """,
        unsafe_allow_html=True
    )

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=st.session_state.messages,

            temperature=0.7,

            max_tokens=1024
        )

        reply = completion.choices[0].message.content

        # SHOW AI RESPONSE

        st.markdown(
            f"""
            <div class='ai-message'>
                {reply}
            </div>
            """,
            unsafe_allow_html=True
        )

        # SAVE AI RESPONSE

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

    except Exception as e:

        st.error(f"Error: {e}")