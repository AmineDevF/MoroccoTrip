"""
Agent Planner (Bloc 1)
Pattern officiel LangChain : create_tool_calling_agent + AgentExecutor
"""
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from config.settings import LLM_CONFIG
from tools.tools import PLANNER_TOOLS


def create_planner_agent(
    model: str | None = None,
    tools=None,
) -> AgentExecutor:
    """
    Agent 2 — Planner
    Rôle : construire l'itinéraire final + budget à partir des infos Research.
    Prompt orienté planification pour construire l'itinéraire.
    """

    cfg = LLM_CONFIG["planner"]
    llm_kwargs = {
        "model": model or cfg["model"],
        "max_tokens": cfg["max_tokens"],
    }
    if cfg.get("reasoning_effort"):
        llm_kwargs["reasoning_effort"] = cfg["reasoning_effort"]
    llm = ChatOpenAI(**llm_kwargs)

    active_tools = list(tools) if tools is not None else PLANNER_TOOLS
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Tu es l'agent Planner. Tu reçois les informations collectées par l'agent Research. "
            "Ton rôle : construire un itinéraire clair jour par jour, avec conseils pratiques "
            "et estimation de budget. "
            "Utilise l'outil estimate_budget si un nombre de jours et un niveau de budget "
            "sont mentionnés. "
            "Structure ta réponse :\n"
            "1. Résumé de la demande\n"
            "2. Itinéraire jour par jour\n"
            "3. Budget estimé\n"
            "4. Conseils pratiques\n"
            "Cite les sources ([source]) quand tu t'appuies sur les documents. "
            "Réponds en français, de façon claire et utile.",
        ),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, active_tools, prompt)
    return AgentExecutor(
        agent=agent,
        tools=active_tools,
        verbose=False,
        handle_parsing_errors=True,
    )
    