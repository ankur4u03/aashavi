import streamlit as st
import os
from groq import Groq
import uuid

# PAGE CONFIG
st.set_page_config(
    page_title="Aashvi AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API KEY
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# CUSTOM CSS
st.markdown("""
<style>

/* HIDE STREAMLIT */

#MainMenu,
footer,
header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stDeployButton"] {
    display: none !important;
}

/* APP BACKGROUND */

.stApp {
    background: #0f172a;
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* SIDEBAR TITLE */

.sidebar-title {
    color: white;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 20px;
}

/* MAIN CONTAINER */

.block-container {
    padding-top: 1rem;
    max-width: 1000px;
}

/* TITLE */

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 700;
    color: white;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    color: #94a3b8;
    font-size: 18px;
    margin-bottom: 35px;
}

/* USER CHAT */

.user-msg {
    background: #2563eb;
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 5px 18px;
    margin-bottom: 12px;
    margin-left: 20%;
    font-size: 16px;
    line-height: 1.5;
}

/* AI CHAT */

.ai-msg {
    background: #1e293b;
    color: white;
    padding: 14px 18px;
    border-radius: 18px 18px 18px 5px;
    margin-bottom: 12px;
    margin-right: 20%;
    font-size: 16px;
    line-height: 1.6;
    border: 1px solid rgba(255,255,255,0.05);
}

/* INPUT */

.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 57%;
    transform: translateX(-50%);
    width: min(850px, calc(100% - 320px));
    z-index: 999;
}

.stChatInput input {
    background: #1e293b !important;
    color: white !important;
    border-radius: 16px !important;
    border: 1px solid #334155 !important;
    padding: 14px !important;
}

/* BUTTON */

.stButton button {
    width: 100%;
    border-radius: 12px;
    background: #2563eb;
    color: white;
    border: none;
    padding: 10px;
    margin-bottom: 10px;
}

/* MOBILE */

@media (max-width: 768px) {

    .main-title {
        font-size: 38px;
    }

    .sub-title {
        font-size: 15px;
    }

    .user-msg {
        margin-left: 5%;
    }

    .ai-msg {
        margin-right: 5%;
    }

    .stChatInput {
        width: calc(100% - 20px);
        left: 50%;
        bottom: 10px;
    }
}

</style>
""", unsafe_allow_html=True)

# SESSION STATE

if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:

    chat_id = str(uuid.uuid4())

    st.session_state.current_chat = chat_id

    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "messages": []
    }

# SIDEBAR

with st.sidebar:

    st.markdown(
        "<div class='sidebar-title'>🌸 Aashvi AI</div>",
        unsafe_allow_html=True
    )

    # NEW CHAT BUTTON

    if st.button("➕ New Chat"):

        new_chat_id = str(uuid.uuid4())

        st.session_state.current_chat = new_chat_id

        st.session_state.chats[new_chat_id] = {
            "title": "New Chat",
            "messages": []
        }

        st.rerun()

    st.markdown("### 💬 Chat History")

    # CHAT LIST

    for chat_id, chat_data in st.session_state.chats.items():

        if st.button(chat_data["title"], key=chat_id):

            st.session_state.current_chat = chat_id

            st.rerun()

# CURRENT CHAT

current_chat = st.session_state.chats[
    st.session_state.current_chat
]

# TITLE

st.markdown(
    "<div class='main-title'>🌸 Aashvi AI</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Think Faster with Aashvi AI ⚡</div>",
    unsafe_allow_html=True
)

# SHOW CHAT HISTORY

for message in current_chat["messages"]:

    if message["role"] == "user":

        st.markdown(
            f"<div class='user-msg'>{message['content']}</div>",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"<div class='ai-msg'>{message['content']}</div>",
            unsafe_allow_html=True
        )

# USER INPUT

prompt = st.chat_input("Message Aashvi AI...")

if prompt:

    # AUTO TITLE

    if current_chat["title"] == "New Chat":

        current_chat["title"] = prompt[:30]

    # SAVE USER MESSAGE

    current_chat["messages"].append({
        "role": "user",
        "content": prompt
    })

    # SHOW USER MESSAGE

    st.markdown(
        f"<div class='user-msg'>{prompt}</div>",
        unsafe_allow_html=True
    )

    # AI RESPONSE

    with st.spinner("Aashvi AI is typing..."):

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

            # SHOW AI MESSAGE

            st.markdown(
                f"<div class='ai-msg'>{reply}</div>",
                unsafe_allow_html=True
            )

            # SAVE AI RESPONSE

            current_chat["messages"].append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:

            st.error(f"Error: {e}")