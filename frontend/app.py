import json
import os

import requests
import streamlit as st

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

# Read website content config
with open("content.json", "r") as config:
    content = json.load(config)

language = "en"
if st.context.locale in ["pt-PT", "pt-BR"]:
    language = "pt"

head_content = content[language]["head"]
st.set_page_config(
    page_title=head_content["title"], page_icon=":robot:", initial_sidebar_state="expanded"
)

# Header section
header_content = content[language]["header"]

st.title(header_content["title"])
st.subheader(header_content["subheader"])
st.markdown(header_content["description"])
st.divider()

# Question examples section
sidebar_content = content[language]["sidebar"]

with st.sidebar:
    st.markdown(sidebar_content["info_panel"]["title"])
    for instruction in sidebar_content["info_panel"]["steps"]:
        st.info(instruction)
    st.divider()
    st.markdown(sidebar_content["freq_questions"]["title"])
    for question in sidebar_content["freq_questions"]["questions"]:
        st.markdown(f"- {question}")
    st.divider()
    st.markdown(sidebar_content["disclaimer"]["title"])
    st.markdown(sidebar_content["disclaimer"]["content"])

# Chat section
chat_content = content[language]["chat"]

st.markdown(chat_content["title"])
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input(chat_content["placeholder"]):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from AI assistant
    with st.spinner(chat_content["spinner_content"]):
        response = query_ai_assistant(prompt)

    stream = generate_stream(response)
    with st.chat_message("assistant"):
        st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
