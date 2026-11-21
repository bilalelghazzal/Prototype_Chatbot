# 1. Imports and page setup: load the libraries used by the chat app.
from openai import OpenAI
import streamlit as st

# Configure the Streamlit page and show the chatbot heading.
st.set_page_config(page_title="StreamlitChatMessageHistory", page_icon="💬")
st.title("Chatbot")


# 2. Gemini client configuration: connect through Google's OpenAI-compatible API.
client = OpenAI(
    api_key=st.secrets["Google_Api_Key"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# model 
MODEL = "gemini-flash-latest"

# 1. Keep the conversation across reruns
if "messages" not in st.session_state:
    st.session_state.messages=[]

# hanlde new history 
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
#handle new meassge :

if prompt := st.chat_input("Your response"):
    st.session_state.messages.append({"role":"user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=MODEL,
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})