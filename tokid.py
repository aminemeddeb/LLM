import os
import json
import ollama  # Assuming this is the library for LLaMA 2 embeddings

# Function to get LLaMA 2 embeddings
def get_llama2_embeddings(text, model="mxbai-embed-large"):
    try:
        # Generate embedding
        response = ollama.embeddings(model=model, prompt=text)
        return response['embedding']
    except Exception as e:
        print(f"Failed to get embedding: {e}")
        return None

# Directory where chunks are saved
chunks_dir = '/home/rayen/focus/chunk'

# List to hold all embeddings
embeddings_list = []

# Counter for unique IDs
id_counter = 0

# Iterate over all files in the directory
for filename in os.listdir(chunks_dir):
    chunk_file_path = os.path.join(chunks_dir, filename)
    try:
        with open(chunk_file_path, 'r') as file:
            chunk_text = file.read()
            # Generate embedding using LLaMA 2
            embedding = get_llama2_embeddings(chunk_text)
            if embedding:
                # Create an entry with unique ID
                embeddings_list.append({'id': id_counter, 'embedding': embedding})
                id_counter += 1
    except Exception as e:
        print(f"Failed to process file {filename}: {e}")

# Save embeddings to JSON file
embeddings_json_path = 'EMBEDDINGSID.json'
try:
    with open(embeddings_json_path, 'w') as json_file:
        json.dump(embeddings_list, json_file)
    print(f"Embeddings saved to {embeddings_json_path}")
    print('Embeddings:', embeddings_list)  # Print embeddings for verification
except Exception as e:
    print(f"Failed to save embeddings to JSON file: {e}")
