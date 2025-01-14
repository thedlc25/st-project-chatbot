import streamlit as st

# Criteria en workflow
CRITERIA = {
    "Horizonbepaling": {
        "vragen": [
            "Identificeer langetermijndoelen",
            "Analyseer trends en ontwikkelingen"
        ]
    },
    "Innovatiebereidheid": {
        "vragen": [
            "Zoek naar innovatieve benaderingen en experimenten"
        ]
    },
    "Wendbaarheid en adaptiviteit": {
        "vragen": [
            "Evalueer monitoring- en aanpassingsmechanismen"
        ]
    },
    "Stakeholderbetrokkenheid": {
        "vragen": [
            "Analyseer betrokkenheid van jongeren, minderheden en andere stakeholders"
        ]
    },
    "Duurzaamheid en inclusiviteit": {
        "vragen": [
            "Zoek naar ecologische, sociale en economische duurzaamheid"
        ]
    },
    "Toekomstscenario’s en strategische visie": {
        "vragen": [
            "Controleer gebruik van scenario’s en strategieën"
        ]
    }
}

SCORE_TO_POINTS = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
    "E": 1
}

# Berekening gemiddelde score
def bereken_gemiddelde(scores):
    punten = [SCORE_TO_POINTS[score] for score in scores.values()]
    gemiddelde = sum(punten) / len(punten)
    return round(gemiddelde, 1)

# UI voor invoer per criterium
def toon_criterium_ui(criterium, data):
    st.subheader(criterium)
    for vraag in data["vragen"]:
        st.write(f"- {vraag}")
    keuze = st.selectbox(f"Score voor {criterium}", options=["A", "B", "C", "D", "E"], key=criterium)
    return keuze

# Hoofdapplicatie
def main():
    st.title("Futri-Bot - Beleidsanalyse AI")
    st.write("De Futri-Bot beoordeelt beleidsplannen op toekomstgerichtheid aan de hand van zes criteria.")

    st.header("Input ontvangen")
    beleid_tekst = st.text_area("Voer je beleidstekst in of beschrijf het voorstel", height=150)

    if beleid_tekst.strip():
        st.header("Analyseer tekst")
        st.write("De ingevoerde tekst wordt geanalyseerd op basis van de zes criteria.")

        scores = {}
        for criterium, data in CRITERIA.items():
            scores[criterium] = toon_criterium_ui(criterium, data)

        if st.button("Bereken Futri-score"):
            gemiddelde = bereken_gemiddelde(scores)
            eindscore = "ABCDE"[int(5 - gemiddelde)]  # Vertaal gemiddelde naar score

            st.subheader("Rapporteer resultaten")
            st.write(f"**Totaalscore:** {eindscore} ({gemiddelde})")

            for criterium, score in scores.items():
                st.write(f"- {criterium}: {score}")

if __name__ == "__main__":
    main()
