import pandas as pd
import matplotlib.pyplot as plt


# Daten von CSV auslesen
data = pd.read_csv("/Users/victorfriedrich/Downloads/Test Kopie/footprintData.csv", engine='python', error_bad_lines=False)

# Konstanten
EqF_f = 1.29
EqF_c = 2.52
EqF_p = 0.46
F_co2 = 0.3
S_co2 = 0.268

# Vereinfachte Berechnung des EFs
data["Footprint"] =  (data["Land Use Beef"] * 0.8 * EqF_p) + (data["Land Use Beef"] * 0.2 * EqF_c) + data["GHG Emissions Beef"] * (1-F_co2)/S_co2 * EqF_f

# Umwandlung von cm in inch
l = 14.25 / 2.54
h = 9.5 / 2.54

# Histogramm zeichnen
hist = data.hist(column='Footprint', bins=24, grid=False, figsize=(l, h), color='#7584B3', zorder=2, rwidth=0.9)[0]

for x in hist:

    # Style für Text
    style = dict(size=9, color='#444444')

    # Achsen entfernen
    x.spines['right'].set_visible(False)
    x.spines['top'].set_visible(False)
    x.spines['left'].set_visible(False)

    # Entferne Ticks
    x.tick_params(axis="both", which="both", bottom=False, top=False, labelbottom=True, left=False, right=False, labelleft=False)

    # Entferne Titel
    x.set_title("")

    # Setze x-Achsenbeschriftung
    x.set_xlabel("Ecological Footprint (gm² / kg Rindfleisch)", size=10, labelpad=12)

    # Linie: 20%-Quantil
    percentile = data["Footprint"].quantile(q=0.2)
    x.axvline(x=percentile, linestyle='dashed', alpha=0.45, color='#333333', zorder=3)
    x.text(percentile, 3300, "20%:\n{:.0f}".format(percentile), ha="center", **style)

    # Linie: 90%-Quantil
    percentile = data["Footprint"].quantile(q=0.9)
    x.axvline(x=percentile, linestyle='dashed', alpha=0.45, color='#333333', zorder=3)
    x.text(percentile, 3300, "90%:\n{:.0f}".format(percentile), ha="center", **style)

    # Linie: Durchschnitt
    mean = data["Footprint"].mean()
    x.axvline(x=mean, linestyle='dashed', alpha=0.45, color='#333333', zorder=3)
    x.text(mean, 3300, "Mittel:\n{:.0f}".format(mean), ha="center", **style)


plt.tight_layout()
plt.show(block=True)
