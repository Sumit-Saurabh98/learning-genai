from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# three types of prompts system, ai, user
prompts = [
    ("system", "You are a java developer"),
    ("user", "How find the second largest element in a array")
]


res = llm.invoke(prompts)

print(res.content)