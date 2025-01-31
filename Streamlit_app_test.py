import streamlit as st
import re
import random

# Initialisatie
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'analysis' not in st.session_state:
    st.session_state.analysis = {}

# Analyse functie
def analyze_text(text):
    analysis = {}
    text_lower = text.lower()
    
    # 1. Horizonbepaling
    time_matches = re.findall(r'\b(\d+)\s*(jaar|jaren)\b', text)
    years = [int(m[0]) for m in time_matches if m[0].isdigit()]
    max_year = max(years) if years else 0
    analysis['Horizonbepaling'] = {
        'score': 'A' if max_year >= 50 else 'B' if max_year >= 25 else 'C' if max_year >= 10 else 'D' if max_year >= 5 else 'E',
        'matches': [f"{m[0]} {m[1]}" for m in time_matches],
        'termijn': max_year
    }

    # 2. Innovatiebereidheid
    innovation_keywords = ['innovati', 'experiment', 'pilot', 'nieuw', 'technologie']
    innovation_matches = [kw for kw in innovation_keywords if kw in text_lower]
    analysis['Innovatiebereidheid'] = {
        'score': 'A' if len(innovation_matches) >=4 else 'B' if len(innovation_matches)>=2 else 'C' if len(innovation_matches)>=1 else 'E',
        'matches': innovation_matches
    }

    # 3. Wendbaarheid
    flexibility_keywords = ['flexibel', 'aanpass', 'monitor', 'evalua', 'feedback']
    flexibility_matches = [kw for kw in flexibility_keywords if kw in text_lower]
    analysis['Wendbaarheid en adaptiviteit'] = {
        'score': 'A' if len(flexibility_matches)>=3 else 'B' if len(flexibility_matches)>=2 else 'D',
        'matches': flexibility_matches
    }

    # 4. Stakeholders
    stakeholder_keywords = ['jongeren', 'toekomstige generaties', 'minderheden', 'stakeholder']
    stakeholder_matches = [kw for kw in stakeholder_keywords if kw in text_lower]
    analysis['Stakeholderbetrokkenheid'] = {
        'score': 'A' if len(stakeholder_matches)>=3 else 'B' if len(stakeholder_matches)>=1 else 'E',
        'matches': stakeholder_matches
    }

    # 5. Duurzaamheid
    sustainability_keywords = ['duurzaam', 'inclusi', 'klimaat', 'circulair', 'sociaal']
    sustainability_matches = [kw for kw in sustainability_keywords if kw in text_lower]
    analysis['Duurzaamheid en inclusiviteit'] = {
        'score': 'A' if len(sustainability_matches)>=4 else 'B' if len(sustainability_matches)>=2 else 'E',
        'matches': sustainability_matches
    }

    # 6. Scenario's
    scenario_keywords = ['scenario', 'onzekerheid', 'visie', 'strategi', 'toekomstbeeld']
    scenario_matches = [kw for kw in scenario_keywords if kw in text_lower]
    analysis["Toekomstscenario's en strategische visie"] = {
        'score': 'A' if len(scenario_matches)>=3 else 'B' if len(scenario_matches)>=1 else 'E',
        'matches': scenario_matches
    }

    return analysis

# Feedback systemen
REFLECTION_QUESTIONS = {
    "Horizonbepaling": [
        "Hoe zou dit beleid eruitzien over 50 jaar?",
        "Welke trends zouden invloed kunnen hebben op uw doelen?"
    ],
    "Innovatiebereidheid": [
        "Welke innovatieve ideeën zouden u kunnen helpen?",
        "Hoe zou u experimenteren met nieuwe benaderingen?"
    ],
    "Wendbaarheid en adaptiviteit": [
        "Hoe snel zou u kunnen reageren op veranderingen?",
        "Welke strategieën zou u kunnen inzetten om flexibel te blijven?"
    ],
    "Stakeholderbetrokkenheid": [
        "Hoe zou u jongeren of minderheden meer betrekken?",
        "Welke waarde kan brede input toevoegen aan uw beleid?"
    ],
    "Duurzaamheid en inclusiviteit": [
        "Hoe kan uw beleid bijdragen aan een duurzame toekomst?",
        "Welke groepen hebben de meeste baat bij inclusiviteit?"
    ],
    "Toekomstscenario's en strategische visie": [
        "Welke scenario’s zou u kunnen ontwikkelen voor de toekomst?",
        "Hoe kunt u uw strategie robuuster maken?"
    ]
}


IMPROVEMENT_TIPS = {
    "Horizonbepaling": [
        "Voeg concrete tijdsaanduidingen toe (bijv. 'tegen 2040', 'binnen 10 jaar')",
        "Beschrijf langetermijntrends die van invloed zijn op uw plannen",
        "Koppel korte-termijnacties aan lange-termijndoelen"
    ],
    "Innovatiebereidheid": [
        "Beschrijf specifieke technologieën die u wilt inzetten",
        "Plan een pilotproject met duidelijke evaluatiemomenten",
        "Reserveer budget voor experimentele oplossingen"
    ],
    "Wendbaarheid en adaptiviteit": [
        "Implementeer een halfjaarlijkse evaluatiecyclus",
        "Ontwikkel een crisisresponsplan voor onverwachte gebeurtenissen",
        "Train medewerkers in agile werkmethoden"
    ],
    "Stakeholderbetrokkenheid": [
        "Organiseer een jongerenadviesraad voor input",
        "Voeg een diversiteitstoets toe aan besluitvorming",
        "Maak een participatietraject voor toekomstige generaties"
    ],
    "Duurzaamheid en inclusiviteit": [
        "Koppel doelstellingen aan de Sustainable Development Goals",
        "Voeg een duurzaamheidsparagraaf toe aan alle plannen",
        "Meet jaarlijks de inclusiviteitsimpact"
    ],
    "Toekomstscenario's en strategische visie": [
        "Ontwikkel 3 verschillende toekomstscenario's",
        "Creëer een adaptief strategisch raamwerk",
        "Integreer regelmatige horizonverkenningen in uw proces"
    ]
}

# Styling
st.markdown("""
<style>
    .score-badge {
        padding: 0.2em 0.5em;
        border-radius: 0.25em;
        font-weight: bold;
        display: inline-block;
        margin-left: 0.5rem;
    }
    .score-A { background: #2ecc71; color: white; }
    .score-B { background: #27ae60; color: white; }
    .score-C { background: #f1c40f; color: black; }
    .score-D { background: #e67e22; color: white; }
    .score-E { background: #e74c3c; color: white; }
    .analysis-box {
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.5rem;
        background: #f8f9fa;
    }
    .positive { border-left: 4px solid #2ecc71; }
    .negative { border-left: 4px solid #e74c3c; }
</style>
""", unsafe_allow_html=True)

# Pagina's
def input_page():
    st.title("🔮 Futri-Bot - Toekomstanalyse")
    input_text = st.text_area(
        "**Beschrijf uw plannen of strategie:**", 
        height=300,
        placeholder="Bijvoorbeeld: 'Onze doelstelling is klimaatneutraliteit in 2050 door innovatieve technologieën...'"
    )
    
    if st.button("📊 Start analyse", type="primary"):
        if input_text.strip():
            st.session_state.analysis = analyze_text(input_text)
            st.session_state.page = 2
            st.rerun()
        else:
            st.error("Voer eerst een tekst in om te analyseren")

def results_page():
    st.title("📈 Analyse Resultaten")
    
    # Header
    st.markdown("---")
    st.subheader("Overzicht scores")
    cols = st.columns(3)
    for idx, (criterion, data) in enumerate(st.session_state.analysis.items()):
        with cols[idx%3]:
            st.markdown(f"**{criterion}**<br><span class='score-badge score-{data['score']}'>{data['score']}</span>", 
                       unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailanalyse
    for criterion, data in st.session_state.analysis.items():
        with st.expander(f"{criterion} - Score: {data['score']}", expanded=True):
            # Analyse
            st.markdown("### 📋 Analyse")
            if data['matches']:
                matches_text = ", ".join(list(set(data['matches']))[:3])
                st.markdown(f"**Gevonden in tekst:** {matches_text}")
            else:
                st.markdown("❌ Geen relevante termen gevonden")
            
            # Reflectievragen
            st.markdown("### ❓ Reflectievragen")
            for question in REFLECTION_QUESTIONS[criterion]:
                st.markdown(f"- {question}")
            
            # Verbeteradvies
            st.markdown("### 🛠️ Verbeteradvies")
            tip = random.choice(IMPROVEMENT_TIPS[criterion])
            st.markdown(f'<div class="analysis-box {"positive" if data["score"] in ["A","B"] else "negative"}">{tip}</div>', 
                       unsafe_allow_html=True)
    
    if st.button("🔄 Nieuwe analyse", type="primary"):
        st.session_state.page = 1
        st.rerun()

# Hoofdapplicatie
if st.session_state.page == 1:
    input_page()
elif st.session_state.page == 2:
    results_page()
