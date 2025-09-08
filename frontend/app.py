import requests
import streamlit as st
import os

API_URL = os.getenv("API_URL")
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

# Header section
st.title("🏛️ Portugal Self-Employeers Assistant")
st.subheader("Your digital guide for self-employment in Portugal")
st.markdown("Get answers about Social Security, Taxes, and labor regulations in Portugal.")
st.divider()

# Question examples section
with st.sidebar:
    st.markdown("### 💡 How to use")
    st.info("✍️ **Write your question** in the chat below")
    st.info("🤖 **Get answers** from the AI assistant")
    st.divider()
    st.markdown("### ❓ Example questions")
    st.markdown(
        """
    - *What are the steps to register as self-employed in Portugal?*
    - *How do I calculate my social security contributions?*
    - *What tax deductions can I claim as a freelancer?*
    - *How often do I need to file my taxes?*
    - *What are the penalties for late tax payments?*
    """
    )
    st.divider()
    st.markdown("### ⚠️ Disclaimer")
    st.markdown(
        """
    This assistant provides general information and is not a substitute for professional legal or financial advice. Always consult with a qualified expert for specific guidance.
    """
    )

# Chat section
# Display chat messages from history on app rerun
st.markdown("### 💬 Chat with the AI Assistant")
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
