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
pdf_dir = '/home/rayen/focus/Solved+Big+Data+and+Data+Science+Projects.pdf'  # Replace with your PDF directory path
combined_text = combine_text_from_pdfs(pdf_dir)
train_tokenizer_on_text(combined_text)



'''
Version:

json

"version": "1.0"

    Indicates the version of the tokenizer format.

Added Tokens:

json

"added_tokens": [
  {
    "id": 0,
    "content": "<s>",
    "single_word": false,
    "lstrip": false,
    "rstrip": false,
    "normalized": false,
    "special": true
  },
  {
    "id": 1,
    "content": "</s>",
    "single_word": false,
    "lstrip": false,
    "rstrip": false,
    "normalized": false,
    "special": true
  },
  {
    "id": 2,
    "content": "<unk>",
    "single_word": false,
    "lstrip": false,
    "rstrip": false,
    "normalized": false,
    "special": true
  }
]

    Added Tokens: Special tokens added to the tokenizer's vocabulary:
        <s>: Start of sentence.
        </s>: End of sentence.
        <unk>: Unknown token (for words not in the vocabulary).

Normalizer:

json

"normalizer": {
  "type": "Sequence",
  "normalizers": [
    {
      "type": "NFC"
    },
    {
      "type": "Strip",
      "strip_left": true,
      "strip_right": true
    },
    {
      "type": "Lowercase"
    }
  ]
}

    Normalizer: Processes text before tokenization:
        NFC: Normalization Form C (Unicode normalization).
        Strip: Removes extra whitespace from both ends of text.
        Lowercase: Converts all characters to lowercase.

Pre-Tokenizer:

json

"pre_tokenizer": {
  "type": "Whitespace"
}

    Pre-Tokenizer: Splits text into tokens based on whitespace.

Post-Processor:

json

"post_processor": null

    Post-Processor: Not used in this tokenizer configuration.

Decoder:

json

"decoder": null

    Decoder: Not used in this tokenizer configuration.

Model:

json

    "model": {
      "type": "WordLevel",
      "vocab": {
        "<s>": 0,
        "</s>": 1,
        "<unk>": 2
      },
      "unk_token": "<unk>"
    }

        Model: Describes the tokenizer model:
            WordLevel: Tokenizes text at the word level.
            Vocab: Dictionary mapping tokens to their IDs.
            unk_token: Token used for unknown words.

Summary:

    Special Tokens: Added tokens like <s>, </s>, and <unk>.
    Text Normalization: Handles text normalization and cleaning.
    Tokenization: Splits text by whitespace.
    Vocabulary: Maps words to numeric IDs.

This configuration defines how the tokenizer processes and tokenizes text data.'''