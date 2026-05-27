import streamlit as st
import google.generativeai as genai

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="✨",
    layout="wide"
)

# ==========================================
# GEMINI API
# ==========================================

genai.configure(
    api_key="AIzaSyAxk68b44Dof-PWUjir9Sm3KBp2XE7hBcU"
)

model = genai.GenerativeModel("gemini-1.5-flash")

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

/* GLOBAL */

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* MAIN BACKGROUND */

.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

/* REMOVE STREAMLIT DEFAULT */

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* MAIN CONTAINER */

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 8rem;
    max-width: 1000px;
}

/* TITLE */

.main-title {
    text-align: center;
    font-size: 64px;
    font-weight: 800;
    color: white;
    margin-top: 20px;
    margin-bottom: 10px;
}

.sub-title {
    text-align: center;
    color: #94a3b8;
    font-size: 22px;
    margin-bottom: 40px;
}

/* CHAT MESSAGE */

.stChatMessage {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 18px;
    border-radius: 20px;
    margin-bottom: 18px;
    backdrop-filter: blur(12px);
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

/* INPUT TEXTAREA */

[data-testid="stChatInput"] textarea {
    background: rgba(15, 23, 42, 0.95) !important;
    color: white !important;
    border-radius: 18px !important;
    border: 1px solid #334155 !important;
    padding: 18px !important;
    font-size: 17px !important;
}

/* INPUT BOX FOCUS */

[data-testid="stChatInput"] textarea:focus {
    border: 1px solid #7c3aed !important;
    box-shadow: 0 0 15px rgba(124,58,237,0.4);
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #081126;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* SIDEBAR TITLE */

.sidebar-title {
    font-size: 34px;
    font-weight: bold;
    color: white;
    margin-top: 20px;
}

.sidebar-text {
    color: #94a3b8;
    font-size: 16px;
    margin-bottom: 10px;
}

/* BUTTON */

.stButton button {
    width: 100%;
    border-radius: 14px;
    height: 50px;
    border: none;
    background: linear-gradient(90deg,#7c3aed,#2563eb);
    color: white;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton button:hover {
    transform: scale(1.02);
    opacity: 0.95;
}

/* MOBILE RESPONSIVE */

@media (max-width: 768px) {

    .main-title {
        font-size: 46px !important;
        line-height: 1.2;
    }

    .sub-title {
        font-size: 18px !important;
    }

    .stChatInput {
        width: calc(100% - 16px);
        bottom: 10px;
    }

    .stChatMessage {
        padding: 14px;
    }

    .main .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-title">✨ Gemini AI</div>
    <div class="sidebar-text">Modern AI Chatbot</div>
    <div class="sidebar-text">Made by Ankur 🚀</div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        st.rerun()

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="main-title">
✨ Gemini AI Assistant
</div>

<div class="sub-title">
Fast • Smart • Modern AI Chatbot
</div>
""", unsafe_allow_html=True)

# ==========================================
# CHAT HISTORY
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# SHOW OLD MESSAGES

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ==========================================
# USER INPUT
# ==========================================

prompt = st.chat_input("Ask anything...")

if prompt:

    # SAVE USER MESSAGE

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # SHOW USER MESSAGE

    with st.chat_message("user"):

        st.markdown(prompt)

    # AI RESPONSE

    with st.chat_message("assistant"):

        try:

            response = model.generate_content(prompt)

            reply = response.text

            st.markdown(reply)

            # SAVE AI RESPONSE

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        except Exception as e:

            st.error(f"Error: {e}")