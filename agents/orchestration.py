
"""Orchestration multi-agent — local ou MCP selon env."""

import os

from agents.research import create_research_agent
from agents.planner import create_planner_agent
from guardrails.guards import check_input, check_output
from tools.tools import estimate_budget, extract_budget_parameters

# mémoire simple
_history: list = []


def _use_mcp() -> bool:
    return os.getenv("MOROCCOTRIP_USE_MCP", "false").lower() in ("1", "true", "yes")


def run_multi_agent(user_input: str, session_id: str = "default") -> str:
    # Branche MCP
    if _use_mcp():
        from agents.mcp_orchestration import run_multi_agent_mcp_sync
        return run_multi_agent_mcp_sync(user_input)

    # Branche locale
    err = check_input(user_input)
    if err:
        return err

    research = create_research_agent()
    research_out = research.invoke({
        "input": user_input,
        "chat_history": _history[-6:],
    })
    research_text = research_out.get("output", "")

    days, level = extract_budget_parameters(user_input)
    budget_text = estimate_budget.invoke({"jours": days, "niveau": level})

    planner = create_planner_agent(tools=[])
    planner_out = planner.invoke({
        "input": (
            f"Demande : {user_input}\n\n"
            f"Infos Research :\n{research_text}\n\n"
            f"Budget contrôlé :\n{budget_text}\n\n"
            "Construis l'itinéraire final sans appeler d'autre outil."
        ),
        "chat_history": [],
    })
    answer = check_output(planner_out.get("output", ""))

    _history.append({"role": "user", "content": user_input})
    _history.append({"role": "assistant", "content": answer})
    return answer


def clear_memory():
    _history.clear()