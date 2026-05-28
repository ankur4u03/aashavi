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
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* MAIN APP */

.stApp {
    background: linear-gradient(135deg, #050816, #0b1026);
    color: white;
    overflow: hidden;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: rgba(10, 15, 31, 0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
}

/* SIDEBAR TITLE */

.sidebar-logo {
    font-size: 28px;
    font-weight: bold;
    color: white;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 25px;
}

/* BUTTONS */

.stButton button {
    width: 100%;
    border-radius: 14px;
    background: rgba(255,255,255,0.05);
    color: white;
    border: 1px solid rgba(255,255,255,0.08);
    padding: 12px;
    transition: 0.3s;
}

.stButton button:hover {
    background: rgba(255,255,255,0.12);
    transform: scale(1.02);
}

/* TITLE */

.main-title {
    text-align: center;
    font-size: 64px;
    font-weight: 800;
    color: white;
    margin-top: 20px;
}

.sub-title {
    text-align: center;
    color: #b0b3c7;
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
    box-shadow: 0px 4px 20px rgba(37,99,235,0.3);
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

/* INPUT BOX */

.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 25%;
    width: 50%;
}

.stChatInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 18px !important;
    padding: 14px !important;
    backdrop-filter: blur(12px);
}

/* PROFILE CARD */

.profile-card {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 16px;
    text-align: center;
    margin-top: 30px;
    border: 1px solid rgba(255,255,255,0.06);
}

.profile-name {
    color: white;
    font-weight: bold;
    margin-top: 10px;
}

/* MOBILE */

@media (max-width: 768px) {

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
""", unsafe_allow_html=True)

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

    for chat in st.session_state.chat_sessions.keys():

        col1, col2 = st.columns([5,1])

        with col1:

            if st.button(f"💬 {chat}", key=chat):

                st.session_state.current_chat = chat

                st.rerun()

        with col2:

            if st.button("🗑️", key=f"delete_{chat}"):

                del st.session_state.chat_sessions[chat]

                if len(st.session_state.chat_sessions) == 0:

                    st.session_state.chat_sessions["New Chat"] = []

                    st.session_state.current_chat = "New Chat"

                else:

                    st.session_state.current_chat = list(
                        st.session_state.chat_sessions.keys()
                    )[0]

                st.rerun()

    # PROFILE CARD

    st.markdown(
        """
        <div class="profile-card">
            👤
            <div class="profile-name">Ankur</div>
            <div style="color:#9ca3af;font-size:14px;">
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
# CHAT DISPLAY
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
# AI CHAT LOGIC
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

    # TYPING ANIMATION

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