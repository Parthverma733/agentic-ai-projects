from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import SystemMessage
from rich.console import Console
from rich.panel import Panel

from core.config import  SYSTEM_PROMPT
from core.chat import  chat
from core.commands import show_help, show_history, clear_history
from core.session import create_session ,list_sessions, load_session

console = Console()

messages = [
    SystemMessage(
        content=(
            SYSTEM_PROMPT
        )
    )
]

session = create_session()

def main():
    global messages,session
    
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

            elif user_input == "/sessions":
                list_sessions()

            elif user_input.startswith("/load "):
                session_id = user_input.split(" ", 1)[1].strip()

                loaded_session, loaded_messages = load_session(session_id)

                if loaded_session is None:
                    console.print("[red]Session not found.[/red]")
                else:
                    session = loaded_session
                    messages = loaded_messages
                    console.print(
                        f"[green]Loaded session:[/green] {session_id}"
                    )
            elif user_input == "/new":
                session = create_session()

                messages = [
                    SystemMessage(content=SYSTEM_PROMPT)
                ]

                console.print("[green]New session created.[/green]")

            else:
                chat(user_input, messages, session)

        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break


if __name__ == "__main__":
    main()
