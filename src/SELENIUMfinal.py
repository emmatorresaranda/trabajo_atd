'''
obtener un csv con el índice de educación terciaria de los países incluidos en el top 100
utilizando Selenium
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import time
import re

countries = set()

with open("arwu_bs4.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f,delimiter=';')
    next(reader)  # saltar cabecera
    for row in reader:
        country=row[1]
        countries.add(country)
# Inicializar el driver
driver = webdriver.Firefox()
driver.get("https://en.wikipedia.org/wiki/List_of_countries_by_tertiary_education_attainment")
time.sleep(3)  # Espera para que cargue la tabla

print(f"Número de países: {len(countries)}")

tertiary_education = {}

table = driver.find_element(By.CSS_SELECTOR, "table.wikitable")
rows = table.find_elements(By.TAG_NAME, "tr")

for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) >= 6:
        country_name = cells[0].text.strip()
        value = re.sub(r"\[.*\]", "", cells[5].text.strip())
        if country_name in countries:
            tertiary_education[country_name] = value
driver.quit()

# Mostrar resultados
for pais, valor in tertiary_education.items():
    print(f"{pais}: {valor}")

# CSV
with open("tertiary_education_simple.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f,delimiter=';')
    w.writerow(["Pais", "Tasa_educacion_terciaria"])
    for pais, valor in tertiary_education.items():
        w.writerow([pais, valor])

print("CSV generado correctamente: tertiary_education_simple.csv")
