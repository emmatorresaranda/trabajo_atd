'''
crear el csv final del proyecto donde se unen todos los csv de los codigos API Rest, 
Selenium y Beautiful Soup
'''
import csv

tertiary = {}
with open("tertiary_education_simple.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter=";"):
        tertiary[row["Pais"]] = row["Tasa_educacion_terciaria"]

worldbank = {}
with open("worldbank.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter=";"):
        worldbank[row["iso2"]] = row["value"]

arwu_count = {}
arwu_best = {}
with open("arwu_bs4.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter=";"):
        country = row["country"]
        arwu_count[country] = arwu_count.get(country, 0) + 1
        try:
            rank = int(row["rank"])
            if country not in arwu_best or rank < arwu_best[country]:
                arwu_best[country] = rank
        except:
            pass

with open("final_dataset.csv", "w", newline="", encoding="utf-8") as out:
    writer = csv.writer(out, delimiter=";")
    writer.writerow([
        "iso2", "country_common_name", "region", "subregion",
        "population", "area_km2",
        "tertiary_rate", "edu_spend_pct_gdp",
        "arwu_top100_count", "arwu_best_rank"
    ])

    with open("fetch_countries.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter=";"):
            iso2 = row["iso2"]

            if iso2 not in worldbank:   
                continue

            country = row["country_common_name"]

            writer.writerow([
                iso2,
                country,
                row["region"],
                row["subregion"],
                row["population"],
                row["area_km2"],
                tertiary.get(country, ""),
                worldbank.get(iso2, ""),
                arwu_count.get(country, 0),
                arwu_best.get(country, "")
            ])

print("CSV final creado: final_dataset.csv")
