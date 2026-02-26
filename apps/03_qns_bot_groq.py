# LLM
# TOOLS - GOOGLE SEARCH
# AGENT
# MEMORY
# STREAMING
# WEB INTERFACE

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langchain_core.tools import Tool, tool
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st

if "memory" not in st.session_state:
    st.session_state.memory = InMemorySaver()
    st.session_state.history = []

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, streaming=True)
@tool
def google_search(query: str) -> str:
    """Search Google for recent information."""
    return GoogleSerperAPIWrapper().run(query)

agent = create_agent(
    model=llm,
    tools=[google_search],
    system_prompt="You are a helpful assistant and you have access to google search tool. Use it when needed.",
    checkpointer=st.session_state.memory
)

st.subheader("Qns Bot Groq: Response in milliseconds")

for message in st.session_state.history:
    st.chat_message(message["role"]).markdown(message["content"])


query = st.chat_input("Ask a question")

if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role": "user", "content": query})
    response = agent.stream(
    {"messages": [{"role": "user", "content": query}]},
    config={"configurable": {"thread_id": "1"}}, stream_mode="messages")
    ai_container = st.chat_message("assistant")
    with ai_container:
        space = st.empty()
        message = ""
        for chunk in response:
            message += chunk[0].content
            space.markdown(message)
    st.session_state.history.append({"role": "assistant", "content": message})