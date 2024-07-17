from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import re
from llama_index.llms.ollama import Ollama  # Corrected import

from pymilvus import connections, Collection, FieldSchema, DataType, CollectionSchema


from pymilvus import connections
connections.connect(
  alias="default", 
  host='localhost', 
  port='19530'
)
# Load a pre-trained model
#model = SentenceTransformer('all-MiniLM-L6-v2')

# Your data
#texts = ["Hello world", "Milvus is a vector database", "Embedding vectors"]
texts = []
# Initialize LLAMA2 model
#llama_model = Ollama(model_name="llama2")  # Corrected initialization
llama_model = Ollama(model="llama2")  # Specify the correct model name



# Generate embeddings
#embeddings = ollama_model.encode(texts)
encoded_texts = [text.encode('utf-8') for text in texts]


# Example PDF path
pdf_path = '/home/rayen/Downloads/LLM-Langchain_start/OA_Automotive_Ethernet_ECU_TestSpecification_v2.0_final_11_17.pdf'

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
chunk_file_paths = []
for i, chunk in enumerate(chunks):
    chunk_file_path = f'/tmp/extracted_text_chunk_{i+1}.txt'
    try:
        with open(chunk_file_path, 'w') as f:
            f.write(chunk)
        print(f"Chunk {i+1} saved to {chunk_file_path}")
        chunk_file_paths.append(chunk_file_path)
    except Exception as e:
        print(f"Failed to save chunk {i+1}: {e}")

# Connect to Milvus
connections.connect("default", host="localhost", port="9091")

# Define and create collection in Milvus
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=len(embeddings[0]))  # Adjust dimension as per your LLAMA2 model
]
schema = CollectionSchema(fields, "Example collection")
collection = Collection(name="example_collection", schema=schema)

# Insert data into Milvus collection
data = [
    [i for i in range(len(texts))],  # IDs
    embeddings.tolist()  # Embeddings
]
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
query_embeddings = llama_model.encode(["Hello world"]).tolist()
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = collection.search(
    query_embeddings,
    anns_field="embedding",
    param=search_params,
    limit=3,
    expr=None
)

# Display search results
for result in results:
    for hit in result:
        print(f"ID: {hit.id}, Distance: {hit.distance}")
