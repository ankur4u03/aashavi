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
# CUSTOM CSS
# =========================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* MAIN BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #050816, #0b1026);
    color: white;
}

/* REMOVE HEADER */
header {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    display: none;
}

/* TITLE */
.main-title {
    text-align: center;
    font-size: 58px;
    font-weight: 700;
    color: white;
    margin-top: 20px;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 20px;
    margin-bottom: 40px;
}

/* CHAT BOX */
.stChatMessage {
    border-radius: 18px;
    padding: 12px;
    margin-bottom: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(10px);
}

/* INPUT BOX */
[data-testid="stChatInput"] {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 75%;
}

[data-testid="stChatInput"] textarea {
    background: #111827 !important;
    color: white !important;
    border-radius: 18px !important;
    border: 2px solid #7c3aed !important;
    padding: 16px !important;
    font-size: 16px !important;
}

/* MOBILE RESPONSIVE */
@media (max-width: 768px) {

    .main-title {
        font-size: 42px;
        margin-top: 10px;
    }

    .subtitle {
        font-size: 16px;
        padding: 0 10px;
    }

    [data-testid="stChatInput"] {
        width: 92%;
        bottom: 10px;
    }

    [data-testid="stChatInput"] textarea {
        font-size: 15px !important;
        padding: 14px !important;
    }

    .stChatMessage {
        padding: 10px;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# API KEY
# =========================

genai.configure(
    api_key=st.secrets["GOOGLE_API_KEY"]
)

# =========================
# TITLE
# =========================

st.markdown("""
<div class="main-title">
✨ Gemini AI Assistant
</div>

<div class="subtitle">
Fast • Smart • Modern AI Chatbot
</div>
""", unsafe_allow_html=True)

# =========================
# CHAT HISTORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []

# SHOW OLD MESSAGES

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# CHAT INPUT
# =========================

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

            model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

            response = model.generate_content(prompt)

            reply = response.text

            st.markdown(reply)

            # SAVE AI MESSAGE
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply
                }
            )

        except Exception as e:

            st.error(f"Error: {e}")