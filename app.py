import streamlit as st
from llama_index import GPTSimpleVectorIndex, Document

# Charger l'index depuis le fichier JSON
index = GPTSimpleVectorIndex.load_from_disk('index.json')

st.title("Chatbot avec LlamaIndex")

query = st.text_input("Pose-moi une question :")

if query:
    response = index.query(query)
    st.write(f"Réponse : {response.response}")
