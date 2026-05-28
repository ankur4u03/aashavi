import streamlit as st
import os
from groq import Groq

# PAGE CONFIG
st.set_page_config(
    page_title="Aashvi AI",
    page_icon="🌸",
    layout="centered"
)

# HIDE STREAMLIT BRANDING + BADGES
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
    visibility: hidden;
    height: 0%;
    position: fixed;
}

.stDeployButton {
    display: none;
}

.viewerBadge_container__1QSob,
.styles_viewerBadge__1yB5_,
.viewerBadge_link__1S137 {
    display: none !important;
}

.stApp {
    background: linear-gradient(to bottom, #050816, #0b1026);
    color: white;
}

.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: white;
    margin-top: 20px;
}

.sub-title {
    text-align: center;
    color: #b0b3c7;
    font-size: 18px;
    margin-bottom: 40px;
}

.chat-user {
    background-color: #ff7849;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: white;
}

.chat-ai {
    background-color: #1b2338;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: white;
}

.stChatInput input {
    background-color: #111827 !important;
    color: white !important;
}

</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# API KEY
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# TITLE
st.markdown(
    "<h1 class='main-title'>🌸 Aashvi AI</h1>",
    unsafe_allow_html=True
)

# SUBTITLE
st.markdown(
    "<p class='sub-title'>Think Faster with Aashvi AI ⚡</p>",
    unsafe_allow_html=True
)

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []

# SHOW CHAT HISTORY
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# USER INPUT
prompt = st.chat_input("Ask anything...")

if prompt:

    # SAVE USER MESSAGE
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # SHOW USER MESSAGE
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI RESPONSE
    with st.chat_message("assistant"):

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

            st.markdown(reply)

            # SAVE AI RESPONSE
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

        except Exception as e:

            st.error(f"Error: {e}")