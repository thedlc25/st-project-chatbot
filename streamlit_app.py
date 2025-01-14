import streamlit as st

# Criteria en hun bijbehorende vragen en scores
CRITERIA = {
    "Horizonbepaling": {
        "vragen": [
            "Welke langetermijndoelen probeert dit beleid te realiseren?",
            "Hoe wordt rekening gehouden met trends en ontwikkelingen in de komende 5, 10, 20, 50 of 100 jaar?"
        ],
        "scores": {
            "A": "Het beleid heeft een duidelijke focus op langetermijndoelen (Heden tot 50+ jaar). Trends en ontwikkelingen worden gedetailleerd geanalyseerd en verwerkt.",
            "B": "Langetermijndoelen zijn aanwezig, maar minder uitgebreid. Er is gekeken naar het heden tot 50 jaar in de toekomst. Trends worden besproken, maar niet diepgaand.",
            "C": "Enkele langetermijndoelen worden genoemd, maar zonder structurele aanpak. Korte termijn is dominant. Er is minder ver in de toekomst gekeken.",
            "D": "Er is enige aandacht voor de toekomst, maar deze blijft beperkt tot korte termijn (< 10 jaar).",
            "E": "Geen aandacht voor trends, ontwikkelingen of doelen op lange termijn. Er is niet verder gekeken dan 5 jaar in de toekomst."
        }
    },
    "Innovatiebereidheid": {
        "vragen": [
            "Welke nieuwe of innovatieve benaderingen worden in het beleid opgenomen?",
            "Hoe wordt geëxperimenteerd met nieuwe ideeën of concepten?"
        ],
        "scores": {
            "A": "Innovatie staat centraal; het beleid maakt gebruik van experimenten, pilots en vernieuwende benaderingen. Er worden gestructureerde en korte feedbackloops besproken en geïmplementeerd.",
            "B": "Innovatie is aanwezig, maar beperkt tot enkele onderdelen van het beleid. Er is ruimte voor feedback.",
            "C": "Er worden bestaande oplossingen toegepast, met enkele innovaties in de marges. Er is weinig ruimte voor feedback.",
            "D": "Er is weinig tot geen ruimte voor innovatie. Het beleid vertrouwt vooral op traditionele methoden.",
            "E": "Innovatie ontbreekt volledig; het beleid is volledig gebaseerd op conventionele benaderingen."
        }
    },
    # Andere criteria zoals Wendbaarheid, Stakeholderbetrokkenheid, enz. kunnen hier worden toegevoegd
}

# Functie om scores om te zetten naar punten
SCORE_TO_POINTS = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2,
    "E": 1
}

# Bereken het gemiddelde van de scores
def bereken_gemiddelde(scores):
    punten = [SCORE_TO_POINTS[score] for score in scores.values()]
    gemiddelde = sum(punten) / len(punten)
    return gemiddelde

# UI voor elke criterium
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

    scores = {}

    # Loop door elk criterium en vraag om input
    for criterium, data in CRITERIA.items():
        scores[criterium] = toon_criterium_ui(criterium, data)

    if st.button("Bereken Totaalscore"):
        gemiddelde = bereken_gemiddelde(scores)
        eindscore = "ABCDE"[int(round(5 - gemiddelde))]  # Vertaal gemiddelde naar eindscore
        st.subheader("Resultaten")
        st.write(f"Totaalscore: {eindscore} ({gemiddelde:.2f} gemiddeld)")

        for criterium, score in scores.items():
            st.write(f"- {criterium}: {score} ({CRITERIA[criterium]['scores'][score]})")

if __name__ == "__main__":
    main()
