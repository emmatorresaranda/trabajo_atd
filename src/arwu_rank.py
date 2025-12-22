'''
obtener un csv con el top 100 de universidades del mundo y sus correspondientes países
utilizando Beautiful Soup
'''
from bs4 import BeautifulSoup  # parsear HTML
import requests  # descargar la web
import csv  # escribir CSV


url = "https://clarivate.com/news/shanghairankings-academic-ranking-of-world-universities-2025/"  # página
html = requests.get(url).text  # descarga HTML
soup = BeautifulSoup(html, "html.parser")  # convierte HTML en soup
tabla = soup.find("table")  # coge la tabla del ranking

filas = []  # aquí guardamos filas del CSV

for tr in tabla.find_all("tr")[1:]:  # recorre filas (salta cabecera)
    tds = tr.find_all("td")  # columnas
    rank = tds[0].get_text(strip=True)  # 2025Rank
    uni = tds[2].get_text(" ", strip=True)  # Institution
    pais = tds[3].get_text(" ", strip=True)  # Country/Region
    filas.append([uni, pais, rank])  # guarda la fila

with open("arwu_bs4.csv", "w", newline="", encoding="utf-8") as f:  # abre el CSV
    w = csv.writer(f, delimiter=";")   # escritor CSV
    w.writerow(["university", "country", "rank"])  # cabecera
    w.writerows(filas)  # escribe filas

print("OK: arwu.csv")  # confirmación
