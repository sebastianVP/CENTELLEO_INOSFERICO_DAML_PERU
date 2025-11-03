import os
import re
import shutil

# === Configuración base ===
# Directorio donde están los archivos
BASE_DIR = os.getcwd()  # o reemplázalo por una ruta absoluta

# Expresión regular para extraer información
patron = re.compile(
    r"cintilacion_(?P<estacion>[A-Z]+)_(?P<dia>\d{2})_(?P<mes>[A-Za-z]+)_(?P<anio>\d{4})\.png"
)

# Traducción de meses inglés → español
meses_traduccion = {
    "December": "DICIEMBRE",
    "January": "ENERO",
    "February": "FEBRERO",
    "March": "MARZO",
    "April": "ABRIL",
    "May": "MAYO",
    "June": "JUNIO",
    "July": "JULIO",
    "August": "AGOSTO",
    "September": "SETIEMBRE",
    "October": "OCTUBRE",
    "November": "NOVIEMBRE"
}

# === Procesar archivos ===
for archivo in os.listdir(BASE_DIR):
    if archivo.lower().endswith(".png"):
        match = patron.match(archivo)
        if match:
            estacion = match.group("estacion")
            mes = match.group("mes")
            anio = match.group("anio")
            
            # Convertir mes al formato español y mayúsculas
            mes_es = meses_traduccion.get(mes, mes.upper())
            
            # Carpeta destino: e.g. HUANCAYO/FEBRERO_2025
            carpeta_destino = os.path.join(BASE_DIR, estacion, f"{mes_es}_{anio}")
            os.makedirs(carpeta_destino, exist_ok=True)
            
            # Mover archivo
            origen = os.path.join(BASE_DIR, archivo)
            destino = os.path.join(carpeta_destino, archivo)
            shutil.move(origen, destino)
            print(f"✅ {archivo} → {carpeta_destino}")

print("\nOrganización completada correctamente 🚀")
