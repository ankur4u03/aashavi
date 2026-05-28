import streamlit as st
import os
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
# API CLIENT
# =========================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# SESSION STATE
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* HIDE STREAMLIT DEFAULT UI */

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

[data-testid="stDecoration"] {
    display: none;
}

[data-testid="stStatusWidget"] {
    display: none;
}

[data-testid="collapsedControl"] {
    display: none;
}

/* APP */

.stApp {
    background-color: #212121;
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #171717;
    border-right: 1px solid #2d2d2d;
    width: 260px !important;
}

/* SIDEBAR LOGO */

.sidebar-logo {
    font-size: 38px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
    margin-bottom: 30px;
}

/* NEW CHAT BUTTON */

.stButton button {
    width: 100%;
    background-color: transparent;
    color: white;
    border: 1px solid #3a3a3a;
    border-radius: 12px;
    padding: 12px;
    text-align: left;
    font-size: 16px;
    transition: 0.3s;
}

.stButton button:hover {
    background-color: #2a2a2a;
    border: 1px solid #555;
}

/* CHAT TITLE */

.main-title {
    text-align: center;
    font-size: 70px;
    font-weight: 800;
    color: white;
    margin-top: 60px;
    margin-bottom: 10px;
}

/* SUBTITLE */

.sub-title {
    text-align: center;
    color: #b4b4b4;
    font-size: 24px;
    margin-bottom: 50px;
}

/* CHAT MESSAGE */

.chat-user {
    background-color: #2f2f2f;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 15px;
    font-size: 18px;
}

.chat-ai {
    background-color: transparent;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 15px;
    font-size: 18px;
    line-height: 1.7;
}

/* INPUT */

.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 320px;
    right: 40px;
}

.stChatInput input {
    background-color: #2b2b2b !important;
    color: white !important;
    border: 1px solid #444 !important;
    border-radius: 18px !important;
    padding: 18px !important;
    font-size: 17px !important;
}

/* RECENT */

.recent-title {
    color: #8e8e8e;
    font-size: 14px;
    margin-top: 25px;
    margin-bottom: 10px;
}

/* CHAT HISTORY */

.chat-history {
    padding: 12px;
    border-radius: 10px;
    color: white;
    margin-bottom: 8px;
    background-color: transparent;
    cursor: pointer;
    transition: 0.3s;
}

.chat-history:hover {
    background-color: #2a2a2a;
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

    if st.button("➕ New Chat"):

        st.session_state.messages = []
        st.rerun()

    st.markdown(
        "<div class='recent-title'>Recent Chats</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='chat-history'>💬 Motivation Ideas</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='chat-history'>💬 Viral Content</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='chat-history'>💬 YouTube SEO</div>",
        unsafe_allow_html=True
    )

# =========================
# MAIN TITLE
# =========================

if len(st.session_state.messages) == 0:

    st.markdown(
        "<div class='main-title'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='sub-title'>Think Faster with Aashvi AI ⚡</div>",
        unsafe_allow_html=True
    )

# =========================
# SHOW CHAT
# =========================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class='chat-user'>
                {message['content']}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class='chat-ai'>
                {message['content']}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# USER INPUT
# =========================

prompt = st.chat_input("Ask anything")

# =========================
# AI RESPONSE
# =========================

if prompt:

    # SAVE USER MESSAGE

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # SHOW USER MESSAGE

    st.markdown(
        f"""
        <div class='chat-user'>
            {prompt}
        </div>
        """,
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

        # SHOW AI RESPONSE

        st.markdown(
            f"""
            <div class='chat-ai'>
                {reply}
            </div>
            """,
            unsafe_allow_html=True
        )

        # SAVE AI RESPONSE

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply
            }
        )

    except Exception as e:

        st.error(f"Error: {e}")