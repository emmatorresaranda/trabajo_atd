from socket import *
import csv

data={}   
names = []
with open("final_dataset.csv", newline="", encoding="utf-8") as f:
    reader=csv.DictReader(f, delimiter=';') 
    for row in reader:
        iso=row['iso2'].upper()
        data[iso]=row
        name=row['country_common_name']
        names.append(f"{iso}: {name}")
names.sort()
names_str="\n".join(names)
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print("Servidor activo y esperando conexiones...")

while True:
    connectionSocket, addr = serverSocket.accept()
    connectionSocket.send(("Bienvenido. Este servidor guarda datos sobre los países que aparecen en el top 100"
                          " dentro del Ranking Académico de las Universidades del Mundo (ARWU)."
                          " Consulta información sobre población, área, educación y ranking universitario.\n"
                          f"Los países dentro del ranking que puedes explorar son:\n{names_str}").encode())
    while True:
        country_iso = connectionSocket.recv(1024).decode().upper()
        if country_iso =="EXIT":
            connectionSocket.send("Conexión cerrada.".encode())
            break
        elif country_iso in data:
            connectionSocket.send("¿Qué información quieres saber?\n1: Demografía\n2: Indicadores socioeconómicos\n3: Ranking de países".encode())
            option=connectionSocket.recv(1024).decode().upper() 
            if option=="EXIT":
                connectionSocket.send("Conexión cerrada".encode())
                break

            country=data[country_iso]
            response = f"Aquí tienes la información solicitada sobre \"{country['country_common_name']}\":\n"
            if option=="1":
                response += (f"Población: {country['population']} personas\n"
                            f"Área: {country['area_km2']} km2\nRegión: {country['region']}\nSubregión: {country['subregion']}")
                            
            elif option == "2":
                response += (f"Tasa de personas con educación terciaria: {country['tertiary_rate']}\nGasto en educación (% PIB): {round(float(country['edu_spend_pct_gdp']),2)}%")
            elif option == "3":
                response += (f"Nº de universidades del país en el top 100 ARWU: {country['arwu_top100_count']}\nPosición más alta en ARWU: top {country['arwu_best_rank']}")
            else:
                response = "Opción no válida."
            connectionSocket.send(response.encode())

        else:
            response = (
                "El país con el ISO introducido no se encuentra en el ranking.\n"
                "Vuelve a intentarlo."
            )
            connectionSocket.send(response.encode())
    connectionSocket.close()
