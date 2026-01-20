## USO DE LA LIBRERIA CKAN PARA EXTRAER BLOQUES DE DATOS##
# pip install -e git+http://intranet.igp.gob.pe:8082/DATABASES/ckanext-jro/api-cliente#egg=jrodb
# NEW LINK DE LISN - https://lisn.igp.gob.pe/database 
# PROBAR EL LINK Y VERIFICAR
from src.jrodb.jrodb import Api

# USAR SERVIDOR PEDIR A GOMERO SI ESTOY DESDE EL ROJ . 
import sys
import os
from jrodb import Api

#print("Test de la libreria")
#print(Api.download.__doc__)
#from jrodb import Api
#DESCARGAMOS EL CONJUNTO DE DATOS
#years   = ["2020","2023","2024","2025"]
years   = ["2025"]
months  = ["january","february","march","april","may","june",
           "july","august","september","october","november","december"]

# JICAMARCA  jic
# HUANCAYO   hyo

# ESTACION S4 ENCONTRADAS DESPUES DE REVISION S4 EN LISN
# CUZCO,JAEN,JICAMARCA,PIURA,HUANCAYO,SAN_BARTOLOME,PUCP,PUCALLPA
# station="puc" # "tac" "cuz" "puc" "piu" "hyo" "jic"
# DIR    ="PUCALLPA" #"TACNA" "CUZCO" "PUCALLPA" "PIURA" "HUANCAYO" "JICAMARCA"

stations = ["cuz","jae","jic","piu","hyo","sbr","ucp","puc","tac","aya","iqu"]
DIRS     = ["CUZCO","JAEN","JICAMARCA","PIURA","HUANCAYO","SAN_BARTOLOME","PUCP","PUCALLPA","TACNA","AYACUCHO","IQUITOS"]
stations = ["jic"]
DIRS     = ["JICAMARCA"]
"""
stations = ["piu"]
DIRS     = ["PIURA"]
stations = ["hyo"]
DIRS     = ["HUANCAYO"]
stations = ["cuz"]
DIRS     = ["CUZCO"]
stations = ["puc"]
DIRS     = ["PUCALLPA"]
stations = ["tac"]
DIRS     = ["TACNA"]
stations = ["aya"]
DIRS     = ["AYACUCHO"]
stations = ["iqu"]
DIRS     = ["IQUITOS"]
"""
#---------------------------------------------------
# NO ENCUENTRO PARAMETRO S4,TACNA, PUERTO MALDONADO
#---------------------------------------------------
for station, DIR in zip(stations,DIRS):
    for year in years:
        for month in months:
            print("--------------------------------------------------------")
            print(f"Descargando el mes {month}/{year}...| STATION: {station} | DIR : {DIR}")
            print("--------------------------------------------------------")
            # Definimos la ruta donde se guardaran los datos
            path=f"/home/soporte/Documents/CENTELLEO_INOSFERICO_DAML_PERU/data/{DIR}"
            # Crea el directorio si no existe
            os.makedirs(path,exist_ok=True)
            # Accede a la API y descarga de los datos
            with Api("https://lisn.igp.gob.pe/database") as access:
                id = f"{year}_{month}_scint_data_l{station}"
                print(access.download(id=id,path=path))

# LUEGO DESCOMPRIMIMOS CON EL COMANDO
# gzip -d *
