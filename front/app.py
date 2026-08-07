"""
Frontend Streamlit
100 % LangChain
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st

from agents.orchestration import run_multi_agent, clear_memory
from front.trip_builder import render_trip_builder


def format_error(exc: Exception) -> str:
    """Affiche une aide adaptee sans confondre quota et cle invalide."""
    message = str(exc)
    if "insufficient_quota" in message or "credit_balance_exhausted" in message:
        return (
            "Le quota ou le crédit de l'API OpenAI est épuisé. "
            "Vérifie l'utilisation et la facturation sur "
            "[OpenAI Platform](https://platform.openai.com/usage)."
        )
    if "429" in message:
        return (
            "La limite de requêtes OpenAI est atteinte. "
            "Attends le délai indiqué, puis réessaie."
        )
    if "invalid_api_key" in message or "401" in message:
        return "La clé OPENAI_API_KEY est absente ou invalide dans le fichier .env."
    return (
        f"Erreur : {message}\n\n"
        "Vérifie la variable OPENAI_API_KEY dans le fichier .env."
    )

@st.cache_data(ttl=1800, show_spinner=False)
def run_multi_agent_cached(user_input: str) -> str:
    return run_multi_agent(user_input)

st.set_page_config(
    page_title="MoroccoTrip AI",
    page_icon="🇲🇦",
    layout="wide",
    initial_sidebar_state="collapsed",
)
render_trip_builder(run_multi_agent_cached, clear_memory, format_error)
