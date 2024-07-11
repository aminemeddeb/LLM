import io
import logging

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader

logging.basicConfig(level=logging.DEBUG)
print ( "extract_pdf_text")
# Function to extract text from PDF
def extract_pdf_text(url):
    logging.info(f"Extracting text from PDF: {url}")
    response = requests.get(url)
    with io.BytesIO(response.content) as open_pdf_file:
        read_pdf = PdfFileReader(open_pdf_file)
        num_pages = read_pdf.getNumPages()
        text = ""
        for page in range(num_pages):
            text += read_pdf.getPage(page).extract_text()
    return text
print ( "Read CSV file")
# Read CSV file containing URLs and PDF links
logging.info("Reading CSV file containing URLs and PDF links")
df_links = pd.read_csv('C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/some_ip.csv')
logging.info(f"CSV Data: /n{df_links}")
print ( "____________")
# Initialize lists to store data
site_types = []
texts = []

# Iterate over each row in the DataFrame
for index, row in df_links.iterrows():
    link_type = row['type']
    url = row['link']
    
    logging.info(f"Processing {link_type} link: {url}")
    logging.info("1")
    logging.info(link_type)
    logging.info("url")
    logging.info(type(link_type))
     
    if link_type == "url":
        logging.info("url")
        try:
            # Fetch HTML content
            response = requests.get(url)
            if response.status_code == 200:
                html_content = response.text
                logging.info(f"HTML content fetched from {url}")

                # Parse HTML
                soup = BeautifulSoup(html_content, 'html.parser')
                # Extract some text for example
                text_content = soup.get_text(strip=True)[::]  # Extract first 500 characters as a sample
                site_types.append(url)
                texts.append(text_content)
                logging.info(f"Successfully processed URL: {url}")
                
            else:
                logging.error(f"Failed to fetch {url}: Status code {response.status_code}")
        except Exception as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            continue
    elif link_type == "pdf":
        try:
            # Extract text from PDF
            pdf_text = extract_pdf_text(url)
            site_types.append("pdf")
            print(1 , pdf_text )
            texts.append(pdf_text[:])  # Extract characters as a sample
            logging.info(f"Successfully extracted text from PDF: {url}")
        except Exception as e:
            
            logging.error(f"Error extracting text from {url}: {str(e)}")
            continue
    else : 
        logging.error("else")
# Create a DataFrame from collected data
df_data = pd.DataFrame({
    "Type": site_types,
    "Text": texts
})

# Export to CSV
output_file = "test_output.csv"
logging.info(f"Exporting data to {output_file}")
df_data.to_csv(output_file, index=False)

# Verify the content of the output CSV
df_processed = pd.read_csv(output_file)
print(df_processed.head())