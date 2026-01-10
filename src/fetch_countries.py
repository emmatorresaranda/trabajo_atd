'''
obtener un csv con información de distintos países (nombre, habitantes, superficie...)
utilizando API Rest
'''                             
import csv                                                
import requests                                           

URL = "https://restcountries.com/v3.1/all?fields=cca2,cca3,name,region,subregion,population,area"  #URL de la API con solo campos necesarios a sacar (all para sacar todos los países, y ?fields=... para sacar solo esos campos)

r = requests.get(URL, timeout=30)                         
r.raise_for_status()                                      
data = r.json()                                          

countries_by_iso2 = {}                                    

for item in data:                                         
    iso2 = (item.get("cca2") or "").strip().upper()                #nombre ISO2 de cada país
    name = ((item.get("name") or {}).get("common") or "").strip()  #nombre común de cada país

    if not iso2 or not name:                              #si falta, se ignora
        continue                                          

    countries_by_iso2[iso2] = {                          
        "iso2": iso2,                                    
        "iso3": (item.get("cca3") or "").strip(),        
        "country_common_name": name,                      
        "region": (item.get("region") or "").strip(),     
        "subregion": (item.get("subregion") or "").strip(),  
        "population": item.get("population") or "",       
        "area_km2": item.get("area") or "",}          # "" significa que puede ser que sean valores faltantes

rows = [countries_by_iso2[k] for k in sorted(countries_by_iso2)]  

fields = ["iso2", "iso3", "country_common_name", "region", "subregion", "population", "area_km2"]  

with open("fetch_countries.csv", "w", newline="", encoding="utf-8") as f:  
    w = csv.DictWriter(f, fieldnames=fields, delimiter=";")        
    w.writeheader()                                                
    w.writerows(rows)                                              
