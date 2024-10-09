import os
import fitz  # PyMuPDF for PDF processing
import openai
from dotenv import load_dotenv
import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_core.documents import Document
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

pinecone_api_key = os.getenv('PINECONE_API_KEY')
pc = Pinecone(api_key=pinecone_api_key)

index_name = "knowledgebase-ptik"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MPNet-base-v2')

pdf_dir = os.path.join('knowledgebase')
documents = []

for file_name in os.listdir(pdf_dir):
    if file_name.endswith('.pdf'):
        file_path = os.path.join(pdf_dir, file_name)
        try:
            with fitz.open(file_path) as pdf_file:
                text = ""
                for page_num in range(pdf_file.page_count):
                    page = pdf_file.load_page(page_num)
                    text += page.get_text()
                if text:
                    documents.append(Document(page_content=text, metadata={"source": file_name}))
                else:
                    print(f"No text found in {file_name}")
        except Exception as e:
            print(f"Error reading {file_name}: {e}")

print(f"Loaded {len(documents)} documents from PDFs.")

try:
    index = LangchainPinecone.from_documents(documents=documents, embedding=embeddings, index_name=index_name)
    print("Documents uploaded to Pinecone successfully.")
except Exception as e:
    print(f"Error initializing Pinecone index: {e}")

openai_api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = openai_api_key

def find_match(query):
    result = index.similarity_search(query, k=5)

    if result:
        combined_content = "\n\n".join([res.page_content for res in result])
        return combined_content
    else:
        return "Saya tidak mempunyai informasi mengenai hal itu."
# Function to refine the user query
def query_refiner(conversation, query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Refine the user query to be more relevant."},
            {"role": "user", "content": f"CONVERSATION LOG: \n{conversation}\n\nQuery: {query}"}
        ],
        temperature=0.7,
        max_tokens=1500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['message']['content']

# Function to get the conversation history as a string
def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])):
        if i < len(st.session_state['requests']):
            conversation_string += "User: " + st.session_state['requests'][i] + "\n"
        if i < len(st.session_state['responses']):
            conversation_string += "Bot: " + st.session_state['responses'][i] + "\n"
    return conversation_string
