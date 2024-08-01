
'''import os
import requests
from bs4 import BeautifulSoup
from goose3 import Goose

# URL of the web page you want to extract content from
urls = '/home/rayen/focus/urls.txt'



url_list = open(urls, "r").read().split("\n")

# loop for each url
for url in url_list:
    g = Goose()
    article = g.extract(url=url)
    # Print the extracted content
    print("Title:", article.title)
    print("Meta Description:", article.meta_description)
    print("Cleaned Text:", article.cleaned_text)
'''

import os
from selenium import webdriver
from goose3 import Goose
import requests
from PyPDF2 import PdfReader
import re


def download_pdf(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        with open(path, 'wb') as file:
            file.write(response.content)
        return path
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
        return None

def extract_pdf_text(pdf_path):
    text = ''
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ''
    except Exception as e:
        print(f"Failed to extract text from PDF: {e}")
    return text

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_text_into_chunks(text, chunk_size):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# File paths
url_file = '/home/rayen/focus/pdfs.txt'  # This is your text file with PDF URLs
download_dir = '/home/rayen/focus/downloads'
chunks_dir = '/home/rayen/focus/chunk'

os.makedirs(download_dir, exist_ok=True)
os.makedirs(chunks_dir, exist_ok=True)




# Read URLs from the file
with open(url_file, 'r') as file:
    pdf_urls = file.readlines()

# Process each PDF URL
for url in pdf_urls:
    url = url.strip()  # Remove any surrounding whitespace/newlines
    if not url:
        continue  # Skip empty lines

    pdf_filename = os.path.join(download_dir, os.path.basename(url) + '.pdf')
    print(f"Downloading PDF from: {url}")
    pdf_path = download_pdf(url, pdf_filename)

    if pdf_path:
        print(f"Extracting text from: {pdf_path}")
        extracted_text = extract_pdf_text(pdf_path)
        cleaned_text = clean_text(extracted_text)
        chunk_size = 100  # Define the chunk size (number of words)
        chunks = split_text_into_chunks(cleaned_text, chunk_size)

        # Save each chunk to a separate file
        for i, chunk in enumerate(chunks):
            chunk_file_path = os.path.join(chunks_dir, f'{os.path.basename(pdf_filename)}_chunk_{i+1}.txt')
            with open(chunk_file_path, 'w') as f:
                f.write(chunk)
            print(f"Chunk {i+1} saved to {chunk_file_path}")






# Function to extract content from a URL
def extract_content(url):
    #g = Goose()
    g = Goose({'strict': False})
    driver = webdriver.Chrome()  # Make sure you have ChromeDriver installed
    try:
        # Check if the URL is accessible
        #response = requests.get(url, timeout=10)
        #response.raise_for_status()  # Raise an error for bad status codes

        #article = g.extract(url=url)
        driver.get(url)
        html = driver.page_source
        article = g.extract(raw_html=html)
        return article.title, article.meta_description, article.cleaned_text
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return None, None, None
    
# Path to the file containing URLs
file_path = '/home/rayen/focus/urls.txt'


# Function to save the extracted text to a file
def save_to_file(content, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error saving content to {file_path}: {e}")



# Function to split a file into chunks
def split_file(file_path, chunk_size=1000):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        base_name = os.path.basename(file_path)
        file_dir = os.path.dirname(file_path)
        chunk_dir = os.path.join(file_dir, 'chunk')
        
        if not os.path.exists(chunk_dir):
            os.makedirs(chunk_dir)
        
        for i in range(0, len(content), chunk_size):
            chunk_content = content[i:i+chunk_size]
            chunk_file_path = os.path.join(chunk_dir, f"{base_name}_chunk_{i//chunk_size + 1}.txt")
            with open(chunk_file_path, 'w') as chunk_file:
                chunk_file.write(chunk_content)
    except Exception as e:
        print(f"Error splitting file {file_path} into chunks: {e}")




def read_urls(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
        urls = [url.strip() for url in urls if url.strip()]
        return urls
    except Exception as e:
        print(f"Error reading URLs from {file_path}: {e}")
        return []


# Read URLs from the file
urls = read_urls(file_path)
e= 0 
p = 0

# Loop through the URLs and extract content
for url in urls:
    print(f"Processing URL: {url}")
    try:
        title, meta_description, cleaned_text = extract_content(url)
        e += 1
        print(e)
        if title or meta_description or cleaned_text:
            p += 1
            print(p)
            print(f"Title: {title}")
            print(f"Meta Description: {meta_description}")
            print(f"Cleaned Text: {cleaned_text}")
            
            # Save extracted content to file
            content_file_path = f"/home/rayen/focus/chunk/content_{p}.txt"
            save_to_file(cleaned_text, content_file_path)
            
            # Split the saved file into chunks
            split_file(content_file_path)
            
        else:
            print("No content extracted.")
        print("-" * 40)
    except Exception as e:
        print(f"Error processing URL {url}: {e}")



''' def read_urls(file_path):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
        urls = [url.strip() for url in urls if url.strip()]
        return urls
    except Exception as e:
        print(f"Error reading URLs from {file_path}: {e}")
        return []


# Read URLs from the file
urls = read_urls(file_path)
e= 0 
p = 0
# Loop through the URLs and extract content
for url in urls:
    print(f"Processing URL: {url}")
    try:
        title, meta_description, cleaned_text = extract_content(url)
        e+=1
        print(e)
        if title or meta_description or cleaned_text:
            p+=1
            print(p)
            print(f"Title: {title}")
            print(f"Meta Description: {meta_description}")
            print(f"Cleaned Text: {cleaned_text}")
        else:
            print("No content extracted.")
        print("-" * 40)
    except:
        print("nothing")


'''
'''# Initialize Goose
g = Goose()

# Extract content
article = g.extract(url=url)
le.cleaned_text)
from goose3 import Goose
import pandas as pd
df_links = pd.read_csv('C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/some_ip.csv')
w=0
for index, row in df_links.iterrows():
    if (row['type']== 'url'):
        url = row['link']
        try:
            g = Goose({'strict': False})
            article = g.extract(url=url)
            w+=1
            print("\033[91mtitle : \033[0m" , article.title)
            print("\033[34mmeta_description : \033[0m" ,article.meta_description)
            print("\033[33mcleaned_text : \033[0m",article.cleaned_text)
        except:
            print('Error')
print (w)
ᐧ
'''
