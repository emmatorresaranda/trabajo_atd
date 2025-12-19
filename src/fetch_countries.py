from pathlib import Path                                              # Para manejar rutas de archivos de forma compatible (Windows/macOS/Linux)
import requests                                                       # Para hacer peticiones HTTP a la API (REST Countries)
import pandas as pd                                                   # Para crear una tabla (DataFrame) y exportarla a CSV

URL = "https://restcountries.com/v3.1/all?fields=cca2,cca3,name,region,subregion,population,area"  # URL de la API con solo campos necesarios a sacar (all para sacar todos los países, y ?fields=... para sacar solo esos campos)

def main():                                                           # Función principal: descarga datos, los limpia y genera el CSV
    out_path = Path("data/processed/countries.csv")                    # Define la ruta del CSV de salida dentro del proyecto
    out_path.parent.mkdir(parents=True, exist_ok=True)                 # Crea la carpeta data/processed si no existe

    r = requests.get(URL, timeout=30)                                  # Llama a la API (GET); timeout evita que se quede colgado
    r.raise_for_status()                                               # Si hay error HTTP (4xx/5xx), para el programa con excepción
    data = r.json()                                                    # Convierte la respuesta JSON en estructuras Python (lista/diccionarios)

    rows = []                                                          # Lista donde guardaremos cada país como una fila (diccionario)
    for item in data:                                                  # Recorre cada país devuelto por la API
        iso2 = item.get("cca2")                                        # Extrae ISO2 (clave de unión en el proyecto, ej. "ES")
        name = (item.get("name") or {}).get("common")                  # Extrae el nombre común; (or {}) evita errores si falta 'name'

        if not iso2 or not name:                                       # Si falta ISO2 o nombre, ese país no sirve para uniones -> lo saltamos
            continue                                                   # Pasa al siguiente país

        rows.append({                                                  # Añade una nueva fila con las columnas estándar del proyecto
            "iso2": iso2.upper(),                                      # ISO2 en mayúsculas para consistencia ("es" -> "ES")
            "iso3": item.get("cca3"),                                  # ISO3 (ej. "ESP"), útil como soporte
            "country_common_name": name,                               # Nombre común del país (texto)
            "region": item.get("region"),                              # Región (para segmentación/análisis)
            "subregion": item.get("subregion"),                        # Subregión (opcional pero útil)
            "population": item.get("population"),                      # Población (para métricas per cápita)
            "area_km2": item.get("area"),                              # Área en km² (variable contextual opcional)
        })                                                             # Cierra el diccionario y el append

    df = pd.DataFrame(rows).drop_duplicates(subset=["iso2"]).sort_values("iso2")  # Convierte filas a DataFrame, elimina duplicados y ordena
    df.to_csv(out_path, index=False)                                   # Exporta el DataFrame a CSV sin columna de índice extra

    print(f"OK: {len(df)} countries -> {out_path}")                    # Mensaje rápido para confirmar que se creó el CSV y cuántas filas tiene

if __name__ == "__main__":                                             # Garantiza que main() se ejecute solo si lanzas este archivo directamente
    main()                                                             # Ejecuta el flujo principal
