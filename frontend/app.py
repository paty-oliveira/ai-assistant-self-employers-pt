import requests
import streamlit as st

API_URL = "http://api:80"
ENDPOINT = "/query"


def query_ai_assistant(prompt):
    try:
        response = requests.post(
            API_URL + ENDPOINT,
            json={"query": prompt, "index_name": "rag_index_test"},
            headers={"Content-Type": "application/json"},
        )

        if response.status_code == 200:
            data = response.json()
            return data["response"]

        else:
            return "Not able to get a response from the AI assistant."

    except requests.exceptions.RequestException:
        return f"Error: {response.status_code}, {response.text}"


def generate_stream(response):
    for word in response.split(" "):
        yield word + " "


# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("AI-Assistant for Self-Employeers in Portugal")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me a question!"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from AI assistant
    with st.spinner("AI Assistant is getting your answer..."):
        response = query_ai_assistant(prompt)

    stream = generate_stream(response)
    with st.chat_message("assistant"):
        st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
