from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(model="gpt-4")
out = StrOutputParser()

def transform_case(result:str):
    return result.upper()

# Create the prompt template (not format_messages here)
prompts = ChatPromptTemplate.from_messages([
    {"role":"system", "content":"You are a translator and convert the given input into {language}."},
    {"role":"user", "content":"{query}"}
])

# Format the template with actual values
# final_prompts = prompts.format_messages(language="Hinglish", query="I love python and javascript.")

# prompts is also invocable
# res = prompts.invoke({"language": "Hinglish", "query":"I love you."})

# print(res)

# Invoke the LLM
#res = llm.invoke(final_prompts)

#print(res.content)

# chains - runnable
chains = prompts | llm | out | transform_case

res = chains.invoke({"language": "Hinglish", "query":"I love you."})

print(res)
