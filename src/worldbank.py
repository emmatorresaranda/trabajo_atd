'''
obtener un csv con el índice de gasto público en educación de los países incluidos en el top 100
utilizando API Rest
'''                                
import csv                                               
import requests                                           

#obtenemos los nombres iso2 de los países correspondientes del top 100 universidades del mundo
countries = set()
with open("arwu_bs4.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter=";")
    next(reader)  
    for row in reader:
        countries.add(row[1])

iso2_set = set()                                          
with open("fetch_countries.csv", newline="", encoding="utf-8") as f:  
    reader = csv.DictReader(f, delimiter=";")                         
    for row in reader:                                                 
        name = row["country_common_name"].strip()                       
        if name in countries:                                      
            iso2_set.add(row["iso2"].strip().upper())                  

countries = sorted(iso2_set)                               
indicator = "SE.XPD.TOTL.GD.ZS"          #indentificador del indicador de gasto público en educación (% PIB)

rows = []                                               

for iso2 in countries:                   #recorre países de la lista iso2 anterior
    url = (f"https://api.worldbank.org/v2/country/{iso2}/indicator/{indicator}"
           f"?format=json&mrv=10")       #pide los últimos 10 registros

    value = ""                           #por defecto está vacío (si no hay dato)

    try:
        r = requests.get(url, timeout=30)                 
        r.raise_for_status()                              
        json_data = r.json()                             
    except Exception:
        rows.append([iso2, value])        #si falla, deja value vacío y pasa al siguiente país
        continue                                          

    try:
        for rec in json_data[1]:                             
            if rec.get("value") is not None:   
                value = rec.get("value")                     
                break                                        
    except (TypeError, IndexError):
        value = ""                         #si json_data no tiene el formato esperado, queda vacío

    rows.append([iso2, value])                               

with open("worldbank.csv", "w", newline="", encoding="utf-8") as f:  
    w = csv.writer(f, delimiter=";")                     
    w.writerow(["iso2", "value"])                         
    w.writerows(rows)                                    
