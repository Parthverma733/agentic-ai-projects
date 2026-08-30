from rich.console import Console
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import json
import os

from core.config import SYSTEM_PROMPT

console = Console()
def create_session():
    now = datetime.now()

    session_id = now.strftime("%Y-%m-%d_%H-%M-%S")

    session = {
        "session_id": session_id,
        "created_at": now.isoformat(),
        "messages": []
    }

    return session

def save_session(session, messages):
    os.makedirs("sessions", exist_ok=True)

    saved_messages = []

    for message in messages:
        if isinstance(message, AIMessage):
            saved_messages.append({
                "role": "ai",
                "content": message.content
            })

        elif isinstance(message, HumanMessage):
            saved_messages.append({
                "role": "user",
                "content": message.content
            })

    session["messages"] = saved_messages

    file_path = f"sessions/{session['session_id']}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(session, file, indent=4)


    

def load_session(session_id):
    file_path = f"sessions/{session_id}.json"

    if not os.path.exists(file_path):
        return None, None

    with open(file_path, "r", encoding="utf-8") as file:
        session = json.load(file)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]

    for message in session["messages"]:
        if message["role"] == "user":
            messages.append(
                HumanMessage(content=message["content"])
            )

        elif message["role"] == "ai":
            messages.append(
                AIMessage(content=message["content"])
            )

    return session, messages


def list_sessions():
    if not os.path.exists("sessions"):
        console.print("[yellow]No saved sessions.[/yellow]")
        return

    files = os.listdir("sessions")

    session_files = [
        file for file in files
        if file.endswith(".json")
    ]

    if not session_files:
        console.print("[yellow]No saved sessions.[/yellow]")
        return

    console.print("\n[bold]Saved Sessions[/bold]\n")

    for file in session_files:
        session_id = file.removesuffix(".json")
        console.print(f"[cyan]{session_id}[/cyan]")