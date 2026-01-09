from dotenv import load_dotenv
load_dotenv()

## working with openai modal
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")

res = llm.invoke("What is Python?")

print(res.content)