# PDF to JSON Extractor (OCR)

A Streamlit-based web application that extracts structured information from PDF files using OCR (Optical Character Recognition) and converts it into JSON format.

## Features

- PDF text extraction using OCR (Tesseract)
- Automatic extraction of:
  - PO (Purchase Order) information
  - Account details
  - List items and their details
- Interactive web interface using Streamlit
- JSON export functionality
- Support for PDF files

## Prerequisites

Before running this application, ensure you have the following installed:

1. Python 3.x
2. Tesseract OCR
3. Poppler (for PDF processing)

### Windows Installation

1. Install Tesseract OCR:
   - Download the installer from [Tesseract GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - Add Tesseract to your system PATH

2. Install Poppler:
   - Download from [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)
   - Extract to `C:\Program Files\poppler`
   - Add the `bin` directory to your system PATH

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run task2pdf_extractor.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Upload a PDF file using the file uploader

4. The application will:
   - Extract text from the PDF using OCR
   - Process and structure the information
   - Display the extracted text and JSON
   - Provide a download button for the JSON file

## Data Extraction

The application extracts the following information:

### PO Information
- PO Number
- PO Date
- PO Expiry
- PO Amount

### Account Information
- Store
- Name
- Delivery Address
- Billing Address
- GST
- Client Number

### List Items
- Sr. No.
- Description
- Quantity
- MRP
- Unit Cost
- Total Value

## Error Handling

The application includes error handling for:
- PDF processing errors
- OCR extraction issues
- File upload problems

## Contributing

Feel free to submit issues and enhancement requests!

## License

[Add your chosen license here] 