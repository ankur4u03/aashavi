import streamlit as st

st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp{
    background: linear-gradient(135deg,#0f172a,#111827,#1e293b);
    color:white;
}

.main-title{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    color:white;
    margin-top:20px;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    font-size:20px;
    margin-bottom:40px;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.title("🤖 Gemini AI")
    st.write("Made by Ankur 🚀")

    st.divider()

    st.button("🗑 Clear Chat")

st.markdown(
    "<div class='main-title'>✨ Gemini AI Assistant</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Fast • Smart • Modern AI Chatbot powered by Gemini 🚀</div>",
    unsafe_allow_html=True
)

st.chat_input("Ask anything...")