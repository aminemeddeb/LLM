import pandas as pd
import requests


def download_pdf(url, save_path):
    """Downloads a PDF from a URL and saves it to a specified path.

    Args:
        url: The URL of the PDF file.
        save_path: The path where the downloaded PDF will be saved.
    """
    response = requests.get(url, stream=True, verify=False)
    if response.status_code == 200:
        with open(save_path, 'wb') as pdf_file:
            for chunk in response.iter_content(1024):
                pdf_file.write(chunk)
        print(f"PDF downloaded from {url} and saved to {save_path}")
    else:
        print(f"Error downloading PDF: {response.status_code}")


i=0
df_links = pd.read_csv('C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/some_ip.csv')

for index, row in df_links.iterrows(): 
    try:
        if row['type']== 'pdf':
            pdf_url = row['link']  # Replace with your actual URL
            save_path = "C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/downloaded/{}.pdf".format(i)  # Replace with your desired path
            print (i)
            i+=1
            download_pdf(pdf_url, save_path)
    except:
        print ( 'error in downloading')