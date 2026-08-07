"""Interface guidée de préparation de séjour pour Streamlit."""

from html import escape
from typing import Callable

import streamlit as st


CITIES = ("Marrakech", "Fès", "Tanger")
INTERESTS = (
    "Patrimoine",
    "Gastronomie",
    "Artisanat",
    "Culture",
    "Nature",
    "Photographie",
    "Shopping local",
)
PACE_OPTIONS = {
    "Tranquille": "Des journées légères avec de vraies pauses",
    "Équilibré": "Un bon équilibre entre visites et temps libre",
    "Intensif": "Un maximum de découvertes chaque jour",
}
TRANSPORT_OPTIONS = {
    "À pied": "walking",
    "Taxi / voiture": "driving",
    "Transports publics": "transit",
    "Vélo": "bicycling",
}


APP_CSS = """
<style>
    :root {
        --ink: #19352f;
        --muted: #65736e;
        --sand: #f7f1e7;
        --paper: #fffdf8;
        --terracotta: #c7603d;
        --terracotta-dark: #a9472d;
        --green: #174c43;
        --gold: #e6b85c;
        --line: rgba(25, 53, 47, 0.12);
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 8% 5%, rgba(230, 184, 92, 0.18), transparent 24rem),
            radial-gradient(circle at 95% 22%, rgba(199, 96, 61, 0.12), transparent 28rem),
            #f7f3ec;
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stStatusWidget"],
    [data-testid="stAppDeployButton"] {
        display: none !important;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    .morocco-hero {
        position: relative;
        overflow: hidden;
        padding: 3.2rem 3.4rem;
        margin-bottom: 1.5rem;
        border-radius: 28px;
        color: white;
        background:
            linear-gradient(115deg, rgba(18, 66, 57, 0.98), rgba(29, 92, 77, 0.92)),
            #174c43;
        box-shadow: 0 24px 70px rgba(29, 70, 61, 0.18);
    }

    .morocco-hero::before {
        content: "";
        position: absolute;
        width: 330px;
        height: 330px;
        right: -95px;
        top: -170px;
        border: 1px solid rgba(255, 255, 255, 0.22);
        border-radius: 50%;
        box-shadow: 0 0 0 36px rgba(255,255,255,0.035), 0 0 0 78px rgba(255,255,255,0.025);
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.42rem 0.78rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.1);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .morocco-hero h1 {
        max-width: 760px;
        margin: 1.25rem 0 0.7rem;
        color: white;
        font-size: clamp(2.25rem, 5vw, 4.5rem);
        line-height: 0.98;
        letter-spacing: -0.045em;
    }

    .morocco-hero p {
        max-width: 670px;
        margin: 0;
        color: rgba(255, 255, 255, 0.78);
        font-size: 1.05rem;
        line-height: 1.65;
    }

    .city-chips, .preference-chips {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 1.25rem;
    }

    .city-chip {
        padding: 0.46rem 0.82rem;
        border-radius: 999px;
        color: #fff6e8;
        background: rgba(255, 255, 255, 0.11);
        font-size: 0.86rem;
        font-weight: 650;
    }

    .section-heading {
        margin: 0 0 1rem;
    }

    .section-eyebrow {
        color: var(--terracotta);
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .section-heading h2 {
        margin: 0.25rem 0 0.25rem;
        color: var(--ink);
        font-size: 1.8rem;
        letter-spacing: -0.025em;
    }

    .section-heading p {
        margin: 0;
        color: var(--muted);
    }

    div[data-testid="stForm"] {
        padding: 1.65rem 1.7rem 1.8rem;
        border: 1px solid var(--line);
        border-radius: 24px;
        background: rgba(255, 253, 248, 0.92);
        box-shadow: 0 16px 50px rgba(37, 62, 56, 0.08);
    }

    div[data-testid="stForm"] label,
    div[data-testid="stForm"] [data-testid="stWidgetLabel"] p {
        color: var(--ink);
        font-weight: 700;
    }

    div[data-testid="stNumberInput"] input,
    div[data-testid="stNumberInputContainer"] input {
        color: var(--ink) !important;
        -webkit-text-fill-color: var(--ink) !important;
        opacity: 1 !important;
    }

    div[data-testid="stNumberInput"] input::placeholder,
    div[data-testid="stNumberInputContainer"] input::placeholder {
        color: var(--muted) !important;
        -webkit-text-fill-color: var(--muted) !important;
        opacity: 1 !important;
    }

    div[data-baseweb="select"] > div,
    div[data-testid="stNumberInputContainer"],
    textarea {
        border-color: rgba(25, 53, 47, 0.15) !important;
        border-radius: 12px !important;
        background: #fffefa !important;
    }

    div[data-testid="stPills"] button {
        border-color: rgba(23, 76, 67, 0.16);
        border-radius: 999px;
    }

    button[kind="primary"] {
        min-height: 3.2rem;
        border: 0;
        border-radius: 14px;
        color: white;
        background: linear-gradient(135deg, var(--terracotta), var(--terracotta-dark));
        box-shadow: 0 12px 28px rgba(169, 71, 45, 0.22);
        font-weight: 800;
    }

    button[kind="primary"]:hover {
        border: 0;
        color: white;
        transform: translateY(-1px);
    }

    .trust-strip {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin: 1rem 0 2rem;
    }

    .trust-item {
        padding: 0.9rem 1rem;
        border: 1px solid var(--line);
        border-radius: 14px;
        color: var(--muted);
        background: rgba(255, 255, 255, 0.58);
        font-size: 0.86rem;
        text-align: center;
    }

    .trust-item strong { color: var(--green); }

    .result-banner {
        margin-top: 2.5rem;
        padding: 1.7rem 1.9rem;
        border-radius: 22px;
        color: white;
        background: linear-gradient(120deg, #b94f31, #d47a4f);
        box-shadow: 0 18px 45px rgba(169, 71, 45, 0.18);
    }

    .result-banner h2 {
        margin: 0.25rem 0 0.3rem;
        color: white;
        font-size: 2rem;
    }

    .result-banner p { margin: 0; color: rgba(255,255,255,0.8); }

    div[data-testid="stMetric"] {
        padding: 1rem 1.1rem;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: rgba(255, 253, 248, 0.86);
    }

    div[data-testid="stMetricValue"] {
        color: var(--green);
        font-size: 1.35rem;
    }

    .preference-chip {
        padding: 0.42rem 0.72rem;
        border-radius: 999px;
        color: var(--green);
        background: #e8f0ec;
        font-size: 0.82rem;
        font-weight: 700;
    }

    .result-note {
        margin-top: 1rem;
        padding: 0.9rem 1rem;
        border-left: 4px solid var(--gold);
        border-radius: 0 12px 12px 0;
        color: var(--muted);
        background: #fff9ea;
        font-size: 0.9rem;
    }

    @media (max-width: 760px) {
        [data-testid="stMainBlockContainer"] { padding: 1rem 1rem 3rem; }
        .morocco-hero { padding: 2rem 1.4rem; border-radius: 20px; }
        .morocco-hero h1 { font-size: 2.55rem; }
        .trust-strip { grid-template-columns: 1fr; }
        div[data-testid="stForm"] { padding: 1.15rem; border-radius: 18px; }
    }
</style>
"""


def build_trip_prompt(selection: dict) -> str:
    """Transforme uniquement les choix du formulaire en demande contrôlée."""
    interests = ", ".join(selection["interests"])
    constraints = selection["constraints"] or "Aucune contrainte particulière"
    daily_budget = selection["budget_mad"] / selection["days"]
    if daily_budget <= 500:
        budget_level = "bas"
    elif daily_budget <= 900:
        budget_level = "moyen"
    else:
        budget_level = "élevé"

    return (
        f"Prépare un programme de voyage exclusivement dans la ville de {selection['city']}.\n"
        f"Durée : {selection['days']} jour(s).\n"
        f"Budget total maximum : {selection['budget_mad']} MAD, niveau {budget_level}.\n"
        f"Centres d'intérêt sélectionnés : {interests}.\n"
        f"Rythme : {selection['pace']}.\n"
        f"Transport préféré : {selection['transport_label']}.\n"
        f"Contraintes : {constraints}.\n\n"
        "Contraintes obligatoires pour la réponse :\n"
        f"- Reste uniquement à {selection['city']} et ne propose aucune autre ville.\n"
        "- Respecte le budget total maximum et les préférences fournies.\n"
        "- Organise chaque journée en matin, après-midi et soirée.\n"
        "- Indique des coûts estimatifs en MAD et des durées réalistes.\n"
        "- Termine par des conseils pratiques et les références [source] utilisées.\n"
        "- Réponds en français avec des titres courts et une présentation claire."
    )


def _reset_trip(clear_memory: Callable[[], None]) -> None:
    st.session_state.trip_result = None
    st.session_state.trip_selection = None
    clear_memory()


def _render_result(result: str, selection: dict, clear_memory: Callable[[], None]) -> None:
    city = escape(selection["city"])
    st.markdown(
        f"""
        <div class="result-banner">
            <div class="section-eyebrow" style="color:#ffe4a8">Votre carnet de route</div>
            <h2>{city}, votre séjour est prêt.</h2>
            <p>Programme construit à partir de vos choix et contrôlé par les agents.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_columns = st.columns(4)
    metric_columns[0].metric("Destination", selection["city"])
    metric_columns[1].metric("Durée", f"{selection['days']} jour(s)")
    metric_columns[2].metric("Budget plafond", f"{selection['budget_mad']:,} MAD".replace(",", " "))
    metric_columns[3].metric("Rythme", selection["pace"])

    program_tab, choices_tab = st.tabs(["🗓️ Programme personnalisé", "✓ Vos choix"])
    with program_tab:
        with st.container(border=True):
            st.markdown(result)
        st.markdown(
            "<div class='result-note'>Les coûts sont indicatifs. Vérifiez les horaires et tarifs avant votre visite.</div>",
            unsafe_allow_html=True,
        )

    with choices_tab:
        tags = "".join(
            f"<span class='preference-chip'>{escape(interest)}</span>"
            for interest in selection["interests"]
        )
        st.markdown(f"<div class='preference-chips'>{tags}</div>", unsafe_allow_html=True)
        st.markdown(f"**Transport :** {selection['transport_label']}")
        st.markdown(
            f"**Contraintes :** {selection['constraints'] or 'Aucune contrainte particulière'}"
        )

    if st.button("Créer un autre séjour", icon="🔄", width="stretch"):
        _reset_trip(clear_memory)
        st.rerun()


def render_trip_builder(
    run_trip: Callable[[str], str],
    clear_memory: Callable[[], None],
    format_error: Callable[[Exception], str],
) -> None:
    """Affiche le configurateur et le programme généré."""
    st.markdown(APP_CSS, unsafe_allow_html=True)

    if "trip_result" not in st.session_state:
        st.session_state.trip_result = None
    if "trip_selection" not in st.session_state:
        st.session_state.trip_selection = None

    st.markdown(
        """
        <section class="morocco-hero">
            <span class="hero-kicker">✦ MoroccoTrip AI · séjour sur mesure</span>
            <h1>Le Maroc, cadré autour de vos envies.</h1>
            <p>Choisissez votre destination et vos préférences. Nos agents construisent un programme réaliste, clair et limité à la ville sélectionnée.</p>
            <div class="city-chips">
                <span class="city-chip">☀ Marrakech</span>
                <span class="city-chip">⌘ Fès</span>
                <span class="city-chip">≈ Tanger</span>
            </div>
        </section>
        <div class="trust-strip">
            <div class="trust-item"><strong>3 destinations</strong><br>Une base volontairement ciblée</div>
            <div class="trust-item"><strong>Programme contrôlé</strong><br>Research → Planner</div>
            <div class="trust-item"><strong>Budget cadré</strong><br>Selon votre plafond en MAD</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    heading_column, reset_column = st.columns([5, 1])
    with heading_column:
        st.markdown(
            """
            <div class="section-heading">
                <span class="section-eyebrow">Étape 1 · Vos préférences</span>
                <h2>Composez votre séjour</h2>
                <p>Quelques choix suffisent. Aucun prompt à rédiger.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with reset_column:
        if st.session_state.trip_result and st.button("Réinitialiser", width="stretch"):
            _reset_trip(clear_memory)
            st.rerun()

    with st.form("trip_form", clear_on_submit=False):
        left, right = st.columns(2, gap="large")
        with left:
            city = st.selectbox("Destination", CITIES, help="Le programme restera dans cette ville.")
            days = st.slider("Nombre de jours", 1, 7, 3)
            budget = st.number_input(
                "Budget total maximum (MAD)",
                min_value=300,
                max_value=50_000,
                value=2_500,
                step=100,
            )
            pace = st.selectbox(
                "Rythme du séjour",
                tuple(PACE_OPTIONS),
                index=1,
                help="Équilibré convient à la plupart des voyageurs.",
            )
            st.caption(PACE_OPTIONS[pace])

        with right:
            interests = st.pills(
                "Centres d'intérêt",
                INTERESTS,
                selection_mode="multi",
                default=["Patrimoine", "Gastronomie"],
                width="stretch",
            )
            transport_label = st.selectbox("Transport préféré", tuple(TRANSPORT_OPTIONS))
            constraints = st.text_area(
                "Contraintes particulières",
                placeholder="Ex. : éviter les longues marches, voyage avec enfants…",
                max_chars=300,
                height=108,
            )

        submitted = st.form_submit_button(
            "Créer mon programme personnalisé",
            type="primary",
            icon="✨",
            width="stretch",
        )

    if submitted:
        if not interests:
            st.warning("Choisissez au moins un centre d'intérêt.")
        else:
            selection = {
                "city": city,
                "days": int(days),
                "budget_mad": int(budget),
                "interests": list(interests),
                "pace": pace,
                "transport_label": transport_label,
                "transport_mode": TRANSPORT_OPTIONS[transport_label],
                "constraints": constraints.strip(),
            }
            clear_memory()
            try:
                with st.spinner("Recherche des meilleures idées puis création du programme…"):
                    st.session_state.trip_result = run_trip(build_trip_prompt(selection))
                    st.session_state.trip_selection = selection
            except Exception as exc:
                st.session_state.trip_result = None
                st.session_state.trip_selection = None
                st.error(format_error(exc))

    if st.session_state.trip_result and st.session_state.trip_selection:
        _render_result(
            st.session_state.trip_result,
            st.session_state.trip_selection,
            clear_memory,
        )
