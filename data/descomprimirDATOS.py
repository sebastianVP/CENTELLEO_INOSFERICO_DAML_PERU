import os
import subprocess

def process_directories(input_directories):
    for input_directory in input_directories:
        print(f"Procesando directorio: {input_directory}")
        try:
            # Cambiar al directorio actual
            os.chdir(input_directory)

            # Ejecutar el comando gzip -d *
            print(f"Descomprimiendo archivos en {input_directory}...")
            subprocess.run(["gzip -d *"], shell=True, check=True)

            print(f"Archivos descomprimidos en {input_directory}")
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando en {input_directory}: {e}")
        except Exception as e:
            print("\n")
            print(f"Error al procesar el directorio {input_directory}: {e}")
            print("\n")



# Ruta del directorio de entrada y archivo de salida
# PATH BASE
PPATH="/home/soporte/Documents/CENTELLEO_INOSFERICO_DAML_PERU/data"
# DIRECTORIO DE ESTACIONES Y ABREVIATURA
DIRS=["CUZCO","JAEN","JICAMARCA","PIURA","HUANCAYO","SAN_BARTOLOME","PUCP","PUCALLPA","AYACUCHO","IQUITOS"]
stations=["cuz","jae","jic","piu","hyo","sbr","ucp","puc","aya","iqu"]

DIRS=["JICAMARCA"]
stations=["jic"]
"""
DIRS = ["PIURA"]
stations=["piu"]

DIRS = ["HUANCAYO"]
stations = ["hyo"]

DIRS = ["CUZCO"]
stations = ["cuz"]

DIRS = ["PUCALLPA"]
stations = ["puc"]

DIRS = ["TACNA"]
stations = ["tac"]

DIRS = ["AYACUCHO"]
stations = ["aya"]

DIRS = ["IQUITOS"]
stations = ["iqu"]
"""
# YEARS
# years= ["2020","2023","2024","2025"]
years= ["2025"]
# MESES
months = ["january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"]


# LISTA DE DIRECTORIOS DE ENTRADA PARA BUSCAR ARCHIVOS Y DESCOMPRIMIR LA DATA DE TODAS LAS ESTACIONES
input_directories= [
      os.path.join(os.path.join(PPATH,DIR),os.path.join(f"{year}_{month}_scint_data_l{station}", "data"))
      for station, DIR in zip(stations, DIRS)  
      for year in years
      for month in months
      ]


# Lista de directorios a procesar
print("Input_directories: ",input_directories)
process_directories(input_directories)
