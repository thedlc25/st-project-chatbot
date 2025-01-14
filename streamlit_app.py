import streamlit as st
import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_20newsgroups
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Eenvoudige trefwoorden die relevant kunnen zijn voor toekomstgericht beleid
FUTURE_KEYWORDS = [
    "duurzaam", "innovatie", "toekomst", "2050", "langetermijn", "klimaat",
    "ecologisch", "circulair", "resilient", "sustainable", "technology"
]

# Sentimentanalyse - training data laden en model voorbereiden
data = fetch_20newsgroups(subset='all', categories=['sci.space', 'rec.autos'], remove=('headers', 'footers', 'quotes'))
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.3, random_state=42)
sentiment_model = make_pipeline(TfidfVectorizer(), LinearSVC())
sentiment_model.fit(X_train, y_train)

# Functie om trefwoorden te analyseren en score te berekenen
def bereken_futriscore(tekst: str, jaren: int) -> float:
    aantal_trefwoorden = sum(1 for woord in re.findall(r'\w+', tekst.lower()) if woord in FUTURE_KEYWORDS)
    score = (aantal_trefwoorden * 5) + (jaren * 0.5)
    return min(score, 100)

# Functie om sentiment te analyseren
def analyseer_sentiment(tekst: str) -> str:
    if not tekst.strip():
        return "Neutraal"
    voorspelling = sentiment_model.predict([tekst])[0]
    return "Positief" if voorspelling == 0 else "Negatief"

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
        "Deze tool gebruikt trefwoordanalyse, sentimentanalyse en visualisaties om jouw tekst te evalueren."
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
