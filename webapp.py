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

/* =========================
   HIDE STREAMLIT
========================= */

#MainMenu,
footer,
header,
[data-testid="stToolbar"]{
    display:none;
}

/* =========================
   APP
========================= */

.stApp{
    background:#0b1120;
    color:white;
}

/* =========================
   SIDEBAR
========================= */

section[data-testid="stSidebar"]{
    background:#111827;
    width:260px !important;
    min-width:260px !important;
    border-right:1px solid rgba(255,255,255,0.06);
}

/* =========================
   LOGO
========================= */

.logo{
    font-size:30px;
    font-weight:700;
    margin-top:10px;
    margin-bottom:30px;
    color:white;
}

/* =========================
   BUTTONS
========================= */

.stButton button{
    width:100%;
    border:none;
    border-radius:14px;
    background:#1e293b;
    color:white;
    padding:12px;
    font-size:14px;
    transition:0.2s;
    margin-bottom:10px;
}

.stButton button:hover{
    background:#334155;
}

/* =========================
   TITLES
========================= */

.recent-title{
    color:#94a3b8;
    font-size:13px;
    margin-top:20px;
    margin-bottom:15px;
}

.main-title{
    text-align:center;
    font-size:62px;
    font-weight:800;
    margin-top:40px;
    color:white;
}

.sub-title{
    text-align:center;
    font-size:20px;
    color:#9ca3af;
    margin-bottom:40px;
}

/* =========================
   CHAT CONTAINER
========================= */

.main .block-container{
    max-width:1000px;
    padding-top:30px;
    padding-bottom:120px;
}

/* =========================
   CHAT AREA
========================= */

.user-wrap{
    display:flex;
    justify-content:flex-end;
    margin-bottom:24px;
}

.user-bubble{
    background:#2563eb;
    color:white;
    padding:14px 18px;
    border-radius:18px 18px 4px 18px;
    max-width:75%;
    font-size:15px;
    line-height:1.8;
    box-shadow:0 2px 10px rgba(37,99,235,0.25);
}

.ai-wrap{
    display:flex;
    justify-content:flex-start;
    margin-bottom:24px;
}

.ai-bubble{
    background:#111827;
    color:white;
    padding:16px 18px;
    border-radius:18px 18px 18px 4px;
    max-width:75%;
    font-size:15px;
    line-height:1.8;
    border:1px solid rgba(255,255,255,0.05);
}

/* =========================
   TEXT
========================= */

p, li{
    font-size:16px !important;
    line-height:1.8 !important;
    color:#f3f4f6 !important;
}

/* =========================
   INPUT BOX
========================= */

.stChatInput{
    position:fixed;
    bottom:20px;
    left:50%;
    transform:translateX(-35%);
    width:60%;
}

.stChatInput input{
    background:#1e293b !important;
    color:white !important;
    border:none !important;
    border-radius:18px !important;
    padding:14px !important;
    font-size:15px !important;
}

/* =========================
   CODE BLOCKS
========================= */

pre{
    background:#0f172a !important;
    border-radius:14px !important;
    padding:16px !important;
    border:1px solid rgba(255,255,255,0.06);
    overflow-x:auto;
}

code{
    color:#38bdf8 !important;
}

/* =========================
   MOBILE
========================= */

@media(max-width:768px){

    .main-title{
        font-size:42px;
    }

    .sub-title{
        font-size:16px;
    }

    .stChatInput{
        width:90%;
        left:50%;
        transform:translateX(-50%);
    }

    section[data-testid="stSidebar"]{
        width:100% !important;
        min-width:100% !important;
    }

    .user-bubble,
    .ai-bubble{
        max-width:95%;
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
# MAIN PAGE
# =========================================

messages = st.session_state.chat_sessions[
    st.session_state.current_chat
]

# =========================================
# HOME SCREEN
# =========================================

if True:

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

# =========================================
# SHOW CHAT HISTORY
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
# CHAT INPUT
# =========================================

user_input = st.chat_input(
    "Ask anything..."
)

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
    # GREETING RESPONSE
    # =========================================

    if clean_input in greetings:

        reply = "What can I help you with today?"

        response_placeholder = st.empty()

        full_response = ""

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

            time.sleep(0.03)

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

                time.sleep(0.03)

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