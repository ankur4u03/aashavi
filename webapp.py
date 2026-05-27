import streamlit as st
import google.generativeai as genai

# =========================
# GEMINI API CONFIG
# =========================

genai.configure(
    api_key="AIzaSyAO-SRIAMQvuUl1D7FCAd-3rAzKhkwnJTE"
)

model = genai.GenerativeModel(
    "models/gemini-1.5-flash"
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
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

.stDeployButton {
    display:none;
}

html, body, [class*="css"] {
    font-family: sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
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

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 20px;
    margin-bottom: 40px;
}

/* CHAT */

.stChatMessage {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 15px;
}

/* INPUT BOX */

[data-testid="stChatInput"] {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 70%;
}

[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
}

/* BUTTON */

.stButton button {
    width: 100%;
    border-radius: 15px;
    background: #2563eb;
    color: white;
    border: none;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("🤖 Gemini AI")

    st.write("Modern AI Chatbot")
    st.write("Made by Ankur 🚀")

    st.divider()

    if st.button("🗑 Clear Chat"):
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

# =========================
# SHOW OLD MESSAGES
# =========================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# =========================
# USER INPUT
# =========================

prompt = st.chat_input("Ask anything...")

# =========================
# CHATBOT LOGIC
# =========================

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

            response = model.generate_content(prompt)

            reply = response.text

            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:

            st.error(e)