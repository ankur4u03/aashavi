import streamlit as st
import google.generativeai as genai

# ======================
# API KEY
# ======================

genai.configure(
    api_key="AIzaSyAO-SRIAMQvuUl1D7FCAd-3rAzKhkwnJTE"
)

# ======================
# MODEL
# ======================

model = genai.GenerativeModel("gemini-pro")

# ======================
# PAGE CONFIG
# ======================

st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ======================
# CSS
# ======================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
background: linear-gradient(135deg,#0f172a,#111827,#1e293b);
color:white;
}

.main-title{
text-align:center;
font-size:60px;
font-weight:bold;
margin-top:20px;
}

.subtitle{
text-align:center;
font-size:20px;
color:#cbd5e1;
margin-bottom:40px;
}

.stChatMessage{
background:rgba(255,255,255,0.05);
padding:15px;
border-radius:20px;
margin-bottom:15px;
}

[data-testid="stChatInput"]{
position:fixed;
bottom:20px;
left:50%;
transform:translateX(-50%);
width:70%;
}

</style>
""", unsafe_allow_html=True)

# ======================
# TITLE
# ======================

st.markdown(
"<div class='main-title'>✨ Gemini AI Assistant</div>",
unsafe_allow_html=True
)

st.markdown(
"<div class='subtitle'>Fast • Smart • AI Chatbot</div>",
unsafe_allow_html=True
)

# ======================
# SESSION
# ======================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
# OLD MESSAGES
# ======================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ======================
# INPUT
# ======================

prompt = st.chat_input("Ask anything...")

# ======================
# CHATBOT
# ======================

if prompt:

    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        try:

            response = model.generate_content(prompt)

            reply = response.text

            st.markdown(reply)

            st.session_state.messages.append({
                "role":"assistant",
                "content":reply
            })

        except Exception as e:

            st.error(f"Error: {e}")