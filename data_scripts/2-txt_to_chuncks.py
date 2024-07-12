import os
import re

text_folder='C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/text_extracted'
chunck_folder='C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/chuncks'
def split_text_into_chunks(text, chunk_size):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks


def select_files(folder_path, extension=".txt"):
    """
    Selects files from a folder based on extension.

    Args:
        folder_path: Path to the folder containing the files.
        extension: Optional file extension filter (defaults to ".pdf").

    Returns:
        A list of filenames that match the criteria.
    """
    filenames = os.listdir(folder_path)
    selected_files = [filename for filename in filenames if filename.endswith(extension)]
    return selected_files


def txt_to_chunck(filename, output_filename="chunck.txt"):
    with open(filename, 'r') as file:
        contents = file.read()

    with open(output_filename, "w") as text_file:
        text_file.write(contents)


files = select_files (text_folder,'.txt'  )

# Define the chunk size (number of words)
chunk_size = 1024 

for i in files :
    txt_to_chunck( text_folder+'/' + i )
    print ( i)
    with open(f'{text_folder}/{i}',"r", encoding='utf-8') as file:
        contents = file.read()
    
    chunks = split_text_into_chunks(contents, chunk_size)

    # Save each chunk to a separate file
    
    for j, chunk in enumerate(chunks):
        
        chunk_file_path = f'{chunck_folder}/{i[:-4]}chunck{j}.txt'

        with open(chunk_file_path, "w") as z:
            z.write(chunk)
        print(f"Chunk {j+1} saved to {chunk_file_path}")