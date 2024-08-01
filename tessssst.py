

import os
import re

import numpy as np
import ollama
from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      MilvusClient, connections, model, utility)
from PyPDF2 import PdfReader
#from sentence_transformers import SentenceTransformer
#from colored import fg, bg, attr

os.environ.get('tcp://192.168.130.122:19530')
connections.connect(
    "default",
    host='192.168.130.122',
    port='19530'

)


# Import the other file
import embbedingss

# Access the list from the other file
encoded_texts = embbedingss.embeddings_list

# Print the list to verify
print(encoded_texts)

txt_path="/home/rayen/focus/chunk/01-SecureSOMEIP-VTM.pdf.pdf_chunk_4.txt"

from goose3 import Goose
import pandas as pd


# Define schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1024),
]
schema = CollectionSchema(fields, description="Example collection5", enable_dynamic_field=True)

# Create collection
collection = Collection(name="example_collection8", schema=schema)

# Check if collection exists
collections = utility.list_collections()
if "example_collection8" in collections:
    print("Collection exists.")
else:
    print("Collection does not exist.")
    # Handle the situation if the collection doesn't exist

# Create an index if it doesn't exist
indexes = collection.indexes
if not indexes:
    print("No indexes found. Creating index.")
    index_params = {
        "index_type": "IVF_FLAT",  # Example index type
        "metric_type": "L2",       # Example metric type
        "params": {"nlist": 1024}
    }
    collection.create_index(field_name="embedding", index_params=index_params)
else:
    print("Indexes already present:", indexes)

# Load the collection
try:
    collection.load()
    print("Collection loaded successfully.")
except Exception as e:
    print(f"Error loading collection: {e}")

# Verify the indexes
indexes = collection.indexes
print("Indexes after creation:", indexes)






# Insert data into Milvus collection
#data = [["id": i, "embedding": encoded_texts[i]["embedding"]] for i in range(len(encoded_texts))
        
data = [{"id": i, "embedding": embedding} for i, embedding in enumerate(encoded_texts)]


collection.insert(data)


collection.load()

search_params = {
    "metric_type": "L2",
    "offset": 0,
    "ignore_growing": False,
    "params": {"nprobe": 10}
}
data1 = ollama.embeddings(model="mxbai-embed-large", prompt="What is the type of data that can be serialized in SomeIP")
data_embed= data1['embedding']
results = collection.search(
    data=[data_embed],
    anns_field="embedding",
    # the sum of `offset` in `param` and `limit`
    # should be less than 16384.
    param=search_params,
    limit=16384,
    expr=None,
    # set the names of the fields you want to
    # retrieve from the search result.
    output_fields=['embedding'],
    consistency_level="Strong"
)


chunks = '/home/rayen/focus/chunk/chuncks'

z=0
L=[]
for i in results[0].ids:
    z+=1
    L.append(i)
    print(chunks[i])
    if( z== 1):
        break




#print(result['response'])

#try:
print("\033[34mTrying generation\033[0m")
result = ollama.generate(model='llama2', prompt='What is the type of data that can be serialized in SomeIP', context=L)
#except Exception as e:
#print(f'Generation error: {e}')

try:
    if isinstance(result, dict) and 'response' in result:
        print(result['response'])
    else:
        print("Unexpected result format:", result)
except Exception as e:
    print(f'Error printing result: {e}')






import tkinter as tk
from tkinter import scrolledtext
def send_to_model(input_text):
        # Replace this with your AI model's logic
        model_output = f"You said: {input_text}"
        return model_output

class ChatApp:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple Chat App")

        # Create chat window
        self.chat_window = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.chat_window.pack(expand=True, fill="both")

        # Create input field
        self.entry = tk.Entry(self.root)
        self.entry.pack(expand=True, fill="x")

        # Create send button
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(side="right")

        self.root.mainloop()

    def send_message(self):
        message = self.entry.get()
        self.chat_window.insert(tk.END, f"You: {message}\n")

        self.chat_window.insert(tk.END, f"Chat RNAM: {send_to_model(message)}\n")

        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    app = ChatApp()
