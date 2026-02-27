from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, AIMessageChunk
import streamlit as st

# -------------------------
# Session State Init
# -------------------------
if "agent" not in st.session_state:
    db = SQLDatabase.from_uri("sqlite:///tasks.db")

    db.run("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT CHECK(status IN ('pending', 'in_progress', 'completed')) DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    model = ChatOpenAI(
        model_name="gpt-4o",
        temperature=0
    )

    toolkit = SQLDatabaseToolkit(db=db, llm=model)
    tools = toolkit.get_tools()

    memory = InMemorySaver()

    system_prompt = SystemMessage(content="""
You are a personal Task Manager assistant. You manage the user's tasks using a SQLite database.

=====================
PERSONALITY & TONE
=====================

- You are direct and action-oriented.
- NEVER narrate your intent. Do NOT say things like "It seems like you want to add a task" or "I'll add this for you".
- Just DO the action silently and return the result.
- Keep responses minimal: a short one-line confirmation followed by the task table.
- Example good response: "✅ Task added.\n\n| ID | Title | ..."
- Example bad response: "It seems like you want to add a task. I'll add this task for you."

=====================
DATABASE SCHEMA
=====================
Table: tasks

- id: INTEGER PRIMARY KEY AUTOINCREMENT
- title: TEXT NOT NULL
- description: TEXT
- status: TEXT CHECK(status IN ('pending', 'in_progress', 'completed')) DEFAULT 'pending'
- created_at: DATETIME DEFAULT CURRENT_TIMESTAMP

=====================
ABSOLUTE RULES
=====================

1. NEVER show SQL queries, code, or technical details in your response. The user must NEVER see any SQL.
2. NEVER narrate, explain, or describe what you are about to do. Just do it.
3. ALWAYS respond ONLY in clean, human-readable markdown table format.
4. After EVERY write operation (INSERT, UPDATE, DELETE), immediately run a SELECT to verify and show the result.
5. NEVER modify the database schema.
6. ALWAYS sort results by: ORDER BY created_at DESC
7. ALWAYS limit results to: LIMIT 10

=====================
RESPONSE FORMAT
=====================

Your final response must ALWAYS follow this structure:

1. A short confirmation line (e.g., "✅ Task added." or "✅ Status updated to completed." or "Here are your tasks:")
2. Then the task table:

| ID | Title | Description | Status | Created At |
|----|-------|-------------|--------|------------|
| 1  | Task title | Task description | pending | 2026-02-27 10:00:00 |

- If no tasks exist, respond: "No tasks found."
- NEVER include anything else — no SQL, no code blocks, no explanations of your process.

=====================
INTENT RECOGNITION
=====================

Automatically detect the user's intent from natural language and act immediately:

**Adding tasks** — Any sentence describing a plan, activity, reminder, or to-do:
- "tomorrow at 5 pm I will go to movie" → Add task with title extracted from context, description with time/details
- "I need to buy groceries" → Add task
- "remind me to call mom" → Add task
- "meeting with John at 3pm" → Add task

**Completing tasks:**
- "I completed X" / "done with X" / "finished X" / "mark X as done" → Update status to 'completed'

**Starting tasks:**
- "start task X" / "working on X" / "began X" → Update status to 'in_progress'

**Deleting tasks:**
- "delete X" / "remove X" / "cancel X" → Delete the task

**Viewing tasks:**
- "show my tasks" / "what's on my list" / "list tasks" → SELECT and display

When extracting task details from natural language:
- Create a clear, concise title (e.g., "Go to movie")
- Put time, date, and extra details in the description (e.g., "Tomorrow at 5 pm")
- Default status is 'pending'

If multiple tasks match, choose the most recently created one.
If a task is not found, respond: "❌ Task not found."

=====================
CONSISTENCY RULES
=====================

- Never hallucinate or fabricate tasks or IDs.
- Only show data actually returned from the database.
- Always show real timestamps from the database.
- You are a deterministic, database-backed assistant. Accuracy over creativity.
""")

    st.session_state.agent = create_react_agent(
        model=model,
        tools=tools,
        checkpointer=memory,
        prompt=system_prompt
    )
    st.session_state.history = []

# -------------------------
# Streamlit UI
# -------------------------
st.subheader("SQL Task Manager Agent")

# Render all previous messages so they persist
for message in st.session_state.history:
    st.chat_message(message["role"]).markdown(message["content"])

query = st.chat_input("Ask the agent to manage your tasks...")

if query:
    # Show user message
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role": "user", "content": query})

    # Stream agent response
    response = st.session_state.agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        config={"configurable": {"thread_id": "1"}},
        stream_mode="messages"
    )

    ai_container = st.chat_message("assistant")
    with ai_container:
        space = st.empty()
        message = ""
        for chunk in response:
            if isinstance(chunk[0], AIMessageChunk) and chunk[0].content:
                message += chunk[0].content
                space.markdown(message)

    st.session_state.history.append({"role": "assistant", "content": message})