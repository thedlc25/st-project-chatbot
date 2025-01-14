import streamlit as st
import streamlit as st
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Eenvoudige trefwoorden die relevant kunnen zijn voor toekomstgericht beleid
FUTURE_KEYWORDS = [
    "duurzaam", "innovatie", "toekomst", "2050", "langetermijn", "klimaat",
    "ecologisch", "circulair", "resilient", "sustainable", "technology"
]

# Functie om trefwoorden te analyseren en score te berekenen
def bereken_futriscore(tekst: str, jaren: int) -> float:
    aantal_trefwoorden = sum(1 for woord in re.findall(r'\w+', tekst.lower()) if woord in FUTURE_KEYWORDS)
    score = (aantal_trefwoorden * 5) + (jaren * 0.5)
    return min(score, 100)

# Functie om sentiment te analyseren (vereenvoudigd zonder externe modules)
def analyseer_sentiment(tekst: str) -> str:
    positieve_woorden = ["goed", "positief", "voordeel", "succes", "groei"]
    negatieve_woorden = ["slecht", "negatief", "nadeel", "falen", "verlies"]

    positieve_score = sum(1 for woord in re.findall(r'\w+', tekst.lower()) if woord in positieve_woorden)
    negatieve_score = sum(1 for woord in re.findall(r'\w+', tekst.lower()) if woord in negatieve_woorden)

    if positieve_score > negatieve_score:
        return "Positief"
    elif negatieve_score > positieve_score:
        return "Negatief"
    else:
        return "Neutraal"

# Genereer een wordcloud
def genereer_wordcloud(tekst: str):
    woorden = " ".join(re.findall(r'\w+', tekst.lower()))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(woorden)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    st.pyplot(plt)

# Functie om advies te geven
def genereer_advies(score: float) -> str:
    if score < 20:
        return "Je plan scoort vrij laag op toekomstgerichtheid. Overweeg meer duurzaamheids- en innovatiedoelen."
    elif score < 50:
        return "Je plan bevat enkele toekomstgerichte elementen. Overweeg verdere uitwerking van concrete langetermijndoelen."
    elif score < 80:
        return "Je plan heeft een sterke basis. Verdiep het met robuuste scenario's en houd rekening met trends."
    else:
        return "Uitstekend! Je plan lijkt zeer toekomstgericht. Blijf echter flexibel voor nieuwe ontwikkelingen."

# Hoofdapplicatie
def main():
    st.title("Geavanceerde Futriscore AI")
    st.write(""
        "**Beoordeel hoe toekomstgericht jouw beleid of plan is.**  \n"
        "Deze tool gebruikt trefwoordanalyse, eenvoudige sentimentanalyse en visualisaties om jouw tekst te evalueren."
    "")

    # Tekst invoer
    beleid_tekst = st.text_area("Plak hier je beleidsplan of beschrijving", height=200)

    # Schuifbalk voor tijdshorizon
    tijdshorizon = st.slider("Over hoeveel jaar kijk je vooruit?", 5, 50, 25)

    # Analyse uitvoeren bij knopdruk
    if st.button("Analyseer mijn plan"):
        if not beleid_tekst.strip():
            st.warning("Voer eerst een tekst in om te analyseren.")
        else:
            # Futriscore berekenen
            score = bereken_futriscore(beleid_tekst, tijdshorizon)
            advies = genereer_advies(score)

            # Sentimentanalyse uitvoeren
            sentiment = analyseer_sentiment(beleid_tekst)

            # Wordcloud genereren
            st.subheader("Resultaten")
            st.write(f"**Futriscore:** {score:.2f}/100")
            st.write(f"**Advies:** {advies}")
            st.write(f"**Sentimentanalyse:** {sentiment}")

            st.subheader("Wordcloud van je tekst")
            genereer_wordcloud(beleid_tekst)

if __name__ == "__main__":
    main()
