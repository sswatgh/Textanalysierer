"""
Textanalysemodul:
- Extraktion von Text von Webseiten oder aus CSV-Dateien
- Textaufbereitung (Normalisierung, Stoppwort-Filterung)
- Kategorien- und Sentiment-Analyse
"""

import re, csv, requests
from collections import Counter
from bs4 import BeautifulSoup
from textblob_de import TextBlobDE


############
# Kategorien
############
KATEGORIEN = {
    "Technik": {"schluesselwoerter": ["computer","software","internet","ki","daten","digital","technik"], "farbe":"#4C72B0"},
    "Wetter": {"schluesselwoerter": ["wetter","regen","sonne","temperatur","wind","wettervorhersage","klima"], "farbe":"#55A868"},
    "Sport": {"schluesselwoerter": ["sport","fußball","olympia","wettkampf","athletik","team","sportart"], "farbe":"#CCB974"},
    "Unterhaltung": {"schluesselwoerter": ["film","musik","kino","buch","unterhaltung","show","kultur"], "farbe":"#64B5CD"},
    "Wissenschaft": {"schluesselwoerter": ["wissenschaft","forschung","physik","biologie","chemie","technologie","innovation"], "farbe":"#D65F5F"},
    "Bildung": {"schluesselwoerter": ["bildung","schule","universität","studium","lehrer","ausbildung","wissen"], "farbe":"#8C564B"},
    "Reisen": {"schluesselwoerter": ["reisen","urlaub","tourismus","abenteuer","kulturreise","entdeckung","reiseziele"], "farbe":"#E377C2"},
    "Familie": {"schluesselwoerter": ["familie","kinder","eltern","beziehung","partnerschaft","erziehung","familienleben"], "farbe":"#7F7F7F"},
    "Kunst": {"schluesselwoerter": ["kunst","malerei","skulptur","fotografie","kunstwerk","künstler","galerie"], "farbe":"#FFBB78"},
    "Essen": {"schluesselwoerter": ["essen","kochen","restaurant","küche","lebensmittel","rezept","ernährung"], "farbe":"#98DF8A"},
    "Mode": {"schluesselwoerter": ["mode","kleidung","stil","accessoires","fashion","designer","trends"], "farbe":"#F7B6D2"},
    "Soziales": {"schluesselwoerter": ["sozial","hilfe","gemeinwohl","ehrenamt","gemeinschaft","solidarität","sozialearbeit"], "farbe":"#C49C94"},
    "Geschichte": {"schluesselwoerter": ["geschichte","historisch","ereignis","zeitgeschichte","kulturgeschichte","archäologie"], "farbe":"#DBDB8D"},
    "Rechtsprechung": {"schluesselwoerter": ["rechtsprechung","urteil","gesetzgebung","jurist","rechtsfall","gerichtsurteil"], "farbe":"#FF9896"},
    "Migration": {"schluesselwoerter": ["migration","flüchtling","integration","asyl","wanderung","kulturwechsel","migrationspolitik"], "farbe":"#9467BD"},
    "Nachhaltigkeit": {"schluesselwoerter": ["nachhaltigkeit","umweltschutz","ressourcen","klimaschutz","erneuerbar","ökologie","grün"], "farbe":"#E377C2"},
    "Schimpfwort": {"schluesselwoerter": ["arsch","scheiße","dumm","idiot","schlampe","blöd","mist","verdammt"], "farbe":"#FF6347"},
    "Politik": {"schluesselwoerter": ["regierung","wahl","eu","gesetz","partei","politik","minister"], "farbe":"#DD8452"},
    "Wirtschaft": {"schluesselwoerter": ["unternehmen","markt","preis","geld","arbeit","wirtschaft","kosten"], "farbe":"#55A868"},
    "Gesundheit": {"schluesselwoerter": ["gesundheit","krankenhaus","arzt","krankheit","medizin","pflege"], "farbe":"#C44E52"}
}


###################
# Stoppwörter laden
###################
def _lade_stoppwoerter():
    """Lädt Stoppwörter aus Datei oder greift auf NLTK zurück"""
    try:
        with open("stopwords_de.txt", encoding="utf-8") as f:
            return {w.strip().lower() for w in f if w.strip()}
    except:
        import nltk
        nltk.download("stopwords")
        return set(nltk.corpus.stopwords.words("german"))
    

#######################
# Stoppwörter erweitern
#######################
STOPPWOERTER = _lade_stoppwoerter().union({"tagesschau"})


##################
# Textaufbereitung
##################
def text_aufbereiten(text):
    """
    Normalisiert Text:
    - wandelt in Kleinbuchstaben um
    - entfernt Sonderzeichen
    - filtert Stoppwörter, Zahlen und sehr kurze Wörter
    """
    text = re.sub(r"[^\wäöüß-]", " ", text.lower())  # Sonderzeichen und Umlaute entfernen
    return [w for w in re.findall(r"\b[\wäöüß-]+\b", text)
            if w not in STOPPWOERTER and len(w) > 2 and not w.isdigit()]


################
# Eingabequellen
################
def text_analysieren(url):
    """
    Extrahiert Text von einer Webseite
    """
    try:
        html = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15).text
        soup = BeautifulSoup(html, "html.parser")
        rohtext = " ".join(e.get_text(" ", strip=True)
                           for e in soup.find_all(["p","h1","h2","h3","article","Artikel","div"])
                           if e.get_text(strip=True))
        print(f"{len(rohtext)} Zeichen extrahiert")
        return text_aufbereiten(rohtext)
    except Exception as e:
        print(f"Laden der Seite: {e} fehlgeschlagen")
        return []

def csv_analysieren(dateipfad):
    """
    Extrahiert Text aus CSV-Datei
    """
    try:
        with open(dateipfad, encoding="utf-8-sig") as f:
            rohtext = " ".join(" ".join(zeile) for zeile in csv.reader(f))
        print(f"{len(rohtext)} Zeichen gelesen")
        return text_aufbereiten(rohtext)
    except Exception as e:
        print(f"Laden der Datei: {e} fehlgeschlagen")
        return []


##########
# Analysen
##########
def kategorien_auswerten(woerter):
    """
    Zählt Treffer für alle Kategorien
    """
    h = Counter(woerter)
    return {k: sum(h.get(w,0) for w in d["schluesselwoerter"]) for k,d in KATEGORIEN.items()}

def sentiment_analysieren(woerter):
    """
    Sentiment-Analyse mit TextBlobDE
    """
    if not woerter: return "Keine zulässigen Wörter zum Auswerten"
    try:
        pol = TextBlobDE(" ".join(woerter)).sentiment.polarity
        return ("POSITIV 😊" if pol>0.2 else "NEGATIV 😠" if pol<-0.2 else "NEUTRAL 😐")+f" (Score {pol:.2f})"
    except Exception as e:
        print(f"Sentiment: {e} fehlerhaft")
        return "ANALYSE FEHLGESCHLAGEN"
