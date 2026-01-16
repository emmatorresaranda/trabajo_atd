'''
obtener un csv con el índice de educación terciaria de los países incluidos en el top 100
utilizando Selenium
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

countries = []

with open("arwu_bs4.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f,delimiter=';')
    next(reader)  # saltar cabecera
    for row in reader:
        country=row[1]
        if country not in countries:
            countries.append(country)

url = "https://ourworldindata.org/grapher/share-of-the-population-with-completed-tertiary-education?tab=table"

driver = webdriver.Chrome()
driver.get(url)

# Esperar a que cargue la tabla hasta 20 segundos
wait = WebDriverWait(driver, 20)  
table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
rows = table.find_elements(By.TAG_NAME, "tr")

# Creamos un diccionario con los datos de la tabla
data_dict = {}
for row in rows[1:]:
    cols = row.find_elements(By.TAG_NAME, "td")
    if len(cols) < 3:
        continue
    name = cols[0].text.strip()
    value = cols[2].text.strip()
    data_dict[name.lower()] = value
    
# Buscamos los índices de los países del ranking
tertiary_education = {}
for country in countries:
    tertiary_education[country] = data_dict.get(country.lower(), "No encontrado")

# Guardar la información obtenida en un CSV
with open("tertiary_education_simple.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(["Pais", "Tasa_educacion_terciaria"])
    for pais, valor in tertiary_education.items():
        w.writerow([pais, valor])

driver.quit()
print("CSV generado correctamente: tertiary_education_simple.csv")

