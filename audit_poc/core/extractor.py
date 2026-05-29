# ============================================
# AUDIT POC - Document Extraction Engine
# ============================================
# Updated to use pdfplumber instead of PyMuPDF
# pdfplumber works perfectly on Python 3.14
# ============================================

import pdfplumber
from docx import Document as DocxDocument
import openpyxl
from pathlib import Path


def extract_all_documents(uploaded_files):
    """Extract text from all uploaded files"""
    extracted = {}
    for file in uploaded_files:
        filename = file.name
        extension = Path(filename).suffix.lower()
        try:
            if extension == ".pdf":
                text = extract_pdf(file)
            elif extension == ".docx":
                text = extract_docx(file)
            elif extension == ".xlsx":
                text = extract_xlsx(file)
            else:
                text = ""
            extracted[filename] = text
        except Exception as e:
            extracted[filename] = f"ERROR: {str(e)}"
    return extracted


def extract_pdf(file):
    """Extract text from PDF using pdfplumber"""
    all_text = []
    with pdfplumber.open(file) as pdf:
        for i, page in enumerate(pdf.pages):
            all_text.append(f"\n--- PAGE {i+1} ---\n")
            text = page.extract_text()
            if text:
                all_text.append(text)
    return "\n".join(all_text)


def extract_docx(file):
    """Extract text from Word document"""
    doc = DocxDocument(file)
    all_text = []
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            all_text.append(paragraph.text)
    for table in doc.tables:
        for row in table.rows:
            row_text = " | ".join(
                cell.text.strip()
                for cell in row.cells
                if cell.text.strip()
            )
            if row_text:
                all_text.append(row_text)
    return "\n".join(all_text)


def extract_xlsx(file):
    """Extract values from Excel file"""
    workbook = openpyxl.load_workbook(file, data_only=True)
    all_text = []
    for sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        all_text.append(f"\n--- SHEET: {sheet_name} ---\n")
        for row in sheet.iter_rows():
            row_values = [
                str(cell.value)
                for cell in row
                if cell.value is not None
            ]
            if row_values:
                all_text.append(" | ".join(row_values))
    workbook.close()
    return "\n".join(all_text)


def combine_extracted_text(extracted_dict):
    """Combine all extracted text into one string"""
    combined = []
    for filename, text in extracted_dict.items():
        combined.append(f"\n{'='*50}")
        combined.append(f"DOCUMENT: {filename}")
        combined.append(f"{'='*50}\n")
        combined.append(text)
    return "\n".join(combined)


class DocumentExtractor:
    """Thin wrapper class around the existing extractor functions.
    Allows app.py to instantiate: extractor = DocumentExtractor()
    """

    def extract(self, file):
        """Extract text from a single uploaded Streamlit file object."""
        return extract_all_documents([file])[file.name]

    def extract_all(self, files):
        """Extract text from a list of uploaded Streamlit file objects."""
        results = {}
        for file in files:
            results[file.name] = self.extract(file)
        return results