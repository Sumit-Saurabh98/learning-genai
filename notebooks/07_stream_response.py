from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4", streaming=True)

question = "Could you please explain merge sort in python with code and dry run?"


res = llm.stream(question)

for chunk in res:
    print(chunk.content, end=" ")

