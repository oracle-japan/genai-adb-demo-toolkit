import os
from typing import Dict
from dotenv import load_dotenv

import streamlit as st

from module.oci_generative_ai import OciGenerativeAi

def initialize_config() -> Dict:
    """Initialize configs"""
    _ = load_dotenv()
    # for Oracle Database 23ai
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    dsn = os.getenv("DSN")
    config_dir = os.getenv("CONFIG_DIR")
    wallet_dir = os.getenv("WALLET_DIR")
    wallet_password = os.getenv("WALLET_PASSWORD")
    table_name = os.getenv("TABLE_NAME")
    # for OCI Generative AI Service
    compartment_id = os.getenv("COMPARTMENT_ID")
    service_endpoint = os.getenv("SERVICE_ENDPOINT")
    return {
        "username": username,
        "password": password,
        "dsn": dsn,
        "config_dir": config_dir,
        "wallet_dir": wallet_dir,
        "wallet_password": wallet_password,
        "table_name": table_name,
        "compartment_id": compartment_id,
        "service_endpoint": service_endpoint
    }

config = initialize_config()

st.title("Chatbot demo")
st.caption("""
    OCI Generative AI Service と Oracle Database 23ai(ADB-S) を用いた RAG 構成のチャットボットです。 
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar.container():
    with st.sidebar:
        st.sidebar.markdown("## Vector Search Options")
        is_vector_search = st.sidebar.radio(label="Use Vector Search", options=[True, False], horizontal=True)
        fetch_k = st.sidebar.slider(label="Fetch k", min_value=1, max_value=20, value=3, step=1)
        st.sidebar.markdown("## LLM Options")
        model_name = st.sidebar.selectbox(label="Model Name", options=["cohere.command-r-plus", "cohere.command-r-16k"])
        is_stream = st.sidebar.radio(label="Streaming", options=[True, False], horizontal=True)
        max_tokens = st.sidebar.number_input(label="Max Tokens", min_value=10, max_value=1024, value=500, step=1)
        temperature = st.sidebar.slider(label="Temperature", min_value=0.0, max_value=1.0, value=0.3, step=0.1)
        top_k = st.sidebar.slider(label="Top k", min_value=0, max_value=500, value=0, step=1)
        top_p = st.sidebar.slider(label="Top p", min_value=0.0, max_value=0.99, value=0.75, step=0.01)
        frequency_penalty = st.sidebar.slider(label="Frequency Penalty", min_value=0.0, max_value=1.0, value=0.0, step=0.1)
        presence_penalty = st.sidebar.slider(label="Presence Penalty", min_value=0.0, max_value=1.0, value=0.0, step=0.1)

chat_model = OciGenerativeAi(
    compartment_id=config.get("compartment_id"),
    service_endpoint=config.get("service_endpoint"),
    model_name=model_name,
    is_stream=is_stream,
    max_tokens=max_tokens,
    temperature=temperature,
    top_k=top_k,
    top_p=top_p,
    frequency_penalty=frequency_penalty,
    presence_penalty=presence_penalty,
)

if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        res = chat_model.chat(input=prompt, is_stream=is_stream, is_vector_search=is_vector_search)
        message = ""
        if is_stream == True:
            for chunk in res:
                message += chunk
                message_placeholder.markdown(message)
        else:
            message = message.join(list(res))
            print(message)
            message_placeholder.markdown(message)
        st.session_state.messages.append({"role": "assistant", "content": message})
