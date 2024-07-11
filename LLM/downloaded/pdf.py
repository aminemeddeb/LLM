import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import logging
import re
import os

logging.basicConfig(level=logging.DEBUG)

# Function to download and save PDF
def download_pdf(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(response.content)
        return local_path
    else:
        logging.error(f"Failed to download PDF: {url}, status code: {response.status_code}")
        return None

# Function to extract text from PDF
def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to clean text
def clean_text(text):
    # Remove non-alphanumeric characters except for spaces
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to split text into chunks of a specific size
def split_text_into_chunks(text, chunk_size):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks


# URL of the PDF
pdf_url = 'https://webthesis.biblio.polito.it/secure/9054/1/Tesi.pdf'
local_pdf_path = '/tmp/temp_pdf.pdf'  # Local path to save the PDF
output_txt_path = '/home/rayen/Documents/stage-focus/output/extracted_text.txt'  # Path to save the extracted text

# Download the PDF
downloaded_pdf_path = download_pdf(pdf_url, local_pdf_path)
if downloaded_pdf_path:
    # Extract text from the downloaded PDF
    extracted_text = extract_pdf_text(downloaded_pdf_path)
    cleaned_text = clean_text(extracted_text)
    
    # Save the extracted text to a .txt file
    with open(output_txt_path, 'w') as f:
        f.write(cleaned_text)
    
    print(f"The extracted text has been saved to {output_txt_path}")
    
    # Split the cleaned text into chunks
    chunk_size = 100  # Define the chunk size (number of words)
    chunks = split_text_into_chunks(cleaned_text, chunk_size)
    
    # Save each chunk to a separate file
    for i, chunk in enumerate(chunks):
        chunk_file_path = f'/tmp/extracted_text_chunk_{i+1}.txt'
        with open(chunk_file_path, 'w') as f:
            f.write(chunk)
        print(f"Chunk {i+1} saved to {chunk_file_path}")
else:
    print(f"Failed to download the PDF from {pdf_url}")

