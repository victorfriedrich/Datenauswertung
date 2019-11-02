import pandas as pd
import matplotlib.pyplot as plt

# Daten von CSV auslesen
data = pd.read_csv("/Users/victorfriedrich/Downloads/Test Kopie/footprintData.csv", engine='python', error_bad_lines=False)

# Konstanten
EqF_f = 1.4
EqF_c = 2.2
EqF_p = 0.5
F_co2 = 0.3
S_co2 = 0.4

# Vereinfachte Berechnung des EFs
data["Footprint_dir"] = (data["Land Use Beef"] * 0.8 * EqF_p) + (data["Land Use Beef"] * 0.2 * EqF_c)
data["Footprint_co2"] = data["GHG Emissions Beef"] * (1-F_co2)/S_co2 * EqF_f
data["Footprint"] =  (data["Land Use Beef"] * 0.8 * EqF_p) + (data["Land Use Beef"] * 0.2 * EqF_c) + data["GHG Emissions Beef"] * (1-F_co2)/S_co2 * EqF_f


# Bestätigung der Ergebnisse durch Vergleich mit Ergebnissen des Authors
print("Mean land use: {:.3f}m^2 / kg beef".format(data["Land Use Beef"].mean())) # ~326 m^2 / kg beef
print("Mean CO2: {:.2f}kg / kg beef".format(data["GHG Emissions Beef"].mean())) # ~100kg / kg beef

print("Mean footprint: {} gm^2 a / kg beef".format(data["Footprint"].mean())) # ~518 gm^2 a / kg beef
print("20% footprint: {} m^2 a / kg beef".format(data["Footprint"].quantile(q=0.2))) # ~200 gm^2 a / kg beef


# Umwandlung von cm in inch
l = 8.75 / 2.54
h = 8.75 / 2.54


# Plot erstellen
scatter = data.plot.scatter(x="GHG Emissions Beef", y="Footprint", grid=False, figsize=(l,h), alpha=0.3, color='#7584B3')

# Style für Text
style = dict(size=9, color='#444444')

# Achsen entfernen
scatter.spines['right'].set_visible(False)
scatter.spines['top'].set_visible(False)

# Entferne Ticks
scatter.tick_params(axis="both", which="both", bottom=False, top=False, labelbottom=True, left=False, right=False, labelleft=True)

# Entferne Titel
scatter.set_title("")

# Setze x-Achsenbeschriftung
scatter.set_ylabel("Ecological Footprint (gm² / kg Rindfleisch)", size=10, labelpad=12)
scatter.set_xlabel("GHG Emissionen\n(kg CO2e / kg Rindfleisch)", size=10, labelpad=12)

# Linie: Median
median = data["GHG Emissions Beef"].quantile(q=0.5) # 60.35
scatter.axvline(x=median, linestyle='dashed', alpha=0.45, color='#333333', zorder=3)
scatter.text(median, 3050, "50% (Median)", ha="center", **style)

# Aufteilung in Gesamtdatensatz und Datensatz bis zum Median
reduced = data[data['GHG Emissions Beef'] < median]
print("Pearson Correlation: {}".format(data['GHG Emissions Beef'].corr(data['Footprint']))) # 0.874 (Hohe Korrelation)
print("Pearson Correlation for GHG emissions below median: {}".format(reduced['GHG Emissions Beef'].corr(reduced['Footprint']))) # 0.375 (GeringeKorrelation)

# Anzeigen der erstellten Abbildung
plt.tight_layout()
plt.show(block=True)
