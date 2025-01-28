import streamlit as st
import re

def analyze_text(text):
    scores = {}
    text_lower = text.lower()
    
    # 1. Horizonbepaling (Langetermijnperspectief)
    time_matches = re.findall(r'\b(\d+)\s*(jaar|jaren)\b', text)
    years = [int(match[0]) for match in time_matches if int(match[0]) > 0]
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
    innovation_keywords = ['innovati', 'experiment', 'pilot', 'nieuw', 'technologie', 'doorbraak']
    innovation_count = sum(text_lower.count(keyword) for keyword in innovation_keywords)
    scores['Innovatiebereidheid'] = 'A' if innovation_count >=4 else 'B' if innovation_count >=2 else 'C' if innovation_count >=1 else 'E'

    # 3. Wendbaarheid en adaptiviteit
    flexibility_keywords = ['flexibel', 'aanpass', 'monitor', 'evalua', 'feedback', 'agile', 'wendbaar']
    flexibility_count = sum(text_lower.count(keyword) for keyword in flexibility_keywords)
    scores['Wendbaarheid en adaptiviteit'] = 'A' if flexibility_count >=3 else 'B' if flexibility_count >=2 else 'D'

    # 4. Stakeholderbetrokkenheid
    stakeholder_keywords = ['jongeren', 'toekomstige generaties', 'minderheden', 'stakeholder', 'inbreng', 'participatie']
    stakeholder_count = sum(text_lower.count(keyword) for keyword in stakeholder_keywords)
    scores['Stakeholderbetrokkenheid'] = 'A' if stakeholder_count >=3 else 'B' if stakeholder_count >=1 else 'E'

    # 5. Duurzaamheid en inclusiviteit
    sustainability_keywords = ['duurzaam', 'inclusi', 'klimaat', 'circulair', 'sociaal', 'diversiteit']
    sustainability_count = sum(text_lower.count(keyword) for keyword in sustainability_keywords)
    scores['Duurzaamheid en inclusiviteit'] = 'A' if sustainability_count >=4 else 'B' if sustainability_count >=2 else 'E'

    # 6. Toekomstscenario's
    scenario_keywords = ['scenario', 'onzekerheid', 'visie', 'strategi', 'toekomstbeeld', 'raming']
    scenario_count = sum(text_lower.count(keyword) for keyword in scenario_keywords)
    scores["Toekomstscenario's en strategische visie"] = 'A' if scenario_count >=3 else 'B' if scenario_count >=1 else 'E'

    return scores

CRITERIA_FEEDBACK = {
    "Horizonbepaling": {
        'A': "Uitstekende langetermijnvisie (>50 jaar) met concrete tijdsaanduidingen",
        'B': "Focus op middellange termijn (10-50 jaar)",
        'C': "Beperkte langetermijnvisie (<10 jaar)",
        'D': "Korte termijn focus (5-10 jaar)",
        'E': "Geen duidelijke tijdsaanduidingen gevonden (>5 jaar)"
    },
    "Innovatiebereidheid": {
        'A': "Sterke innovatieve focus met meerdere concrete voorbeelden",
        'B': "Enkele innovatieve elementen aanwezig",
        'C': "Beperkte aandacht voor innovatie",
        'E': "Geen innovatieve elementen gedetecteerd"
    },
    "Wendbaarheid en adaptiviteit": {
        'A': "Duidelijke flexibiliteitsmechanismen aanwezig",
        'B': "Enige mogelijkheden voor aanpassing",
        'D': "Weinig aandacht voor wendbaarheid"
    },
    "Stakeholderbetrokkenheid": {
        'A': "Brede stakeholderbetrokkenheid gedetecteerd",
        'B': "Beperkte betrokkenheid specifieke groepen",
        'E': "Geen aandacht voor stakeholders"
    },
    "Duurzaamheid en inclusiviteit": {
        'A': "Sterke duurzaamheids- en inclusiviteitsfocus",
        'B': "Enige aandacht voor duurzaamheid",
        'E': "Geen duurzaamheidselementen gevonden"
    },
    "Toekomstscenario's en strategische visie": {
        'A': "Meerdere toekomstscenario's en duidelijke strategie",
        'B': "Enige scenario-ontwikkeling aanwezig",
        'E': "Geen scenario-planning gedetecteerd"
    }
}

RECOMMENDATIONS = {
    "Horizonbepaling": "Overweeg langetermijndoelen (>25 jaar) te formuleren",
    "Innovatiebereidheid": "Experimenteer met pilots en nieuwe technologieën",
    "Wendbaarheid en adaptiviteit": "Implementeer regelmatige evaluatiemomenten",
    "Stakeholderbetrokkenheid": "Betrek jongeren en toekomstige generaties",
    "Duurzaamheid en inclusiviteit": "Integreer SDG's in uw beleid",
    "Toekomstscenario's en strategische visie": "Ontwikkel meerdere toekomstscenario's"
}

st.set_page_config(page_title="Futri-Bot", layout="wide")

if 'page' not in st.session_state:
    st.session_state.page = 1
if 'scores' not in st.session_state:
    st.session_state.scores = {}

if st.session_state.page == 1:
    st.title("🏭 Futri-Bot - Toekomstanalyse")
    input_text = st.text_area("**Beschrijf uw plannen of strategie:**", height=300, 
                            placeholder="Bijvoorbeeld: 'Onze doelstelling is klimaatneutraliteit in 2050 door innovatieve technologieën...'")
    
    if st.button("📊 Analyseer toekomstgerichtheid"):
        if input_text.strip():
            st.session_state.scores = analyze_text(input_text)
            st.session_state.page = 2
            st.rerun()
        else:
            st.error("Voer eerst een tekst in om te analyseren")

elif st.session_state.page == 2:
    st.title("📈 Analyse Resultaten")
    
    # Bereken gemiddelde score
    score_values = {'A':5, 'B':4, 'C':3, 'D':2, 'E':1}
    total = sum(score_values[s] for s in st.session_state.scores.values())
    avg_score = total / len(st.session_state.scores)
    final_score = chr(ord('A') + int(4 - (avg_score - 1)))
    
    col1, col2 = st.columns([1,3])
    with col1:
        st.metric(label="**Totale Futri-Score**", value=final_score)
        st.write(f"Gemiddelde: {avg_score:.1f}/5.0")
    with col2:
        st.progress(avg_score/5)
        st.caption("Een hogere score betekent meer toekomstgerichtheid")
    
    st.divider()
    
    for criterion in st.session_state.scores:
        score = st.session_state.scores[criterion]
        with st.expander(f"{criterion} - Score: {score}", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("Analyse")
                st.write(CRITERIA_FEEDBACK[criterion][score])
                
                st.subheader("🔧 Aanbeveling")
                st.write(RECOMMENDATIONS[criterion])
            
            with col_b:
                st.subheader("❓ Reflectievragen")
                if criterion == "Horizonbepaling":
                    st.write("- Hoe ziet uw ideale toekomstscenario eruit over 50 jaar?")
                    st.write("- Welke trends kunnen uw huidige plannen beïnvloeden?")
                elif criterion == "Innovatiebereidheid":
                    st.write("- Welke nieuwe technologieën zouden uw doelstellingen kunnen versnellen?")
                    st.write("- Hoe zou u experimenten kunnen structureren?")
                # Voeg vragen voor andere criteria toe
    
    if st.button("🔄 Nieuwe analyse"):
        st.session_state.page = 1
        st.rerun()
