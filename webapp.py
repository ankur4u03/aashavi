# =========================================
# AASHVI AI - FINAL MODERN CHATGPT UI
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

def save_message(chat_name, role, content):

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

/* =================================
HIDE STREAMLIT
================================= */

#MainMenu,
footer,
header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"]{
    display:none !important;
}

/* =================================
APP
================================= */

.stApp{
    background:#212121;
    color:white;
}

/* =================================
SIDEBAR
================================= */

section[data-testid="stSidebar"]{
    background:#171717;
    border-right:1px solid #2b2b2b;
    width:260px !important;
}

/* =================================
SIDEBAR TEXT
================================= */

.logo{
    font-size:28px;
    font-weight:700;
    color:white;
    margin-bottom:25px;
}

.recent-title{
    color:#9ca3af;
    font-size:13px;
    margin-top:20px;
    margin-bottom:15px;
}

/* =================================
BUTTONS
================================= */

.stButton button{
    width:100%;
    background:transparent;
    color:white;
    border:none;
    border-radius:12px;
    text-align:left;
    padding:12px;
    transition:0.2s;
    font-size:15px;
}

.stButton button:hover{
    background:#2a2a2a;
}

/* =================================
MAIN TITLE
================================= */

.main-title{
    text-align:center;
    font-size:70px;
    font-weight:800;
    margin-top:80px;
    color:white;
}

.sub-title{
    text-align:center;
    color:#a1a1aa;
    font-size:24px;
    margin-bottom:50px;
}

/* =================================
CHAT AREA
================================= */

.main .block-container{
    max-width:950px;
    padding-top:20px;
    padding-bottom:120px;
}

/* =================================
USER MESSAGE
================================= */

.user-wrap{
    display:flex;
    justify-content:flex-end;
    margin-top:25px;
    margin-bottom:25px;
}

.user-bubble{
    background:#303030;
    color:white;
    padding:16px 20px;
    border-radius:22px;
    max-width:75%;
    font-size:16px;
    line-height:1.8;
}

/* =================================
AI MESSAGE
================================= */

.ai-wrap{
    display:flex;
    justify-content:flex-start;
    margin-top:25px;
    margin-bottom:25px;
}

.ai-bubble{
    background:transparent;
    color:white;
    padding:10px 4px;
    max-width:90%;
    font-size:16px;
    line-height:1.9;
}

/* =================================
INPUT BOX
================================= */

.stChatInput{
    position:fixed;
    bottom:20px;
    left:50%;
    transform:translateX(-40%);
    width:60%;
}

.stChatInput input{
    background:#2f2f2f !important;
    color:white !important;
    border:none !important;
    border-radius:18px !important;
    padding:18px !important;
    font-size:16px !important;
}

/* =================================
CODE BLOCK
================================= */

pre{
    background:#111827 !important;
    border-radius:16px !important;
    padding:16px !important;
    overflow-x:auto;
}

code{
    color:#67e8f9 !important;
}

/* =================================
TEXT
================================= */

p, li{
    color:white !important;
    line-height:1.9 !important;
}

/* =================================
MOBILE RESPONSIVE
================================= */

@media(max-width:768px){

    .main-title{
        font-size:46px;
        margin-top:40px;
    }

    .sub-title{
        font-size:18px;
    }

    .stChatInput{
        width:92%;
        left:50%;
        transform:translateX(-50%);
    }

    .user-bubble{
        max-width:88%;
        font-size:15px;
    }

    .ai-bubble{
        max-width:95%;
        font-size:15px;
    }

    section[data-testid="stSidebar"]{
        width:240px !important;
    }
}

/* =================================
REMOVE FOOTER SPACE
================================= */

.block-container{
    padding-bottom:120px;
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

    # RECENT

    st.markdown(
        "<div class='recent-title'>Recent Chats</div>",
        unsafe_allow_html=True
    )

    # CHAT LIST

    for chat_name in list(
        st.session_state.chat_sessions.keys()
    ):

        if st.button(
            f"💬 {chat_name}",
            key=f"chat_{chat_name}"
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
            Think Faster with Aashvi AI ⚡
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================
# SHOW MESSAGES
# =========================================

for message in messages:

    # USER

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class="user-wrap">
                <div class="user-bubble">
                    {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # AI

    else:

        st.markdown(
            f"""
            <div class="ai-wrap">
                <div class="ai-bubble">
                    {message["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================================
# INPUT
# =========================================

user_input = st.chat_input(
    "Ask anything"
)

# =========================================
# AI RESPONSE
# =========================================

if user_input:

    # AUTO RENAME

    if (
        st.session_state.current_chat.startswith("Chat")
        or st.session_state.current_chat == "New Chat"
    ):

        title = user_input[:25]

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
            "role":"user",
            "content":user_input
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
        <div class="user-wrap">
            <div class="user-bubble">
                {user_input}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # AI BOX

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
                f"""
                <div class="ai-wrap">
                    <div class="ai-bubble">
                        {full_response}▌
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            time.sleep(0.02)

        response_placeholder.markdown(
            f"""
            <div class="ai-wrap">
                <div class="ai-bubble">
                    {reply}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # SAVE AI

        st.session_state.chat_sessions[
            st.session_state.current_chat
        ].append(
            {
                "role":"assistant",
                "content":reply
            }
        )

        save_message(
            st.session_state.current_chat,
            "assistant",
            reply
        )

    except Exception as e:

        st.error(f"Error: {e}")