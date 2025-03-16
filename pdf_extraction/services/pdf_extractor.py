import os
import pytesseract
import pdfplumber
from pdf2image import convert_from_path
import cv2
import numpy as np
import tempfile
import logging

logger = logging.getLogger(__name__)

class PDFExtractor:
    """Service for extracting text and tables from PDF documents"""
    
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.extracted_text = {}
        
    def extract_text_with_pdfplumber(self):
        """Extract text from PDF using pdfplumber"""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        page_num = str(i + 1)
                        self.extracted_text[page_num] = text
                        
            return self.extracted_text
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            raise