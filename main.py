"""
Hauptmodul zur Steuerung der Textanalyse
"""

import os
from analysator import text_analysieren, csv_analysieren, kategorien_auswerten, sentiment_analysieren
from visualisierung import wolkendiagramm_erstellen, kategorien_darstellen


def frage_bool(frage):
    """Hilfsfunktion für Ja/Nein-Abfragen"""
    return input(f"{frage} (j/n): ").lower().startswith("j")


def eingabe_abfragen():
    """
    Fragt Benutzer nach Eingabequelle (Webseite oder CSV)
    """
    while True:
        wahl = input("\n1=Webseite, 2=CSV: ").strip()
        if wahl == "1":
            url = input("Web-URL(Format: https://www.abc.de): ").strip()
            if url.startswith(("http://", "https://")):
                return {"typ": "web", "quelle": url}
            print("Ungültige URL. Format: https://www.xyz.de zwingend")
        elif wahl == "2":
            pfad = input("CSV-Datei: ").strip()
            if os.path.exists(pfad):
                return {"typ": "csv", "quelle": pfad}
            print("Datei nicht gefunden")


def hauptprogramm():
    """Steuert den Analyseablauf"""
    eingabe = eingabe_abfragen()
    optionen = {
        "kategorien": frage_bool("Kategorienanalyse?"),
        "sentiment": frage_bool("Sentiment-Analyse?"),
        "grafiken": frage_bool("Visualisierungen?")
    }

    # Quelle einlesen
    woerter = text_analysieren(eingabe["quelle"]) if eingabe["typ"] == "web" else csv_analysieren(eingabe["quelle"])

    # Analysen
    if optionen["kategorien"]:
        print("\nKATEGORIEN:")
        for k, v in kategorien_auswerten(woerter).items():
            if v:
                print(f" - {k}: {v}")

    if optionen["sentiment"]:
        print("\nSENTIMENT:")
        print(sentiment_analysieren(woerter))

    # Diagramme
    if optionen["grafiken"]:
        wolkendiagramm_erstellen(woerter)
        if optionen["kategorien"]:
            kategorien_darstellen(woerter)

    input("\nAnalyse abgeschlossen. Beenden mit Enter.")


if __name__ == "__main__":
    hauptprogramm()
