import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from wmm2020 import wmm
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec

# ------------------------------------------------------------
# 1. Configuración de Lienzo IEEE
# ------------------------------------------------------------
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['font.weight'] = 'bold'

fig = plt.figure(figsize=(12.0, 6.2), facecolor='#FFFFFF')

# wspace = 0.005 para eliminar prácticamente toda la franja blanca central
gs = GridSpec(1, 2, figure=fig, width_ratios=[1.0, 1.15], wspace=0.005)

ax_map = fig.add_subplot(gs[0], projection=ccrs.PlateCarree())
ax_pipe = fig.add_subplot(gs[1])
ax_pipe.axis('off')

fig.subplots_adjust(left=0.03, right=0.98, top=0.97, bottom=0.05)

# ------------------------------------------------------------
# 2. PANEL A: Mapa Geofísico (Texto Aumentado)
# ------------------------------------------------------------
lons = np.linspace(-81.8, -68.0, 100)
lats = np.linspace(-18.8, 0.8, 100)
lon_grid, lat_grid = np.meshgrid(lons, lats)

inclination = np.zeros_like(lat_grid)
for i in range(lat_grid.shape[0]):
    for j in range(lat_grid.shape[1]):
        B = wmm(lat_grid[i, j], lon_grid[i, j], 0.100, 2025.0)
        inclination[i, j] = B['incl']

ax_map.set_extent([-81.8, -68.0, -18.8, 0.8])
ax_map.set_facecolor('#EBF5FB')

# Capas base
land = cfeature.NaturalEarthFeature('physical', 'land', '10m', facecolor='#F5F5DC', edgecolor='none')
ax_map.add_feature(land, zorder=1)
ax_map.add_feature(cfeature.RIVERS.with_scale('10m'), linewidth=0.4, alpha=0.5, edgecolor='#5DADE2', zorder=2)
ax_map.add_feature(cfeature.COASTLINE.with_scale('10m'), linewidth=0.6, edgecolor='#2C3E50', zorder=3)
ax_map.add_feature(cfeature.BORDERS.with_scale('10m'), linestyle='-', linewidth=0.8, edgecolor='#34495E', zorder=3)

try:
    states_shp = shpreader.natural_earth(resolution='10m', category='cultural', name='admin_1_states_provinces')
    states = cfeature.ShapelyFeature([geom for geom in shpreader.Reader(states_shp).geometries()],
                                     ccrs.PlateCarree(), facecolor='none', edgecolor='#B0BEC5', linewidth=0.5, linestyle=':')
    ax_map.add_feature(states, zorder=4)
except Exception:
    pass

# Ecuador Magnético
ax_map.contour(lon_grid, lat_grid, inclination, levels=[0], colors='#1A237E', linewidths=2.0, linestyles='--', zorder=5)

# Estaciones
estaciones = {
    "PIURA":         (-5.1945,  -80.6328, "Piura",        (0.35,  0.20, 'left')),
    "JAEN":          (-5.7082,  -78.8024, "Jaén",         (0.35,  0.15, 'left')),
    "IQUITOS":       (-3.7437,  -73.2516, "Iquitos",      (0.35,  0.15, 'left')),
    "PUCALLPA":      (-8.3791,  -74.5539, "Pucallpa",     (0.35,  0.15, 'left')),
    "PUCP":          (-12.0682, -77.0803, "PUCP",         (-0.35, -0.65, 'right')),
    "SAN_BARTOLOME": (-11.8714, -76.7295, "S. Bartolomé", (-0.35,  0.50, 'right')),
    "JICAMARCA":     (-11.9500, -76.8700, "Jicamarca",    (0.40,  0.55, 'left')),
    "HUANCAYO":      (-12.0650, -75.2049, "Huancayo",     (0.40,  0.00, 'left')),
    "AYACUCHO":      (-13.1631, -74.2236, "Ayacucho",     (0.40, -0.55, 'left')),
    "CUZCO":         (-13.5320, -71.9675, "Cusco",        (0.40, -0.20, 'left')),
    "TACNA":         (-18.0066, -70.2463, "Tacna",        (-0.35, 0.35, 'right')),
}
estaciones_modelo = {"PIURA", "JICAMARCA", "HUANCAYO", "CUZCO"}

for key, (lat, lon, display, offset) in estaciones.items():
    es_modelo = key in estaciones_modelo
    dx, dy, ha = offset
    
    if es_modelo:
        ax_map.scatter(lon, lat, s=130, color='#D32F2F', edgecolor='black', linewidth=1.0, marker='*', zorder=7)
    else:
        ax_map.scatter(lon, lat, s=50, color='#1976D2', edgecolor='white', linewidth=0.8, marker='o', zorder=6)
    
    txt = ax_map.text(lon + dx, lat + dy, display, fontsize=9.0, weight='bold',
                      ha=ha, va='center', color='#000000', zorder=8)
    txt.set_bbox(dict(facecolor='#FFFFFF', alpha=0.85, edgecolor='none', boxstyle='round,pad=0.10'))

# Países vecinos
vecinos = {
    "COLOMBIA": (-0.4, -75.0),
    "ECUADOR":  (-1.6, -78.8),
    "BRASIL":   (-7.0, -70.2),
    "BOLIVIA":  (-15.8, -69.0),
    "CHILE":    (-18.5, -68.8),
}
for pais, (plat, plon) in vecinos.items():
    ax_map.text(plon, plat, pais, fontsize=9.0, color='#607D8B', style='italic', ha='center', weight='bold', zorder=4)

gl = ax_map.gridlines(draw_labels=True, linewidth=0.4, color='gray', alpha=0.3, linestyle='--')
gl.top_labels = False
gl.right_labels = False
gl.xlabel_style = {'size': 9.0, 'weight': 'bold'}
gl.ylabel_style = {'size': 9.0, 'weight': 'bold'}

legend_elements = [
    Line2D([0], [0], marker='*', color='w', markerfacecolor='#D32F2F', markeredgecolor='black', markersize=12, label='Nodo Modelo S₄'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#1976D2', markeredgecolor='white', markersize=8.5, label='Estación LISN/IGP'),
    Line2D([0], [0], color='#1A237E', lw=2.0, linestyle='--', label='Ecuador Magnético'),
]
ax_map.legend(handles=legend_elements, loc='lower left', fontsize=8.5, framealpha=0.92, edgecolor='#B0BEC5', fancybox=True)

# ------------------------------------------------------------
# 3. PANEL B: Pipeline Optimizado y Letra Aún Más Grande
# ------------------------------------------------------------
ax_pipe.set_xlim(0, 10)
ax_pipe.set_ylim(0, 10)

def draw_box(ax, x, y, w, h, color_bg, color_border):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12", 
                         fc=color_bg, ec=color_border, lw=1.4, zorder=2)
    ax.add_patch(box)

# CAJA 1: DATOS LOCALES
draw_box(ax_pipe, 0.1, 7.3, 4.6, 2.4, "#E3F2FD", "#1976D2")
ax_pipe.text(2.4, 9.2, "Observaciones Locales", ha='center', va='center', fontsize=11.5, weight='bold', color='#0D47A1')
ax_pipe.text(2.4, 8.2, "• Red LISN y ROJ\n• Parámetros: S₄, TEC, ROTI\n• Cadencia: 1 min", 
             ha='center', va='center', fontsize=10.0, color='#1A237E', linespacing=1.4)

# CAJA 2: DATOS GLOBALES
draw_box(ax_pipe, 5.3, 7.3, 4.6, 2.4, "#FFF3E0", "#F57C00")
ax_pipe.text(7.6, 9.2, "Parámetros Globales", ha='center', va='center', fontsize=11.5, weight='bold', color='#E65100')
ax_pipe.text(7.6, 8.2, "• OMNIWeb & SWPC\n• Geomagnetismo: Kp, Dst, AE\n• Actividad Solar: F10.7", 
             ha='center', va='center', fontsize=10.0, color='#E65100', linespacing=1.4)

# Flechas Entradas -> ETL
arrow1 = FancyArrowPatch((2.4, 7.2), (3.6, 6.4), connectionstyle="arc3,rad=-0.08",
                         arrowstyle='->', mutation_scale=15, color='#1976D2', lw=1.8)
arrow2 = FancyArrowPatch((7.6, 7.2), (6.4, 6.4), connectionstyle="arc3,rad=0.08",
                         arrowstyle='->', mutation_scale=15, color='#F57C00', lw=1.8)
ax_pipe.add_patch(arrow1)
ax_pipe.add_patch(arrow2)

# CAJA 3: ETL & PREPROCESAMIENTO (Más estrecha: x=0.5, ancho=9.0, completamente centrada)
draw_box(ax_pipe, 0.5, 2.1, 9.0, 4.2, "#F4F6F7", "#34495E")
ax_pipe.text(5.0, 5.85, "ETL & Preprocesamiento", ha='center', va='center', fontsize=12.5, weight='bold', color='#2C3E50')

pasos_titulos = [
    "1. Filtro de Elevación:",
    "2. Limpieza de Datos:",
    "3. Agregación Crítica:",
    "4. Codificación Temporal:"
]
pasos_formulas = [
    r"Ángulo $\theta \geq 30^\circ$ (Filtro de ruido/multipath)",
    r"Eliminación de saltos e interpolación en brechas > 5 min",
    r"$S_{4,\mathrm{global}}(t) = \max_{s} S_{4,s}(t)$ (Peor escenario)",
    r"Seno/Coseno: $\sin(2\pi t / 1440)$, $\cos(2\pi t / 1440)$"
]

y_base = 5.25
for i in range(4):
    y_t = y_base - (i * 0.85)
    y_f = y_t - 0.28
    ax_pipe.text(0.8, y_t, pasos_titulos[i], fontsize=10.5, weight='bold', color='#1A252C', va='center')
    ax_pipe.text(0.8, y_f, pasos_formulas[i], fontsize=10.0, color='#2C3E50', va='center')

# Flecha Salida ETL -> Tensor
arrow3 = FancyArrowPatch((5.0, 2.05), (5.0, 1.65), arrowstyle='->', mutation_scale=15, color='#2C3E50', lw=2.0)
ax_pipe.add_patch(arrow3)

# CAJA 4: TENSOR DE ENTRADA
draw_box(ax_pipe, 0.1, 0.2, 9.8, 1.4, "#E8F8F5", "#117A65")
ax_pipe.text(5.0, 1.15, "Tensor de Entrada Deep Learning", ha='center', va='center', fontsize=11.5, weight='bold', color='#0E6251')
ax_pipe.text(5.0, 0.55, r"Matriz $X_t \in \mathbf{R}^{70 \times F}$  |  Historial: 70 min  |  Predicción: 10 min", 
             ha='center', va='center', fontsize=10.2, color='#117A65')

# Guardar con márgenes ultra-ajustados
plt.savefig("Figura1_Pipeline_Ionostera_Final.png", dpi=300, bbox_inches='tight', pad_inches=0.01, facecolor='#FFFFFF')
plt.show()