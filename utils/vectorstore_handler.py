import os
import streamlit as st

from utils.pdf_handler import get_pdf_text, get_text_chunks
from utils.config import MODEL_OPTIONS

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


PERSIST_DIR = {
    key.lower(): f"./data/{key.lower()}_vector_store.chroma"
    for key in MODEL_OPTIONS.keys()
}


@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2"
    )


def get_or_create_vectorstore(uploaded_files, model_provider):

    if not uploaded_files:
        return None

    raw_text = get_pdf_text(uploaded_files)

    chunks = get_text_chunks(raw_text)

    embedding = get_embeddings()

    persist_path = PERSIST_DIR[model_provider]

    # Load existing collection
    vectorstore = Chroma(
        persist_directory=persist_path,
        embedding_function=embedding
    )

    # Remove ALL old chunks
    try:
        existing = vectorstore.get()

        if existing and existing.get("ids"):
            vectorstore.delete(existing["ids"])

    except Exception:
        pass

    # Add fresh chunks only
    vectorstore.add_texts(chunks)

    # DEBUG
    print("\n========== INDEXED PDFs ==========")

    for file in uploaded_files:
        print(file.name)

    print(f"Total chunks indexed: {len(chunks)}")

    print("=================================\n")

    return vectorstore