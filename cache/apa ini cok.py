# main.py
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import openai
import streamlit as st
from streamlit_chat import message
from utils import find_match, get_conversation_string  # Ensure this import is correct
from dotenv import load_dotenv
import os

load_dotenv()

st.title("Judul Projek")

# Set OpenAI API key from environment
openai.api_key = os.getenv('OPENAI_API_KEY')

# Initialize session state variables
if 'responses' not in st.session_state:
    st.session_state['responses'] = []
if 'requests' not in st.session_state:  # Initialize requests list
    st.session_state['requests'] = []
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How can I assist you?"}]

# Display chat messages from history on app rerun
for message_data in st.session_state.messages:
    with st.chat_message(message_data["role"]):
        st.markdown(message_data["content"])

# Initialize conversation chain
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai.api_key)
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
and if the answer is not contained within the text below, say 'I don't know'""")
human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.requests.append(prompt)  # Add to requests

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Search for context in Pinecone database
    context = find_match(prompt)  # Use the user's input directly

    # Include the entire conversation history in the context
    full_conversation_context = get_conversation_string()  # Ensure this function is accessible

    if context:
        # Get a response from OpenAI based on the found context
        response = conversation.predict(input=f"Context:\n {full_conversation_context} \n\n Query:\n{prompt}")
    else:
        # If no context found, provide a default message
        response = "Saya tidak mempunyai informasi mengenai hal itu."

    # Add the response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    # st.session_state.responses.append(response)  # Add to responses

    # Display the response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

# Menampilkan string percakapan
conversation_string = get_conversation_string()
st.write(conversation_string)
