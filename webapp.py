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
# HIDE STREAMLIT ELEMENTS
# =========================

hide_streamlit_style = """
<style>

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

[data-testid="manage-app-button"] {
    display: none;
}

.viewerBadge_container__1QSob {
    display: none !important;
}

.st-emotion-cache-1avcm0n {
    display: none !important;
}

.st-emotion-cache-z5fcl4 {
    display: none !important;
}

</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# =========================
# API KEY
# =========================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# SESSION STATE
# =========================

if "chat_sessions" not in st.session_state:

    st.session_state.chat_sessions = {
        "Chat 1": []
    }

if "current_chat" not in st.session_state:

    st.session_state.current_chat = "Chat 1"

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(to bottom, #050816, #0b1026);
    color: white;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background-color: #0a0f1f;
    border-right: 1px solid #1f2937;
}

.sidebar-title {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: white;
    margin-bottom: 20px;
}

/* MAIN TITLE */

.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: white;
    margin-top: 10px;
}

.sub-title {
    text-align: center;
    color: #b0b3c7;
    font-size: 18px;
    margin-bottom: 30px;
}

/* CHAT BUBBLES */

.user-message {
    background: #2563eb;
    padding: 14px;
    border-radius: 18px;
    margin-bottom: 12px;
    color: white;
    max-width: 75%;
    margin-left: auto;
    font-size: 16px;
}

.ai-message {
    background: #1e293b;
    padding: 14px;
    border-radius: 18px;
    margin-bottom: 12px;
    color: white;
    max-width: 75%;
    margin-right: auto;
    font-size: 16px;
}

/* CHAT INPUT */

.stChatInput input {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 12px !important;
}

/* BUTTONS */

.stButton button {
    width: 100%;
    border-radius: 10px;
    background-color: #111827;
    color: white;
    border: 1px solid #374151;
}

.stButton button:hover {
    background-color: #1f2937;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.markdown(
        "<h1 class='sidebar-title'>🌸 Aashvi AI</h1>",
        unsafe_allow_html=True
    )

    # NEW CHAT BUTTON

    if st.button("➕ New Chat"):

        new_chat_id = f"Chat {len(st.session_state.chat_sessions) + 1}"

        st.session_state.chat_sessions[new_chat_id] = []

        st.session_state.current_chat = new_chat_id

        st.rerun()

    st.markdown("---")

    # CHAT HISTORY

    for chat_name in list(st.session_state.chat_sessions.keys()):

        col1, col2 = st.columns([5,1])

        # OPEN CHAT

        with col1:

            if st.button(chat_name, key=f"chat_{chat_name}"):

                st.session_state.current_chat = chat_name

                st.rerun()

        # DELETE CHAT

        with col2:

            if st.button("🗑️", key=f"delete_{chat_name}"):

                del st.session_state.chat_sessions[chat_name]

                # IF CURRENT CHAT DELETED

                if st.session_state.current_chat == chat_name:

                    if len(st.session_state.chat_sessions) > 0:

                        st.session_state.current_chat = list(
                            st.session_state.chat_sessions.keys()
                        )[0]

                    else:

                        new_chat_id = "Chat 1"

                        st.session_state.chat_sessions[new_chat_id] = []

                        st.session_state.current_chat = new_chat_id

                st.rerun()

# =========================
# MAIN TITLE
# =========================

st.markdown(
    "<h1 class='main-title'>🌸 Aashvi AI</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>Think Faster with Aashvi AI ⚡</p>",
    unsafe_allow_html=True
)

# =========================
# SHOW CHAT HISTORY
# =========================

messages = st.session_state.chat_sessions[
    st.session_state.current_chat
]

for message in messages:

    if message["role"] == "user":

        st.markdown(
            f"<div class='user-message'>{message['content']}</div>",
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"<div class='ai-message'>{message['content']}</div>",
            unsafe_allow_html=True
        )

# =========================
# USER INPUT
# =========================

prompt = st.chat_input("Ask anything...")

# =========================
# CHAT LOGIC
# =========================

if prompt:

    # SAVE USER MESSAGE

    st.session_state.chat_sessions[
        st.session_state.current_chat
    ].append({
        "role": "user",
        "content": prompt
    })

    # SHOW USER MESSAGE

    st.markdown(
        f"<div class='user-message'>{prompt}</div>",
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

        # SHOW AI MESSAGE

        st.markdown(
            f"<div class='ai-message'>{reply}</div>",
            unsafe_allow_html=True
        )

        # SAVE AI RESPONSE

        st.session_state.chat_sessions[
            st.session_state.current_chat
        ].append({
            "role": "assistant",
            "content": reply
        })

    except Exception as e:

        st.error(f"Error: {e}")