import streamlit as st

# Criteria en bijbehorende vragen en scores
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
    "Wendbaarheid en adaptiviteit": {
        "vragen": [
            "Hoe kan dit beleid aangepast worden aan onverwachte toekomstige veranderingen?",
            "Welke monitoring- of evaluatiestrategieën zijn ingebouwd om bij te sturen?"
        ],
        "scores": {
            "A": "Het beleid is zeer flexibel en omvat duidelijke monitoring- en evaluatiemechanismen. Het kan snel aangepast worden aan veranderingen. Er zijn veel korte feedbackloops aanwezig.",
            "B": "Aanpassingsmogelijkheden zijn aanwezig, maar minder gedetailleerd uitgewerkt. Er zijn wel monitoring- en evaluatiemechanismen aanwezig.",
            "C": "Er is beperkte flexibiliteit, en monitoring speelt slechts een marginale rol.",
            "D": "Het beleid is grotendeels inflexibel en biedt minimale ruimte voor bijsturing.",
            "E": "Geen aandacht voor adaptiviteit of monitoring; het beleid is volledig rigide."
        }
    },
    "Stakeholderbetrokkenheid": {
        "vragen": [
            "Hoe zijn jongeren, toekomstige generaties of minderheden betrokken in de beleidsvorming?",
            "Welke stappen zijn genomen om brede input te verzamelen?"
        ],
        "scores": {
            "A": "Diverse stakeholders, inclusief een exclusieve focus op jongeren en toekomstige generaties, zijn actief betrokken bij alle fasen van de beleidsvorming. Hun input is structureel geïntegreerd.",
            "B": "Stakeholders worden betrokken, met lichte nadruk op inclusiviteit of toekomstige generaties. Er zijn consultaties geweest, maar niet altijd diepgaand.",
            "C": "Er is stakeholderbetrokkenheid, maar deze is beperkt in reikwijdte of doelgroepen. Toekomstige generaties en inclusiviteit worden niet benadrukt.",
            "D": "Stakeholderbetrokkenheid is minimaal en beperkt tot een klein aantal belanghebbenden.",
            "E": "Geen inspanningen zijn geleverd om stakeholders of toekomstige generaties te betrekken."
        }
    },
    "Duurzaamheid en inclusiviteit": {
        "vragen": [
            "Hoe draagt dit beleid bij aan een duurzame toekomst?",
            "Welke effecten heeft dit beleid op toekomstige generaties?"
        ],
        "scores": {
            "A": "Duurzaamheid en inclusiviteit zijn kernprincipes van het beleid. Het beleid is ontworpen met expliciete aandacht voor ecologische, sociale en economische duurzaamheid.",
            "B": "Duurzaamheid en inclusiviteit worden serieus genomen, maar niet altijd even diepgaand uitgewerkt.",
            "C": "Er wordt rekening gehouden met duurzaamheid, maar zonder structurele aanpak of expliciete doelen. Inclusiviteit is beperkt.",
            "D": "Duurzaamheid wordt slechts oppervlakkig genoemd, en inclusiviteit is nauwelijks aanwezig.",
            "E": "Geen aandacht voor duurzaamheid of inclusiviteit."
        }
    },
    "Toekomstscenario’s en strategische visie": {
        "vragen": [
            "Zijn er meerdere scenario’s ontwikkeld om toekomstige onzekerheden te analyseren?",
            "Welke strategische prioriteiten zijn vastgesteld op basis van de toekomstscenario’s?",
            "Worden externe experts of modellen gebruikt om de strategie te onderbouwen?"
        ],
        "scores": {
            "A": "De analyse is gebaseerd op gedetailleerde scenario’s en een duidelijke strategische visie, met robuuste maatregelen voor meerdere mogelijke toekomsten.",
            "B": "Er is gebruikgemaakt van scenario’s, maar deze zijn minder gedetailleerd of beperkt in reikwijdte.",
            "C": "Scenario’s worden genoemd, maar spelen geen grote rol in de beleidsvorming. De strategische visie is beperkt.",
            "D": "Er is nauwelijks gebruikgemaakt van scenario’s, en strategieën zijn ad hoc en kortetermijngericht.",
            "E": "Geen aandacht voor scenario’s of strategische visie."
        }
    }
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
