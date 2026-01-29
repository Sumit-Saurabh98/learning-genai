from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from typing import List

llm = ChatOpenAI(model="gpt-5")

text = "Hello, My name is Sumit Saurabh and age is 25 years. My email is 'sumitsaurabh112@gmail.com'"

# res = llm.invoke(f"Please tell me what is my name, email and age?: {text}")

# print(res.content) # Type of this output is string

#Structured output

from pydantic import BaseModel, Field

class ResponseStructure(BaseModel):
    name: str = Field(description="Complete Name")
    email: str = Field(description="Email Address")
    age: int = Field(description="Age")

# structured_llm = llm.with_structured_output(ResponseStructure)   

# res = structured_llm.invoke(f"Please tell me what is my name, email and age?: {text}")

class Movies(BaseModel):
    title: str = Field(description="Movie Title")
    year: int = Field(description="Movie release year.")

class AllMovies(BaseModel):
    movies: List[Movies]    

movie_llm = llm.with_structured_output(AllMovies)

res = movie_llm.invoke("Give me 5 recent movie")

print(res)