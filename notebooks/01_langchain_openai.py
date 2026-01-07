from dotenv import load_dotenv

load_dotenv()
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

res = llm.invoke("Why trump attacked on present maduro?")
print(res.content)
