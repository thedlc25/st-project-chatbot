import streamlit as st
import re
import random

# Analysefunctie
def analyze_text(text):
    scores = {}
    text_lower = text.lower()
    
    # 1. Horizonbepaling
    time_matches = re.findall(r'\b(\d+)\s*(jaar|jaren)\b', text)
    years = [int(match[0]) for match in time_matches if int(match[0]) > 0]
    max_year = max(years) if years else 0
    scores['Horizonbepaling'] = 'A' if max_year >=50 else 'B' if max_year >=25 else 'C' if max_year >=10 else 'D' if max_year >=5 else 'E'

    # 2. Innovatiebereidheid
    innovation_keywords = ['innovati', 'experiment', 'pilot', 'nieuw', 'technologie', 'doorbraak']
    innovation_count = sum(text_lower.count(kw) for kw in innovation_keywords)
    scores['Innovatiebereidheid'] = 'A' if innovation_count >=4 else 'B' if innovation_count >=2 else 'C' if innovation_count >=1 else 'E'

    # 3. Wendbaarheid
    flexibility_keywords = ['flexibel', 'aanpass', 'monitor', 'evalua', 'feedback', 'agile']
    flexibility_count = sum(text_lower.count(kw) for kw in flexibility_keywords)
    scores['Wendbaarheid en adaptiviteit'] = 'A' if flexibility_count >=3 else 'B' if flexibility_count >=2 else 'D'

    # 4. Stakeholders
    stakeholder_keywords = ['jongeren', 'toekomstige generaties', 'minderheden', 'stakeholder', 'participatie']
    stakeholder_count = sum(text_lower.count(kw) for kw in stakeholder_keywords)
    scores['Stakeholderbetrokkenheid'] = 'A' if stakeholder_count >=3 else 'B' if stakeholder_count >=1 else 'E'

    # 5. Duurzaamheid
    sustainability_keywords = ['duurzaam', 'inclusi', 'klimaat', 'circulair', 'sociaal', 'diversiteit']
    sustainability_count = sum(text_lower.count(kw) for kw in sustainability_keywords)
    scores['Duurzaamheid en inclusiviteit'] = 'A' if sustainability_count >=4 else 'B' if sustainability_count >=2 else 'E'

    # 6. Scenario's
    scenario_keywords = ['scenario', 'onzekerheid', 'visie', 'strategi', 'toekomstbeeld', 'raming']
    scenario_count = sum(text_lower.count(kw) for kw in scenario_keywords)
    scores["Toekomstscenario's en strategische visie"] = 'A' if scenario_count >=3 else 'B' if scenario_count >=1 else 'E'

    return scores

# Feedback systemen
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
    "Horizonbepaling": "Formuleer concrete doelen voor 25+ jaar",
    "Innovatiebereidheid": "Start een innovatielab met experimenteerbudget",
    "Wendbaarheid en adaptiviteit": "Implementeer kwartaal evaluaties",
    "Stakeholderbetrokkenheid": "Organiseer jongerenpanels",
    "Duurzaamheid en inclusiviteit": "Integreer SDG's in KPI's",
    "Toekomstscenario's en strategische visie": "Ontwikkel 3 toekomstscenario's"
}

REFLECTION_QUESTIONS = {
    "Horizonbepaling": [
        "Welke trends over 50+ jaar zijn nu al relevant?",
        "Hoe blijft uw beleid relevant bij langzamere/snellere verandering?"
    ],
    "Innovatiebereidheid": [
        "Welke technologieën zouden uw sector kunnen ontwrichten?",
        "Hoe faciliteert u experimenteerruimte?"
    ],
    "Wendbaarheid en adaptiviteit": [
        "Wat is uw plan B bij onverwachte crises?",
        "Hoe meet u aanpassingssnelheid?"
    ],
    "Stakeholderbetrokkenheid": [
        "Welke stemmen ontbreken in uw planning?",
        "Hoe betrekt u toekomstige generaties concreet?"
    ],
    "Duurzaamheid en inclusiviteit": [
        "Welke externaliteiten exporteert u naar de toekomst?",
        "Hoe meet u inclusiviteitsimpact?"
    ],
    "Toekomstscenario's en strategische visie": [
        "Wat zijn uw assumpties over de toekomst?",
        "Hoe vaak update u uw scenario's?"
    ]
}

POSITIVE_FEEDBACK = {
    "Horizonbepaling": [
        "Indrukwekkende langetermijnvisie!",
        "Uitstekende balans tussen nu en later"
    ],
    "Innovatiebereidheid": [
        "Voorhoede in innovatie!",
        "Inspirerende experimenteercultuur"
    ],
    "Wendbaarheid en adaptiviteit": [
        "Voorbeeldige flexibiliteit!",
        "Sterke feedbackmechanismen"
    ],
    "Stakeholderbetrokkenheid": [
        "Inclusieve aanpak!",
        "Voorbeeldige participatie"
    ],
    "Duurzaamheid en inclusiviteit": [
        "Koploper in duurzaamheid!",
        "Inspirerende inclusiviteit"
    ],
    "Toekomstscenario's en strategische visie": [
        "Uitstekende scenario-planning!",
        "Robuuste toekomstvisie"
    ]
}

# Streamlit UI
st.set_page_config(page_title="Futri-Bot", layout="wide", page_icon="🔮")

if 'page' not in st.session_state:
    st.session_state.page = 1

if st.session_state.page == 1:
    st.title("🔮 Futri-Bot - Toekomstscan")
    
    input_text = st.text_area(
        "**Beschrijf uw plannen of strategie:**", 
        height=250,
        placeholder="Bijvoorbeeld: 'Onze visie voor 2040 is...'",
        help="Beschrijf zo concreet mogelijk uw plannen, doelstellingen en aanpak"
    )
    
    if st.button("📊 Start analyse", type="primary"):
        if input_text.strip():
            st.session_state.scores = analyze_text(input_text)
            st.session_state.page = 2
            st.rerun()
        else:
            st.error("Voer eerst een tekst in om te analyseren")

elif st.session_state.page == 2:
    st.title("📈 Analyse Resultaten")
    
    # Score berekening
    score_values = {'A':5, 'B':4, 'C':3, 'D':2, 'E':1}
    total = sum(score_values[s] for s in st.session_state.scores.values())
    avg_score = total / len(st.session_state.scores)
    final_score = chr(ord('A') + int(4 - (avg_score - 1)))
    
    # Header
    col1, col2 = st.columns([1,3])
    with col1:
        st.metric(label="**Totaalscore**", value=final_score)
        st.caption(f"Gemiddelde: {avg_score:.1f}/5.0")
    with col2:
        st.progress(avg_score/5)
        st.caption("🔍 Interpretatie: A = Uitstekend, E = Sterke verbetering nodig")
    
    st.divider()
    
    # Detailrapport
    for criterion, score in st.session_state.scores.items():
        with st.expander(f"{criterion} - Score: {score}", expanded=True):
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.subheader("📋 Analyse")
                st.write(CRITERIA_FEEDBACK[criterion][score])
                
                st.subheader("⚙️ Aanbeveling")
                if score in ['D','E']:
                    st.write(RECOMMENDATIONS[criterion])
                else:
                    st.success(f"💡 {random.choice(POSITIVE_FEEDBACK[criterion])}")
            
            with col_b:
                st.subheader("❓ Reflectie")
                if score in ['D','E']:
                    for question in REFLECTION_QUESTIONS[criterion]:
                        st.markdown(f"- {question}")
                else:
                    st.markdown("**Ter consolidatie:**")
                    st.markdown(f"- Hoe behoudt u deze sterke punten?")
                    st.markdown(f"- Welke kansen ziet u voor verdere verbetering?")
    
    st.divider()
    
    if st.button("🔄 Nieuwe analyse", type="primary"):
        st.session_state.page = 1
        st.rerun()
