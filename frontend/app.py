import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI PDF Chatbot",
    page_icon="📄",
    layout="wide"
)

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Sidebar
with st.sidebar:

    st.title("📚 Documents")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if st.button("📤 Upload"):

        if uploaded_file is not None:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "application/pdf"
                )
            }

            with st.spinner("Uploading..."):

                response = requests.post(
                    f"{API_URL}/upload",
                    files=files
                )

            if response.status_code == 200:

                st.success("Uploaded Successfully")

                if uploaded_file.name not in st.session_state.uploaded_files:
                    st.session_state.uploaded_files.append(
                        uploaded_file.name
                    )

    st.divider()

    st.subheader("Uploaded PDFs")

    for pdf in st.session_state.uploaded_files:
        st.write(f"📄 {pdf}")

    stats = requests.get(
        f"{API_URL}/stats"
    ).json()

    st.divider()

    st.subheader("📊 Statistics")

    st.metric(
        "📄Uploaded PDFs",
        len(st.session_state.uploaded_files)
    )

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []
        st.rerun()

# Main Page
st.title("📄 AI PDF Chatbot")
st.caption("Chat with your PDF documents")

if len(st.session_state.messages) == 0:

    st.info(
        """
👋 Welcome to AI PDF Chatbot

Upload one or more PDFs and ask questions about them.

        """
    )

# Display Chat History
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
question = st.chat_input(
    "Ask a question about your PDFs..."
)

if question:

    # User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Assistant Message
    with st.chat_message("assistant"):

        with st.spinner("🤖 Thinking..."):

            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "question": question
                }
            )

            data = response.json()

            answer = f"""
{data["answer"]}

📎 Source: {data["source"]}

"""

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )