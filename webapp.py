import streamlit as st
import os
import time
from groq import Groq

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
# API
# =====================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================
# CSS
# =====================================

st.markdown("""
<style>

/* APP */

.stApp {
    background-color: #212121;
    color: white;
}

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

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #171717;
    border-right: 1px solid #2b2b2b;
    width: 240px !important;
}

/* REMOVE BUTTON STYLE */

.stButton button {
    background: transparent;
    border: none;
    color: white;
    text-align: left;
    padding: 12px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 500;
}

.stButton button:hover {
    background: #2a2a2a;
}

/* LOGO */

.logo {
    font-size: 30px;
    font-weight: 700;
    color: white;
    margin-bottom: 25px;
}

/* TITLE */

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 700;
    color: white;
    margin-top: 40px;
}

.sub-title {
    text-align: center;
    color: #9ca3af;
    font-size: 18px;
    margin-bottom: 40px;
}

/* USER CHAT */

.user-message {
    background: #303030;
    padding: 16px;
    border-radius: 14px;
    margin-top: 18px;
    margin-bottom: 18px;
    color: white;
    font-size: 16px;
    line-height: 1.6;
}

/* AI CHAT */

.ai-message {
    background: transparent;
    padding: 16px;
    border-radius: 14px;
    margin-bottom: 18px;
    color: white;
    font-size: 16px;
    line-height: 1.7;
}

/* CHAT INPUT */

.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 28%;
    width: 65%;
}

.stChatInput input {
    background: #2f2f2f !important;
    color: white !important;
    border: 1px solid #3f3f3f !important;
    border-radius: 18px !important;
    padding: 16px !important;
    font-size: 16px !important;
}

/* MOBILE */

@media (max-width: 768px) {

    .stChatInput {
        left: 3%;
        width: 94%;
    }

    .main-title {
        font-size: 38px;
    }

    section[data-testid="stSidebar"] {
        width: 100% !important;
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

    st.button("➕ New Chat")

    st.markdown("---")

    st.markdown(
        """
        <div style='color:#9ca3af;
        font-size:14px;
        margin-top:10px;
        margin-bottom:15px;'>

        Recent Chats

        </div>
        """,
        unsafe_allow_html=True
    )

    st.button("💬 Motivation Ideas")

    st.button("💬 Viral Content")

    st.button("💬 YouTube SEO")

# =====================================
# MAIN TITLE
# =====================================

st.markdown(
    "<div class='main-title'>🌸 Aashvi AI</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Think Faster with Aashvi AI ⚡</div>",
    unsafe_allow_html=True
)

# =====================================
# SHOW CHAT
# =====================================

for message in st.session_state.messages:

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

# =====================================
# INPUT
# =====================================

prompt = st.chat_input("Ask anything")

# =====================================
# RESPONSE
# =====================================

if prompt:

    # SAVE USER MESSAGE

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    st.markdown(
        f"""
        <div class='user-message'>
        {prompt}
        </div>
        """,
        unsafe_allow_html=True
    )

    thinking = st.empty()

    thinking.markdown(
        """
        <div class='ai-message'>
        ✨ Aashvi AI is thinking...
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

        time.sleep(1)

        thinking.empty()

        st.markdown(
            f"""
            <div class='ai-message'>
            {reply}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

    except Exception as e:

        st.error(f"Error: {e}")