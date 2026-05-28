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
    background: #0b1120;
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #111827;
    width: 240px !important;
    min-width: 240px !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* LOGO */

.logo {
    font-size: 22px;
    font-weight: 700;
    color: white;
    margin-top: 8px;
    margin-bottom: 25px;
}

/* BUTTON */

.stButton button {
    width: 100%;
    border-radius: 12px;
    border: none;
    background: #1e293b;
    color: white;
    padding: 10px;
    transition: 0.2s;
    font-size: 13px;
    font-weight: 500;
    text-align: left;
    margin-bottom: 8px;
}

.stButton button:hover {
    background: #334155;
}

/* RECENT */

.recent-title {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 20px;
    margin-bottom: 12px;
    padding-left: 5px;
}

/* MAIN TITLE */

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    color: white;
    margin-top: 20px;
}

.sub-title {
    text-align: center;
    color: #9ca3af;
    font-size: 16px;
    margin-bottom: 35px;
}

/* CHAT */

.user-message {
    background: #2563eb;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    width: fit-content;
    max-width: 75%;
    margin-left: auto;
    margin-bottom: 14px;
    font-size: 14px;
}

.ai-message {
    background: #1e293b;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    width: fit-content;
    max-width: 75%;
    margin-bottom: 14px;
    font-size: 14px;
}

/* INPUT */

.stChatInput {
    position: fixed;
    bottom: 18px;
    left: 28%;
    width: 63%;
}

.stChatInput input {
    background: #1e293b !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    padding: 10px !important;
    font-size: 14px !important;
}

/* CARDS */

.card-btn .stButton button {
    background: #172033;
    border-radius: 14px;
    padding: 10px;
    text-align: center;
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 12px;
    min-height: 48px;
}

.card-btn .stButton button:hover {
    background: #253046;
}

/* MOBILE */

@media (max-width: 768px) {

    section[data-testid="stSidebar"] {
        width: 100% !important;
        min-width: 100% !important;
    }

    .main-title {
        font-size: 38px;
    }

    .sub-title {
        font-size: 14px;
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

    # RECENT CHATS TITLE

    st.markdown(
        "<div class='recent-title'>Recent Chats</div>",
        unsafe_allow_html=True
    )

    # CHAT LIST

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

    # SMALL CARDS

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("<div class='card-btn'>", unsafe_allow_html=True)

        if st.button(
            "✨ Create Viral Reel Script",
            key="viral_script"
        ):
            prompt = "Create a viral Instagram reel script"

        if st.button(
            "🚀 YouTube Video Ideas",
            key="youtube_ideas"
        ):
            prompt = "Give me viral YouTube video ideas"

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:

        st.markdown("<div class='card-btn'>", unsafe_allow_html=True)

        if st.button(
            "💻 Fix Python Error",
            key="python_error"
        ):
            prompt = "Help me fix my Python error"

        if st.button(
            "📈 SEO Strategy",
            key="seo_strategy"
        ):
            prompt = "Create an SEO strategy for YouTube"

        st.markdown("</div>", unsafe_allow_html=True)

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
# HANDLE CARD BUTTONS
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

    # THINKING

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