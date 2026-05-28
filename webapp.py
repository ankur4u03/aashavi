import streamlit as st
import os
from groq import Groq

# PAGE CONFIG
st.set_page_config(
    page_title="Aashvi AI",
    page_icon="🌸",
    layout="wide"
)

# API KEY
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

# CUSTOM CSS
st.markdown("""
<style>

/* MAIN APP */
.stApp{
    background: linear-gradient(to bottom, #020817, #07122b);
    color:white;
    overflow:hidden;
}

/* REMOVE STREAMLIT */
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

/* SIDEBAR */
.sidebar{
    background:#081225;
    height:100vh;
    padding:25px 18px;
    border-right:1px solid rgba(255,255,255,0.08);
}

.logo{
    font-size:28px;
    font-weight:700;
    margin-bottom:35px;
}

.newchat{
    background:#182742;
    padding:14px 18px;
    border-radius:16px;
    font-size:20px;
    font-weight:600;
    margin-bottom:35px;
    cursor:pointer;
    width:180px;
}

.newchat:hover{
    background:#223455;
}

.recent{
    color:#9aa4bf;
    font-size:15px;
    margin-bottom:18px;
}

.chat-item{
    background:#13203a;
    padding:13px 16px;
    border-radius:14px;
    margin-bottom:12px;
    cursor:pointer;
    transition:0.3s;
}

.chat-item:hover{
    background:#1d2a4a;
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
    color:#b9c1d9;
    margin-top:10px;
}

/* CARDS */
.cards-container{
    display:flex;
    justify-content:center;
    gap:18px;
    margin-top:50px;
    flex-wrap:wrap;
}

.card{
    background:#16213a;
    padding:14px 18px;
    border-radius:14px;
    color:white;
    font-size:16px;
    font-weight:500;
    cursor:pointer;
    border:1px solid rgba(255,255,255,0.05);
    transition:0.3s;
    min-width:220px;
    max-width:220px;
    text-align:center;
}

.card:hover{
    background:#1d2a4a;
    transform:translateY(-2px);
}

/* CHAT */
.user-msg{
    background:#2563eb;
    padding:14px 18px;
    border-radius:18px;
    width:fit-content;
    margin-left:auto;
    margin-top:25px;
    margin-bottom:12px;
    max-width:60%;
    text-align:left;
}

.ai-msg{
    background:#182742;
    padding:14px 18px;
    border-radius:18px;
    width:fit-content;
    margin-right:auto;
    margin-bottom:18px;
    max-width:70%;
    text-align:left;
}

/* INPUT */
.stChatInput{
    position:fixed;
    bottom:20px;
    left:340px;
    right:40px;
}

.stChatInput input{
    background:#111827 !important;
    color:white !important;
    border:1px solid rgba(255,255,255,0.08) !important;
    border-radius:18px !important;
    padding:18px !important;
}

</style>
""", unsafe_allow_html=True)

# LAYOUT
col1, col2 = st.columns([1, 4])

# SIDEBAR
with col1:

    st.markdown("""
    <div class="sidebar">

        <div class="logo">🌸 Aashvi AI</div>

        <div class="newchat">➕ New Chat</div>

        <div class="recent">Recent Chats</div>

        <div class="chat-item">💬 Motivation Ideas</div>

        <div class="chat-item">💬 Viral Content</div>

        <div class="chat-item">💬 YouTube SEO</div>

    </div>
    """, unsafe_allow_html=True)

# MAIN AREA
with col2:

    st.markdown("""
    <div class="main-area">

        <div class="title">🌸 Aashvi AI</div>

        <div class="subtitle">
            Think Faster with Aashvi AI ⚡
        </div>

    </div>
    """, unsafe_allow_html=True)

    # SHOW CARDS ONLY IF NO CHAT
    if len(st.session_state.messages) == 0:

        st.markdown("""
        <div class="cards-container">

            <div class="card">✨ Create Viral Reel Script</div>

            <div class="card">💻 Fix Python Error</div>

            <div class="card">🚀 YouTube Video Ideas</div>

            <div class="card">📈 SEO Strategy</div>

        </div>
        """, unsafe_allow_html=True)

    # SHOW CHAT
    for msg in st.session_state.messages:

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

# CHAT INPUT
prompt = st.chat_input("Ask anything...")

if prompt:

    # SAVE USER MSG
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

        # SAVE AI MSG
        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

        st.rerun()

    except Exception as e:

        st.error(f"Error: {e}")