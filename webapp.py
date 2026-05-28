import streamlit as st
from groq import Groq

# PAGE CONFIG
st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="✨",
    layout="centered"
)

# API KEY
import os
from groq import Groq

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# CUSTOM CSS
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to bottom, #050816, #0b1026);
    color: white;
}

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    margin-top: 20px;
}

.subtitle {
    text-align: center;
    color: #a0a0a0;
    margin-bottom: 40px;
}

.chat-box {
    padding: 15px;
    border-radius: 15px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# TITLE
st.markdown(
    "<div class='main-title'>✨ Gemini AI Assistant</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Fast • Smart • Modern AI Chatbot</div>",
    unsafe_allow_html=True
)

# CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# SHOW OLD MESSAGES
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# USER INPUT
prompt = st.chat_input("Ask anything...")

if prompt:

    # USER MESSAGE
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

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

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:
            st.error(f"Error: {e}")