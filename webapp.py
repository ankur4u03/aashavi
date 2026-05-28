import streamlit as st
import time

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Aashvi AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# SESSION STATE
# =====================================

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {
        "New Chat": []
    }

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# =====================================
# CSS
# =====================================

st.markdown("""
<style>

/* HIDE */

#MainMenu,
footer,
header{
    display:none;
}

/* APP */

.stApp{
    background:#0b1020;
    color:white;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{
    background:#111827;
    width:260px !important;
    min-width:260px !important;
    border-right:1px solid rgba(255,255,255,0.08);
}

/* LOGO */

.logo{
    font-size:34px;
    font-weight:800;
    color:white;
    margin-bottom:30px;
}

/* BUTTON */

.stButton button{
    width:100%;
    background:#1f2937;
    color:white;
    border:none;
    border-radius:14px;
    padding:12px;
    font-size:15px;
    transition:0.2s;
    margin-bottom:8px;
    text-align:left;
}

.stButton button:hover{
    background:#374151;
}

/* RECENT */

.recent{
    margin-top:20px;
    margin-bottom:10px;
    color:#9ca3af;
    font-size:14px;
}

/* TITLE */

.main-title{
    text-align:center;
    font-size:72px;
    font-weight:800;
    margin-top:30px;
    color:white;
}

.sub-title{
    text-align:center;
    color:#9ca3af;
    font-size:22px;
    margin-bottom:40px;
}

/* CHAT AREA */

.chat-container{
    width:100%;
    max-width:900px;
    margin:auto;
    padding-bottom:120px;
}

/* USER */

.user-row{
    display:flex;
    justify-content:flex-end;
    margin-top:20px;
}

.user-msg{
    background:#2563eb;
    color:white;
    padding:14px 18px;
    border-radius:18px 18px 4px 18px;
    max-width:70%;
    font-size:15px;
}

/* BOT */

.bot-row{
    display:flex;
    justify-content:flex-start;
    margin-top:20px;
}

.bot-msg{
    background:#1f2937;
    color:white;
    padding:14px 18px;
    border-radius:18px 18px 18px 4px;
    max-width:70%;
    font-size:15px;
}

/* INPUT */

.stChatInput{
    position:fixed;
    bottom:20px;
    left:55%;
    transform:translateX(-50%);
    width:65%;
}

.stChatInput input{
    background:#1f2937 !important;
    color:white !important;
    border:none !important;
    border-radius:18px !important;
    padding:16px !important;
}

/* MOBILE */

@media(max-width:768px){

    .main-title{
        font-size:42px;
    }

    .sub-title{
        font-size:17px;
    }

    .user-msg,
    .bot-msg{
        max-width:90%;
    }

    .stChatInput{
        width:92%;
        left:50%;
        transform:translateX(-50%);
    }
}

</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.markdown(
        "<div class='logo'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    # NEW CHAT

    if st.button("➕ New Chat"):

        new_chat = f"Chat {len(st.session_state.chat_sessions)+1}"

        st.session_state.chat_sessions[new_chat] = []

        st.session_state.current_chat = new_chat

        st.rerun()

    # RECENT CHATS

    st.markdown(
        "<div class='recent'>Recent Chats</div>",
        unsafe_allow_html=True
    )

    for chat_name in st.session_state.chat_sessions.keys():

        if st.button(
            f"💬 {chat_name}",
            key=chat_name
        ):

            st.session_state.current_chat = chat_name

            st.rerun()

# =====================================
# CURRENT CHAT
# =====================================

messages = st.session_state.chat_sessions[
    st.session_state.current_chat
]

# =====================================
# TITLE
# =====================================

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

# =====================================
# SHOW CHAT
# =====================================

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in messages:

    if msg["role"] == "user":

        st.markdown(
            f"""
            <div class='user-row'>
                <div class='user-msg'>
                    {msg["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class='bot-row'>
                <div class='bot-msg'>
                    {msg["content"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)

# =====================================
# INPUT
# =====================================

prompt = st.chat_input("Ask anything...")

# =====================================
# RESPONSE
# =====================================

if prompt:

    # SAVE USER

    st.session_state.chat_sessions[
        st.session_state.current_chat
    ].append({
        "role":"user",
        "content":prompt
    })

    greetings = [
        "hi",
        "hello",
        "hey",
        "hii"
    ]

    clean = prompt.lower().strip()

    # BOT REPLY

    if clean in greetings:

        reply = "Hello 👋 How can I help you today?"

    else:

        reply = f"You said: {prompt}"

    # SAVE BOT

    st.session_state.chat_sessions[
        st.session_state.current_chat
    ].append({
        "role":"assistant",
        "content":reply
    })

    time.sleep(0.2)

    st.rerun()