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
from utils import find_match
from dotenv import load_dotenv
import os

load_dotenv()

st.title("Chatbot-PTIK🤖")

# Set OpenAI API key from environment
openai.api_key = os.getenv('OPENAI_API_KEY')    

if 'responses' not in st.session_state:
    st.session_state['responses'] = []

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo, apa yang bisa kubantu?"}]


# Display chat messages from history on app rerun
for message_data in st.session_state.messages:
    with st.chat_message(message_data["role"]):
        st.markdown(message_data["content"])

# Initialize conversation chain
llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai.api_key)
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=2, return_messages=True)

system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question as truthfully as possible using the provided context, 
and if the answer is not contained within the text below, say 'Saya tidak mempunyai informasi mengenai pertanyaan itu. Sebaliknya tanyakan hal seputar PTIK tentang saya!'""")
human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")
prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# Function to set the theme based on the checkbox
def set_theme(is_night):
    if is_night:
        st.markdown("<style>body { background-color: rgb(20, 26, 34); color: white; }</style>", unsafe_allow_html=True)
    else:
        st.markdown("<style>body { background-color: #fafafa; color: black; }</style>", unsafe_allow_html=True)

# Sidebar layout
st.sidebar.markdown("<style>#switch { display: none; } .content { height: 25px; width: 45px; background-color: #c7d3d3; display: flex; align-items: center; border-radius: 50px; cursor: pointer; } .circle { height: 12px; width: 12px; margin-left: 4px; background-color: #f5f5f5; border-radius: 50%; box-shadow: 0 2px 2px rgba(0, 0, 0, 0.3); transition: 0.3s; }</style>", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.image("img/unimed.png", use_column_width=True)

    st.markdown("<p style='text-align: justify'>Proyek ini bertujuan menjembatani komunikasi antara mahasiswa dengan pihak kampus agar dapat memahami informasi mengenai kampus, serta menyediakan platform digital sebagai helpdesk untuk berbagi informasi secara cepat.</p>", unsafe_allow_html=True)
    
    checkbox_value = st.checkbox("Show more information")
    if checkbox_value:
        st.write("""<details><summary>Fitur Utama</summary><ul>
            <li>Tanyakan informasi jurusan: Kamu bisa menanyakan info tentang mengakses AKAD, Mengisi KRS, Pendaftaran KKN, Pendaftaran PLP maupun Sidang PKLI loh!</li>
            <li>Multi Bahasa: Chatbot ini mendukung beberapa bahasa. Kamu dapat mencobanya dengan memasukkan pertanyaan dengan bahasa asing!</li>
            <li>Mode Malam: Kamu bisa merubah tampilan chatbot ini ke mode gelap!</li>
            </ul></details>""", unsafe_allow_html=True)
        
        st.write("""<details><summary>Pengembang</summary><p>Anggota Tim</p><ul>
            <li>Afif Hamzah (5213151004)</li>
            <li>Julio Aldrin Purba (5213151003)</li>
            <li>Gracia Napare Sihombing (5213151010)</li>
            </ul><p>Dosen Pembimbing </p><ul>
            <li>Bakti Dwi Waluyo, S.Pd., M.T. (199003272019031009)</li>
            </ul></details>""", unsafe_allow_html=True)

    is_night = st.sidebar.checkbox("Toggle Dark Mode", value=False, key="dark_mode")
    set_theme(is_night)

def format_response_with_spacing(response, lines_per_spacing=7):
    lines = response.splitlines()
    formatted_response = ""
    
    for i in range(0, len(lines), lines_per_spacing):
        group = lines[i:i + lines_per_spacing]
        formatted_response += "\n".join(group) + "\n\n"

    return formatted_response.strip()

# Accept user input
if prompt := st.chat_input("Bagaimana cara isi KRS?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Search for context in Pinecone database
    context = find_match(prompt)

    if context:
        # Log the context for debugging
        print(f"Retrieved context: {context}")
        
        # Get a response from OpenAI based on the found context 
        response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{prompt}")
        formatted_response = format_response_with_spacing(response)
    else:
        print("No context found for the query.")
        formatted_response = "Saya tidak mempunyai informasi mengenai hal itu. Namun, untuk pertanyaan tentang KRS, Anda bisa menghubungi bagian akademik."

    st.session_state.messages.append({"role": "assistant", "content": formatted_response})

    with st.chat_message("assistant"):
        st.markdown(formatted_response)

def get_conversation_string():
    if 'responses' in st.session_state:
        return ' '.join(st.session_state['responses'])
    return ""

conversation_string = get_conversation_string()
st.write(conversation_string)
