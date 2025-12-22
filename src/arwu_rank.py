'''
obtener un csv con el top 100 de universidades del mundo y sus correspondientes países
utilizando Beautiful Soup
'''
from bs4 import BeautifulSoup  
import requests  
import csv 


url = "https://clarivate.com/news/shanghairankings-academic-ranking-of-world-universities-2025/"  
html = requests.get(url).text  
soup = BeautifulSoup(html, "html.parser")  
tabla = soup.find("table")  

filas = []  

for tr in tabla.find_all("tr")[1:]:  
    tds = tr.find_all("td")  
    rank = tds[0].get_text(strip=True)       # 2025Rank
    uni = tds[2].get_text(" ", strip=True)   # Institution
    pais = tds[3].get_text(" ", strip=True)  # Country
    filas.append([uni, pais, rank])          # guarda la fila

with open("arwu_bs4.csv", "w", newline="", encoding="utf-8") as f:  
    w = csv.writer(f, delimiter=";")   
    w.writerow(["university", "country", "rank"])  # cabecera
    w.writerows(filas)  

print("OK: arwu.csv")  
