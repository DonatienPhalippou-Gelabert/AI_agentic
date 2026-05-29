# AI_agentic
Personal project of building tools from scratch for a LLM

This project is a straightforward implementation designed to understand the core concepts of agentic AI and Function Calling without relying on high-level, black-box frameworks. The objective is to observe the raw interaction between a Large Language Model (LLM) and local Python functions.

## Features
- Simplified ReAct Loop: Manual management of the Question -> Intention (Tool Call) -> Python Execution -> Final Response cycle.
- Custom Local Tool: Integration of a currency conversion function to extend the model's capabilities.
- Data Security: API key management via environment variables to prevent accidental leaks on public repositories.

## Tech Stack
- Language: Python 3.10+
- LLM: OpenAI gpt-4o (via langchain-openai)
- Environment Management: python-dotenv

## Architecture and Workflow

The script does not use the LLM to directly generate a text response based on mathematical intuition, but rather to decide whether an external tool is required.

1. The user asks a question that requires a precise calculation.
2. The LLM inspects the provided function signature and returns a JSON structure containing the required arguments.
3. The local Python code intercepts this JSON, executes the native function, and sends the raw result back to the model.
4. The LLM formulates the final response to the user based on this result.

## Project Structure

- `main.py`: Entry point of the script containing the connection logic and the decision loop.
- `tools.py`: Collection of local functions available for the agent to use.
- `requirements.txt`: List of dependencies required for the project.
- `.env`: Local file (excluded from Git) containing the OpenAI API key.
