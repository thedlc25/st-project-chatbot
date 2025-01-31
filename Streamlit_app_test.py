import streamlit as st
import re
import random
import pandas as pd
import io
import csv

# Zet de pagina-configuratie bovenaan, vóór alle andere Streamlit-aanroepen
st.set_page_config(page_title="Futri-Bot", layout="wide", page_icon="🔮")

# ------------------------
# Functie: Tekstanalyse
# ------------------------
def analyze_text(text):
    scores = {}
    text_lower = text.lower()

    # 1. Horizonbepaling
    time_matches = re.findall(r'\b(\d{1,3})\s*jaar\b', text)
    years = [int(match) for match in time_matches if int(match) > 0]
    max_year = max(years) if years else 0
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

    # 2. Innovatiebereidheid
    innovation_keywords = ['innovatie', 'experiment', 'pilot', 'technologie', 'doorbraak']
    innovation_count = len(re.findall(r'\b(?:' + '|'.join(innovation_keywords) + r')\b', text_lower))
    if innovation_count >= 4:
        scores['Innovatiebereidheid'] = 'A'
    elif innovation_count >= 2:
        scores['Innovatiebereidheid'] = 'B'
    elif innovation_count == 1:
        scores['Innovatiebereidheid'] = 'C'
    else:
        scores['Innovatiebereidheid'] = 'E'

    # 3. Wendbaarheid
    flexibility_keywords = ['flexibel', 'aanpass', 'monitor', 'evaluatie', 'feedback', 'agile']
    flexibility_count = len(re.findall(r'\b(?:' + '|'.join(flexibility_keywords) + r')\b', text_lower))
    if flexibility_count >= 3:
        scores['Wendbaarheid en adaptiviteit'] = 'A'
    elif flexibility_count >= 2:
        scores['Wendbaarheid en adaptiviteit'] = 'B'
    elif flexibility_count == 1:
        scores['Wendbaarheid en adaptiviteit'] = 'C'
    else:
        scores['Wendbaarheid en adaptiviteit'] = 'E'

    # 4. Stakeholderbetrokkenheid
    stakeholder_keywords = ['jongeren', 'toekomstige generaties', 'minderheden', 'stakeholder', 'participatie']
    stakeholder_count = len(re.findall(r'\b(?:' + '|'.join(stakeholder_keywords) + r')\b', text_lower))
    if stakeholder_count >= 3:
        scores['Stakeholderbetrokkenheid'] = 'A'
    elif stakeholder_count >= 1:
        scores['Stakeholderbetrokkenheid'] = 'B'
    else:
        scores['Stakeholderbetrokkenheid'] = 'E'

    # 5. Duurzaamheid
    sustainability_keywords = ['duurzaam', 'inclusie', 'klimaat', 'circulair', 'sociaal', 'diversiteit']
    sustainability_count = len(re.findall(r'\b(?:' + '|'.join(sustainability_keywords) + r')\b', text_lower))
    if sustainability_count >= 4:
        scores['Duurzaamheid en inclusiviteit'] = 'A'
    elif sustainability_count >= 2:
        scores['Duurzaamheid en inclusiviteit'] = 'B'
    else:
        scores['Duurzaamheid en inclusiviteit'] = 'E'

    # 6. Scenario's
    scenario_keywords = ['scenario', 'onzekerheid', 'visie', 'strategie', 'toekomstbeeld', 'raming']
    scenario_count = len(re.findall(r'\b(?:' + '|'.join(scenario_keywords) + r')\b', text_lower))
    if scenario_count >= 3:
        scores["Toekomstscenario's en strategische visie"] = 'A'
    elif scenario_count >= 1:
        scores["Toekomstscenario's en strategische visie"] = 'B'
    else:
        scores["Toekomstscenario's en strategische visie"] = 'E'

    return scores

# ------------------------
# CSS-Styling
# ------------------------
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
        /* Aangepaste gradient voor de progress bar */
        .stProgress > div > div > div > div {
            background-image: linear-gradient(90deg, var(--score-a) 0%, var(--score-e) 100%);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------
# Score label helper
# ------------------------
def score_label(score):
    return f'<span class="score-label score-{score}">{score}</span>'

# ------------------------
# Paginabeheer
# ------------------------
if 'page' not in st.session_state:
    st.session_state.page = 1

# ------------------------
# Pagina 1: Invoer
# ------------------------
if st.session_state.page == 1:
    st.title("🔮 Futri-Bot - Toekomstscan")
    input_text = st.text_area(
        "**Beschrijf uw plannen of strategie:**",
        height=250,
        placeholder="Bijvoorbeeld: 'Onze visie voor 2040 is...'"
    )
    if st.button("📊 Start analyse", type="primary"):
        if input_text.strip():
            st.session_state.scores = analyze_text(input_text)
            st.session_state.page = 2
            st.experimental_rerun()
        else:
            st.warning("⚠️ Voer eerst een tekst in om te analyseren.")

# ------------------------
# Pagina 2: Resultaten
# ------------------------
elif st.session_state.page == 2:
    st.title("📈 Analyse Resultaten")

    # Bepaal totalscore
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

    # Lijst van scores
    for criterion, score in st.session_state.scores.items():
        st.markdown(f"**{criterion}:** {score_label(score)}", unsafe_allow_html=True)

    # Download resultaten als CSV
    csv_data = io.StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(["Criterium", "Score"])
    for key, value in st.session_state.scores.items():
        writer.writerow([key, value])

    st.download_button(
        label="📥 Download resultaten als CSV",
        data=csv_data.getvalue(),
        file_name="futri_analyse.csv",
        mime="text/csv"
    )

    # Terugknop
    if st.button("🔄 Nieuwe analyse", type="primary"):
        st.session_state.page = 1
        st.experimental_rerun()
