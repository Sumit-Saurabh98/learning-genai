from dotenv import load_dotenv
load_dotenv()
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(model_name="claude-sonnet-4-5")

res = llm.invoke("What is python?")

print(res.content)