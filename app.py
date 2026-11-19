from openai import OpenAI
import streamlit as st

# Setting up the Streamlit page configuration
st.set_page_config(page_title="StreamlitChatMessageHistory", page_icon="💬")
st.title("Chatbot")

st.title("Chatbot")

client = OpenAI(
    api_key=st.secrets["Google_Api_Key"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

if "googlemodel" not in st.session_state:
    st.session_state.googlemodel = "gemini-3.5-flash-lite"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Your answer:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model=st.session_state.googlemodel,
                messages=[
                    {
                        "role": message["role"],
                        "content": message["content"],
                    }
                    for message in st.session_state.messages
                ],
            )
            answer = response.choices[0].message.content
            st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
    except Exception as exc:
        st.error(f"Unable to get a response: {exc}")
