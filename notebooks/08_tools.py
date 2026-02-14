from dotenv import load_dotenv
load_dotenv()
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
@tool
def addNumber(num1:int, num2:int) -> int:
    """
    It will return the sum of two numbers.

    Args:
        num1(int): number 1
        num2(int): number 2

        Return:
         int: sum of two numbers
    """
    return num1 + num2

@tool
def multiplyNumber(num1:int, num2:int) -> int:
    """
    It will return the multiplication of two numbers.

    Args:
        num1(int): number 1
        num2(int): number 2

        Return:
         int: multiplication of two numbers
    """
    return num1 * num2  


@tool("web_search")
def  search(query:str) -> str:
    """
    Search the web for information. Particularly the crickbuzz.com.

    Args(str): user query

    Return(str): search result
    """

    return f"Result for: {query}"


# res = addNumber.invoke({"num1":10, "num2":20})

# print(res)

llm = ChatOpenAI(model='gpt-4')

# agents = create_agent(model=llm, tools=[addNumber, multiplyNumber, search], system_prompt="You are a math teacher and always use tools for calculation.")

agents = create_agent(model=llm, tools=[search], system_prompt="You are a cricket experts and you provide the answer for all the question based on you knowledge.")

response = agents.invoke({"messages":[{"role":"user", "content":"Tomorrow India ans Pakistan has world cup 2026 match in Sri Lanka. What will be the probable 11 for both the team?"}]})

# for res in response['messages']:
#     print(res)
#     print("\n")

print(response['messages'][-1].content)