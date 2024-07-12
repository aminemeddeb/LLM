from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

loader = TextLoader('C:/Users/medde/Desktop/ENSI/2eme/Stage/LLM/data/text_extracted/OA_Automotive_Ethernet_ECU_TestSpecification_v2.0_final_11_17.txt')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
print(len(texts))