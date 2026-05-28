import streamlit as st
import os
import time
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
# HIDE STREAMLIT UI
# =========================

hide_style = """
<style>

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

.viewerBadge_container__1QSob {
    display: none !important;
}

/* MAIN APP */

.stApp {
    background: linear-gradient(135deg, #050816, #0b1026);
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: rgba(10, 15, 31, 0.98);
    border-right: 1px solid rgba(255,255,255,0.06);
    width: 320px !important;
    min-width: 320px !important;
}

/* LOGO */

.sidebar-logo {
    font-size: 32px;
    font-weight: bold;
    color: white;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 30px;
}

/* BUTTONS */

.stButton button {
    width: 100%;
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
    color: white;
    border: 1px solid rgba(255,255,255,0.06);
    padding: 14px;
    transition: 0.3s;
    font-size: 15px;
    font-weight: 500;
}

.stButton button:hover {
    background: rgba(255,255,255,0.12);
    transform: scale(1.02);
}

/* CHAT ROW */

.chat-row {
    margin-bottom: 12px;
}

/* MAIN TITLE */

.main-title {
    text-align: center;
    font-size: 64px;
    font-weight: 800;
    color: white;
    margin-top: 30px;
}

.sub-title {
    text-align: center;
    color: #9ca3af;
    font-size: 20px;
    margin-bottom: 40px;
}

/* CHAT BUBBLES */

.user-msg {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    margin-bottom: 14px;
    margin-left: auto;
    width: fit-content;
    max-width: 75%;
    color: white;
    box-shadow: 0px 4px 18px rgba(37,99,235,0.3);
    font-size: 16px;
}

.ai-msg {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(10px);
    padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    margin-bottom: 14px;
    width: fit-content;
    max-width: 75%;
    color: white;
    border: 1px solid rgba(255,255,255,0.05);
    font-size: 16px;
}

/* INPUT */

.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 28%;
    width: 48%;
}

.stChatInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    color: white !important;
    border-radius: 18px !important;
    padding: 14px !important;
}

/* PROFILE CARD */

.profile-card {
    margin-top: 60px;
    padding: 22px;
    border-radius: 20px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.06);
    text-align: center;
}

.profile-name {
    font-size: 18px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
}

.profile-role {
    color: #9ca3af;
    font-size: 14px;
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

    .user-msg,
    .ai-msg {
        max-width: 95%;
    }
}

</style>
"""

st.markdown(hide_style, unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================

if "chat_sessions" not in st.session_state:

    st.session_state.chat_sessions = {
        "New Chat": []
    }

if "current_chat" not in st.session_state:

    st.session_state.current_chat = "New Chat"

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown(
        "<div class='sidebar-logo'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    # NEW CHAT

    if st.button("➕ New Chat"):

        chat_name = f"Chat {len(st.session_state.chat_sessions)+1}"

        st.session_state.chat_sessions[chat_name] = []

        st.session_state.current_chat = chat_name

        st.rerun()

    st.markdown("---")

    # CHAT HISTORY

    for chat in list(st.session_state.chat_sessions.keys()):

        st.markdown("<div class='chat-row'>", unsafe_allow_html=True)

        col1, col2 = st.columns([5,1])

        # OPEN CHAT

        with col1:

            if st.button(f"💬 {chat}", key=f"chat_{chat}"):

                st.session_state.current_chat = chat

                st.rerun()

        # 3 DOT MENU

        with col2:

            with st.popover("⋮"):

                st.write(chat)

                if st.button(
                    "🗑️ Delete Chat",
                    key=f"delete_{chat}"
                ):

                    del st.session_state.chat_sessions[chat]

                    if len(st.session_state.chat_sessions) == 0:

                        st.session_state.chat_sessions["New Chat"] = []

                        st.session_state.current_chat = "New Chat"

                    else:

                        st.session_state.current_chat = list(
                            st.session_state.chat_sessions.keys()
                        )[0]

                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # PROFILE CARD

    st.markdown(
        """
        <div class="profile-card">
            👤
            <div class="profile-name">Ankur</div>
            <div class="profile-role">
                Aashvi AI Creator
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# MAIN TITLE
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
# SHOW CHAT HISTORY
# =========================

messages = st.session_state.chat_sessions[
    st.session_state.current_chat
]

for msg in messages:

    if msg["role"] == "user":

        st.markdown(
            f"<div class='user-msg'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"<div class='ai-msg'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

# =========================
# CHAT INPUT
# =========================

prompt = st.chat_input("Ask anything...")

# =========================
# AI RESPONSE
# =========================

if prompt:

    # SAVE USER MESSAGE

    st.session_state.chat_sessions[
        st.session_state.current_chat
    ].append({
        "role": "user",
        "content": prompt
    })

    st.markdown(
        f"<div class='user-msg'>{prompt}</div>",
        unsafe_allow_html=True
    )

    # THINKING

    typing_placeholder = st.empty()

    typing_placeholder.markdown(
        "<div class='ai-msg'>✨ Aashvi AI is thinking...</div>",
        unsafe_allow_html=True
    )

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.7,
            max_tokens=1024
        )

        reply = completion.choices[0].message.content

        time.sleep(1)

        typing_placeholder.empty()

        st.markdown(
            f"<div class='ai-msg'>{reply}</div>",
            unsafe_allow_html=True
        )

        # SAVE AI RESPONSE

        st.session_state.chat_sessions[
            st.session_state.current_chat
        ].append({
            "role": "assistant",
            "content": reply
        })

    except Exception as e:

        st.error(f"Error: {e}")