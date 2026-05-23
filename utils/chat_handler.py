"""
Chat Section Module
--------------------

This module handles all logic related to chat functionalities, including:
- Initializing session state
- Rendering chat history
- Handling user queries and responses
- Displaying uploaded PDF files
- Downloading chat history as PDF

All UI components are built with Streamlit widgets.
"""

import streamlit as st

from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def setup_session_state():
    """
    Initialize necessary Streamlit session state variables if they are not already defined.
    Ensures stable app behavior across reruns.
    """
    for key, default in {
        "chat_history": [],
        "vector_store": None,
        "pdf_files": [],
        "last_provider": None,
        "unsubmitted_files": False,
        "uploader_key": 0
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default


def render_chat_history():
    """
    Display all previous user and AI messages from chat history.
    """
    for q, a, *_ in st.session_state.get("chat_history", []):
        with st.chat_message("user"):
            st.markdown(q)

        with st.chat_message("ai"):
            st.markdown(a)


def handle_user_input(model_provider, model, chain):
    """
    Handles user input from the chat input box.
    Invokes the LLM chain using the provided question and displays the result.

    Parameters:
    - model_provider (str): The selected LLM provider
    - model (str): The specific model used for answering
    - chain (RetrievalChain): The LangChain retrieval chain for querying vectorstore
    """

    disable_question_input = (
        st.session_state.get("unsubmitted_files", False)
        or not st.session_state.get(
            f"uploaded_files_{st.session_state.uploader_key}", []
        )
        or not chain
    )

    question = st.chat_input(
        "💬 Ask a Question from the PDF Files",
        disabled=disable_question_input
    )

    if not question:
        return

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            try:
                output = chain.invoke(
                    {"input": question}
                )["answer"]

                st.markdown(output)

                pdf_names = [
                    f.name
                    for f in st.session_state.get("pdf_files")
                ]

                st.session_state.chat_history.append(
                    (
                        question,
                        output,
                        model_provider,
                        model,
                        pdf_names,
                        datetime.now()
                    )
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")


def render_uploaded_files_expander():
    """
    Displays the list of successfully uploaded PDF files in an expander.
    Shown only if files are submitted and not pending.
    """

    uploaded_files = st.session_state.get(
        f"uploaded_files_{st.session_state.uploader_key}",
        []
    )

    if uploaded_files and not st.session_state.get("unsubmitted_files"):

        with st.expander("📎 Uploaded Files:"):

            for f in uploaded_files:
                st.markdown(f"- {f.name}")


def generate_chat_pdf(chat_history):
    """
    Generate PDF containing only Questions and Answers.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "RAG PDFBot Chat History",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 12))

    for i, chat in enumerate(chat_history, start=1):

        question = chat[0]
        answer = chat[1]

        elements.append(
            Paragraph(
                f"<b>Question {i}:</b> {question}",
                styles["BodyText"]
            )
        )

        elements.append(Spacer(1, 5))

        elements.append(
            Paragraph(
                f"<b>Answer {i}:</b> {answer}",
                styles["BodyText"]
            )
        )

        elements.append(Spacer(1, 15))

    doc.build(elements)

    pdf_data = buffer.getvalue()

    buffer.close()

    return pdf_data


def render_download_chat_history():
    """
    Adds a button to download chat history as PDF.
    Only Questions and Answers are included.
    """

    pdf_data = generate_chat_pdf(
        st.session_state.chat_history
    )

    with st.expander("📎 Download Chat History"):

        st.download_button(
            label="📥 Download Chat History PDF",
            data=pdf_data,
            file_name="chat_history.pdf",
            mime="application/pdf"
        )