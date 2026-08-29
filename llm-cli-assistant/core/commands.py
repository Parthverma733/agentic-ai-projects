from rich.console import Console
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from rich.markdown import Markdown
from rich.console import Group
from core.config import SYSTEM_PROMPT

console = Console()

def show_help():
    console.print(
        """
[bold]Available Commands[/bold]

/help      Show available commands
/history   Show conversation history
/clear     Clear conversation history
/exit      Exit the assistant
"""
    )

def show_history(messages):
    if len(messages) == 1:
        console.print("[yellow]No conversation history yet.[/yellow]")
        return
    console.print("\n[bold]Conversation History[/bold]\n")
    for message in messages[1:]:
        if isinstance(message,HumanMessage):
            content = Group(
                "[cyan]You:[/cyan]",
                Markdown(message.content)
            )
            console.print(content)
        elif isinstance(message, AIMessage):
            content = Group(
                "[green]AI:[/green]",
                Markdown(message.content)
            )
            console.print(content)


def clear_history():

    messages = [
        SystemMessage(
            content=(
                SYSTEM_PROMPT
            )
        )
    ]

    console.print("[green]Conversation cleared.[/green]")
    return messages