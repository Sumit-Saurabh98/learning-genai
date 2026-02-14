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


# res = addNumber.invoke({"num1":10, "num2":20})

# print(res)

llm = ChatOpenAI(model='gpt-4')

agents = create_agent(model=llm, tools=[addNumber], system_prompt="You are a math teacher and always use tools for calculation.")

response = agents.invoke({"messages":[{"role":"user", "content":"What is 10 + 20"}]})

# for res in response['messages']:
#     print(res)
#     print("\n")

print(response['messages'][-1].content)