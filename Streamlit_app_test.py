import streamlit as st
import re
import io
import csv
import pandas as pd

###############################################################################
# 1) PAGE CONFIG   ->  MOET ALS EERSTE STREAMLIT-AANROEP
###############################################################################
st.set_page_config(page_title="Futri-Bot", layout="wide", page_icon="🔮")

###############################################################################
# 2) DATASTRUCTUREN VOOR REFLECTIE, AANBEVELINGEN EN (OPTIONEEL) ANALYSE-TIPS
###############################################################################

# Per criterium: standaard reflectievragen (altijd tonen, ongeacht score)
REFLECTION_QUESTIONS = {
    "Horizonbepaling": [
        "Hoe kunt u verder vooruitkijken dan de geplande horizon?",
        "Welke ontwikkelingen zouden grote impact kunnen hebben in uw verdere toekomst?"
    ],
    "Innovatiebereidheid": [
        "Op welke gebieden is er nog ruimte voor experiment en vernieuwing?",
        "Hoe stimuleert u een cultuur waar innovatieve ideeën kunnen ontstaan?"
    ],
    "Wendbaarheid en adaptiviteit": [
        "Hoe kunt u zich beter voorbereiden op onverwachte veranderingen of schokken?",
        "Welke processen kunt u vereenvoudigen om wendbaarder te worden?"
    ],
    "Stakeholderbetrokkenheid": [
        "Wie zijn op dit moment ondervertegenwoordigd of hebben te weinig inspraak?",
        "Hoe kunt u structureel feedback verzamelen van alle belanghebbenden?"
    ],
    "Duurzaamheid en inclusiviteit": [
        "Welke quick wins ziet u op het gebied van duurzaamheidsmaatregelen?",
        "Hoe kunt u inclusie verder verankeren in uw beleidsprocessen?"
    ],
    "Toekomstscenario's en strategische visie": [
        "Welke scenario’s denkt u te gaan ontwikkelen, en hoe gebruikt u ze in beslissingen?",
        "Hoe vaak evalueert en vernieuwt u uw strategische visie?"
    ]
}

# Per criterium: aanbevelingen om de score te verhogen
RECOMMENDATIONS = {
    "Horizonbepaling": "Formuleer mijlpalen voor 10+, 25+ en 50+ jaar en evalueer regelmatig of deze nog realistisch zijn.",
    "Innovatiebereidheid": "Investeer in een innovatieteam of experimenteerruimte; deel successen en leermomenten breed.",
    "Wendbaarheid en adaptiviteit": "Voer periodiek een ‘stress test’ uit om snel knelpunten in wendbaarheid te signaleren.",
    "Stakeholderbetrokkenheid": "Organiseer interactieve sessies of panels met diverse groepen om hun inbreng te garanderen.",
    "Duurzaamheid en inclusiviteit": "Integreer meetbare doelstellingen (KPI’s) op duurzaamheid en inclusie in alle projectfases.",
    "Toekomstscenario's en strategische visie": "Creëer minimaal drie toekomstscenario’s (optimistisch, realistisch, pessimistisch) en veranker deze in uw besluitvorming."
}

###############################################################################
# 3) SCOREBEREKENING MET ANALYSE
###############################################################################
def analyze_text(text):
    """
    Analyseert de input-tekst en retourneert:
      1) scores: dict per criterium (A-E)
      2) details: dict per criterium met info over gevonden keywords en korte analyse
    """
    scores = {}
    details = {}

    # lowercase om case-insensitive te zoeken
    text_lower = text.lower()

    # 1. Horizonbepaling
    time_matches = re.findall(r'\b(\d{1,3})\s*jaar\b', text)
    years = [int(m) for m in time_matches if int(m) > 0]
    max_year = max(years) if years else 0

    # Bepaal score
    if max_year >= 50:
        scores['Horizonbepaling'] = 'A'
    elif max_year >= 25:
        scores['Horizonbepaling'] = 'B'
    elif max_year >= 10:
        scores['Horizonbepaling'] = 'C'
    elif max_year >= 5:
        scores['Horizonbepaling'] = 'D'
    else:
        scores['Horizonbepaling'] = 'E'
    
    # Maak analyse info
    if years:
        detail_text = f"Er zijn tijdsdoelen benoemd tot het jaar {max_year}. "
    else:
        detail_text = "Er zijn geen expliciete jaartallen gevonden. "

    detail_text += (
        "Dit suggereert een "
        + ("zeer lange termijnvisie" if max_year >= 50 else
           "redelijk lange termijnvisie" if max_year >= 25 else
           "middellange termijn" if max_year >= 10 else
           "korte termijnfocus" if max_year >= 5 else
           "zeer korte of ongedefinieerde horizon")
        + "."
    )
    details['Horizonbepaling'] = detail_text

    # 2. Innovatiebereidheid
    innovation_keywords = ['innovatie', 'experiment', 'pilot', 'technologie', 'doorbraak']
    found_innovation = re.findall(r'\b(?:' + '|'.join(innovation_keywords) + r')\b', text_lower)
    count_innovation = len(found_innovation)
    if count_innovation >= 4:
        scores['Innovatiebereidheid'] = 'A'
    elif count_innovation >= 2:
        scores['Innovatiebereidheid'] = 'B'
    elif count_innovation == 1:
        scores['Innovatiebereidheid'] = 'C'
    else:
        scores['Innovatiebereidheid'] = 'E'
    
    if found_innovation:
        unique_words = set(found_innovation)
        detail_text = (
            f"Er zijn {count_innovation} innovatiesleutelwoorden gevonden: {', '.join(unique_words)}. "
            "Dit wijst op een actieve aandacht voor vernieuwing."
        )
    else:
        detail_text = (
            "Er zijn geen duidelijke innovatiesleutelwoorden gevonden. "
            "Dit kan betekenen dat innovatie niet expliciet benoemd wordt in het plan."
        )
    details['Innovatiebereidheid'] = detail_text

    # 3. Wendbaarheid en adaptiviteit
    flexibility_keywords = ['flexibel', 'aanpass', 'monitor', 'evaluatie', 'feedback', 'agile']
    found_flexibility = re.findall(r'\b(?:' + '|'.join(flexibility_keywords) + r')\b', text_lower)
    count_flexibility = len(found_flexibility)

    if count_flexibility >= 3:
        scores['Wendbaarheid en adaptiviteit'] = 'A'
    elif count_flexibility >= 2:
        scores['Wendbaarheid en adaptiviteit'] = 'B'
    elif count_flexibility == 1:
        scores['Wendbaarheid en adaptiviteit'] = 'C'
    else:
        scores['Wendbaarheid en adaptiviteit'] = 'E'

    if found_flexibility:
        unique_words = set(found_flexibility)
        detail_text = (
            f"De tekst bevat {count_flexibility} trefwoorden rond wendbaarheid/aanpassen: {', '.join(unique_words)}. "
            "Dit duidt op bewustzijn van veranderbaarheid."
        )
    else:
        detail_text = (
            "Geen trefwoorden rond wendbaarheid/aanpassing gevonden. "
            "Wellicht is er weinig aandacht voor flexibiliteit."
        )
    details['Wendbaarheid en adaptiviteit'] = detail_text

    # 4. Stakeholderbetrokkenheid
    stakeholder_keywords = ['jongeren', 'toekomstige generaties', 'minderheden', 'stakeholder', 'participatie']
    found_stakeholders = re.findall(r'\b(?:' + '|'.join(stakeholder_keywords) + r')\b', text_lower)
    count_stakeholders = len(found_stakeholders)

    if count_stakeholders >= 3:
        scores['Stakeholderbetrokkenheid'] = 'A'
    elif count_stakeholders >= 1:
        scores['Stakeholderbetrokkenheid'] = 'B'
    else:
        scores['Stakeholderbetrokkenheid'] = 'E'

    if found_stakeholders:
        unique_words = set(found_stakeholders)
        detail_text = (
            f"Gevonden trefwoorden over stakeholders: {', '.join(unique_words)}. "
            "Er is aandacht voor (diverse) belanghebbenden."
        )
    else:
        detail_text = (
            "Geen aanduidingen gevonden van specifieke stakeholders of participatie. "
            "Dit kan impliceren dat belanghebbenden niet expliciet genoemd worden."
        )
    details['Stakeholderbetrokkenheid'] = detail_text

    # 5. Duurzaamheid en inclusiviteit
    sustainability_keywords = ['duurzaam', 'inclusie', 'klimaat', 'circulair', 'sociaal', 'diversiteit']
    found_sustain = re.findall(r'\b(?:' + '|'.join(sustainability_keywords) + r')\b', text_lower)
    count_sustain = len(found_sustain)

    if count_sustain >= 4:
        scores['Duurzaamheid en inclusiviteit'] = 'A'
    elif count_sustain >= 2:
        scores['Duurzaamheid en inclusiviteit'] = 'B'
    else:
        scores['Duurzaamheid en inclusiviteit'] = 'E'

    if found_sustain:
        unique_words = set(found_sustain)
        detail_text = (
            f"In totaal {count_sustain} trefwoorden over duurzaamheid/inclusie: {', '.join(unique_words)}. "
            "Hieruit blijkt aandacht voor milieuvraagstukken en/of inclusie."
        )
    else:
        detail_text = (
            "Geen trefwoorden gevonden op het gebied van duurzaamheid of inclusiviteit. "
            "Mogelijk is het plan nog niet expliciet duurzaam of inclusief geformuleerd."
        )
    details['Duurzaamheid en inclusiviteit'] = detail_text

    # 6. Toekomstscenario's en strategische visie
    scenario_keywords = ['scenario', 'onzekerheid', 'visie', 'strategie', 'toekomstbeeld', 'raming']
    found_scenarios = re.findall(r'\b(?:' + '|'.join(scenario_keywords) + r')\b', text_lower)
    count_scenarios = len(found_scenarios)

    if count_scenarios >= 3:
        scores["Toekomstscenario's en strategische visie"] = 'A'
    elif count_scenarios >= 1:
        scores["Toekomstscenario's en strategische visie"] = 'B'
    else:
        scores["Toekomstscenario's en strategische visie"] = 'E'

    if found_scenarios:
        unique_words = set(found_scenarios)
        detail_text = (
            f"Gevonden {count_scenarios} woorden rond toekomstscenario's/visie: {', '.join(unique_words)}. "
            "Duidt op een zekere mate van toekomstplanning."
        )
    else:
        detail_text = (
            "Geen scenario-gerelateerde trefwoorden gevonden. "
            "Er lijkt weinig expliciete strategische toekomstvisie opgenomen."
        )
    details["Toekomstscenario's en strategische visie"] = detail_text

    return scores, details

def do_rerun():
    """Hulpfunctie om st.experimental_rerun() of st.rerun() betrouwbaar te gebruiken."""
    if hasattr(st, 'experimental_rerun'):
        st.experimental_rerun()
    else:
        st.rerun()

###############################################################################
# 4) HELPER VOOR SCORE LABEL
###############################################################################
st.markdown(
    """
    <style>
        :root {
            --score-a: #2ecc71;
            --score-b: #27ae60;
            --score-c: #f39c12;
            --score-d: #e74c3c;
            --score-e: #c0392b;
        }
        .score-label {
            padding: 0.2em 0.5em;
            border-radius: 0.25em;
            font-weight: 600;
            font-size: 0.9em;
        }
        .score-A { background: var(--score-a); color: white; }
        .score-B { background: var(--score-b); color: white; }
        .score-C { background: var(--score-c); color: white; }
        .score-D { background: var(--score-d); color: white; }
        .score-E { background: var(--score-e); color: white; }
        .stProgress > div > div > div > div {
            background-image: linear-gradient(90deg, var(--score-a) 0%, var(--score-e) 100%);
        }
    </style>
    """,
    unsafe_allow_html=True
)

def score_label(score):
    """Geeft de score als gekleurde label terug in HTML."""
    return f'<span class="score-label score-{score}">{score}</span>'

###############################################################################
# 5) PAGINABEHEER
###############################################################################
if 'page' not in st.session_state:
    st.session_state.page = 1

###############################################################################
# 6) PAGINA 1: INVOER
###############################################################################
if st.session_state.page == 1:
    st.title("🔮 Futri-Bot - Toekomstscan")

    input_text = st.text_area(
        label="**Beschrijf uw plannen of strategie:**",
        height=250,
        placeholder="Bijvoorbeeld: 'Onze visie voor 2040 is...'"
    )

    if st.button("📊 Start analyse", type="primary"):
        if input_text.strip():
            scores, details = analyze_text(input_text)
            st.session_state.scores = scores
            st.session_state.details = details
            st.session_state.input_text = input_text  # Bewaar de originele input voor latere referentie indien nodig
            st.session_state.page = 2
            do_rerun()
        else:
            st.warning("⚠️ Voer eerst een tekst in om te analyseren.")

###############################################################################
# 7) PAGINA 2: RESULTATEN
###############################################################################
elif st.session_state.page == 2:
    st.title("📈 Analyse Resultaten")

    score_values = {'A': 5, 'B': 4, 'C': 3, 'D': 2, 'E': 1}
    total = sum(score_values[s] for s in st.session_state.scores.values())
    avg_score = total / len(st.session_state.scores)

    # Converteer gemiddelde naar A-E
    final_score = (
        'A' if avg_score >= 4.5 else
        'B' if avg_score >= 3.5 else
        'C' if avg_score >= 2.5 else
        'D' if avg_score >= 1.5 else
        'E'
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(f"### Totale Futri-Score {score_label(final_score)}", unsafe_allow_html=True)
        st.caption(f"Gemiddelde: {avg_score:.1f}/5.0")

    with col2:
        st.progress(avg_score / 5)

    st.write("---")

    # Details per criterium
    for criterion, score in st.session_state.scores.items():
        st.subheader(criterion)
        # Score
        st.markdown(f"**Score:** {score_label(score)}", unsafe_allow_html=True)

        # Analyse-uitleg
        detail_text = st.session_state.details[criterion]
        st.write(f"**Analyse:** {detail_text}")

        # Aanbeveling -> altijd tonen
        st.write(f"**Aanbeveling:** {RECOMMENDATIONS[criterion]}")

        # Reflectievragen -> altijd 2 vragen tonen
        st.markdown("**Reflectievragen:**")
        for question in REFLECTION_QUESTIONS[criterion]:
            st.markdown(f"- {question}")

        st.write("---")

    # Downloadknop voor CSV
    csv_data = io.StringIO()
    columns = ["Criterium", "Score", "Details", "Aanbeveling"]
    writer = csv.writer(csv_data)
    writer.writerow(columns)

    for criterion, score in st.session_state.scores.items():
        detail_info = st.session_state.details[criterion]
        recommendation = RECOMMENDATIONS[criterion]
        writer.writerow([criterion, score, detail_info, recommendation])

    st.download_button(
        label="📥 Download resultaten als CSV",
        data=csv_data.getvalue(),
        file_name="futri_analyse.csv",
        mime="text/csv"
    )

    # Nieuwe analyse
    if st.button("🔄 Nieuwe analyse", type="primary"):
        st.session_state.page = 1
        do_rerun()
