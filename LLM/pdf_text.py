import PyPDF2


def pdf_to_text(pdf_path, output_filename="extracted_text.txt"):
    """
    Extracts text from a PDF file and saves it to a text file.

    Args:
        pdf_path: Path to the PDF file.
        output_filename: Optional filename for the output text file. Defaults to "extracted_text.txt".
    """
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    with open(output_filename, "w", encoding="utf-8") as text_file:
        text_file.write(text)

    print(f"Text extracted from PDF and saved to: {output_filename}")

# Download the PDF from the URL (replace with your download logic)
# ... (download code using libraries like requests or urllib)

# Set the path to the downloaded PDF file
pdf_path = "C:/Users/medde/Downloads/someip1.pdf"  # Replace with your actual path

pdf_to_text(pdf_path)
