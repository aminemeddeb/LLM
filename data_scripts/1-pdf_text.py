import os
import PyPDF2
import re 


def clean_text(text):
    # Remove non-alphanumeric characters except for spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Normalize whitespace
    text= text.strip(' ')
    #text = re.sub(r'\s+', ' ', text)
    return text
def select_files(folder_path, extension=".pdf"):
    """
    Selects files from a folder based on extension.

    Args:
        folder_path: Path to the folder containing the files.
        extension: Optional file extension filter (defaults to ".pdf").

    Returns:
        A list of filenames that match the criteria.
    """
    filenames = os.listdir(folder_path)
    selected_files = [filename for filename in filenames if filename.endswith(extension)]
    return selected_files

# Example usage



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
            text += '\n \n'
    with open(output_filename, "w", encoding="utf-8") as text_file:
        text_file.write(clean_text(text))

    print(f"Text extracted from PDF and saved to: {output_filename}")

# Download the PDF from the URL (replace with your download logic)
# ... (download code using libraries like requests or urllib)

# Set the path to the downloaded PDF file

for i in select_files('C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/downloaded','.pdf'):
    try: 
        pdf_path = 'C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/downloaded/' + i  # Replace with your actual path
        output_path= 'C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/text_extracted/'+i[:-3]+"txt"
        pdf_to_text(pdf_path ,output_path)
    except:
        print('error pdf to text ')