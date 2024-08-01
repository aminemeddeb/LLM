from langchain_community.llms import HuggingFace
from langchain_community.chains import LLMChain
import langchain_community.llms as llms

# Initialize a Hugging Face model
model_name = "LLama2"  # You can replace this with the model of your choice
llm = HuggingFace(model_name=model_name, temperature=0.7)

# Define your prompt
prompt = "What is the capital of France?"

# Create the LLMChain instance
chain1 = LLMChain(llm=llm, prompt=prompt)

# Generate a response (this step is optional and depends on how you want to use the chain)
response = chain1.run()
print(response)
