# LLM CLI Assistant

A simple command-line AI assistant built with **Python, LangChain, and Groq**.

This project is part of my Agentic AI learning journey, starting with basic LLM interaction before moving toward LangGraph, tool calling, and MCP.

## Features

* Interactive CLI chat
* Groq LLM integration
* Streaming responses
* In-memory conversation history
* Hidden model reasoning
* Basic error handling
* Rich terminal interface

## Commands

| Command    | Description                |
| ---------- | -------------------------- |
| `/help`    | Show available commands    |
| `/history` | Show conversation history  |
| `/clear`   | Clear conversation history |
| `/model`   | Show the current LLM model |
| `/exit`    | Exit the assistant         |

## Tech Stack

* Python
* LangChain
* LangChain Groq
* Groq API
* Rich
* python-dotenv
* uv

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd llm-cli-assistant
```

### 2. Install dependencies

Using `uv`:

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit the `.env` file to GitHub.

### 4. Run the assistant

```bash
uv run main.py
```

## Example

```text
╭─────────────────────────────╮
│ Developer CLI Assistant     │
│ Type /help to see commands. │
╰─────────────────────────────╯

> What is LangGraph?

AI: LangGraph is a framework for building stateful,
multi-step AI applications.

> /history

Conversation History

You:
What is LangGraph?

AI:
LangGraph is a framework for...
```

## Current Version

**Version 1**

The current version focuses on understanding:

* LLM API interaction
* LangChain messages
* System, human, and AI messages
* Conversation state
* Response streaming
* CLI command handling

## Planned Improvements

* Persistent conversation sessions
* Model switching
* Tool calling
* File-system tools
* LangGraph integration
* MCP integration

## Learning Roadmap

```text
LLM CLI Assistant
       ↓
Memory & Sessions
       ↓
Tool Calling
       ↓
LangGraph
       ↓
Agentic AI
       ↓
MCP
```
