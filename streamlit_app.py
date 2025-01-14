import streamlit as st
import streamlit as st

# Eenvoudige trefwoorden die relevant kunnen zijn voor toekomstgericht beleid
FUTURE_KEYWORDS = [
    "duurzaam", "innovatie", "toekomst", "2050", "langetermijn", "klimaat",
    "ecologisch", "circulair", "resilient", "sustainable", "technology"
]

def bereken_futriscore(tekst: str, jaren: int) -> float:
    """
    Deze functie geeft een simpele 'Futriscore' terug op basis van:
    - Hoe vaak 'toekomstige' trefwoorden in de tekst voorkomen
    - Hoe groot de tijdshorizon is
    Scorebereik (0 - 100) in deze demo.
    """
    # Tel trefwoorden
    aantal_trefwoorden = 0
    woorden = tekst.lower().split()
    for woord in woorden:
        if woord.strip(",.!?") in FUTURE_KEYWORDS:
            aantal_trefwoorden += 1
    
    # Simpele formule:
    # Meer trefwoorden = hogere score
    # Grotere tijdshorizon = hogere score
    score = (aantal_trefwoorden * 5) + (jaren * 0.5)
    # Max 100 in deze demo
    return min(score, 100)

def genereer_advies(score: float) -> str:
    """
    Eenvoudig advies: hoe hoger de score, hoe toekomstgerichter
    """
    if score < 20:
        return (
            "Je plan scoort vrij laag op toekomstgerichtheid. Overweeg om meer aandacht te besteden "
            "aan duurzaamheid, innovatie en de gevolgen op lange termijn."
        )
    elif score < 50:
        return (
            "Je plan bevat enkele toekomstgerichte elementen, maar kan worden verbeterd. "
            "Verwerk bijvoorbeeld meer concrete lange-termijndoelen of innovatieve ideeën."
        )
    elif score < 80:
        return (
            "Je plan heeft al een goede basis voor de toekomst, maar er is ruimte voor verdere verdieping. "
            "Zorg voor robuuste scenario's en houd rekening met technologische of maatschappelijke trends."
        )
    else:
        return (
            "Uitstekend! Je plan lijkt goed voorbereid op de toekomst. Blijf wel alert op nieuwe ontwikkelingen "
            "en blijf je beleid updaten om future-proof te blijven."
        )

def main():
    st.title("Futriscore AI - Demo")
    st.write("""
    **Beoordeel hoe toekomstgericht jouw beleid of plan is.**  
    Deze demo scant je tekst op trefwoorden en houdt rekening met de gekozen tijdshorizon.
    """)

    # Tekst invoer
    beleid_tekst = st.text_area("Plak hier je beleidsplan of beschrijving", height=200)

    # Schuifbalk voor tijdshorizon
    tijdshorizon = st.slider("Over hoeveel jaar kijk je vooruit?", 5, 50, 25)

    # Als er op de knop wordt gedrukt, dan rekenen we de score uit
    if st.button("Bereken Futriscore"):
        if not beleid_tekst.strip():
            st.warning("Voer eerst een tekst in om te analyseren.")
        else:
            score = bereken_futriscore(beleid_tekst, tijdshorizon)
            advies = genereer_advies(score)
            
            # Toon resultaat
            st.subheader(f"Futriscore: {score:.2f}/100")
            st.write(advies)

if __name__ == "__main__":
    main()

