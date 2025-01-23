import streamlit as st

# Functie om scores toe te kennen per criterium
def calculate_scores(input_text):
    scores = {}
    explanations = {}

    # Horizonbepaling
    if "50 jaar" in input_text or "langetermijn" in input_text:
        scores["Horizonbepaling"] = 5
        explanations["Horizonbepaling"] = "Het beleid heeft een duidelijke focus op langetermijndoelen (50+ jaar)."
    elif "10 jaar" in input_text:
        scores["Horizonbepaling"] = 3
        explanations["Horizonbepaling"] = "Het beleid richt zich op middellange termijn (5-10 jaar), met enige aandacht voor trends."
    else:
        scores["Horizonbepaling"] = 2
        explanations["Horizonbepaling"] = "Het beleid richt zich voornamelijk op de korte termijn (<10 jaar)."

    # Innovatiebereidheid
    if "innovatie" in input_text or "experiment" in input_text:
        scores["Innovatiebereidheid"] = 4
        explanations["Innovatiebereidheid"] = "Het beleid bevat enkele innovatieve elementen en experimenteerruimte."
    else:
        scores["Innovatiebereidheid"] = 2
        explanations["Innovatiebereidheid"] = "Er is weinig ruimte voor innovatie en het beleid vertrouwt vooral op traditionele methoden."

    # Wendbaarheid en adaptiviteit
    if "flexibiliteit" in input_text or "monitoring" in input_text:
        scores["Wendbaarheid en adaptiviteit"] = 4
        explanations["Wendbaarheid en adaptiviteit"] = "Flexibiliteit en monitoringmechanismen zijn goed aanwezig."
    else:
        scores["Wendbaarheid en adaptiviteit"] = 2
        explanations["Wendbaarheid en adaptiviteit"] = "Minimale mogelijkheden voor aanpassing en monitoring."

    # Stakeholderbetrokkenheid
    if "jongeren" in input_text or "consultatie" in input_text:
        scores["Stakeholderbetrokkenheid"] = 4
        explanations["Stakeholderbetrokkenheid"] = "Sterke betrokkenheid van diverse stakeholders, inclusief jongeren en minderheden."
    else:
        scores["Stakeholderbetrokkenheid"] = 2
        explanations["Stakeholderbetrokkenheid"] = "Stakeholderbetrokkenheid is minimaal en beperkt."

    # Duurzaamheid en inclusiviteit
    if "duurzaamheid" in input_text or "inclusiviteit" in input_text:
        scores["Duurzaamheid en inclusiviteit"] = 5
        explanations["Duurzaamheid en inclusiviteit"] = "Duurzaamheid en inclusiviteit zijn kernprincipes met aandacht voor ecologische en sociale aspecten."
    else:
        scores["Duurzaamheid en inclusiviteit"] = 3
        explanations["Duurzaamheid en inclusiviteit"] = "Beperkte aandacht voor duurzaamheid en inclusiviteit."

    # Toekomstscenario’s en strategische visie
    if "scenario" in input_text or "strategie" in input_text:
        scores["Toekomstscenario’s en strategische visie"] = 4
        explanations["Toekomstscenario’s en strategische visie"] = "Het beleid bevat enkele toekomstscenario’s en strategische prioriteiten."
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
st.title("🤖 Futri-Bot: Beleidsanalyse")
st.subheader("Welkom! Laten we samen jouw beleid analyseren.")
st.write("Beschrijf jouw beleid hieronder. De Futri-Bot zal jouw input analyseren en feedback geven op basis van verschillende criteria. Stel vragen alsof je met een slimme assistent praat!")

# Input veld
input_text = st.text_area("👩‍💻 Wat wil je analyseren?", placeholder="Beschrijf hier het beleid dat je wilt laten analyseren...", height=200)

# Analyse knop
if st.button("Analyseer mijn beleid!"):
    if input_text.strip():
        # Scores berekenen
        scores, explanations = calculate_scores(input_text)
        avg_score = calculate_average(scores)
        final_grade = score_to_letter(avg_score)

        # Dialoog tonen
        st.header("📊 Analyse resultaten")
        st.write(f"**Futri-Bot:** Bedankt voor je input! Op basis van mijn analyse is jouw totale score: **{final_grade} ({avg_score:.1f} gemiddeld)**.")
        
        st.subheader("⚙️ Gedetailleerde scores")
        for criterion, score in scores.items():
            letter = score_to_letter(score)
            st.write(f"- **{criterion}**: {letter} ({score} punten)")
            st.write(f"  > Analyse: {explanations[criterion]}")
        
        st.subheader("💡 Aanbevelingen")
        for criterion, score in scores.items():
            if score < 5:
                st.write(f"- **{criterion}:** {explanations[criterion]} Overweeg aanvullende verbeteringen voor dit aspect.")
    else:
        st.error("🚨 Voer alstublieft informatie in voordat je op de analyse-knop drukt.")
