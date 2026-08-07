"""
Tools (Bloc 5)
Pattern officiel : @tool de langchain_core.tools
"""
import re

from langchain_core.tools import tool
from rag.vectorstore import get_vectorstore

_CITY_ALIASES = {
    "Marrakech": ("marrakech",),
    "Fès": ("fès", "fes"),
    "Tanger": ("tanger", "tangier"),
}



def extract_budget_parameters(text: str) -> tuple[int, str]:
    """Extrait rapidement le nombre de jours et le niveau de budget du prompt."""
    normalized = (
        text.casefold()
        .replace("é", "e")
        .replace("è", "e")
        .replace("ê", "e")
    )
    days_match = re.search(r"(\d+)\s*jour", normalized)
    days = max(1, min(30, int(days_match.group(1)))) if days_match else 1

    level_match = re.search(
        r"(?:niveau|budget)[^\n,.]{0,24}\b(bas|faible|moyen|eleve|haut)\b",
        normalized,
    )
    aliases = {
        "bas": "bas",
        "faible": "bas",
        "moyen": "moyen",
        "eleve": "élevé",
        "haut": "élevé",
    }
    level = aliases.get(level_match.group(1), "moyen") if level_match else "moyen"
    return days, level

@tool(return_direct=True)
def search_tourism_docs(query: str) -> str:
    """Recherche dans la base documentaire tourisme Maroc.
    Utilise pour obtenir des infos fiables sur les villes, budgets, activités.
    """
    vs = get_vectorstore()
    normalized_query = query.casefold()
    selected_city = next(
        (
            city
            for city, aliases in _CITY_ALIASES.items()
            if any(alias in normalized_query for alias in aliases)
        ),
        None,
    )
    if selected_city:
        docs = vs.similarity_search(query, k=3, filter={"ville": selected_city})
        docs += vs.similarity_search(query, k=1, filter={"ville": "général"})
    else:
        docs = vs.similarity_search(query, k=3)
    if not docs:
        return "Aucun document trouvé."
    results = []
    for d in docs:
        source = d.metadata.get("source", "?")
        url = d.metadata.get("url")
        reference = f"[{source}]" + (f" {url}" if url else "")
        results.append(f"{reference}\n{d.page_content}")
    return "\n\n".join(results)


@tool
def estimate_budget(jours: int, niveau: str = "moyen") -> str:
    """Estime le budget total pour un voyage au Maroc.
    jours: nombre de jours (1-30)
    niveau: 'bas', 'moyen' ou 'élevé'
    """
    if jours < 1 or jours > 30:
        return "Erreur : nombre de jours doit être entre 1 et 30."
    niveaux = {"bas": 450, "moyen": 700, "élevé": 1200}
    if niveau not in niveaux:
        return "Erreur : niveau doit être 'bas', 'moyen' ou 'élevé'."
    total = jours * niveaux[niveau]
    return (
        f"Budget estimé ({niveau}) pour {jours} jour(s) : "
        f"environ {total} MAD (hébergement + repas + transport local). "
        f"Hors vols internationaux."
    )


RESEARCH_TOOLS = [search_tourism_docs]
PLANNER_TOOLS = [estimate_budget]
ALL_TOOLS = [search_tourism_docs, estimate_budget]