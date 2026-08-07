"""
Agent Research (Bloc 1)
Pattern officiel LangChain : create_tool_calling_agent + AgentExecutor
"""
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from config.settings import LLM_CONFIG
from tools.tools import RESEARCH_TOOLS


def create_research_agent(
    model: str | None = None,
    tools=None,
) -> AgentExecutor:
    """
    Agent 1 — Research
    Rôle : collecter les informations factuelles via RAG.
    Prompt strict pour rester factuel.
    """

    cfg = LLM_CONFIG["research"]
    llm_kwargs = {
        "model": model or cfg["model"],
        "max_tokens": cfg["max_tokens"],
    }
    if cfg.get("reasoning_effort"):
        llm_kwargs["reasoning_effort"] = cfg["reasoning_effort"]
    llm = ChatOpenAI(**llm_kwargs)

    active_tools = list(tools) if tools is not None else RESEARCH_TOOLS
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Tu es l'agent Research. Ton seul rôle est de collecter des informations "
            "factuelles sur le Maroc. "
            "Utilise OBLIGATOIREMENT l'outil search_tourism_docs pour chaque demande. "
            "Mentionne toujours la ville sélectionnée dans la requête envoyée à l'outil. "
            "Résume clairement les infos trouvées (villes, activités, budgets indicatifs, conseils). "
            "Ne construis pas d'itinéraire. Ne réponds pas de façon créative. "
            "Juste les faits extraits des documents. "
            "Réponds en français.",
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
