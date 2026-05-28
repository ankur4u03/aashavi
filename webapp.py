# =========================================
# AASHVI AI FULL PREMIUM VERSION
# =========================================

import streamlit as st
import os
import time
import sqlite3
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
# SESSION STATE
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
    font-size: 24px;
    font-weight: 700;
    color: white;
    margin-top: 8px;
    margin-bottom: 25px;
}

/* BUTTONS */

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

/* TITLES */

.recent-title {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 20px;
    margin-bottom: 12px;
}

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    color: white;
    margin-top: 25px;
}

.sub-title {
    text-align: center;
    color: #9ca3af;
    font-size: 16px;
    margin-bottom: 35px;
}

/* CHAT */

[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0px !important;
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

/* MARKDOWN */

h1, h2, h3 {
    color: white !important;
}

p, li {
    color: #e5e7eb !important;
    line-height: 1.8;
}

/* CODE BLOCK */

pre {
    background: #111827 !important;
    border-radius: 12px !important;
    padding: 16px !important;
    overflow-x: auto;
}

code {
    color: #38bdf8 !important;
    background: #111827 !important;
    padding: 3px 6px;
    border-radius: 6px;
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

        st.session_state.current_chat = new_chat_name

        st.rerun()

    # RECENT CHATS

    st.markdown(
        "<div class='recent-title'>Recent Chats</div>",
        unsafe_allow_html=True
    )

    # CHAT LIST

    for chat_name in list(
        st.session_state.chat_sessions.keys()
    ):

        col1, col2 = st.columns([5,1])

        # OPEN CHAT

        with col1:

            if st.button(
                f"💬 {chat_name}",
                key=f"open_{chat_name}"
            ):

                st.session_state.current_chat = (
                    chat_name
                )

                st.rerun()

        # DELETE CHAT

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
# MAIN PAGE
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
            What can I help you with today?
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if st.button(
            "✨ Viral Reel Script"
        ):

            prompt = (
                "Create a viral Instagram reel script"
            )

    with col2:

        if st.button(
            "🚀 YouTube Ideas"
        ):

            prompt = (
                "Give me viral YouTube video ideas"
            )

    with col3:

        if st.button(
            "💻 Python Error"
        ):

            prompt = (
                "Help me fix my Python error"
            )

    with col4:

        if st.button(
            "📈 SEO Strategy"
        ):

            prompt = (
                "Create an SEO strategy"
            )

# =========================================
# SHOW CHAT HISTORY
# =========================================

for message in messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =========================================
# CHAT INPUT
# =========================================

user_input = st.chat_input(
    "Ask anything..."
)

if "prompt" in locals():

    user_input = prompt

# =========================================
# AI RESPONSE
# =========================================

if user_input:

    # =========================================
    # AUTO CHAT RENAME
    # =========================================

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

    # =========================================
    # SAVE USER MESSAGE
    # =========================================

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

    # SHOW USER MESSAGE

    with st.chat_message("user"):

        st.markdown(user_input)

    # =========================================
    # GREETING CHECK
    # =========================================

    greetings = [
        "hi",
        "hello",
        "hey",
        "hii",
        "yo",
        "hola",
        "hlo"
    ]

    clean_input = user_input.lower().strip()

    # =========================================
    # ONLY FOR HI / HELLO
    # =========================================

    if clean_input in greetings:

        reply = "What can I help you with today?"

        with st.chat_message("assistant"):

            response_placeholder = st.empty()

            full_response = ""

            for word in reply.split():

                full_response += word + " "

                response_placeholder.markdown(
                    full_response + "▌"
                )

                time.sleep(0.03)

            response_placeholder.markdown(reply)

        # SAVE RESPONSE

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

    # =========================================
    # NORMAL AI RESPONSE
    # =========================================

    else:

        with st.chat_message("assistant"):

            response_placeholder = st.empty()

            full_response = ""

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

                # STREAM EFFECT

                for word in reply.split():

                    full_response += word + " "

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

                    time.sleep(0.03)

                response_placeholder.markdown(reply)

                # SAVE AI RESPONSE

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