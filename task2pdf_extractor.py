import streamlit as st
import pytesseract
from pdf2image import convert_from_path
import json
import re
import os
from PIL import Image
import tempfile

# Set poppler path
POPPLER_PATH = r"C:\Program Files\poppler\Library\bin"

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file using OCR."""
    # Convert PDF to images
    images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    
    # Extract text from each image using OCR
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    
    return text

def extract_po_info(text):
    """Extract PO information from text."""
    # Regular expressions to find PO information
    po_number = re.search(r"PO\s*Number[:\s]+(\d+)", text, re.IGNORECASE)
    po_date = re.search(r"PO\s*Date[:\s]+(\d{2}[-/][A-Za-z]{3}[-/]\d{4})", text, re.IGNORECASE)
    po_expiry = re.search(r"PO\s*Expiry[:\s]+(\d{2}[-/][A-Za-z]{3}[-/]\d{4})", text, re.IGNORECASE)
    po_amount = re.search(r"PO\s*Amount[:\s]+(\d+[.,]?\d*)", text, re.IGNORECASE)
    
    return {
        "PO Number": po_number.group(1) if po_number else "",
        "PO Date": po_date.group(1) if po_date else "",
        "PO Expiry": po_expiry.group(1) if po_expiry else "",
        "PO Amount": po_amount.group(1) if po_amount else "",
    }

def extract_account_info(text):
    """Extract account information from text."""
    # Regular expressions to find account information
    store = re.search(r"Store[:\s]+([A-Z]+)", text, re.IGNORECASE)
    name = re.search(r"Name[:\s]+([A-Za-z\s]+)", text, re.IGNORECASE)
    delivery = re.search(r"Delivery\s*Address[:\s]+([A-Za-z\s,]+)", text, re.IGNORECASE)
    billing = re.search(r"Billing\s*Address[:\s]+([A-Za-z\s,]+)", text, re.IGNORECASE)
    gst = re.search(r"GST[:\s]+(\d+[A-Z])", text, re.IGNORECASE)
    client = re.search(r"Client\s*Number[:\s]+(\d+)", text, re.IGNORECASE)
    
    return {
        "Account Store": store.group(1) if store else "",
        "Account Name": name.group(1).strip() if name else "",
        "Account Delivery Address": delivery.group(1).strip() if delivery else "",
        "Account Billing Address": billing.group(1).strip() if billing else "",
        "Account GST": gst.group(1) if gst else "",
        "Account Client Number": client.group(1) if client else "",
    }

def extract_list_items(text):
    """Extract list items from text."""
    items = []
    
    # Split text into lines
    lines = text.split('\n')
    
    # Look for table-like patterns
    table_pattern = re.compile(r'(\d+)\s+([A-Za-z\s]+)\s+(\d+)\s+(\d+[.,]?\d*)\s+(\d+[.,]?\d*)\s+(\d+)')
    
    for line in lines:
        match = table_pattern.search(line)
        if match:
            items.append({
                "Sr. No.": match.group(1),
                "Description": match.group(2).strip(),
                "A": "",
                "B": "",
                "C": "",
                "Qty": match.group(3),
                "MRP": match.group(4),
                "Unit Cost": match.group(5),
                "Disc %": "",
                "Total Value": match.group(6)
            })
    
    return items

def process_pdf(pdf_path):
    """Process PDF and return structured JSON."""
    # Extract text from PDF using OCR
    text = extract_text_from_pdf(pdf_path)
    
    # Extract different sections
    po_info = extract_po_info(text)
    account_info = extract_account_info(text)
    list_items = extract_list_items(text)
    
    # Combine all information
    result = {
        **po_info,
        **account_info,
        "List Items": list_items
    }
    
    return result

def main():
    st.title("PDF to JSON Extractor (OCR)")
    
    # Add instructions
    st.markdown("""
    ### Instructions:
    1. Upload a PDF file
    2. The system will extract text using OCR
    3. The extracted information will be converted to JSON format
    4. You can download the resulting JSON file
    """)
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            # Process the PDF
            result = process_pdf(tmp_path)
            
            # Display the extracted text
            st.subheader("Extracted Text")
            st.text_area("Raw Text", extract_text_from_pdf(tmp_path), height=200)
            
            # Display the JSON
            st.subheader("Extracted JSON")
            st.json(result)
            
            # Add download button
            st.download_button(
                label="Download JSON",
                data=json.dumps(result, indent=4),
                file_name="extracted.json",
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

if __name__ == "__main__":
    main() 