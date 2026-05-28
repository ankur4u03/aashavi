import streamlit as st
import os
from groq import Groq

# PAGE CONFIG
st.set_page_config(
    page_title="Aashvi AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
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

/* MAIN CONTAINER */

.block-container {
    padding-top: 1rem;
    max-width: 900px;
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

/* CHAT BUBBLE */

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

/* CHAT INPUT */

.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: min(900px, calc(100% - 30px));
    z-index: 999;
}

.stChatInput input {
    background: #1e293b !important;
    color: white !important;
    border-radius: 16px !important;
    border: 1px solid #334155 !important;
    padding: 14px !important;
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
        width: calc(100% - 16px);
        bottom: 10px;
    }
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown(
    "<div class='main-title'>🌸 Aashvi AI</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='sub-title'>Think Faster with Aashvi AI ⚡</div>",
    unsafe_allow_html=True
)

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

# SHOW CHAT HISTORY
for message in st.session_state.messages:

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

    # SAVE USER MESSAGE
    st.session_state.messages.append({
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
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:

            st.error(f"Error: {e}")