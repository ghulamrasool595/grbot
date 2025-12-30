import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="سنڌي چيٽ بوٽ", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
        .stApp { direction: rtl; text-align: right; }
        textarea { direction: rtl; text-align: right; }
        @import url('https://fonts.googleapis.com/css2?family=Noto+Nastaliq+Urdu:wght@400;700&display=swap');
        body { font-family: 'Noto Nastaliq Urdu', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("🤖 سنڌي چيٽ بوٽ")
st.caption("توھان سان سنڌي ۾ ڳالھائڻ لاءِ تيار آهيان!")

# Secure API key from secrets
try:
    genai.configure(api_key=st.secrets["gemini_api_key"])
except Exception as e:
    st.error("API Key نه مليو! .streamlit/secrets.toml ۾ gemini_api_key شامل ڪريو.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "سلام! مان هڪ سنڌي چيٽ بوٽ آهيان. ڪا به شيءِ پڇو!"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

if prompt := st.chat_input("پنهنجو پيغام هتي لکو..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("ٽائپ ڪري رهيو آهي..."):
            try:
                # Latest stable fast model (Dec 2025)
                model = genai.GenerativeModel("gemini-2.5-flash")
                
                full_prompt = f"هميشه سنڌي ٻولي ۾ جواب ڏيو، عربي رسم الخط ۾ استعمال ڪندي: {prompt}"
                response = model.generate_content(full_prompt)
                bot_response = response.text
                
                st.markdown(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                error_msg = "معاف ڪجو، غلطي ٿي وئي. ٻيهر ڪوشش ڪريو."
                st.markdown(error_msg + f" (تفصيل: {str(e)})")
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

with st.sidebar:
    st.header("سيٽنگس")
    if st.button("چيٽ صاف ڪريو"):
        st.session_state.messages = [{"role": "assistant", "content": "سلام! مان هڪ سنڌي چيٽ بوٽ آهيان."}]
        st.rerun()
    st.success("ماڊل: gemini-2.5-flash (تيز ۽ بهترين سنڌي سپورٽ)")
    st.info("نئون AIzaSyBNgs5XzdpKjn52ItZ48ZCO_31PXnZ7Ato ۾ رکو!")
