import streamlit as st
import google.generativeai as genai

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="✨",
    layout="wide"
)

# =========================
# GEMINI API
# =========================

genai.configure(
    api_key="AIzaSyAXsEN8dC7z-PhNzLBB-Lk0Db3KfxNq8hI"
)

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(to bottom right, #020617, #0f172a);
    color: white;
}

/* REMOVE STREAMLIT HEADER */
header {
    visibility: hidden;
}

/* REMOVE FOOTER */
footer {
    visibility: hidden;
}

/* MAIN TITLE */
.main-title {
    text-align: center;
    font-size: 60px;
    font-weight: 800;
    color: white;
    margin-top: 20px;
    margin-bottom: 10px;
}

.sub-title {
    text-align: center;
    font-size: 20px;
    color: #94a3b8;
    margin-bottom: 40px;
}

/* CHAT MESSAGE */
.stChatMessage {
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 16px;
}

/* INPUT BOX FIX */
.stChatInput {
    position: fixed;
    bottom: 20px;
    left: 320px;
    right: 30px;
    background: transparent;
}

/* TEXTAREA */
[data-testid="stChatInput"] textarea {
    background: rgba(15, 23, 42, 0.95) !important;
    color: white !important;
    border-radius: 18px !important;
    border: 1px solid #334155 !important;
    padding: 18px !important;
    font-size: 17px !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #081126;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* SIDEBAR TEXT */
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
}

.stButton button:hover {
    opacity: 0.9;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================

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

# =========================
# HERO SECTION
# =========================

st.markdown("""
<div class="main-title">
✨ Gemini AI Assistant
</div>

<div class="sub-title">
Fast • Smart • Modern AI Chatbot
</div>
""", unsafe_allow_html=True)

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
# CHAT INPUT
# =========================

prompt = st.chat_input("Ask anything...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

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