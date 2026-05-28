import streamlit as st
import os
from groq import Groq

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Aashvi AI",
    page_icon="🌸",
    layout="wide"
)

# ---------------- GROQ API ----------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- CSS ----------------
st.markdown("""
<style>

/* APP */
.stApp{
    background: linear-gradient(to bottom, #020817, #07152f);
    color:white;
}

/* HIDE STREAMLIT */
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

/* SIDEBAR */
.sidebar{
    background:#081225;
    height:100vh;
    padding:25px 20px;
    border-right:1px solid rgba(255,255,255,0.06);
}

.logo{
    font-size:26px;
    font-weight:700;
    color:white;
    margin-bottom:30px;
}

.new-chat{
    background:#182742;
    padding:14px;
    border-radius:14px;
    color:white;
    font-weight:600;
    text-align:center;
    margin-bottom:35px;
    cursor:pointer;
}

.new-chat:hover{
    background:#223455;
}

.recent-title{
    color:#9ca3af;
    font-size:14px;
    margin-bottom:18px;
}

.chat-history{
    background:#13203a;
    padding:12px 14px;
    border-radius:12px;
    margin-bottom:12px;
    color:white;
    font-size:15px;
}

/* MAIN */
.main-area{
    padding-top:70px;
    text-align:center;
}

.title{
    font-size:72px;
    font-weight:800;
    color:white;
}

.subtitle{
    font-size:24px;
    color:#b8c1d9;
    margin-top:10px;
}

/* SUGGESTION CARDS */
.cards{
    display:flex;
    justify-content:center;
    gap:18px;
    flex-wrap:wrap;
    margin-top:50px;
}

.card{
    background:#16213a;
    padding:16px 20px;
    border-radius:16px;
    width:220px;
    text-align:center;
    font-size:16px;
    font-weight:600;
    color:white;
    border:1px solid rgba(255,255,255,0.05);
}

.card:hover{
    background:#1d2a4a;
}

/* CHAT UI */
.user-message{
    background:#2563eb;
    color:white;
    padding:14px 18px;
    border-radius:18px;
    margin-top:25px;
    margin-left:auto;
    width:fit-content;
    max-width:65%;
    text-align:left;
}

.ai-message{
    background:#182742;
    color:white;
    padding:14px 18px;
    border-radius:18px;
    margin-top:18px;
    margin-right:auto;
    width:fit-content;
    max-width:75%;
    text-align:left;
}

/* INPUT */
.stChatInput{
    position:fixed;
    bottom:20px;
    left:330px;
    right:40px;
}

.stChatInput input{
    background:#111827 !important;
    color:white !important;
    border-radius:18px !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    padding:18px !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LAYOUT ----------------
sidebar, main = st.columns([1, 4])

# ---------------- SIDEBAR ----------------
with sidebar:

    st.markdown("""
    <div class="sidebar">

        <div class="logo">🌸 Aashvi AI</div>

        <div class="new-chat">
            ➕ New Chat
        </div>

        <div class="recent-title">
            Recent Chats
        </div>

        <div class="chat-history">
            💬 Motivation Ideas
        </div>

        <div class="chat-history">
            💬 Viral Content
        </div>

        <div class="chat-history">
            💬 YouTube SEO
        </div>

    </div>
    """, unsafe_allow_html=True)

# ---------------- MAIN ----------------
with main:

    st.markdown("""
    <div class="main-area">

        <div class="title">
            🌸 Aashvi AI
        </div>

        <div class="subtitle">
            Think Faster with Aashvi AI ⚡
        </div>

    </div>
    """, unsafe_allow_html=True)

    # SHOW CARDS ONLY WHEN CHAT EMPTY
    if len(st.session_state.messages) == 0:

        st.markdown("""
        <div class="cards">

            <div class="card">
                ✨ Create Viral Reel Script
            </div>

            <div class="card">
                💻 Fix Python Error
            </div>

            <div class="card">
                🚀 YouTube Video Ideas
            </div>

            <div class="card">
                📈 SEO Strategy
            </div>

        </div>
        """, unsafe_allow_html=True)

    # CHAT HISTORY
    for msg in st.session_state.messages:

        if msg["role"] == "user":

            st.markdown(
                f"<div class='user-message'>{msg['content']}</div>",
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"<div class='ai-message'>{msg['content']}</div>",
                unsafe_allow_html=True
            )

# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Ask anything...")

if prompt:

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

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

        # SAVE AI MESSAGE
        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

        st.rerun()

    except Exception as e:

        st.error(f"Error: {e}")