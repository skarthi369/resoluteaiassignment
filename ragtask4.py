


import streamlit as st
import google.generativeai as genai
import fitz  # PyMuPDF for PDF reading
from docx import Document  # For DOCX reading
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
import os

# Configure Streamlit page settings
st.set_page_config(page_title="RAG Document Chat", page_icon="📚", layout="wide")

# Configure Gemini API (Replace with your actual API key)
genai.configure(api_key="apikey")  # Ensure you securely manage your API key

# Initialize the Gemini model
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Failed to initialize Gemini model: {str(e)}")
    st.stop()

# Step 1: Extract text from different file types
def extract_text(file):
    """Extract text from PDF, DOCX, or TXT files."""
    try:
        file_ext = os.path.splitext(file.name)[1].lower()
        text = ""
        
        if file_ext == ".pdf":
            doc = fitz.open(stream=file.read(), filetype="pdf")
            for page in doc:
                text += page.get_text()
            doc.close()
        
        elif file_ext == ".docx":
            doc = Document(file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        
        elif file_ext == ".txt":
            text = file.read().decode("utf-8", errors="ignore")
        
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
        
        return text.strip()
    
    except Exception as e:
        raise Exception(f"Error extracting text from {file.name}: {str(e)}")

# Step 2: Chunk text into smaller segments
def chunk_text(text, chunk_size=300):
    """Split text into chunks of specified word size."""
    if not text:
        return []
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Step 3: Build FAISS vector index for retrieval
def build_vector_store(chunks):
    """Create a FAISS index from text chunks using TF-IDF vectors."""
    if not chunks:
        raise ValueError("No chunks provided for indexing.")
    
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        vectors = vectorizer.fit_transform(chunks).toarray()
        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(vectors.astype('float32'))
        return index, vectorizer, chunks
    except Exception as e:
        raise Exception(f"Error building vector store: {str(e)}")

# Step 4: Retrieve top-k similar chunks
def retrieve_context(query, index, vectorizer, chunks, top_k=3):
    """Retrieve the top-k most relevant chunks for a given query."""
    try:
        query_vec = vectorizer.transform([query]).toarray().astype('float32')
        D, I = index.search(query_vec, top_k)
        return [chunks[i] for i in I[0] if i < len(chunks)]
    except Exception as e:
        raise Exception(f"Error retrieving context: {str(e)}")

# Streamlit app
st.title("📚 RAG-based Document Chat Application")
st.markdown("Upload your documents (PDF, DOCX, TXT) and ask questions about their content.")

# File uploader for multiple documents
uploaded_files = st.file_uploader(
    "Upload documents",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    help="Supports PDF, DOCX, and TXT files."
)

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = None
    st.session_state.vectorizer = None
    st.session_state.chunks = []
    st.session_state.chat_history = []

# Process uploaded files
if uploaded_files:
    try:
        all_text = ""
        for file in uploaded_files:
            text = extract_text(file)
            all_text += text + "\n"
        
        # Chunk and index the combined text
        chunks = chunk_text(all_text)
        if not chunks:
            st.warning("No content extracted from the uploaded files.")
        else:
            index, vectorizer, chunk_store = build_vector_store(chunks)
            st.session_state.vector_store = index
            st.session_state.vectorizer = vectorizer
            st.session_state.chunks = chunk_store
            st.success(f"Processed {len(uploaded_files)} document(s) with {len(chunks)} chunks indexed.")
    
    except Exception as e:
        st.error(f"Error processing documents: {str(e)}")

# Chat interface
st.subheader("💬 Chat with Your Documents")
user_input = st.text_input("Ask a question about the documents:", placeholder="e.g., What is the main topic of the document?")

if user_input and st.session_state.vector_store:
    try:
        # Retrieve context
        context_chunks = retrieve_context(
            user_input,
            st.session_state.vector_store,
            st.session_state.vectorizer,
            st.session_state.chunks
        )
        context = "\n".join(context_chunks) if context_chunks else "No relevant context found."
        
        # Build prompt
        prompt = f"""You are a helpful assistant answering questions based on the provided document context. Provide a concise and accurate answer. If the context is insufficient, say so and provide a general response if possible.

Context:
{context}

Question: {user_input}
Answer:
"""
        
        # Send to Gemini
        response = model.generate_content(prompt)
        answer = response.text.strip()
        
        # Update chat history
        st.session_state.chat_history.append({"question": user_input, "answer": answer})
        
        # Display response
        st.markdown("**Answer:**")
        st.markdown(answer)
        with st.expander("View Retrieved Context"):
            st.text(context)
    
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")

# Display chat history
if st.session_state.chat_history:
    st.subheader("🕒 Chat History")
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.container():
            st.markdown(f"**Q{i+1}:** {chat['question']}")
            st.markdown(f"**A{i+1}:** {chat['answer']}")
            st.markdown("---")

# Sidebar instructions
st.sidebar.header("📖 How to Use")
st.sidebar.markdown("""
1. **Upload Documents**: Use the file uploader to add one or more PDF, DOCX, or TXT files.
2. **Wait for Processing**: The app will extract text, chunk it, and index it for retrieval.
3. **Ask Questions**: Enter your question in the text box to query the document content.
4. **View Responses**: See the AI's answer and retrieved context, plus the chat history below.
5. **Tips**:
   - Ensure documents contain readable text.
   - Ask specific questions for best results.
   - Check the context under the answer for transparency.
""")

# Sidebar notes
st.sidebar.header("⚙️ Notes")
st.sidebar.markdown("""
- **Supported Formats**: PDF, DOCX, TXT.
- **Model**: Uses Gemini 1.5 Flash for generation.
- **Retrieval**: FAISS with TF-IDF for efficient context retrieval.
- **API Key**: Ensure a valid Gemini API key is set.
""")