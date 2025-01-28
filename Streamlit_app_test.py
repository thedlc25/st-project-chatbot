import streamlit as st
import random

# Mock analyse functie
def analyze_text(text):
    criteria = [
        "Horizonbepaling",
        "Innovatiebereidheid",
        "Wendbaarheid en adaptiviteit",
        "Stakeholderbetrokkenheid",
        "Duurzaamheid en inclusiviteit",
        "Toekomstscenario's en strategische visie"
    ]
    return {criterion: random.choice(['A','B','C','D','E']) for criterion in criteria}

# Feedback templates
CRITERIA_FEEDBACK = {
    "Horizonbepaling": {
        'A': "Uitstekende langetermijnvisie met gedetailleerde plannen voor >50 jaar",
        'E': "Geen aandacht voor lange termijn (>5 jaar)"
    },
    # Voeg feedback voor andere criteria toe
}

# Pagina configuratie
st.set_page_config(page_title="Futri-Bot", layout="wide")

# Sessie state initialisatie
if 'page' not in st.session_state:
    st.session_state.page = 1

# Pagina 1: Input
if st.session_state.page == 1:
    st.title("🏭 Futri-Bot - Toekomstanalyse")
    
    input_text = st.text_area("**Voer uw tekst in:**", height=300, help="Beschrijf uw plannen of strategie")
    
    if st.button("📊 Bereken Futri-Score"):
        if input_text.strip():
            st.session_state.scores = analyze_text(input_text)
            st.session_state.page = 2
            st.rerun()
        else:
            st.error("Voer eerst een tekst in")

# Pagina 2: Resultaten
elif st.session_state.page == 2:
    st.title("📈 Jouw Futri-Score Analyse")
    
    # Gemiddelde score berekenen
    score_values = {'A':5, 'B':4, 'C':3, 'D':2, 'E':1}
    avg_score = sum(score_values[s] for s in st.session_state.scores.values())/6
    final_score = chr(ord('A') + int(4 - (avg_score - 1)))
    
    # Header sectie
    col1, col2 = st.columns([1,3])
    with col1:
        st.metric(label="**Gemiddelde Score**", value=final_score)
    with col2:
        st.progress(avg_score/5)
        st.caption("Toelichting: Deze score geeft aan hoe toekomstgericht uw plannen zijn")
    
    # Detail scores
    st.subheader("🧮 Detailanalyse per Criterium")
    for criterion, score in st.session_state.scores.items():
        with st.expander(f"{criterion} - Score: {score}", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**Analyse:**\n{CRITERIA_FEEDBACK.get(criterion, {}).get(score, 'Geen feedback beschikbaar')}")
                st.markdown(f"**Aanbeveling:**\n- Concreet verbeterpunt voor {criterion}")
            with col_b:
                st.markdown("**Vragen voor reflectie:**")
                st.markdown("- Hoe zou u dit aspect kunnen verbeteren?")
                st.markdown("- Welke kansen ziet u voor ontwikkeling?")
    
    if st.button("🔄 Nieuwe analyse"):
        st.session_state.page = 1
        st.rerun()
