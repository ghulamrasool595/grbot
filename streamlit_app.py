import streamlit as st
import google.generativeai as genai
import os

# Page config - RTL for Sindhi Arabic script
st.set_page_config(
    page_title="سنڌي چيٽ بوٽ",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for better UX (RTL, font, colors)
st.markdown("""
    <style>
        .stApp { direction: rtl; text-align: right; }
        .stChatMessage { direction: rtl; }
        textarea { direction: rtl; text-align: right; }
        .stButton>button { float: left; }
        @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
        body { font-family: 'Noto Nastaliq Urdu', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("🤖 سنڌي چيٽ بوٽ")
st.caption("توھان سان سنڌي ۾ ڳالھائڻ لاءِ تيار آهيان!")

# Get Gemini API key securely (use secrets on Streamlit Cloud)
if "gemini_api_key" not in st.session_state:
    api_key = st.text_input("Gemini API Key داخل ڪريو:", type="password", placeholder="ai.google.dev تان حاصل ڪريو")
    if api_key:
        st.session_state.gemini_api_key = api_key
        st.rerun()
else:
    genai.configure(api_key=st.session_state.gemini_api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "سلام! مان هڪ سنڌي چيٽ بوٽ آهيان. توهان سان ڳالهائڻ ۾ خوشي ٿيندي. ڪا به شيءِ پڇو!"}
    ]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("پنهنجو پيغام هتي لکو..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate bot response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("ٽائپ ڪري رهيو آهي..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                # Force response in Sindhi
                full_prompt = f"هميشه سنڌي ٻولي ۾ جواب ڏيو، سنڌي عربي رسم الخط ۾: {prompt}"
                
                response = model.generate_content(full_prompt)
                bot_response = response.text
                
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                error_msg = "معاف ڪجو، ڪا غلطي ٿي وئي. ٻيهر ڪوشش ڪريو."
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar extras
with st.sidebar:
    st.header("سيٽنگس")
    if st.button("چيٽ صاف ڪريو"):
        st.session_state.messages = [{"role": "assistant", "content": "سلام! مان هڪ سنڌي چيٽ بوٽ آهيان. توهان سان ڳالهائڻ ۾ خوشي ٿيندي."}]
        st.rerun()
    
    st.info("Gemini API مفت آهي (ai.google.dev تان حاصل ڪريو)")
    st.markdown("### بهتر UX لاءِ")
    st.markdown("- RTL support سنڌي لاءِ")
    st.markdown("- ٽائپنگ انڊيڪيٽر")
    st.markdown("- موبائل فرينڊلي")
