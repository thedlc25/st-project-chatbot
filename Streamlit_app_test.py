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
st.title("🤖 Futri-Bot: Beleidsanalyse Assistent")

# Introductie van de chatbot
st.write("Welkom! Ik ben Futri-Bot, jouw slimme assistent voor beleidsanalyse. Ik stel je een aantal vragen over jouw beleid en analyseer je antwoorden.")

# Chat-sessie instellen
if "questions" not in st.session_state:
    st.session_state.questions = [
        "Wat is de naam van je beleid?",
        "Wat zijn de belangrijkste doelen van je beleid?",
        "Hoe ver in de toekomst richt je beleid zich?",
        "Zijn er innovatieve oplossingen opgenomen in je beleid?",
        "Welke monitoringmechanismen heb je ingebouwd?",
        "Hoe betrek je stakeholders bij het beleid?",
        "Welke stappen heb je genomen om duurzaamheid te waarborgen?",
        "Zijn er specifieke toekomstscenario's die je hebt overwogen?",
        "Hoe worden jongeren en minderheden betrokken in je beleid?",
        "Welke trends heb je geanalyseerd voor de komende 10 jaar?",
        "Wat maakt jouw beleid flexibel voor onverwachte veranderingen?",
        "Zijn er pilots of experimenten in je beleid opgenomen?",
        "Welke rol spelen externe experts in jouw beleid?",
        "Hoe wordt inclusiviteit in het beleid bevorderd?",
        "Hoe vaak plan je een evaluatie van het beleid?",
        "Hoe waarborg je dat het beleid blijft aansluiten bij trends?",
        "Welke langetermijnimpact verwacht je van het beleid?",
        "Hoe plan je het beleid aan te passen als omstandigheden veranderen?",
        "Zijn er financiële middelen gereserveerd voor innovatie?",
        "Hoe worden resultaten gedeeld met stakeholders?",
        "Wat zijn de ecologische voordelen van je beleid?",
        "Hoeveel nadruk ligt er op sociale duurzaamheid?",
        "Zijn er scenario-analyses uitgevoerd voor risico's?",
        "Wat zijn de belangrijkste uitdagingen van het beleid?",
        "Welke indicatoren gebruik je om het succes van het beleid te meten?",
        "Wat zou je aanpassen als het beleid faalt?",
        "Hoe wordt feedback van stakeholders verwerkt?",
        "Welke strategische prioriteiten staan centraal?",
        "Hoe wordt technologische vooruitgang gebruikt?",
        "Zijn er plannen om toekomstige generaties te beschermen?"
    ]
    st.session_state.current_question = 0
    st.session_state.answers = []

# Vragen beantwoorden
if st.session_state.current_question < len(st.session_state.questions):
    question = st.session_state.questions[st.session_state.current_question]
    st.write(f"**Futri-Bot:** {question}")
    user_input = st.text_input("Jouw antwoord:", key=f"answer_{st.session_state.current_question}")

    if st.button("Verzend antwoord"):
        if user_input.strip():
            st.session_state.answers.append(user_input)
            st.session_state.current_question += 1
            st.experimental_rerun()
        else:
            st.error("Je antwoord mag niet leeg zijn. Probeer het opnieuw.")
else:
    st.write("Bedankt voor het beantwoorden van alle vragen! Hier is je analyse:")
    input_text = " ".join(st.session_state.answers)

    # Analyse uitvoeren
    scores, explanations = calculate_scores(input_text)
    avg_score = calculate_average(scores)
    final_grade = score_to_letter(avg_score)

    # Resultaten weergeven
    st.success(f"Je totale score is: **{final_grade} ({avg_score:.1f} gemiddeld)**.")

    st.subheader("🔍 Gedetailleerde analyse per criterium:")
    for criterion, score in scores.items():
        letter = score_to_letter(score)
        st.write(f"**{criterion}**: {letter} ({score} punten)")
        st.write(f"*Inzicht van Futri-Bot:* {explanations[criterion]}")

    st.subheader("💡 Aanbevelingen voor verbetering:")
    for criterion, score in scores.items():
        if score < 5:
            st.write(f"- **{criterion}:** Overweeg verbeteringen. {explanations[criterion]}")

    st.write("\nBedankt dat je Futri-Bot hebt gebruikt! Voor verdere analyses kun je altijd opnieuw starten.")
