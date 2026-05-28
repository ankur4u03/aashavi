import streamlit as st
import time

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Aashvi AI",
    page_icon="🌸",
    layout="wide"
)

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_list" not in st.session_state:
    st.session_state.chat_list = ["New Chat"]

# =========================
# CSS
# =========================

st.markdown("""
<style>

#MainMenu,
footer,
header {
    display:none;
}

.stApp{
    background:#0b1020;
    color:white;
}

/* Sidebar */

section[data-testid="stSidebar"]{
    background:#111827;
    width:260px !important;
}

/* Logo */

.logo{
    font-size:34px;
    font-weight:700;
    margin-bottom:25px;
}

/* New Chat Button */

.stButton button{
    width:100%;
    border-radius:12px;
    background:#1f2937;
    color:white;
    border:none;
    padding:12px;
    font-size:15px;
}

.stButton button:hover{
    background:#374151;
}

/* Chat Messages */

.user-msg{
    background:#2563eb;
    padding:14px 18px;
    border-radius:18px;
    width:fit-content;
    max-width:70%;
    margin-left:auto;
    margin-top:12px;
    color:white;
}

.bot-msg{
    background:#1f2937;
    padding:14px 18px;
    border-radius:18px;
    width:fit-content;
    max-width:70%;
    margin-top:12px;
    color:white;
}

/* Center Title */

.main-title{
    text-align:center;
    margin-top:60px;
    font-size:70px;
    font-weight:800;
}

.sub{
    text-align:center;
    color:#9ca3af;
    font-size:22px;
    margin-bottom:50px;
}

/* Input */

.stChatInput{
    position:fixed;
    bottom:20px;
    left:50%;
    transform:translateX(-40%);
    width:60%;
}

/* Mobile */

@media(max-width:768px){

    .main-title{
        font-size:42px;
    }

    .stChatInput{
        width:90%;
        left:50%;
        transform:translateX(-50%);
    }

    .user-msg,
    .bot-msg{
        max-width:90%;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown(
        "<div class='logo'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("### Recent Chats")

    for chat in st.session_state.chat_list:
        st.markdown(f"💬 {chat}")

# =========================
# MAIN TITLE
# =========================

if len(st.session_state.messages) == 0:

    st.markdown(
        "<div class='main-title'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='sub'>What can I help you with today?</div>",
        unsafe_allow_html=True
    )

# =========================
# SHOW MESSAGES
# =========================

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(
            f"""
            <div class='user-msg'>
                {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class='bot-msg'>
                {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# CHAT INPUT
# =========================

prompt = st.chat_input("Ask anything...")

# =========================
# RESPONSE
# =========================

if prompt:

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    greetings = ["hi","hello","hey","hii"]

    if prompt.lower() in greetings:
        reply = "Hello 👋 How can I help you today?"
    else:
        reply = f"You said: {prompt}"

    st.session_state.messages.append({
        "role":"assistant",
        "content":reply
    })

    st.rerun()