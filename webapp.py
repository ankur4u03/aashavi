import streamlit as st
import os
import time
from groq import Groq

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Aashvi AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# GROQ CLIENT
# =========================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================================
# SESSION STATE
# =========================================

if "chat_sessions" not in st.session_state:

    st.session_state.chat_sessions = {
        "New Chat": []
    }

if "current_chat" not in st.session_state:

    st.session_state.current_chat = "New Chat"

# =========================================
# CUSTOM CSS
# =========================================

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
    background: #0f172a;
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #111827;
    width: 260px !important;
    min-width: 260px !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* LOGO */

.logo {
    font-size: 30px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
    margin-bottom: 30px;
}

/* BUTTON */

.stButton button {
    width: 100%;
    border-radius: 14px;
    border: none;
    background: #1e293b;
    color: white;
    padding: 14px;
    transition: 0.3s;
    font-size: 15px;
    font-weight: 600;
    text-align: left;
    margin-bottom: 10px;
}

.stButton button:hover {
    background: #334155;
    transform: scale(1.02);
}

/* RECENT TITLE */

.recent-title {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 25px;
    margin-bottom: 15px;
    padding-left: 5px;
}

/* MAIN TITLE */

.main-title {
    text-align: center;
    font-size: 68px;
    font-weight: 800;
    color: white;
    margin-top: 60px;
}

.sub-title {
    text-align: center;
    color: #9ca3af;
    font-size: 22px;
    margin-bottom: 45px;
}

/* CHAT AREA */

.user-message {
    background: #2563eb;
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    width: fit-content;
    max-width: 75%;
    margin-left: auto;
    margin-bottom: 15px;
    font-size: 16px;
    box-shadow: 0px 4px 18px rgba(37,99,235,0.3);
}

.ai-message {
    background: #1e293b;
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    width: fit-content;
    max-width: 75%;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,0.05);
    font-size: 16px;
}

/* INPUT */

.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 28%;
    width: 65%;
}

.stChatInput input {
    background: #1e293b !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 16px !important;
    padding: 14px !important;
}

/* MOBILE */

@media (max-width: 768px) {

    section[data-testid="stSidebar"] {
        width: 100% !important;
        min-width: 100% !important;
    }

    .main-title {
        font-size: 42px;
    }

    .stChatInput {
        left: 5%;
        width: 90%;
    }

    .user-message,
    .ai-message {
        max-width: 95%;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.markdown(
        "<div class='logo'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    # NEW CHAT

    if st.button("➕ New Chat"):

        new_chat_name = f"Chat {len(st.session_state.chat_sessions)+1}"

        st.session_state.chat_sessions[new_chat_name] = []

        st.session_state.current_chat = new_chat_name

        st.rerun()

    # RECENT TITLE

    st.markdown(
        "<div class='recent-title'>Recent Chats</div>",
        unsafe_allow_html=True
    )

    # CHAT HISTORY

    for chat_name in list(st.session_state.chat_sessions.keys()):

        if st.button(
            f"💬 {chat_name}",
            key=f"open_{chat_name}"
        ):

            st.session_state.current_chat = chat_name

            st.rerun()

# =========================================
# MAIN PAGE
# =========================================

messages = st.session_state.chat_sessions[
    st.session_state.current_chat
]

# =========================================
# WELCOME SCREEN
# =========================================

if len(messages) == 0:

    st.markdown(
        "<div class='main-title'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='sub-title'>Think Faster with Aashvi AI ⚡</div>",
        unsafe_allow_html=True
    )

    # SUGGESTION CARDS

    col1, col2 = st.columns(2)

    with col1:

        if st.button("✨ Create Viral Reel Script"):

            prompt = "Create a viral Instagram reel script"

        if st.button("🚀 YouTube Video Ideas"):

            prompt = "Give me viral YouTube video ideas"

    with col2:

        if st.button("💻 Fix Python Error"):

            prompt = "Help me fix my Python error"

        if st.button("📈 SEO Strategy"):

            prompt = "Create an SEO strategy for YouTube"

# =========================================
# SHOW CHAT HISTORY
# =========================================

for message in messages:

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

# =========================================
# CHAT INPUT
# =========================================

user_input = st.chat_input("Ask anything...")

# =========================================
# HANDLE SUGGESTION BUTTONS
# =========================================

if "prompt" in locals():

    user_input = prompt

# =========================================
# AI RESPONSE
# =========================================

if user_input:

    # SAVE USER MESSAGE

    st.session_state.chat_sessions[
        st.session_state.current_chat
    ].append(
        {
            "role": "user",
            "content": user_input
        }
    )

    st.markdown(
        f"<div class='user-message'>{user_input}</div>",
        unsafe_allow_html=True
    )

    # THINKING EFFECT

    thinking = st.empty()

    thinking.markdown(
        "<div class='ai-message'>✨ Aashvi AI is thinking...</div>",
        unsafe_allow_html=True
    )

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=st.session_state.chat_sessions[
                st.session_state.current_chat
            ],

            temperature=0.7,
            max_tokens=1024
        )

        reply = completion.choices[0].message.content

        time.sleep(1)

        thinking.empty()

        st.markdown(
            f"<div class='ai-message'>{reply}</div>",
            unsafe_allow_html=True
        )

        # SAVE AI RESPONSE

        st.session_state.chat_sessions[
            st.session_state.current_chat
        ].append(
            {
                "role": "assistant",
                "content": reply
            }
        )

    except Exception as e:

        st.error(f"Error: {e}")