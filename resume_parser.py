import docx2txt
import pytesseract
from pdfminer.high_level import extract_text
from PIL import Image
import os
import re

def clean_text(text):
    """Clean and normalize extracted text"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove non-printable characters
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t')
    return text

def parse_resume(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    text = ''

    try:
        if ext == '.pdf':
            text = extract_text(filepath)
        elif ext == '.docx':
            text = docx2txt.process(filepath)
        elif ext in ['.png', '.jpg', '.jpeg']:
            # Configure Tesseract path if needed (uncomment and set your path)
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            text = pytesseract.image_to_string(Image.open(filepath))
        elif ext == '.txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        
        return clean_text(text)
    except Exception as e:
        print(f"Error parsing file: {str(e)}")
        return ''