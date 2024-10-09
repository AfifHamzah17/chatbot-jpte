# from langchain.chat_models import ChatOpenAI
# from langchain.chains import ConversationChain
# from langchain.chains.conversation.memory import ConversationBufferWindowMemory
# from langchain.prompts import (
#     SystemMessagePromptTemplate,
#     HumanMessagePromptTemplate,
#     ChatPromptTemplate,
#     MessagesPlaceholder
# )
# import openai
# import streamlit as st
# from streamlit_chat import message
# from utils import find_match
# from dotenv import load_dotenv
# import os

# load_dotenv()

# st.title("Chatbot-PTIK🤖")

# if 'responses' not in st.session_state:
#     st.session_state['responses'] = []

# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"

# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "assistant", "content": "Halo, apa yang bisa kubantu?"}]

# for message_data in st.session_state.messages:
#     with st.chat_message(message_data["role"]):
#         st.markdown(message_data["content"])

# if "messages" not in st.session_state:
#     st.session_state.messages = [{"role": "assistant", "content": "Halo, apa yang bisa kubantu?"}]

# for message_data in st.session_state.messages:
#     with st.chat_message(message_data["role"]):
#         st.markdown(message_data["content"])

# llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai.api_key)
# if 'buffer_memory' not in st.session_state:
#     st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

# system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
# and if the answer is not contained within the text below, say 'I don't know'""")
# human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
# prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

# st.sidebar.markdown(
#     """
#     <style>
#     /* Custom CSS for sidebar styling */
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# if prompt := st.chat_input("Bang, tutorial isi akad ada?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})

# context = find_match(prompt)  # Use the user's input directly

# if context:
#     response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{prompt}")
# else:
#     response = "Saya tidak mempunyai informasi mengenai hal itu."

# st.session_state.messages.append({"role": "assistant", "content": response})

# with st.chat_message("assistant"):
#     st.markdown(response)

# def get_conversation_string():
#     if 'responses' in st.session_state:
#         return ' '.join(st.session_state['responses'])
#     return ""
