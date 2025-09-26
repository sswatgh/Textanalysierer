# Textanalysierer (Web & CSV)

Dieses Script kann Webseiten oder CSV-Dateien wie folgt bearbeiten:
- Stoppwörter entfernen und Text bereinigen
- Vorkommen von Wörtern in vordefinierten Kategorien zählen
- Sentiment-Analyse (positiv/negativ/neutral) durchführen
- Visualisierungen erstellen:
  - Wortwolke der häufigsten Begriffe
  - Balkendiagramm der vorkommenden Kategorien

---

## Installation

1. Repo lokal speichern
2. Abhängigkeiten installieren

```bash
pip install requests beautifulsoup4 textblob-de matplotlib wordcloud nltk
```

3. ggf. Stoppwörter-Datei anlegen/erweitern  
   - Dateiname und Speicherort: `stopwords_de.txt` im gleichen Ordner wie `main.py`
   - pro Zeile ein Stoppwort in Kleinbuchstaben

(ohne Stoppwörter-Datei werden deutsche Stoppwörter aus NLTK geladen)

---

## Nutzung

1. Programm starten

```bash
python main.py
```

2. Eingabequelle wählen  
   - `1` = Webseite (z.B. `https://www.tagesschau.de`, Format zwingend)  
   - `2` = CSV-Datei (beliebiger Textinhalt)
3. Analyseoptionen wählen
   - Kategorienanalyse
   - Sentiment-Analyse
   - Visualisierungen erstellen

---

## Ergebnisse

- Wortwolke: `wolkendiagramm.png`  
- Kategorien: `kategorien.png`    
- Speicherpfad siehe Terminal nach jeder Analyse

---

## Hinweise

- Anpassung der Kategorien in `analysator.py` möglich  
- eigene Stoppwörter einfach in `stopwords_de.txt` eintragen
- bei Webcontent-Analyse wird nur die Webseite analysiert, nicht die komplette Domain

---

## Mögliche Erweiterungen

- Crawling für Analyse kompletter Domains 
- Ergebnisse zusätzlich als CSV/JSON speichern  
- GUI  
- Clustering für dynamische Kategorisierung 
- Stoppwörter dynamisch nach ihrer Häufigkeit bestimmen
- weitere Visualisierungsarten
