"""
Guardrails (Bloc 4)
Fonctions simples d'entrée / sortie.
"""
import re
from typing import Any


def check_input(text: str) -> str | None:
    """Retourne un message d'erreur si input invalide, sinon None."""
    if not text or len(text.strip()) < 3:
        return "Message trop court."

    patterns = [
        r"ignore\s+(previous|all)\s+instructions",
        r"system\s*prompt",
        r"jailbreak",
        r"forget\s+everything",
    ]
    lower = text.lower()
    for p in patterns:
        if re.search(p, lower):
            return "Requête non autorisée (guardrail input)."

    if any(w in lower for w in ["bitcoin", "crypto trading", "code python complet", "hacking"]):
        return "Je suis spécialisé uniquement sur le tourisme au Maroc."

    return None


def _normalize_text(value: Any) -> str:
    """Convertit les blocs de contenu LangChain en texte simple."""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(
            part for item in value if (part := _normalize_text(item))
        )
    if isinstance(value, dict):
        for key in ("text", "content", "output"):
            if key in value:
                return _normalize_text(value[key])
        return ""
    return "" if value is None else str(value)


def check_output(text: Any) -> str:
    """Valide / nettoie la sortie."""
    text = _normalize_text(text).strip()
    if not text or len(text.strip()) < 10:
        return "Désolé, je n'ai pas pu générer une réponse pertinente. Reformule ta demande."
    return text
