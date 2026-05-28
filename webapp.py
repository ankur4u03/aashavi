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
# CUSTOM CSS
# =========================================

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

/* APP BACKGROUND */

.stApp {
    background: #0f172a;
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #111827;
    width: 300px !important;
    min-width: 300px !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* SIDEBAR LOGO */

.logo {
    font-size: 32px;
    font-weight: bold;
    color: white;
    text-align: center;
    margin-top: 10px;
    margin-bottom: 25px;
}

/* NEW CHAT BUTTON */

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
}

.stButton button:hover {
    background: #334155;
    transform: scale(1.01);
}

/* CHAT LIST */

.chat-item {
    background: rgba(255,255,255,0.04);
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    border: 1px solid rgba(255,255,255,0.04);
}

/* MAIN TITLE */

.main-title {
    text-align: center;
    font-size: 65px;
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

/* USER CHAT */

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

/* AI CHAT */

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

/* CHAT INPUT */

.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 33%;
    width: 55%;
}

.stChatInput input {
    background: #1e293b !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 16px !important;
    padding: 14px !important;
}

/* PROFILE CARD */

.profile-card {
    margin-top: 40px;
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,255,255,0.04);
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
}

.profile-name {
    color: white;
    font-size: 18px;
    font-weight: bold;
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
        font-size: 40px;
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
# SESSION STATE
# =========================================

if "chat_sessions" not in st.session_state:

    st.session_state.chat_sessions = {
        "New Chat": []
    }

if "current_chat" not in st.session_state:

    st.session_state.current_chat = "New Chat"

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.markdown(
        "<div class='logo'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    # NEW CHAT BUTTON

    if st.button("➕ New Chat"):

        new_chat_name = f"Chat {len(st.session_state.chat_sessions)+1}"

        st.session_state.chat_sessions[new_chat_name] = []

        st.session_state.current_chat = new_chat_name

        st.rerun()

    st.markdown("---")

    # CHAT HISTORY

    for chat_name in list(st.session_state.chat_sessions.keys()):

        col1, col2 = st.columns([5,1])

        # OPEN CHAT

        with col1:

            if st.button(
                f"💬 {chat_name}",
                key=f"open_{chat_name}"
            ):

                st.session_state.current_chat = chat_name

                st.rerun()

        # 3 DOT MENU

        with col2:

            with st.popover("⋮"):

                st.write(chat_name)

                if st.button(
                    "🗑 Delete Chat",
                    key=f"delete_{chat_name}"
                ):

                    del st.session_state.chat_sessions[chat_name]

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
            <div class="profile-role">Aashvi AI Creator</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================
# MAIN PAGE
# =========================================

st.markdown(
    "<div class='main-title'>🌸 Aashvi AI</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Think Faster with Aashvi AI ⚡</div>",
    unsafe_allow_html=True
)

# =========================================
# SHOW CHAT HISTORY
# =========================================

messages = st.session_state.chat_sessions[
    st.session_state.current_chat
]

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

prompt = st.chat_input("Ask anything...")

# =========================================
# AI RESPONSE
# =========================================

if prompt:

    # SAVE USER MESSAGE

    st.session_state.chat_sessions[
        st.session_state.current_chat
    ].append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.markdown(
        f"<div class='user-message'>{prompt}</div>",
        unsafe_allow_html=True
    )

    # TYPING EFFECT

    thinking = st.empty()

    thinking.markdown(
        "<div class='ai-message'>✨ Aashvi AI is thinking...</div>",
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