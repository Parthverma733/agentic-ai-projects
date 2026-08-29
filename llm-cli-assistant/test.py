import os

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

load_dotenv()

console = Console()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.7,
)

messages = [
    SystemMessage(
        content=(
            "You are a helpful developer assistant. "
            "Explain technical concepts clearly and concisely."
        )
    )
]


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


def show_history():
    if len(messages) == 1:
        console.print("[yellow]No conversation history yet.[/yellow]")
        return

    console.print("\n[bold]Conversation History[/bold]\n")

    for message in messages[1:]:
        if isinstance(message, HumanMessage):
            console.print(f"[cyan]You:[/cyan] {message.content}")

        elif isinstance(message, AIMessage):
            console.print(f"[green]AI:[/green] {message.content}")


def clear_history():
    global messages

    messages = [
        SystemMessage(
            content=(
                "You are a helpful developer assistant. "
                "Explain technical concepts clearly and concisely."
            )
        )
    ]

    console.print("[green]Conversation cleared.[/green]")


def chat(user_input):
    messages.append(HumanMessage(content=user_input))

    console.print("\n[bold green]AI:[/bold green] ", end="")

    full_response = ""

    try:
        for chunk in llm.stream(messages):
            if chunk.content:
                console.print(chunk.content, end="")
                full_response += chunk.content

        console.print("\n")

        messages.append(
            AIMessage(content=full_response)
        )

    except Exception as e:
        console.print(f"\n[red]Error:[/red] {e}")

        # Remove failed user message
        messages.pop()


def main():
    console.print(
        Panel.fit(
            "[bold cyan]Developer CLI Assistant[/bold cyan]\n"
            "Type /help to see commands."
        )
    )

    while True:
        try:
            user_input = console.input("\n[bold cyan]> [/bold cyan]").strip()

            if not user_input:
                continue

            if user_input == "/exit":
                console.print("[yellow]Goodbye![/yellow]")
                break

            elif user_input == "/help":
                show_help()

            elif user_input == "/history":
                show_history()

            elif user_input == "/clear":
                clear_history()

            else:
                chat(user_input)

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break


if __name__ == "__main__":
    main()