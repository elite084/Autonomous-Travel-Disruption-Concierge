# Aegis: Agentic AI Travel Operating System

**Tagline:** Protecting Every Journey, Automatically.

Aegis is an Agentic AI Travel Operating System designed to autonomously recover a traveler's journey whenever disruptions such as flight cancellations, delays, or missed connections occur. This prototype implements the core AI Orchestrator backend.

## Architecture & Technology Stack
*   **Backend:** FastAPI (Python)
*   **AI Framework:** LangGraph + LangChain
*   **LLM:** OpenAI GPT (Mocked in this prototype for execution without API keys)
*   **Workflow:** An AI Orchestrator powered by LangGraph activates a team of specialized AI agents.

## Core Features Implemented
*   **Multi-Agent AI:** Includes specialized agents for Flight, Hotel, Benefits, Policy, and Preferences.
*   **Journey Recovery Score (JRS):** Evaluates plans based on arrival delay, total recovery cost, traveler preferences, loyalty benefit utilization, and risk of further disruption.
*   **Confidence Threshold Check:** Determines if the recovery plan can be executed autonomously or requires user approval based on a calculated confidence score.

## Setup Instructions

1.  **Install dependencies:**
    ```bash
    pip install fastapi uvicorn pydantic langgraph langchain-core pytest httpx
    ```
2.  **Run the FastAPI server:**
    ```bash
    uvicorn main:app --reload
    ```
3.  **Run the tests:**
    ```bash
    pytest test_main.py
    ```