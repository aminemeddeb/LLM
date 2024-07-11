import os
import glob
import logging
from PyPDF2 import PdfReader
from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.normalizers import Sequence, NFC, Strip, Lowercase
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.trainers import WordLevelTrainer

logging.basicConfig(level=logging.DEBUG)

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

def combine_text_from_pdfs(pdf_dir):
    combined_text = ''
    pdf_files = glob.glob(os.path.join(pdf_dir, '*.pdf'))
    
    for pdf_file in pdf_files:
        logging.info(f"Extracting text from {pdf_file}")
        text = extract_text_from_pdf(pdf_file)
        combined_text += text + "\n"  # Add newline to separate texts from different PDFs
    
    return combined_text

def train_tokenizer_on_text(combined_text, vocab_size=75000):
    tokenizer = Tokenizer(WordLevel(unk_token='<unk>'))
    tokenizer.normalizer = Sequence([NFC(), Strip(), Lowercase()])
    tokenizer.pre_tokenizer = Whitespace()
    
    # Create a trainer for the tokenizer
    trainer = WordLevelTrainer(vocab_size=vocab_size, special_tokens=['<s>', '</s>', '<unk>'])
    
    # Tokenize the text
    tokenizer.train_from_iterator([combined_text], trainer=trainer)
    
    # Save the tokenizer
    tokenizer.save('tokenizer.json', pretty=True)

# Example usage
pdf_dir = '/home/rayen/Documents/stage-focus/OA_Automotive_Ethernet_ECU_TestSpecification_v2.0_final_11_17.pdf'  # Replace with your PDF directory path
combined_text = combine_text_from_pdfs(pdf_dir)
train_tokenizer_on_text(combined_text)
