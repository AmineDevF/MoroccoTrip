
"""Orchestration via tools MCP (Streamable HTTP)."""

import asyncio
import os

from langchain_mcp_adapters.client import MultiServerMCPClient

from agents.research import create_research_agent
from agents.planner import create_planner_agent
from guardrails.guards import check_input, check_output
from tools.tools import extract_budget_parameters

MCP_URL = os.getenv("MOROCCOTRIP_MCP_URL", "http://127.0.0.1:8001/mcp")


async def _get_mcp_tools() -> list:
    client = MultiServerMCPClient({
        "moroccotrip": {"transport": "http", "url": MCP_URL}
    })
    tools = await client.get_tools()
    if not tools:
        raise RuntimeError(f"Aucun tool MCP à {MCP_URL}. Lance le serveur MCP.")
    return tools


async def run_multi_agent_mcp(user_input: str) -> str:
    err = check_input(user_input)
    if err:
        return err

    tools = await _get_mcp_tools()
    tools_by_name = {tool.name: tool for tool in tools}
    search_tool = tools_by_name.get("search_tourism_docs_tool")
    budget_tool = tools_by_name.get("estimate_budget_tool")
    if search_tool is None or budget_tool is None:
        raise RuntimeError("Les tools MCP MoroccoTrip requis sont indisponibles.")

    # Research conserve son appel RAG, mais retourne directement les sources.
    search_tool.return_direct = True
    research = create_research_agent(tools=[search_tool])
    days, level = extract_budget_parameters(user_input)
    research_out, budget_text = await asyncio.gather(
        research.ainvoke({
            "input": user_input,
            "chat_history": [],
        }),
        budget_tool.ainvoke({"jours": days, "niveau": level}),
    )
    research_text = research_out.get("output", "")

    # Le budget déterministe est déjà contrôlé : Planner produit en un seul appel.
    planner = create_planner_agent(tools=[])
    planner_out = await planner.ainvoke({
        "input": (
            f"Demande : {user_input}\n\n"
            f"Infos MCP Research :\n{research_text}\n\n"
            f"Budget MCP contrôlé :\n{budget_text}\n\n"
            "Construis l'itinéraire final sans appeler d'autre outil."
        ),
        "chat_history": [],
    })
    return check_output(planner_out.get("output", ""))


def run_multi_agent_mcp_sync(user_input: str) -> str:
    """Version synchrone pour Streamlit."""
    return asyncio.run(run_multi_agent_mcp(user_input))