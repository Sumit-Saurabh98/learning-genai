from dotenv import load_dotenv
load_dotenv()
from langchain_ollama import ChatOllama

llm = ChatOllama(model="phi3:latest")

res = llm.invoke("Can you explain me Merge sort ?")

print(res.content)