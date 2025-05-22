# RAG-based Document Chat Application

A powerful Streamlit application that enables users to chat with their documents using Retrieval-Augmented Generation (RAG) and Google's Gemini AI. The application supports multiple document formats and provides intelligent responses based on document content.

## Features

- 📚 Multi-document support (PDF, DOCX, TXT)
- 🤖 Powered by Google's Gemini 1.5 Flash model
- 🔍 Advanced text retrieval using FAISS and TF-IDF
- 💬 Interactive chat interface
- 📝 Chat history tracking
- 🔄 Real-time document processing
- 📊 Context-aware responses
- 🎯 Smart text chunking and indexing

## Prerequisites

Before running this application, ensure you have:

1. Python 3.8 or higher
2. Google Gemini API key
3. Required Python packages (listed in requirements.txt)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up your Gemini API key:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Replace `"apikey"` in the code with your actual API key
   - For production, use environment variables or secure key management

## Usage

1. Run the Streamlit application:
```bash
streamlit run ragtask4.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Using the Application:
   - Upload one or more documents (PDF, DOCX, TXT)
   - Wait for document processing
   - Ask questions about the document content
   - View AI-generated responses
   - Check retrieved context
   - Review chat history

## How It Works

1. **Document Processing**:
   - Documents are uploaded and text is extracted
   - Text is chunked into manageable segments
   - Chunks are indexed using FAISS and TF-IDF

2. **Query Processing**:
   - User questions are processed
   - Relevant document chunks are retrieved
   - Context is combined with the question
   - Gemini AI generates a response

3. **Response Generation**:
   - AI generates answers based on retrieved context
   - Responses are displayed with source context
   - Chat history is maintained

## Project Structure

```
├── ragtask4.py           # Main application file
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Dependencies

The project uses the following main dependencies:
- `streamlit`: Web application framework
- `google-generativeai`: Google's Gemini AI API
- `PyMuPDF (fitz)`: PDF processing
- `python-docx`: DOCX file handling
- `scikit-learn`: TF-IDF vectorization
- `faiss-cpu`: Vector similarity search
- `numpy`: Numerical operations

## Error Handling

The application includes comprehensive error handling for:
- Document processing errors
- API connection issues
- Invalid file formats
- Text extraction failures
- Vector store creation issues
- Query processing errors

## Security Considerations

1. **API Key Management**:
   - Never commit API keys to version control
   - Use environment variables or secure key management
   - Implement proper key rotation

2. **Document Security**:
   - Process documents locally
   - Implement proper access controls
   - Clear sensitive data after processing

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google Gemini AI for the language model
- Streamlit for the web interface framework
- FAISS for efficient similarity search
- PyMuPDF and python-docx for document processing 
