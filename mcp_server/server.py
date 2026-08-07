
"""Serveur MCP Streamable HTTP — expose les tools MoroccoTrip."""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mcp.server.fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from tools.tools import search_tourism_docs, estimate_budget

HOST = os.getenv("MOROCCOTRIP_MCP_HOST", "127.0.0.1")
PORT = int(os.getenv("MOROCCOTRIP_MCP_PORT", "8001"))

mcp = FastMCP(
    name="MoroccoTrip",
    host=HOST,
    port=PORT,
    streamable_http_path="/mcp",
    stateless_http=True,
    json_response=True,
)


@mcp.tool()
def search_tourism_docs_tool(query: str) -> str:
    """Recherche d'infos touristiques Maroc (RAG)."""
    return search_tourism_docs.invoke({"query": query})


@mcp.tool()
def estimate_budget_tool(jours: int, niveau: str = "moyen") -> str:
    """Estime le budget d'un séjour au Maroc (MAD)."""
    return estimate_budget.invoke({"jours": jours, "niveau": niveau})


@mcp.custom_route("/health", methods=["GET"])
async def health(_: Request) -> JSONResponse:
    return JSONResponse({
        "status": "ok",
        "transport": "streamable-http",
        "endpoint": f"http://{HOST}:{PORT}/mcp",
        "tools": ["search_tourism_docs_tool", "estimate_budget_tool"],
    })


if __name__ == "__main__":
    mcp.run(transport="streamable-http")