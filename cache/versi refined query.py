from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *
from dotenv import load_dotenv

load_dotenv()

st.title("Judul Projek")


# Set OpenAI API key from Streamlit secrets
openai.api_key = os.getenv('OPENAI_API_KEY')

if 'responses' not in st.session_state:
    st.session_state['responses'] = []

# Set a default model
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
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="")
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
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Process the input with query refinement and context retrieval
    conversation_string = get_conversation_string()
    refined_query = query_refiner(conversation_string, prompt)
    st.subheader("Refined Query:")
    st.write(refined_query)
    context = find_match(refined_query)

    # Get the response from the conversation chain
    response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{prompt}")

    # Add the response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display the response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

def get_conversation_string():
    if 'responses' in st.session_state:
        return ' '.join(st.session_state['responses'])
    return ""
# Menampilkan string percakapan
conversation_string = get_conversation_string()
st.write(conversation_string)