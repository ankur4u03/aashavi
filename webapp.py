import streamlit as st
import google.generativeai as genai

# ============================================
# GEMINI API
# ============================================

genai.configure(
    api_key=st.secrets["AIzaSyAXsEN8dC7z-PhNzLBB-Lk0Db3KfxNq8hI"]
)


# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="✨",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

/* MAIN APP */
.stApp{
    background: linear-gradient(135deg,#020617,#0f172a,#111827);
    color: white;
    overflow-x:hidden;
}

/* REMOVE DEFAULT SPACE */
.block-container{
    padding-top: 2rem;
    padding-bottom: 8rem;
    max-width: 1000px;
}

/* SIDEBAR */
section[data-testid="stSidebar"]{
    background: rgba(15,23,42,0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] *{
    color:white;
}

/* TITLE */
.main-title{
    text-align:center;
    font-size:72px;
    font-weight:800;
    color:white;
    margin-top:20px;
    line-height:1;
}

/* SUBTITLE */
.sub-title{
    text-align:center;
    color:#94a3b8;
    font-size:22px;
    margin-top:10px;
    margin-bottom:50px;
}

/* CHAT MESSAGE */
.stChatMessage{
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 12px;
    margin-bottom: 18px;
    backdrop-filter: blur(10px);
}

/* CHAT TEXT */
[data-testid="stChatMessageContent"] p{
    color:white;
    font-size:16px;
}

/* INPUT CONTAINER */
[data-testid="stChatInput"]{
    position: fixed;
    bottom: 20px;
    left: 340px;
    right: 30px;
    width: auto;
    z-index: 999;
}

/* INPUT BOX */
[data-testid="stChatInput"] textarea{
    background: rgba(15,23,42,0.95) !important;
    color: white !important;
    border-radius: 18px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    padding: 14px !important;
    font-size:16px !important;
}

/* BUTTON */
.stButton button{
    width:100%;
    border:none;
    border-radius:14px;
    background: linear-gradient(135deg,#2563eb,#7c3aed);
    color:white;
    font-size:16px;
    font-weight:600;
    padding:12px;
    transition:0.3s;
}

/* BUTTON HOVER */
.stButton button:hover{
    transform:scale(1.03);
    background: linear-gradient(135deg,#1d4ed8,#6d28d9);
}

/* SCROLLBAR */
::-webkit-scrollbar{
    width:10px;
}

::-webkit-scrollbar-track{
    background:#0f172a;
}

::-webkit-scrollbar-thumb{
    background:#334155;
    border-radius:10px;
}

/* MOBILE */
@media(max-width:768px){

    .main-title{
        font-size:42px;
    }

    .sub-title{
        font-size:16px;
    }

    [data-testid="stChatInput"]{
        width:95%;
    }
}

</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.title("🤖 Gemini AI")

    st.write("Modern AI Chatbot")

    st.write("Made by Ankur 🚀")

    st.divider()

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ============================================
# TITLE
# ============================================

st.markdown("""
<div class="main-title">
✨ Gemini AI Assistant
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sub-title">
Fast • Smart • Modern AI Chatbot
</div>
""", unsafe_allow_html=True)

# ============================================
# CHAT HISTORY
# ============================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ============================================
# USER INPUT
# ============================================

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

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(prompt)

        reply = response.text

        st.markdown(reply)

    except Exception as e:

        st.error(f"Error: {e}")