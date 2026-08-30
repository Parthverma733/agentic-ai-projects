from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from rich.console import Console
from rich.markdown import Markdown

from core.llm import llm
from core.session import save_session

console = Console()


def chat(user_input, messages, session):
    messages.append(HumanMessage(content=user_input))

    console.print("\n[bold green]AI:[/bold green] ", end="")

    full_response = ""

    try:
        for chunk in llm.stream(messages):
            if chunk.content:
                # console.print(chunk.content, end="", markup=False)
                full_response += chunk.content
        console.print(Markdown(full_response))
        

        console.print("\n")
        messages.append(
            AIMessage(content=full_response)
        )
        save_session(session, messages)
    except Exception as e:
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
