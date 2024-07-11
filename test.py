import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import logging
import re

logging.basicConfig(level=logging.DEBUG)


# Function to clean text
def clean_text(text):
    # Remove non-alphanumeric characters except for spaces
    Text = re.sub(r'[^a-zA-Z0-9\s]', '', Text)
    # Normalize whitespace
    Text = re.sub(r'\s+', ' ', text).strip()
    print("Normalize whitespace")
    return text

# Function to download and save PDF
def download_pdf(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(response.content)
        return local_path
    else:
        logging.error(f"Failed to download PDF: {url}, status code: {response.status_code}")
        print("Failed to download pdf")
        return None


# Function to extract text from PDF
def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

pdf_path = '/home/rayen/Documents/stage-focus/29408.pdf'
extracted_text = extract_pdf_text(pdf_path)
print(extracted_text[:500])  # Print the first 500 characters

# Function to extract text from a URL
def extract_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_contents = soup.get_text(strip=True)[:500]  # Extract first 500 characters
        return text_contents
    else:
        return None

# Example URL
url = 'https://stackoverflow.com/questions/51182471/whats-the-difference-between-dds-and-some-ip'
extracted_text = extract_text_from_url(url)
if extracted_text:
    print(extracted_text)
else:
    print(f"Failed to fetch content from {url}")

# Read CSV file containing URLs and PDF links
logging.info("Reading CSV file containing URLs and PDF links")
df_links = pd.read_csv('/home/rayen/Documents/stage-focus/some_ip.csv')
logging.info(f"CSV Data: \n{df_links}")

# Initialize lists to store data
site_types = []
texts = []

# Iterate over each row in the DataFrame
for index, row in df_links.iterrows():
    link_type = row['type']
    url = row['link']
    
    logging.info(f"Processing {link_type} link: {url}")
    
    if link_type == 'url':
        try:
            # Fetch HTML content
            response = requests.get(url)
            if response.status_code == 200:
                print("link url")
                html_content = response.text
                logging.info(f"HTML content fetched from {url}")

                # Parse HTML
                soup = BeautifulSoup(html_content, 'html.parser')
                # Extract some text for example
                text_content = soup.get_text(strip=True)[:500]  # Extract first 500 characters as a sample
                site_types.append('url')
                texts.append(text_content)
                logging.info(f"Successfully processed URL: {url}")
            else:
                logging.error(f"Failed to fetch {url}: Status code {response.status_code}")
        except Exception as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            continue
    elif link_type == 'pdf':
        try:
            # Extract text from PDF
            print("link pdf")
            pdf_text = extract_pdf_text(url)
            site_types.append('pdf')
            texts.append(pdf_text[:500])  # Extract first 500 characters as a sample
            logging.info(f"Successfully extracted text from PDF: {url}")
        except Exception as e:
            logging.error(f"Error extracting text from {url}: {str(e)}")
            continue

# Create a DataFrame from collected data
df_data = pd.DataFrame({
    'Type': site_types,
    'Text': texts
})

# Export to CSV
output_file = 'test_output.csv'
df_data.to_csv(output_file, index=False)

# Verify the content of the output CSV
df_processed = pd.read_csv(output_file)
print(df_processed.head())
