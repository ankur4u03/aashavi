# =========================================
# AASHVI AI - PERFECT CHATGPT STYLE UI
# =========================================

import streamlit as st
import os
import sqlite3
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
# DATABASE
# =========================================

conn = sqlite3.connect(
    "aashvi_ai.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_name TEXT,
    role TEXT,
    content TEXT
)
""")

conn.commit()

# =========================================
# GROQ CLIENT
# =========================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================================
# LOAD CHATS
# =========================================

def load_chats():

    cursor.execute(
        "SELECT DISTINCT chat_name FROM chats"
    )

    chat_names = cursor.fetchall()

    chat_sessions = {}

    for name in chat_names:

        chat_name = name[0]

        cursor.execute(
            """
            SELECT role, content
            FROM chats
            WHERE chat_name=?
            """,
            (chat_name,)
        )

        messages = cursor.fetchall()

        chat_sessions[chat_name] = []

        for msg in messages:

            chat_sessions[chat_name].append(
                {
                    "role": msg[0],
                    "content": msg[1]
                }
            )

    if not chat_sessions:

        chat_sessions["New Chat"] = []

    return chat_sessions

# =========================================
# SAVE MESSAGE
# =========================================

def save_message(
    chat_name,
    role,
    content
):

    cursor.execute(
        """
        INSERT INTO chats
        (chat_name, role, content)
        VALUES (?, ?, ?)
        """,
        (
            chat_name,
            role,
            content
        )
    )

    conn.commit()

# =========================================
# SESSION
# =========================================

if "chat_sessions" not in st.session_state:

    st.session_state.chat_sessions = load_chats()

if "current_chat" not in st.session_state:

    st.session_state.current_chat = list(
        st.session_state.chat_sessions.keys()
    )[0]

# =========================================
# CSS
# =========================================

st.markdown("""
<style>

/* HIDE */

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
    background: #0a0a0a;
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {

    background: #111111;

    width: 260px !important;
    min-width: 260px !important;

    border-right: 1px solid rgba(255,255,255,0.05);
}

/* LOGO */

.logo {

    font-size: 26px;
    font-weight: 700;

    color: white;

    margin-top: 10px;
    margin-bottom: 25px;
}

/* BUTTONS */

.stButton button {

    width: 100%;

    border-radius: 12px;

    border: none;

    background: #1b1b1b;

    color: white;

    padding: 11px;

    transition: 0.2s;

    font-size: 14px;

    text-align: left;

    margin-bottom: 8px;
}

.stButton button:hover {

    background: #2a2a2a;
}

/* RECENT */

.recent-title {

    color: #888;

    font-size: 12px;

    margin-top: 20px;
    margin-bottom: 12px;
}

/* HOME */

.main-title {

    text-align: center;

    font-size: 64px;

    font-weight: 800;

    color: white;

    margin-top: 140px;
}

.sub-title {

    text-align: center;

    color: #9ca3af;

    font-size: 20px;

    margin-bottom: 40px;
}

/* CHAT */

.user-message {

    background: #2563eb;

    color: white;

    padding: 14px 18px;

    border-radius: 18px 18px 4px 18px;

    width: fit-content;

    max-width: 700px;

    margin-left: auto;
    margin-right: 40px;

    margin-top: 18px;
    margin-bottom: 18px;

    font-size: 15px;

    line-height: 1.7;

    white-space: pre-wrap;
}

.ai-message {

    background: #1a1a1a;

    color: white;

    padding: 14px 18px;

    border-radius: 18px 18px 18px 4px;

    width: fit-content;

    max-width: 700px;

    margin-left: 40px;

    margin-top: 18px;
    margin-bottom: 18px;

    font-size: 15px;

    line-height: 1.7;

    white-space: pre-wrap;

    overflow-wrap: break-word;
}

/* INPUT */

.stChatInput {

    position: fixed;

    bottom: 20px;

    left: 50%;

    transform: translateX(-50%);

    width: 760px;

    max-width: 90%;
}

.stChatInput input {

    background: #1a1a1a !important;

    color: white !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    border-radius: 18px !important;

    padding: 14px !important;

    font-size: 15px !important;
}

/* HOME BUTTONS */

.home-btn .stButton button {

    background: #1a1a1a;

    border-radius: 30px;

    text-align: center;

    font-size: 13px;

    min-height: 45px;
}

/* CODE */

pre {

    background: #111827 !important;

    border-radius: 12px !important;

    padding: 16px !important;

    overflow-x: auto;
}

code {

    color: #38bdf8 !important;
}

/* MARKDOWN */

p, li {

    line-height: 1.8;
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

        st.session_state.chat_sessions[
            new_chat_name
        ] = []

        st.session_state.current_chat = (
            new_chat_name
        )

        st.rerun()

    # RECENT

    st.markdown(
        "<div class='recent-title'>Recent Chats</div>",
        unsafe_allow_html=True
    )

    # CHAT LIST

    for chat_name in list(
        st.session_state.chat_sessions.keys()
    ):

        col1, col2 = st.columns([5,1])

        with col1:

            if st.button(
                f"💬 {chat_name}",
                key=f"open_{chat_name}"
            ):

                st.session_state.current_chat = (
                    chat_name
                )

                st.rerun()

        with col2:

            if st.button(
                "🗑️",
                key=f"delete_{chat_name}"
            ):

                cursor.execute(
                    """
                    DELETE FROM chats
                    WHERE chat_name=?
                    """,
                    (chat_name,)
                )

                conn.commit()

                del st.session_state.chat_sessions[
                    chat_name
                ]

                if len(
                    st.session_state.chat_sessions
                ) == 0:

                    st.session_state.chat_sessions[
                        "New Chat"
                    ] = []

                    st.session_state.current_chat = (
                        "New Chat"
                    )

                else:

                    st.session_state.current_chat = list(
                        st.session_state.chat_sessions.keys()
                    )[0]

                st.rerun()

# =========================================
# MAIN
# =========================================

messages = st.session_state.chat_sessions[
    st.session_state.current_chat
]

# =========================================
# HOME SCREEN
# =========================================

if len(messages) == 0:

    st.markdown(
        """
        <div class='main-title'>
            🌸 Aashvi AI
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='sub-title'>
            How can I help you today?
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='home-btn'>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button("🎬 Reel Ideas"):

            prompt = "Give me viral reel ideas"

    with col2:

        if st.button("💻 Python Help"):

            prompt = "Help me with Python"

    with col3:

        if st.button("📈 SEO Tips"):

            prompt = "Give me SEO tips"

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# SHOW CHAT
# =========================================

for message in messages:

    if message["role"] == "user":

        st.markdown(
            f"""
<div class='user-message'>

{message['content']}

</div>
""",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
<div class='ai-message'>

{message['content']}

</div>
""",
            unsafe_allow_html=True
        )

# =========================================
# INPUT
# =========================================

user_input = st.chat_input(
    "Ask anything..."
)

if "prompt" in locals():

    user_input = prompt

# =========================================
# RESPONSE
# =========================================

if user_input:

    # AUTO RENAME

    if (
        st.session_state.current_chat.startswith("Chat")
        or st.session_state.current_chat == "New Chat"
    ):

        title = user_input[:30]

        title = title.replace("\n", " ")

        if len(title) > 25:

            title = title[:25] + "..."

        old_chat = st.session_state.current_chat

        st.session_state.chat_sessions[title] = (
            st.session_state.chat_sessions.pop(old_chat)
        )

        cursor.execute(
            """
            UPDATE chats
            SET chat_name=?
            WHERE chat_name=?
            """,
            (
                title,
                old_chat
            )
        )

        conn.commit()

        st.session_state.current_chat = title

    # SAVE USER

    st.session_state.chat_sessions[
        st.session_state.current_chat
    ].append(
        {
            "role": "user",
            "content": user_input
        }
    )

    save_message(
        st.session_state.current_chat,
        "user",
        user_input
    )

    # SHOW USER

    st.markdown(
        f"""
<div class='user-message'>

{user_input}

</div>
""",
        unsafe_allow_html=True
    )

    # SYSTEM PROMPT

    system_prompt = {
        "role": "system",
        "content": """
You are Aashvi AI.

Behave like ChatGPT.

Keep replies:
- clean
- modern
- direct
- minimal
"""
    }

    # AI

    try:

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                system_prompt,
                *st.session_state.chat_sessions[
                    st.session_state.current_chat
                ]
            ],

            temperature=0.7,
            max_tokens=1024
        )

        reply = completion.choices[0].message.content

        # REALTIME TYPING

        response_placeholder = st.empty()

        full_response = ""

        for word in reply.split():

            full_response += word + " "

            response_placeholder.markdown(
                f"""
<div class='ai-message'>

{full_response}

</div>
""",
                unsafe_allow_html=True
            )

            time.sleep(0.02)

        # FINAL RESPONSE

        response_placeholder.markdown(
            f"""
<div class='ai-message'>

{reply}

</div>
""",
            unsafe_allow_html=True
        )

        # SAVE AI

        st.session_state.chat_sessions[
            st.session_state.current_chat
        ].append(
            {
                "role": "assistant",
                "content": reply
            }
        )

        save_message(
            st.session_state.current_chat,
            "assistant",
            reply
        )

    except Exception as e:

        st.error(f"Error: {e}")