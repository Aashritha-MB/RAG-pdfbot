import streamlit as st

from utils.config import (
    OPENROUTER_API_KEY,
    GROQ_API_KEY,
    GOOGLE_API_KEY
)

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOpenAI


def get_llm_chain(model_provider, model, vectorstore):

    import streamlit as st

from utils.config import (
    OPENROUTER_API_KEY,
    GROQ_API_KEY,
    GOOGLE_API_KEY
)

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOpenAI


def get_llm_chain(model_provider, model, vectorstore):

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are a PDF Question Answering Assistant.

IMPORTANT RULES:

1. Answer ONLY from the provided context.
2. Do NOT use your own knowledge.
3. Do NOT guess.
4. Do NOT infer information that is not explicitly present.
5. If the answer is not found in the context, reply exactly:

"I don't know based on the uploaded documents."

6. If the context contains only partial information, answer only with the available information.
7. Cite information from the context whenever possible.
"""
        ),
        (
            "human",
            """
Context:
{context}

Question:
{input}
"""
        )
    ])

    if not model:
        return None

    # Select LLM
    if model_provider == "groq":
        llm = ChatGroq(
            model=model,
            api_key=GROQ_API_KEY
        )

    elif model_provider == "gemini":
        llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=GOOGLE_API_KEY
        )

    elif model_provider == "openrouter":
        llm = ChatOpenAI(
            model=model,
            openai_api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )

    else:
        return None

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 8}
    )

    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )

    chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    return chain