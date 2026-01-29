from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq

llm = ChatGroq(model="openai/gpt-oss-20b")

res = llm.invoke("Can you explain me Merge sort ?")

print(res.content)