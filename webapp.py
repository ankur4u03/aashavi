import streamlit as st
import google.generativeai as genai

# =========================
# GEMINI API
# =========================

genai.configure(
    api_key="AIzaSyAO-SRIAMQvuUl1D7FCAd-3rAzKhkwnJTE"
)

model = genai.GenerativeModel("gemini-1.5-flash")

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# =========================
# HIDE STREAMLIT THINGS
# =========================

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}

html, body, [class*="css"] {
    font-family: sans-serif;
}

.stApp{
    background: linear-gradient(135deg,#0f172a,#111827,#1e293b);
    color:white;
}

.main-title{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    color:white;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    margin-bottom:30px;
}

.stChatMessage{
    background: rgba(255,255,255,0.05);
    border-radius:20px;
    padding:10px;
    margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("🤖 Gemini AI")
    st.write("Made by Ankur 🚀")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# =========================
# TITLE
# =========================

st.markdown(
    "<div class='main-title'>✨ Gemini AI Assistant</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Fast • Smart • AI Chatbot</div>",
    unsafe_allow_html=True
)

# =========================
# CHAT HISTORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# INPUT
# =========================

prompt = st.chat_input("Ask anything...")

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

            st.error(e)