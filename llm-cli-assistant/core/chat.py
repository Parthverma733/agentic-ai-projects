from langchain_core.messages import HumanMessage
from rich.console import Console
from rich.markdown import Markdown

from core.agent.agent import run_agent
from core.session import save_session

console = Console()


def chat(user_input, messages, session):
    messages.append(HumanMessage(content=user_input))

    console.print("\n[bold green]AI:[/bold green] ", end="")

    full_response = ""

    try:
        with console.status("[bold cyan]AI is thinking...[/bold cyan]", spinner="dots"):
            result = run_agent(messages)

        full_response = result.content
        console.print("\n[bold green]AI:[/bold green] ", end="")

        console.print(Markdown(full_response))
        

        console.print("\n")
        save_session(session, messages)
    except Exception as e:
        print("ERROR:", repr(e))
        error = str(e).lower()
        if "api key" in error or "authentication" in error:
            console.print("[red]Invalid Groq API key.[/red]")
        elif "rate limit" in error:
            console.print("[red]Rate limit reached. Try again later.[/red]")
        elif "connection" in error or "timeout" in error:
            console.print("[red]Unable to connect to Groq.[/red]")
        elif "model" in error:
            console.print("[red]Invalid or unavailable model.[/red]")
        else:
            console.print("[red]Something went wrong.[/red]")
            

        if isinstance(messages[-1], HumanMessage):
            messages.pop()
