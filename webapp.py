import streamlit as st
import google.generativeai as genai

# =========================
# GEMINI API KEY
# =========================

genai.configure(
    api_key="AIzaSyAO-SRIAMQvuUl1D7FCAd-3rAzKhkwnJTE"
)

# =========================
# MODEL
# =========================

model = genai.GenerativeModel(
    "gemini-1.5-flash-latest"
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="✨",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* HIDE STREAMLIT */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* MAIN APP */

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
    color: white;
    font-family: sans-serif;
}

/* TITLE */

.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    margin-top: 20px;
    color: white;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 20px;
    margin-bottom: 40px;
}

/* CHAT MESSAGE */

.stChatMessage {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 15px;
    margin-bottom: 15px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* INPUT BOX */

[data-testid="stChatInput"] {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 70%;
}

/* INPUT TEXTAREA */

[data-testid="stChatInput"] textarea {
    background: rgba(255,255,255,0.08) !important;
    color: white !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.08);
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

    st.title("🧠 Gemini AI")

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
    """
    <div class='main-title'>
        ✨ Gemini AI Assistant
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class='subtitle'>
        Fast • Smart • AI Chatbot
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# CHAT HISTORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# SHOW OLD CHATS

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# =========================
# USER INPUT
# =========================

prompt = st.chat_input("Ask anything...")

# =========================
# CHATBOT
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

            st.error(f"Error: {e}")