import streamlit as st
import os
from groq import Groq

# PAGE CONFIG
st.set_page_config(
    page_title="Aashvi AI",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# HIDE STREAMLIT BRANDING
hide_streamlit_style = """
<style>

/* HIDE MENU + FOOTER + HEADER */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* HIDE TOOLBAR */

[data-testid="stToolbar"] {
    display: none !important;
}

/* HIDE TOP RIGHT DEPLOY BUTTON */

[data-testid="stDeployButton"] {
    display: none !important;
}

/* HIDE STREAMLIT BADGE */

.viewerBadge_container__1QSob {
    display: none !important;
}

.styles_viewerBadge__1yB5_ {
    display: none !important;
}

.viewerBadge_link__1S137 {
    display: none !important;
}

a[title="Hosted with Streamlit"] {
    display: none !important;
}

/* HIDE FLOATING BUTTON */

.stActionButton {
    display: none !important;
}

/* HIDE STATUS */

[data-testid="stStatusWidget"] {
    display: none !important;
}

/* REMOVE EXTRA SPACE */

.block-container {
    padding-top: 1rem;
}

/* APP BACKGROUND */

.stApp {
    background: linear-gradient(to bottom, #050816, #0b1026);
    color: white;
}

/* TITLE */

.main-title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: white;
    margin-top: 20px;
}

/* SUBTITLE */

.sub-title {
    text-align: center;
    color: #b0b3c7;
    font-size: 18px;
    margin-bottom: 40px;
}

/* CHAT INPUT */

.stChatInput input {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 12px;
}

/* CHAT MESSAGE */

.stChatMessage {
    background-color: #1b2338;
    border-radius: 15px;
    padding: 10px;
    margin-bottom: 10px;
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