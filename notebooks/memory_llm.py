from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

history = []

while True:
    query = input("User :")
    print("User: ", query)
    if query.lower() in ["quit", "exit", "bye"]:
        print("Good Bye ✌️")
        break
    history.append({"role":"user", "content":query})
    res = llm.invoke(history)
    print("AI: ", res.content, "\n")
    history.append({"role":"ai", "content":res.content})