import streamlit as st
import random
from audio_recorder_streamlit import audio_recorder

# Mock data en functies
def analyze_text(text):
    # Mock analysis - vervangen door echte NLP analyse
    scores = {criterion: random.choice(['A','B','C','D','E']) for criterion in criteria}
    return scores

def get_feedback(criterion, score):
    feedback = {
        'Horizonbepaling': {
            'A': "Uitstekend langetermijnperspectief (>50 jaar) met gedetailleerde planning",
            'E': "Geen aandacht voor lange termijn (>5 jaar)"
        },
        # Voeg feedback voor alle criteria toe
    }
    return feedback[criterion].get(score, "Geen feedback beschikbaar")

# Criteria lijst
criteria = [
    "Horizonbepaling",
    "Innovatiebereidheid",
    "Wendbaarheid en adaptiviteit",
    "Stakeholderbetrokkenheid",
    "Duurzaamheid en inclusiviteit",
    "Toekomstscenario's en strategische visie"
]

# Pagina layout
st.set_page_config(page_title="Futri-Bot", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 1
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# Pagina 1: Input
if st.session_state.page == 1:
    st.title("Futri-Bot - Toekomstanalyse")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tekstinvoer")
        input_text = st.text_area("Voer uw tekst in:", height=300)
        
    with col2:
        st.subheader("Audio-invoer")
        audio_bytes = audio_recorder()
        if audio_bytes:
            # Voeg hier spraakherkenning toe
            st.session_state.input_text = "Transcript van audio komt hier"
    
    if st.button("Bereken Futri-Score"):
        if st.session_state.input_text:
            st.session_state.scores = analyze_text(st.session_state.input_text)
            st.session_state.page = 2
            st.rerun()

# Pagina 2: Resultaten
elif st.session_state.page == 2:
    st.title("Jouw Futri-Score Analyse")
    
    # Gemiddelde score berekenen
    score_values = {'A':5, 'B':4, 'C':3, 'D':2, 'E':1}
    avg_score = sum(score_values[s] for s in st.session_state.scores.values())/len(criteria)
    final_score = chr(ord('A') + int(4 - (avg_score - 1)))  # Simpele conversie
    
    st.header(f"Gemiddelde Futri-Score: {final_score}")
    st.progress(avg_score/5)
    
    for criterion in criteria:
        with st.expander(f"{criterion} - Score: {st.session_state.scores[criterion]}"):
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Analyse")
                st.write(get_feedback(criterion, st.session_state.scores[criterion]))
                
                st.subheader("Aanbevelingen")
                st.write("Concrete verbeterpunten voor dit criterium...")
                
            with col2:
                st.subheader("Vragen voor reflectie")
                st.write("- Hoe zou u dit aspect kunnen verbeteren?")
                st.write("- Welke kansen ziet u voor ontwikkeling?")
    
    if st.button("Nieuwe analyse"):
        st.session_state.page = 1
        st.session_state.input_text = ""
        st.rerun()
