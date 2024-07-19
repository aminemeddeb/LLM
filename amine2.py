import os
import re

import numpy as np
import ollama
from llama_index.llms.ollama import Ollama  # Corrected import
#from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,connections)
from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      MilvusClient, connections, model)
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

ollama.embeddings(
  model='mxbai-embed-large',
  prompt='define some IP',
)

os.environ.get('tcp://172.17.48.1:19530')


connections.connect(
    "default", 
    host='172.17.48.1', 
    port='19530'
)
pdf_path = 'C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/downloaded/OA_Automotive_Ethernet_ECU_TestSpecification_v2.0_final_11_17.pdf'
#pdf_path = 'file:///C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/downloaded/3.pdf'

# Function to extract text from PDF
def extract_pdf_text(pdf_path):
    text = ''
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        print(f"Failed to extract text from PDF: {e}")
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

# Extract text from the PDF
extracted_text = extract_pdf_text(pdf_path)

# Clean the extracted text
cleaned_text = clean_text(extracted_text)

# Split the cleaned text into chunks
chunk_size = 100  # Define the chunk size (number of words)
chunks = split_text_into_chunks(cleaned_text, chunk_size)
# Save each chunk to a separate file


encoded_texts=[]
for i, chunk in enumerate(chunks):
    chunk_file_path = f'C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/RAG from github/Nouveau dossier/chuncks/{i+1}.txt'
    
    try:
        with open(chunk_file_path, 'w') as f:
            f.write(chunk)
        print(i+1)
        
        #print(f"Chunk {i+1} saved to {chunk_file_path}")
        encoded= ollama.embeddings(model="mxbai-embed-large", prompt=chunk)
        #print( encoded['embedding'])
        encoded_texts.append(encoded)
        
        
    except Exception as e:
        print(f"Failed to save chunk {i+1}: {e}")
    if (i+1  == 10 ):
        break

# Save embeddings to a separate file
'''embed_file_paths =[]
for i, embed in enumerate(encoded_texts):
    embed_file_path = f'C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/RAG from github/Nouveau dossier/embed{i+1}.txt'
    try:
        with open(chunk_file_path, 'w') as f:
            f.write(embed)
        print(f"Chunk {i+1} saved to {chunk_file_path}")
        embed_file_paths.append(chunk_file_path)
    except Exception as e:
        print(f"Failed to save chunk {i+1}: {e}")
print (encoded_texts)'''
print( '7atchaia ')


#print (encoded_texts )
# Connect to Milvus
# connections.connect("default", host="172.17.48.1", port="9091")
#connections.connect("default", host="172.17.48.1", port="19530")
# Drop the existing collection (if it exists)
try:
  connections.remove_connection("example_collection6")
except:
  pass  # Ignore error if collection doesn't exist
# Define and create collection in Milvus
'''fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=len(encoded_texts[0]))  # Adjust dimension as per your LLAMA2 model
]'''
fields = [ 
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),
]
schema = CollectionSchema(fields, "Example collection5", enable_dynamic_field=True)
collection = Collection(name="example_collection8", schema=schema)

# Insert data into Milvus collection
'''data = [
    [ (i ,encoded_texts[i]['embedding'] ) for i in range(len(encoded_texts))]  # Embeddings
]
'''

data = [{"id": i, "embedding": encoded_texts[i]["embedding"]} for i in range(len(encoded_texts))]
'''data=[]

for i in range (len(encoded_texts)):
    data.append ( [i+1,encoded_texts[i]['embedding']])
'''
#print (encoded_texts )
print(data) 
collection.insert(data)

# Create index and load collection
index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 100}
}
collection.create_index(field_name="embedding", index_params=index_params)
collection.load()

# Perform search (example)
query_embeddings = ollama.embeddings(model="mxbai-embed-large", prompt="Hello world")
#search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
search_params = {"metric_type": "L2", "limit": 10}
print (query_embeddings)
results = collection.search(
    query_embeddings['embedding'],
    anns_field="embedding",
    param=search_params,
    limit=3,
    #expr=None
)

# Display search results
for result in results:
    for hit in result:
        print(f"ID: {hit.id}, Distance: {hit.distance}")

'''f2e2d1eb714a   zilliz/attu:v2.3.6                         "docker-entrypoint.s…"   37 minutes ago   Up 36 minutes          0.0.0.0:8000->3000/tcp                             attu
02ec463d48e2   milvusdb/milvus:v2.3.19 '''