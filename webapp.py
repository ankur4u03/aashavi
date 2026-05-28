import streamlit as st
import os
from groq import Groq

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="Aashvi AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# GROQ CLIENT
# =====================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =====================================
# SESSION STATE
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

/* HIDE STREAMLIT */

#MainMenu,
footer,
header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"]{
    display:none !important;
}

/* APP */

.stApp{
    background:#0f172a;
    color:white;
}

/* MAIN CONTAINER */

.block-container{
    max-width:1000px;
    padding-top:2rem;
    padding-bottom:7rem;
}

/* TITLE */

.main-title{
    text-align:center;
    font-size:72px;
    font-weight:800;
    color:white;
    margin-top:30px;
}

.sub-title{
    text-align:center;
    color:#cbd5e1;
    font-size:24px;
    margin-bottom:50px;
}

/* USER CHAT */

.user-msg{
    background:#2563eb;
    color:white;
    padding:16px 22px;
    border-radius:22px;
    width:fit-content;
    max-width:75%;
    margin-left:auto;
    margin-top:18px;
    margin-bottom:18px;
    font-size:17px;
    word-wrap:break-word;
    box-shadow:0px 4px 15px rgba(37,99,235,0.25);
}

/* AI CHAT */

.ai-msg{
    background:#1e293b;
    color:white;
    padding:16px 22px;
    border-radius:22px;
    width:fit-content;
    max-width:75%;
    margin-right:auto;
    margin-top:18px;
    margin-bottom:18px;
    font-size:17px;
    line-height:1.7;
    word-wrap:break-word;
}

/* CHAT INPUT */

.stChatInput{
    position:fixed;
    bottom:18px;
    left:50%;
    transform:translateX(-50%);
    width:90%;
    max-width:900px;
}

.stChatInput input{
    background:#1e293b !important;
    color:white !important;
    border:none !important;
    border-radius:18px !important;
    padding:18px !important;
    font-size:16px !important;
}

/* MOBILE */

@media (max-width:768px){

    .main-title{
        font-size:46px;
        margin-top:10px;
    }

    .sub-title{
        font-size:18px;
        margin-bottom:30px;
    }

    .user-msg,
    .ai-msg{
        max-width:90%;
        font-size:15px;
        padding:14px 18px;
    }

    .stChatInput{
        width:95%;
        bottom:10px;
    }
}

</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================

if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div class='main-title'>
            🌸 Aashvi AI
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class='sub-title'>
            Think Faster with Aashvi AI ⚡
        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================
# CHAT HISTORY
# =====================================

for message in st.session_state.messages:

    if message["role"] == "user":

        st.markdown(
            f"""
            <div class='user-msg'>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class='ai-msg'>
                {message["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# =====================================
# CHAT INPUT
# =====================================

prompt = st.chat_input("Ask anything...")

# =====================================
# AI RESPONSE
# =====================================

if prompt:

    # SAVE USER MESSAGE

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    # SHOW USER MESSAGE

    st.markdown(
        f"""
        <div class='user-msg'>
            {prompt}
        </div>
        """,
        unsafe_allow_html=True
    )

    try:

        # AI RESPONSE

        completion = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=st.session_state.messages,

            temperature=0.7,

            max_tokens=1024
        )

        reply = completion.choices[0].message.content

        # SHOW AI MESSAGE

        st.markdown(
            f"""
            <div class='ai-msg'>
                {reply}
            </div>
            """,
            unsafe_allow_html=True
        )

        # SAVE AI MESSAGE

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":reply
            }
        )

    except Exception as e:

        st.error(f"Error: {e}")