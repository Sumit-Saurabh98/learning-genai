from dotenv import load_dotenv
load_dotenv()

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools import Tool, tool


llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
@tool
def google_search(query: str) -> str:
    """Search Google for recent information."""
    return GoogleSerperAPIWrapper().run(query)


agent = create_agent(
    model=llm,
    tools=[google_search],
    system_prompt="You are a helpful assistant and you have access to google search tool. Use it when needed."
)

while True:
    question = input("User: ")
    if question.lower() == "exit":
        break
    response = agent.invoke({"messages":[{"role":"user","content":question}]})
    print("AI: ", response["messages"][-1].content)