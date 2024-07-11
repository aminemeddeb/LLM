import io

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader


# Function to extract text from PDF
def extract_pdf_text(url):
    response = requests.get(url)
    with io.BytesIO(response.content) as open_pdf_file:
        read_pdf = PdfFileReader(open_pdf_file)
        num_pages = read_pdf.getNumPages()
        text = ''
        for page in range(num_pages):
            text += read_pdf.getPage(page).extract_text()
    return text

# Read CSV file containing URLs and PDF links
df_links = pd.read_csv('C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/some_ip.csv')

# Initialize lists to store data
site_types = []
texts = []

# Iterate over each row in the DataFrame
for index, row in df_links.iterrows():
    link_type = row['type']
    url = row['link']
    
    if link_type == 'url':
        try:
            # Fetch HTML content
            response = requests.get(url)
            html_content = response.text

            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Example: Extracting site name (uncomment if needed)
            # site_name = soup.find('h1').text.strip()  # Adjust based on your HTML structure

            # Append to lists
            site_types.append('url')
            texts.append('')
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            continue
    elif link_type == 'pdf':
        try:
            # Extract text from PDF
            pdf_text = extract_pdf_text(url)

            # Append to lists
            site_types.append('pdf')
            texts.append(pdf_text)
        except Exception as e:
            print(f"Error extracting text from {url}: {str(e)}")
            continue

# Create a DataFrame from collected data
df_data = pd.DataFrame({
    'Type': site_types,
    'Text': texts
})

# Export to CSV
df_data.to_csv('C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/te.csv', index=False)