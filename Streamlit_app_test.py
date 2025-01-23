import streamlit as st

# Functie om scores toe te kennen per criterium
def calculate_scores(input_text):
    scores = {}
    explanations = {}

    # Horizonbepaling
    if "50 jaar" in input_text or "langetermijn" in input_text:
        scores["Horizonbepaling"] = 5
        explanations["Horizonbepaling"] = "Duidelijke focus op langetermijndoelen (50+ jaar)."
    elif "10 jaar" in input_text:
        scores["Horizonbepaling"] = 3
        explanations["Horizonbepaling"] = "Focus op middellange termijn (5-10 jaar) met aandacht voor trends."
    else:
        scores["Horizonbepaling"] = 2
        explanations["Horizonbepaling"] = "Beleid richt zich voornamelijk op de korte termijn (<10 jaar)."

    # Innovatiebereidheid
    if "innovatie" in input_text or "experiment" in input_text:
        scores["Innovatiebereidheid"] = 4
        explanations["Innovatiebereidheid"] = "Beleid bevat enkele innovatieve elementen en ruimte voor experimenten."
    else:
        scores["Innovatiebereidheid"] = 2
        explanations["Innovatiebereidheid"] = "Weinig tot geen ruimte voor innovatie, vertrouwend op traditionele methoden."

    # Wendbaarheid en adaptiviteit
    if "flexibiliteit" in input_text or "monitoring" in input_text:
        scores["Wendbaarheid en adaptiviteit"] = 4
        explanations["Wendbaarheid en adaptiviteit"] = "Flexibiliteit en monitoringmechanismen zijn aanwezig."
    else:
        scores["Wendbaarheid en adaptiviteit"] = 2
        explanations["Wendbaarheid en adaptiviteit"] = "Minimale ruimte voor bijsturing en weinig monitoringmechanismen."

    # Stakeholderbetrokkenheid
    if "jongeren" in input_text or "consultatie" in input_text:
        scores["Stakeholderbetrokkenheid"] = 4
        explanations["Stakeholderbetrokkenheid"] = "Betrokkenheid van stakeholders, inclusief jongeren en minderheden, is sterk."
    else:
        scores["Stakeholderbetrokkenheid"] = 2
        explanations["Stakeholderbetrokkenheid"] = "Stakeholderbetrokkenheid is minimaal en beperkt."

    # Duurzaamheid en inclusiviteit
    if "duurzaamheid" in input_text or "inclusiviteit" in input_text:
        scores["Duurzaamheid en inclusiviteit"] = 5
        explanations["Duurzaamheid en inclusiviteit"] = "Duurzaamheid is een kernprincipe met aandacht voor ecologische en sociale aspecten."
    else:
        scores["Duurzaamheid en inclusiviteit"] = 3
        explanations["Duurzaamheid en inclusiviteit"] = "Beperkte aandacht voor duurzaamheid en inclusiviteit."

    # Toekomstscenario’s en strategische visie
    if "scenario" in input_text or "strategie" in input_text:
        scores["Toekomstscenario’s en strategische visie"] = 4
        explanations["Toekomstscenario’s en strategische visie"] = "Beleid bevat enkele toekomstscenario’s en strategische prioriteiten."
    else:
        scores["Toekomstscenario’s en strategische visie"] = 2
        explanations["Toekomstscenario’s en strategische visie"] = "Weinig tot geen aandacht voor toekomstscenario’s en strategische visie."

    return scores, explanations

# Functie om gemiddelde score te berekenen
def calculate_average(scores):
    total = sum(scores.values())
    avg = total / len(scores)
    return avg

# Mapping van score naar letter
def score_to_letter(avg_score):
    if avg_score >= 4.5:
        return "A"
    elif avg_score >= 3.5:
        return "B"
    elif avg_score >= 2.5:
        return "C"
    elif avg_score >= 1.5:
        return "D"
    else:
        return "E"

# Streamlit UI
st.title("Futri-Bot: Beleidsanalyse TEST")
st.write("Voer hieronder de beleidsinformatie in. De Futri-Bot analyseert de input en geeft scores voor elk criterium.")

# Input veld
input_text = st.text_area("Beschrijf het beleid", height=200)

# Analyse knop
if st.button("Futri-Score Berekenen"):
    if input_text.strip():
        # Scores berekenen
        scores, explanations = calculate_scores(input_text)
        avg_score = calculate_average(scores)
        final_grade = score_to_letter(avg_score)

        # Resultaten tonen
        st.header(f"Totaalscore: {final_grade} ({avg_score:.1f} gemiddeld)")
        st.write("Hieronder volgt de uitsplitsing per criterium:")

        for criterion, score in scores.items():
            letter = score_to_letter(score)
            st.subheader(f"{criterion}: {letter} ({score} punten)")
            st.write(f"**Analyse:** {explanations[criterion]}")

        # Aanbevelingen
        st.header("Aanbevelingen voor Verbetering")
        for criterion, score in scores.items():
            if score < 5:
                st.write(f"- **{criterion}:** {explanations[criterion]} Overweeg aanvullende maatregelen.")
    else:
        st.error("Voer alstublieft informatie in het tekstvak in.")
