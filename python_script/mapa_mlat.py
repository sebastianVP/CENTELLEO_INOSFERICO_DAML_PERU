import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import aacgmv2
from datetime import datetime
"""
El modelo AACGM (Altitude Adjusted Corrected Geomagnetic) NO está definido globalmente.

👉 AACGM solo es válido en regiones aurorales y de latitudes medias–altas, típicamente:

✔ Latitudes geomagnéticas ≳ |30°–35°

❌ No funciona bien en latitudes bajas / ecuatoriales

📍 Lima (~12° S geográfica) está muy cerca del ecuador geomagnético, por eso:

mlat = NaN


No es que tu código esté mal.
Es una limitación física y matemática del modelo.

🌍 ¿Por qué AACGM falla cerca del ecuador?

AACGM:

Sigue líneas de campo magnético

Requiere que esas líneas intersecten una altitud de referencia

Cerca del ecuador:

Las líneas son casi horizontales

No intersectan correctamente

El algoritmo no converge

Resultado → NaN

👉 Esto está documentado oficialmente por los autores del modelo.

🧲 la inclinación magnética (dip angle) es 0°
Región	Latitud (°)	Longitud (°)
Pacífico oriental	~ +5°	−110°
Norte de Perú	~ +3° a +5°	−80°
Amazonía	~ 0° a +2°	−70°
"""
# =====================================================
# 1. COORDENADA DE ENTRADA
# =====================================================
lat_geo = -12.05   # Lima
lon_geo = -77.05
#lat_geo = +3  # NORTE DEL PERU
#long_geo = -80 
alt_km = 10.0 # aqui se pone la altura Lima es practicamente perpendicular
date = datetime(2026, 2, 10)

# =====================================================
# 2. FUNCIÓN: LATITUD GEOMAGNÉTICA (AACGM)
# =====================================================
def geomagnetic_latitude(lat, lon, alt_km, date):
    mlat, mlon, r = aacgmv2.get_aacgm_coord(
        lat, lon, alt_km, date
    )
    return mlat

# Cálculo puntual
mlat_point = geomagnetic_latitude(lat_geo, lon_geo, alt_km, date)

print("===================================")
print(f"Latitud geográfica : {lat_geo:.2f}°")
print(f"Longitud geográfica: {lon_geo:.2f}°")
print(f"Latitud geomagnética AACGM: {mlat_point:.2f}°")
print("===================================")

# =====================================================
# 3. MAPA GLOBAL DE LATITUD GEOMAGNÉTICA
# =====================================================
lats = np.linspace(-90, 90, 181)
lons = np.linspace(-180, 180, 361)
Lon, Lat = np.meshgrid(lons, lats)

mlat_map = np.zeros_like(Lat)

for i in range(Lat.shape[0]):
    for j in range(Lat.shape[1]):
        mlat_map[i, j] = geomagnetic_latitude(
            Lat[i, j], Lon[i, j], alt_km, date
        )
# =====================================================
# 4. GRÁFICA
# =====================================================
fig = plt.figure(figsize=(14, 7))
ax = plt.axes(projection=ccrs.PlateCarree())

# Mapa de latitud geomagnética
levels = np.arange(-90, 91, 10)
cs = ax.contourf(
    Lon, Lat, mlat_map,
    levels=levels,
    cmap="coolwarm",
    transform=ccrs.PlateCarree(),
    zorder=1
)

# Costas y fronteras
ax.coastlines(zorder=3)
ax.add_feature(cfeature.BORDERS, linewidth=0.5, zorder=3)

# ===== PUNTO GNSS (VISIBLE SIEMPRE) =====
ax.plot(
    lon_geo, lat_geo,
    marker="o",
    color="black",
    markersize=8,
    markeredgecolor="white",
    markeredgewidth=1.2,
    transform=ccrs.PlateCarree(),
    zorder=5,
    label=f"Lima GNSS\nAACGM @ {alt_km:.0f} km\nMLAT = {mlat_point:.2f}°"
)

# Leyenda
ax.legend(
    loc="lower left",
    frameon=True,
    facecolor="white",
    framealpha=0.9
)

# Barra de color
cbar = plt.colorbar(cs, orientation="horizontal", pad=0.05)
cbar.set_label("Latitud geomagnética AACGM (°)")

# Título
ax.set_title("Mapa global de latitud geomagnética (AACGM, 350 km)")

plt.show()
