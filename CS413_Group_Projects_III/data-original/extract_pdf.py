import os
from pathlib import Path
import PyPDF2


def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


def process_pdfs_in_directory(root_path):
    """Processes all PDFs in the original_report directory."""
    original_report_dir = Path(root_path) / "original_report"
    extract_report_dir = Path(root_path) / "extract_report"
    if not os.path.exists(extract_report_dir):
        os.mkdir(extract_report_dir)

    # Ensure the directory exists
    if not original_report_dir.exists():
        print(f"Directory {original_report_dir} does not exist.")
        return

    # Process each PDF file in the directory
    for pdf_file in original_report_dir.glob("*.pdf"):
        # Extract the filename without the extension
        txt_filename = pdf_file.stem + ".txt"
        txt_file_path = extract_report_dir / txt_filename

        # Extract text from the PDF
        text = extract_text_from_pdf(pdf_file)

        # Save the extracted text to a .txt file
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)

        print(f"Processed {pdf_file.name} -> {txt_file_path.name}")

if __name__ == '__main__':
    # Example usage
    root_path = "C:\\Users\\Administrator\\Desktop\\22CS103报告文件"  # Replace with your actual root path
    process_pdfs_in_directory(root_path)
