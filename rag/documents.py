"""
Base documentaire Maroc (Bloc 2 — RAG)
8 documents comme demandé dans le cahier des charges.
"""
from langchain_core.documents import Document

DOCS = [
    Document(
        page_content=(
            "Marrakech : la médina, la place Jemaa el-Fna, la Koutoubia et les jardins "
            "de la Ménara forment un parcours culturel majeur. Les souks permettent de "
            "découvrir l'artisanat et l'ambiance locale. Budget indicatif : 600 à 900 "
            "MAD par jour pour hébergement, repas et transport local."
        ),
        metadata={
            "source": "office_tourisme_marrakech", "ville": "Marrakech",
            "url": "https://www.visitmorocco.com/fr/voyage/marrakech",
        },
    ),
    Document(
        page_content=(
            "Fès : la médina Fès-El-Bali, Bab Boujloud, les tanneries, le musée Nejjarine "
            "et la mosquée-université Al Quaraouiyine composent le cœur culturel. La médina "
            "se visite surtout à pied. Budget indicatif : 500 à 800 MAD par jour."
        ),
        metadata={
            "source": "office_tourisme_fes", "ville": "Fès",
            "url": "https://www.visitmorocco.com/fr/voyage/fes/medina",
        },
    ),
    Document(
        page_content=(
            "Tanger : la Kasbah, la médina, le Grand Socco et les jardins de la Mendoubia "
            "illustrent son héritage multiculturel. Le palais du Sultan, aujourd'hui musée "
            "des arts marocains, complète une journée culturelle. Budget indicatif : "
            "550 à 850 MAD par jour."
        ),
        metadata={
            "source": "office_tourisme_tanger", "ville": "Tanger",
            "url": "https://www.visitmorocco.com/en/travel/tangier",
        },
    ),
    Document(
        page_content=(
            "Marrakech propose aussi le Jardin Majorelle, le palais El Badi, les tombeaux "
            "saadiens et les quartiers de Guéliz et de l'Hivernage. Pour un rythme équilibré, "
            "prévoir une grande visite le matin, une pause aux heures chaudes et Jemaa el-Fna "
            "en fin de journée. La tanjia est une spécialité locale."
        ),
        metadata={
            "source": "experiences_marrakech", "ville": "Marrakech",
            "url": "https://www.visitmorocco.com/fr/voyage/marrakech/medina",
        },
    ),
    Document(
        page_content=(
            "Fès est reconnue pour les tanneurs, tisserands, dinandiers, potiers et zelliges. "
            "Le jardin Jnan Sbil offre une pause calme près de la médina. La pastilla et la "
            "cuisine fassie conviennent à un parcours gastronomie et patrimoine."
        ),
        metadata={
            "source": "experiences_fes", "ville": "Fès",
            "url": "https://www.visitmorocco.com/en/travel/fez",
        },
    ),
    Document(
        page_content=(
            "Tanger associe patrimoine et littoral : musée de la Kasbah, médina, légation "
            "américaine, Café Hafa, Cap Spartel et grottes d'Hercule. Regrouper Cap Spartel "
            "et les grottes dans une même demi-journée limite les déplacements."
        ),
        metadata={
            "source": "experiences_tanger", "ville": "Tanger",
            "url": "https://www.visitmorocco.com/en/travel/tangier",
        },
    ),
    Document(
        page_content=(
            "Déplacements locaux : les médinas de Marrakech, Fès et Tanger se découvrent "
            "surtout à pied. Les petits taxis servent pour les trajets urbains plus longs. "
            "Vérifier l'usage du compteur ou convenir du tarif avant le départ. Prévoir des "
            "chaussures confortables et un temps de marge dans les ruelles."
        ),
        metadata={"source": "mobilite_locale", "ville": "général"},
    ),
    Document(
        page_content=(
            "Conseils pratiques pour Marrakech, Fès et Tanger : monnaie MAD, eau en bouteille "
            "recommandée, tenue respectueuse dans les lieux religieux et négociation courante "
            "dans les souks. Les horaires et prix des monuments peuvent changer : les vérifier "
            "avant la visite et réserver les sites populaires quand cela est possible."
        ),
        metadata={"source": "conseils_pratiques", "ville": "général"},
    ),
]