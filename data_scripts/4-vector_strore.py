# import
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_text_splitters import CharacterTextSplitter

# load the document and split it into chunks
loader = TextLoader('C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/text_extracted/OA_Automotive_Ethernet_ECU_TestSpecification_v2.0_final_11_17.txt')
documents = loader.load()

# split it into chunks
text_splitter = CharacterTextSplitter(separator='\n \n' , chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings()

# load it into Chroma
db = Chroma.from_documents(docs, embedding_function)

# query it
query = "what is some ip "
docs = db.similarity_search(query)

# print results
print ( len(docs))
print(docs[0].page_content)