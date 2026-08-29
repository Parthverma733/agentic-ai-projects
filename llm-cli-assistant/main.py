from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import SystemMessage
from rich.console import Console
from rich.panel import Panel

from core.config import  SYSTEM_PROMPT
from core.chat import  chat
from core.commands import show_help, show_history, clear_history

console = Console()

messages = [
    SystemMessage(
        content=(
            SYSTEM_PROMPT
        )
    )
]

def main():
    global messages
    
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
                show_history(messages)

            elif user_input == "/clear":
                messages = clear_history()

            else:
                chat(user_input,messages)

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break


if __name__ == "__main__":
    main()
