import streamlit as st
from google import genai

# =========================
# GEMINI CLIENT
# =========================

client = genai.Client(
    api_key="AIzaSyAO-SRIAMQvuUl1D7FCAd-3rAzKhkwnJTE"
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

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
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

/* MAIN TITLE */

.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: white;
    margin-top: 20px;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 20px;
    margin-bottom: 40px;
}

/* CHAT MESSAGE */

.stChatMessage {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(12px);
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
    width: 60%;
}

[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    padding: 15px !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* BUTTON */

.stButton button {
    width: 100%;
    border-radius: 15px;
    background: #2563eb;
    color: white;
    border: none;
    padding: 10px;
    font-size: 16px;
}

.stButton button:hover {
    background: #1d4ed8;
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
    "<div class='subtitle'>Fast • Smart • Modern AI Chatbot powered by Gemini 🚀</div>",
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
# CHAT LOGIC
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

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        reply = response.text

        st.markdown(reply)

    # SAVE RESPONSE
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })