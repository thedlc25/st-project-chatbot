import streamlit as st
import re

def analyze_text(text):
    scores = {}
    text_lower = text.lower()
    
    # 1. Horizonbepaling
    time_matches = re.findall(r'\b(\d+)\s*(jaar|jaren)\b', text)
    years = [int(match[0]) for match in time_matches if int(match[0]) > 0]
    max_year = max(years) if years else 0
    scores['Horizonbepaling'] = 'A' if max_year >=50 else 'B' if max_year >=25 else 'C' if max_year >=10 else 'D' if max_year >=5 else 'E'

    # 2. Innovatiebereidheid
    innovation_keywords = ['innovati', 'experiment', 'pilot', 'nieuw', 'technologie']
    innovation_count = sum(text_lower.count(kw) for kw in innovation_keywords)
    scores['Innovatiebereidheid'] = 'A' if innovation_count >=4 else 'B' if innovation_count >=2 else 'C' if innovation_count >=1 else 'E'

    # 3. Wendbaarheid
    flexibility_keywords = ['flexibel', 'aanpass', 'monitor', 'evalua', 'feedback']
    flexibility_count = sum(text_lower.count(kw) for kw in flexibility_keywords)
    scores['Wendbaarheid en adaptiviteit'] = 'A' if flexibility_count >=3 else 'B' if flexibility_count >=2 else 'D'

    # 4. Stakeholders
    stakeholder_keywords = ['jongeren', 'toekomstige generaties', 'minderheden', 'stakeholder']
    stakeholder_count = sum(text_lower.count(kw) for kw in stakeholder_keywords)
    scores['Stakeholderbetrokkenheid'] = 'A' if stakeholder_count >=3 else 'B' if stakeholder_count >=1 else 'E'

    # 5. Duurzaamheid
    sustainability_keywords = ['duurzaam', 'inclusi', 'klimaat', 'circulair', 'sociaal']
    sustainability_count = sum(text_lower.count(kw) for kw in sustainability_keywords)
    scores['Duurzaamheid en inclusiviteit'] = 'A' if sustainability_count >=4 else 'B' if sustainability_count >=2 else 'E'

    # 6. Scenario's
    scenario_keywords = ['scenario', 'onzekerheid', 'visie', 'strategi', 'toekomstbeeld']
    scenario_count = sum(text_lower.count(kw) for kw in scenario_keywords)
    scores["Toekomstscenario's en strategische visie"] = 'A' if scenario_count >=3 else 'B' if scenario_count >=1 else 'E'

    return scores

CRITERIA_QUESTIONS = {
    "Horizonbepaling": [
        "Hoe zou dit beleid eruitzien over 50 jaar?",
        "Welke trends zouden invloed kunnen hebben op uw doelen?"
    ],
    "Innovatiebereidheid": [
        "Welke innovatieve ideeën zouden u kunnen helpen?",
        "Hoe zou u experimenteren met nieuwe benaderingen?"
    ],
    "Wendbaarheid en adaptiviteit": [
        "Hoe snel zou u kunnen reageren op onverwachte veranderingen?",
        "Welke feedbackmechanismen kunt u implementeren?"
    ],
    "Stakeholderbetrokkenheid": [
        "Hoe zou u jongeren structureel kunnen betrekken?",
        "Welke minderheidsgroepen zijn nog niet vertegenwoordigd?"
    ],
    "Duurzaamheid en inclusiviteit": [
        "Hoe meet u de impact op toekomstige generaties?",
        "Welke duurzame alternatieven zijn nog mogelijk?"
    ],
    "Toekomstscenario's en strategische visie": [
        "Hoe zou uw strategie omgaan met een radicaal ander toekomstscenario?",
        "Welke vroege signalen van verandering mist u mogelijk?"
    ]
}

st.set_page_config(page_title="Futri-Bot", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 1
    st.session_state.scores = {}

if st.session_state.page == 1:
    st.title("🔮 Futri-Bot - Toekomstverkenner")
    input_text = st.text_area("**Beschrijf uw plannen of strategie:**", height=250,
                            placeholder="Bijvoorbeeld: 'Onze visie voor 2040 is...'")
    
    if st.button("🪄 Analyseer toekomstgerichtheid"):
        if input_text.strip():
            st.session_state.scores = analyze_text(input_text)
            st.session_state.page = 2
            st.rerun()
        else:
            st.error("Voer eerst een tekst in om te analyseren")

elif st.session_state.page == 2:
    st.title("📊 Analyse Resultaten")
    
    # Toon scores
    st.subheader("Jouw Futri-Scores:")
    cols = st.columns(3)
    for idx, (criterion, score) in enumerate(st.session_state.scores.items()):
        with cols[idx%3]:
            st.metric(label=criterion, value=score)
    
    st.divider()
    
    # Detailanalyse per criterium
    st.subheader("🧐 Reflectievragen en Aanbevelingen")
    for criterion, score in st.session_state.scores.items():
        with st.expander(f"{criterion} - Score: {score}", expanded=True):
            st.write("**Vragen voor verdere reflectie:**")
            for question in CRITERIA_QUESTIONS[criterion]:
                st.markdown(f"- {question}")
            
            st.write("**Suggesties voor verbetering:**")
            if score in ['D', 'E']:
                st.markdown(f"- Focus op {criterion.lower()} in volgende plannen")
                st.markdown(f"- Betrek experts op dit gebied")
            else:
                st.markdown(f"- Behoud en versterk de huidige aanpak")
                st.markdown(f"- Deel beste praktijken met anderen")

    if st.button("🔄 Nieuwe analyse"):
        st.session_state.page = 1
        st.rerun()
