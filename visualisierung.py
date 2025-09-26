"""
Modul zur Visualisierung der Analyseergebnisse:
- Wortwolke der häufigsten Begriffe
- Balkendiagramm der Kategorienhäufigkeiten
"""

import os, matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from analysator import KATEGORIEN, kategorien_auswerten


def wolkendiagramm_erstellen(woerter):
    """
    Erzeugt eine Wortwolke und speichert sie als PNG
    """
    wolke = WordCloud(width=1200, height=600, background_color="white",
                      font_path="arial.ttf", max_words=200).generate_from_frequencies(Counter(woerter))

    plt.imshow(wolke, interpolation="bilinear")
    plt.axis("off")
    datei = os.path.abspath("wolkendiagramm.png")
    plt.savefig(datei, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Wortwolke gespeichert unter: {datei}")


def kategorien_darstellen(woerter):
    """
    Erzeugt ein Balkendiagramm der Kategorienhäufigkeiten und speichert es als PNG
    """
    daten = kategorien_auswerten(woerter)
    plt.bar(daten.keys(), daten.values(), color=[d["farbe"] for d in KATEGORIEN.values()])

    # Achsen & Titel
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Treffer")
    plt.title("Kategorien")

    # Treffer über Balken anzeigen
    for bar in plt.gca().patches:
        h = bar.get_height()
        if h:
            plt.text(bar.get_x() + bar.get_width()/2, h+0.5, int(h), ha="center")

    plt.tight_layout()
    datei = os.path.abspath("kategorien.png")
    plt.savefig(datei, dpi=150)
    plt.close()
    print(f"Kategorienhäufigkeiten gespeichert unter: {datei}")
