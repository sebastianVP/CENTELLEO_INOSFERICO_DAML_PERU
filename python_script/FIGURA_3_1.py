import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from wmm2020 import wmm
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec

# ------------------------------------------------------------
# 1. Grilla ajustada al Perú continental
# ------------------------------------------------------------
lons = np.linspace(-81.8, -68.0, 150)
lats = np.linspace(-18.8, 0.8, 150)
lon_grid, lat_grid = np.meshgrid(lons, lats)

# ------------------------------------------------------------
# 2. Calcular inclinación magnética (Modelo WMM)
# ------------------------------------------------------------
inclination = np.zeros_like(lat_grid)
for i in range(lat_grid.shape[0]):
    for j in range(lat_grid.shape[1]):
        B = wmm(lat_grid[i, j], lon_grid[i, j], 0.100, 2025.0)
        inclination[i, j] = B['incl']

# ------------------------------------------------------------
# 3. Estaciones con clasificación regional y altitud aprox.
# ------------------------------------------------------------
estaciones = {
    "PIURA":         (-5.1945,  -80.6328, "Costa",  29,    "Piura"),
    "PUCP":          (-12.0682, -77.0803, "Costa",  156,   "PUCP"),
    "SAN_BARTOLOME": (-11.8714, -76.7295, "Costa",  600,   "San Bartolomé"),
    "TACNA":         (-18.0066, -70.2463, "Costa",  475,   "Tacna"),
    "JICAMARCA":     (-11.9500, -76.8700, "Sierra", 510,   "Jicamarca"),
    "JAEN":          (-5.7082,  -78.8024, "Sierra", 739,   "Jaén"),
    "HUANCAYO":      (-12.0650, -75.2049, "Sierra", 3259,  "Huancayo"),
    "CUZCO":         (-13.5320, -71.9675, "Sierra", 3400,  "Cusco"),
    "AYACUCHO":      (-13.1631, -74.2236, "Sierra", 2761,  "Ayacucho"),
    "PUCALLPA":      (-8.3791,  -74.5539, "Selva",  154,   "Pucallpa"),
    "IQUITOS":       (-3.7437,  -73.2516, "Selva",  104,   "Iquitos"),
}

estaciones_modelo = {"PIURA", "JICAMARCA", "HUANCAYO", "CUZCO"}

colores_region = {
    "Costa": "#2196F3",   # Azul
    "Sierra": "#4CAF50",  # Verde
    "Selva":  "#FF9800",  # Naranja
}

# ------------------------------------------------------------
# 4. FIGURA COMPACTA (FUERZA LETRAS GRANDES EN HOJA A4)
# ------------------------------------------------------------
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['text.color'] = '#000000'

fig = plt.figure(figsize=(6.5, 5.8), facecolor='#F8F9FA')

# GridSpec balanceado para optimizar el área del mapa en la hoja
gs = GridSpec(1, 2, figure=fig, width_ratios=[2.5, 1.0], wspace=0.04)

ax = fig.add_subplot(gs[0], projection=ccrs.PlateCarree())
ax_info = fig.add_subplot(gs[1])
ax_info.axis('off')

ax.set_extent([-81.8, -68.0, -18.8, 0.8])
ax.set_facecolor('#D6EAF8') 

# ------------------------------------------------------------
# 5. Capas geográficas
# ------------------------------------------------------------
land = cfeature.NaturalEarthFeature('physical', 'land', '10m', facecolor='#F5F5DC', edgecolor='none')
ax.add_feature(land, zorder=1)

ax.add_feature(cfeature.RIVERS.with_scale('10m'), linewidth=0.4, alpha=0.5, edgecolor='#5DADE2', zorder=2)
ax.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.6, edgecolor='#2C3E50', zorder=3)
ax.add_feature(cfeature.BORDERS.with_scale('10m'), linestyle='-', linewidth=1.0, edgecolor='#7F8C8D', zorder=3)

try:
    states_shp = shpreader.natural_earth(resolution='10m', category='cultural', name='admin_1_states_provinces')
    states = cfeature.ShapelyFeature([geom for geom in shpreader.Reader(states_shp).geometries()],
                                     ccrs.PlateCarree(), facecolor='none', edgecolor='#95A5A6', linewidth=0.5, linestyle=':')
    ax.add_feature(states, zorder=4)
except Exception as e:
    print(f"Advertencia límites: {e}")

# ------------------------------------------------------------
# 6. Fondo de inclinación magnética
# ------------------------------------------------------------
cf = ax.contourf(lon_grid, lat_grid, inclination, levels=np.arange(-30, 15, 2.5), cmap='RdYlBu_r', alpha=0.15, zorder=2)

cs = ax.contour(lon_grid, lat_grid, inclination, levels=np.arange(-25, 15, 5), colors='#78909C', linewidths=0.3, alpha=0.5, zorder=3)
ax.clabel(cs, fmt='%d°', fontsize=5.5, inline=True, colors='#37474F')

# Ecuador Magnético (Línea robusta y visible)
ax.contour(lon_grid, lat_grid, inclination, levels=[0], colors='#1A237E', linewidths=1.8, linestyles='--', zorder=5)

# ------------------------------------------------------------
# 7. Dibujar estaciones con fuentes GRANDES
# ------------------------------------------------------------
offsets = {
    "PIURA":         (0.3,   0.3,  'left'),
    "PUCP":          (-0.4, -0.6,  'right'),
    "SAN_BARTOLOME": (-0.4,  0.55, 'right'),
    "JICAMARCA":     (0.4,   0.45, 'left'),
    "TACNA":         (0.3,   0.35, 'left'),
    "HUANCAYO":      (0.3,  -0.55, 'left'),
    "CUZCO":         (0.3,  -0.4,  'left'),
    "AYACUCHO":      (-0.3,  0.35, 'right'),
    "JAEN":          (0.3,   0.3,  'left'),
    "PUCALLPA":      (0.3,   0.3,  'left'),
    "IQUITOS":       (0.3,   0.3,  'left'),
}

for nombre, (lat, lon, region, alt, display) in estaciones.items():
    color = colores_region[region]
    es_modelo = nombre in estaciones_modelo

    if es_modelo:
        ax.scatter(lon, lat, s=220, color='red', alpha=0.2, zorder=5)
        ax.scatter(lon, lat, s=70, color='red', edgecolor='#B71C1C', linewidth=1.2, marker='*', zorder=7)
    else:
        ax.scatter(lon, lat, s=40, color=color, edgecolor='white', linewidth=1.0, marker='o', zorder=6)

    dx, dy, ha = offsets.get(nombre, (0.3, 0.3, 'left'))

    # Letras de las estaciones en el mapa notablemente ampliadas (fontsize=6.8)
    txt = ax.text(lon + dx, lat + dy, f"{display}\n({alt} m)", fontsize=6.8,
                  weight='bold' if es_modelo else 'bold', ha=ha, va='center', color='#1A1A1A', zorder=8)
    txt.set_bbox(dict(facecolor='white', alpha=0.75, edgecolor='none', boxstyle='round,pad=0.12'))

# ------------------------------------------------------------
# 8. Etiquetas de países vecinos
# ------------------------------------------------------------
vecinos = {
    "COLOMBIA": (-0.5, -75.5),
    "ECUADOR":  (-1.8, -78.5),
    "BRASIL":   (-7.0, -70.5),
    "BOLIVIA":  (-16.5, -69.2),
    "CHILE":    (-18.3, -69.7),
}
for pais, (plat, plon) in vecinos.items():
    if -81.8 < plon < -68.0 and -18.8 < plat < 0.8:
        ax.text(plon, plat, pais, fontsize=6.8, color='#546E7A', style='italic', ha='center', weight='bold', zorder=3)

# ------------------------------------------------------------
# 9. Ticks de meridianos y paralelos legibles
# ------------------------------------------------------------
gl = ax.gridlines(draw_labels=True, linewidth=0.4, color='gray', alpha=0.3, linestyle='--')
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 6.8, 'weight': 'bold'}
gl.ylabel_style = {'size': 6.8, 'weight': 'bold'}

# ------------------------------------------------------------
# 10. Leyenda principal compacta pero con fuentes GRANDES
# ------------------------------------------------------------
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colores_region["Costa"], markeredgecolor='white', markersize=7, label='Costa'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colores_region["Sierra"], markeredgecolor='white', markersize=7, label='Sierra'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colores_region["Selva"], markeredgecolor='white', markersize=7, label='Selva'),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='red', markeredgecolor='#B71C1C', markersize=10, label='Estación S4'),
    Line2D([0], [0], color='#1A237E', lw=1.8, linestyle='--', label='Ecuador Magnético'),
]

leg = ax.legend(handles=legend_elements, loc='lower left', fontsize=6.2, framealpha=0.95, edgecolor='#90A4AE', fancybox=True)

# ------------------------------------------------------------
# 11. Panel lateral de información optimizado para A4
# ------------------------------------------------------------
ax_info.set_xlim(0, 1)
ax_info.set_ylim(0, 1)

ax_info.text(0.5, 0.98, "Red LISN–IGP", ha='center', va='top', fontsize=9.5, weight='bold', color='#1A237E')
ax_info.text(0.5, 0.94, "Estaciones GNSS Activas", ha='center', va='top', fontsize=7.2, color='#37474F')
ax_info.axhline(0.92, color='#90A4AE', linewidth=0.6)

# Tabla de estaciones con textos claros y escalados
headers = ["Estación", "Región", "Alt (m)"]
col_x = [0.02, 0.52, 0.80]
y_start = 0.89

ax_info.text(col_x[0], y_start, headers[0], fontsize=7.0, weight='bold', va='top', color='#263238')
ax_info.text(col_x[1], y_start, headers[1], fontsize=7.0, weight='bold', va='top', color='#263238')
ax_info.text(col_x[2], y_start, headers[2], fontsize=7.0, weight='bold', va='top', color='#263238')
ax_info.axhline(y_start - 0.015, color='#CFD8DC', linewidth=0.5)

y = y_start - 0.035
for nombre, (lat, lon, region, alt, display) in estaciones.items():
    es_modelo = nombre in estaciones_modelo
    color_txt = 'red' if es_modelo else '#263238'
    weight_txt = 'bold'
    marker = "★ " if es_modelo else "  "

    ax_info.text(col_x[0], y, f"{marker}{display}", fontsize=6.2, va='top', color=color_txt, weight=weight_txt)
    ax_info.text(col_x[1], y, region, fontsize=6.2, va='top', color=colores_region[region], weight='bold')
    ax_info.text(col_x[2], y, f"{alt:,}", fontsize=6.2, va='top', color='#37474F')
    ax_info.axhline(y - 0.012, color='#ECEFF1', linewidth=0.3)
    y -= 0.052

# Resumen estadístico
ax_info.axhline(y - 0.005, color='#90A4AE', linewidth=0.6)
y -= 0.04

n_total = len(estaciones)
n_costa  = sum(1 for v in estaciones.values() if v[2] == "Costa")
n_sierra = sum(1 for v in estaciones.values() if v[2] == "Sierra")
n_selva  = sum(1 for v in estaciones.values() if v[2] == "Selva")

ax_info.text(0.5, y, "Resumen Regional", ha='center', fontsize=7.2, weight='bold', va='top', color='#1A237E')
y -= 0.035
resumen = [
    (f"Total estaciones: {n_total}", '#263238'),
    (f"Costa: {n_costa} | Sierra: {n_sierra} | Selva: {n_selva}", '#37474F'),
    (f"Modelo S4 Activo: {len(estaciones_modelo)}", 'red'),
]
for txt, col in resumen:
    ax_info.text(0.05, y, txt, fontsize=6.5, va='top', color=col, weight='bold')
    y -= 0.032

# Nota científica al pie del panel
ax_info.axhline(y - 0.005, color='#90A4AE', linewidth=0.6)
y -= 0.035
ax_info.text(0.5, y, "Referencia Geomagnética", ha='center', fontsize=7.0, weight='bold', va='top', color='#B71C1C')
y -= 0.032
nota = ("Ecuador Magnético\ncalculado mediante\nWMM2020 a altitud\nde 100 km (época 2025.0).\n\n"
        "★ Representa nodos con\nmodelo predictivo local.")
ax_info.text(0.5, y, nota, ha='center', fontsize=5.8, va='top', color='#37474F', linespacing=1.3)

# ------------------------------------------------------------
# 12. Título principal e impresión síncrona
# ------------------------------------------------------------
fig.suptitle("Distribución Espacial de la Red LISN–IGP y Nodos del Modelo $S_4$", 
             fontsize=10.0, weight='bold', color='#1A237E', y=0.97)

# Nota marginal inferior
fig.text(0.5, 0.01, "Proyección: Plate Carree | Datos: LISN-IGP / Natural Earth | Coordenadas: WGS84",
         ha='center', fontsize=5.8, color='#78909C', style='italic', weight='bold')

plt.savefig("Mapa_LISN_IGP_Mejorado.png", dpi=300, bbox_inches='tight', pad_inches=0.02, facecolor=fig.get_facecolor())
print("✓ Mapa de alta visibilidad para formato A4 exportado con éxito.")
plt.show()