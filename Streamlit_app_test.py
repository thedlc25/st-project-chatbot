import streamlit as st
import re
import random
import pandas as pd
import io
import csv

# --- CSS Styling ---
st.markdown("""
<style>
    :root {
        --score-a: #2ecc71;
        --score-b: #27ae60;
        --score-c: #f39c12;
        --score-d: #e74c3c;
        --score-e: #c0392b;
    }
    .score-label { padding: 0.2em 0.5em; border-radius: 0.25em; font-weight: 600; font-size: 0.9em; }
    .score-A { background: var(--score-a); color: white; }
    .score-B { background: var(--score-b); color: white; }
    .score-C { background: var(--score-c); color: white; }
    .score-D { background: var(--score-d); color: white; }
    .score-E { background: var(--score-e); color: white; }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(90deg, var(--score-a) 0%, var(--score-e) 100%);
    }
</style>
""", unsafe_allow_html=True)

# --- Functie voor score labels ---
def score_label(score):
    return f'<span class="score-label score-{score}">{score}</span>'

# --- Functie om tekst te analyseren ---
def analyze_text(text):
    scores = {}
    text_lower = text.lower()
    
    # 1. Horizonbepaling
    time_matches = re.findall(r'\b(\d{1,3})\s*jaar\b', text)
    years = [int(match) for match in time_matches if int(match) > 0]
    max_year = max(years) if years else 0
    scores['Horizonbepaling'] = 'A' if max_year >=50 else 'B' if max_year >=25 else 'C' if max_year >=10 else 'D' if max_year >=5 else 'E'

    # 2. Innovatiebereidheid
    innovation_keywords = ['innovatie', 'experiment', 'pilot', 'technologie', 'doorbraak']
    innovation_count = len(re.findall(r'\b(?:' + '|'.join(innovation_keywords) + r')\b', text_lower))
    scores['Innovatiebereidheid'] = 'A' if innovation_count >=4 else 'B' if innovation_count >=2 else 'C' if innovation_count >=1 else 'E'

    # 3. Wendbaarheid
    flexibility_keywords = ['flexibel', 'aanpass', 'monitor', 'evaluatie', 'feedback', 'agile']
    flexibility_count = len(re.findall(r'\b(?:' + '|'.join(flexibility_keywords) + r')\b', text_lower))
    scores['Wendbaarheid en adaptiviteit'] = 'A' if flexibility_count >=3 else 'B' if flexibility_count >=2 else 'C' if flexibility_count == 1 else 'E'

    # 4. Stakeholderbetrokkenheid
    stakeholder_keywords = ['jongeren', 'toekomstige generaties', 'minderheden', 'stakeholder', 'participatie']
    stakeholder_count = len(re.findall(r'\b(?:' + '|'.join(stakeholder_keywords) + r')\b', text_lower))
    scores['Stakeholderbetrokkenheid'] = 'A' if stakeholder_count >=3 else 'B' if stakeholder_count >=1 else 'E'

    # 5. Duurzaamheid
    sustainability_keywords = ['duurzaam', 'inclusie', 'klimaat', 'circulair', 'sociaal', 'diversiteit']
    sustainability_count = len(re.findall(r'\b(?:' + '|'.join(sustainability_keywords) + r')\b', text_lower))
    scores['Duurzaamheid en inclusiviteit'] = 'A' if sustainability_count >=4 else 'B' if sustainability_count >=2 else 'E'

    # 6. Scenario's
    scenario_keywords = ['scenario', 'onzekerheid', 'visie', 'strategie', 'toekomstbeeld', 'raming']
    scenario_count = len(re.findall(r'\b(?:' + '|'.join(scenario_keywords) + r')\b', text_lower))
    scores["Toekomstscenario's en strategische visie"] = 'A' if scenario_count >=3 else 'B' if scenario_count >=1 else 'E'
    
    return scores

# --- UI Layout ---
st.set_page_config(page_title="Futri-Bot", layout="wide", page_icon="🔮")

if 'page' not in st.session_state:
    st.session_state.page = 1

if st.session_state.page == 1:
    st.title("🔮 Futri-Bot - Toekomstscan")
    input_text = st.text_area("**Beschrijf uw plannen of strategie:**", height=250, placeholder="Bijvoorbeeld: 'Onze visie voor 2040 is...'")
    if st.button("📊 Start analyse", type="primary"):
        if input_text.strip():
            st.session_state.scores = analyze_text(input_text)
            st.session_state.page = 2
            st.rerun()
        else:
            st.warning("⚠️ Voer eerst een tekst in om te analyseren.")

elif st.session_state.page == 2:
    st.title("📈 Analyse Resultaten")
    score_values = {'A':5, 'B':4, 'C':3, 'D':2, 'E':1}
    total = sum(score_values[s] for s in st.session_state.scores.values())
    avg_score = total / len(st.session_state.scores)
    final_score = 'A' if avg_score >= 4.5 else 'B' if avg_score >= 3.5 else 'C' if avg_score >= 2.5 else 'D' if avg_score >= 1.5 else 'E'

    col1, col2 = st.columns([1,3])
    with col1:
        st.markdown(f"### Totale Futri-Score {score_label(final_score)}", unsafe_allow_html=True)
        st.caption(f"Gemiddelde: {avg_score:.1f}/5.0")
    
    with col2:
        st.progress(avg_score/5)

    for criterion, score in st.session_state.scores.items():
        st.markdown(f"**{criterion}:** {score_label(score)}", unsafe_allow_html=True)

    csv_data = io.StringIO()
    writer = csv.writer(csv_data)
    writer.writerow(["Criterium", "Score"])
    for key, value in st.session_state.scores.items():
        writer.writerow([key, value])

    st.download_button("📥 Download resultaten als CSV", data=csv_data.getvalue(), file_name="futri_analyse.csv", mime="text/csv")
    if st.button("🔄 Nieuwe analyse", type="primary"):
        st.session_state.page = 1
        st.rerun()
