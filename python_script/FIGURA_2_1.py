import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# --- 1. CONFIGURACIÓN DE ALTA CALIDAD ---
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['text.color'] = 'black'

fig, ax = plt.subplots(figsize=(16, 9)) 
ax.set_facecolor('#FFFFFF') 
ax.axis('off')

# --- 2. DEFINICIÓN DE LÍMITES Y COORDENADAS ---
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)

# --- 3. PALETA DE COLORES ACADÉMICOS Y ESTILOS DE FUENTE ---
COLOR_BORDE = '#2C3E50'    
COLOR_PLASMA = '#AED6F1'   
COLOR_HIGH_DENS = '#E67E22' 
COLOR_LOW_DENS = '#21618C'  
COLOR_B_FIELD = '#34495E'  
COLOR_TEXTO_TITLE = 'black'

font_standard_bold = {'weight': 'bold', 'size': 14, 'color': COLOR_BORDE, 'family': 'sans-serif'}

# --- 4. DATOS Y DIBUJO GEOMÉTRICO ---
x_min_graph, x_max_graph = 1.0, 15.0
y_min_graph, y_max_graph = 1.0, 7.5
x_equator = 8.0 
y_ground = 1.5 

# --- 4a. SUPERFICIE TERRESTRE Y ALTITUDES ---
earth_arc = patches.Arc((x_equator, y_ground - 10.0), 12.0, 20.0, theta1=0, theta2=180,
                        linewidth=3.0, edgecolor='gray', zorder=5)
ax.add_patch(earth_arc)
ax.text(x_equator-1.75, y_ground + 0.1, "Superficie Terrestre (Perú)",
        ha='center', va='bottom', fontsize=14, fontweight='bold', color='gray')
ax.text(x_equator, y_ground - 0.2, "Ecuador Magnético (Lat. $0^\circ$)",
        ha='center', va='top', fontsize=13, fontweight='bold', color='gray')

ax.annotate('', xy=(x_min_graph, y_max_graph + 0.2), xytext=(x_min_graph, y_ground - 0.2),
            arrowprops=dict(arrowstyle="<->", color='black', lw=1.5, zorder=5))
ax.text(x_min_graph - 0.2, y_max_graph, "Altitud\n(km)", ha='right', va='center', **font_standard_bold)

alt_E = 100
alt_F_peak = 350
y_E = y_ground + (alt_E / 1000.0) * (y_max_graph - y_ground) 
y_F = y_ground + (alt_F_peak / 1000.0) * (y_max_graph - y_ground)

ax.text(x_min_graph - 0.1, y_E, f"Región E\n~{alt_E} km", ha='right', va='center', fontsize=12, fontweight='bold')
ax.text(x_min_graph - 0.1, y_F, f"Pico F2\n~{alt_F_peak} km", ha='right', va='center', fontsize=12, fontweight='bold')

ax.text(x_equator + 3.0, y_ground - 0.7, r"Latitud Magnética ($\lambda_{Mag}$)", ha='left', va='center', **font_standard_bold)
ax.text(x_min_graph + 1.0, y_ground - 0.3, r"$-30^\circ$S", ha='center', va='top', fontsize=13)
ax.text(x_max_graph - 1.0, y_ground - 0.3, r"$+30^\circ$N", ha='center', va='top', fontsize=13)

# --- 4b. FONDO DE PLASMA Y CRESTAS EIA ---
rect_plasma = patches.Rectangle((x_min_graph, y_ground), x_max_graph - x_min_graph, y_max_graph - y_ground,
                                facecolor=COLOR_PLASMA, alpha=0.6, zorder=1)
ax.add_patch(rect_plasma)

w_crest = 2.5
h_crest = 1.8
z_crests = 3

# Cresta Sur
ellipse_south = patches.Ellipse((x_equator - 3.5, y_F), w_crest, h_crest, angle=20,
                                facecolor=COLOR_HIGH_DENS, edgecolor='black', linewidth=1.0, alpha=0.85, zorder=z_crests)
ax.add_patch(ellipse_south)
ax.text(x_equator - 3.5, y_F, "Cresta EIA Sur\n" + r"($\sim 18^\circ$S Lat. Mag.)",
        ha='center', va='center', fontsize=14, fontweight='bold', color='black', zorder=z_crests+1,
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

# Cresta Norte
ellipse_north = patches.Ellipse((x_equator + 3.5, y_F), w_crest, h_crest, angle=-20,
                                facecolor=COLOR_HIGH_DENS, edgecolor='black', linewidth=1.0, alpha=0.85, zorder=z_crests)
ax.add_patch(ellipse_north)
ax.text(x_equator + 3.5, y_F, "Cresta EIA Norte\n" + r"($\sim 18^\circ$N Lat. Mag.)",
        ha='center', va='center', fontsize=14, fontweight='bold', color='black', zorder=z_crests+1,
        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', boxstyle='round,pad=0.2'))

# Valle Ecuatorial
ax.text(x_equator-1.35, y_ground + 1.75, "Valle Ecuatorial\n(Baja Densidad)",
        ha='center', va='center', fontsize=14, fontweight='bold', color=COLOR_LOW_DENS, zorder=z_crests+1)

# --- 4c. DIBUJO ELECTRODINÁMICO ---
def draw_magnetic_arc(ax, center_x, center_y, width, height, zorder=10):
    arc = patches.Arc((center_x, center_y), width, height, theta1=0, theta2=180,
                       linewidth=1.5, edgecolor=COLOR_B_FIELD, linestyle='-', zorder=zorder)
    ax.add_patch(arc)

mag_y_center = y_ground - 1.0 
draw_magnetic_arc(ax, x_equator, mag_y_center, 16.0, 12.0)
draw_magnetic_arc(ax, x_equator, mag_y_center, 12.0, 9.0)
draw_magnetic_arc(ax, x_equator, mag_y_center, 8.0, 6.0)

ax.text(x_equator, y_max_graph + 0.3, r"Líneas de Campo Magnético ($\mathbf{B}$)",
        ha='center', va='bottom', fontsize=16, fontweight='bold', color=COLOR_B_FIELD)

e_field_x, e_field_y = x_equator + 0.1, y_ground + 0.6
e_field_circle = patches.Circle((e_field_x, e_field_y), 0.2, linewidth=1.5, edgecolor='black', facecolor='white', zorder=15)
ax.add_patch(e_field_circle)
ax.text(e_field_x, e_field_y, r"$\mathbf{\cdot}$", ha='center', va='center', fontsize=18, fontweight='bold', color='black', zorder=16)
ax.text(e_field_x + 0.3, e_field_y, r"$\mathbf{E}$ (Este)", ha='left', va='center', fontsize=14, fontweight='bold', color='black', zorder=16)

# DERIVA E x B
ax.annotate('', xy=(x_equator, y_F - 0.2), xytext=(x_equator, y_ground + 0.1),
            arrowprops=dict(facecolor='black', edgecolor='none', width=12, headwidth=25, headlength=18, zorder=20))
ax.text(x_equator+1.25, y_F - 1.0, r"Deriva $\mathbf{E} \times \mathbf{B}$" + "\n(Efecto Fuente)",
        ha='center', va='center', fontsize=14, fontweight='bold', color='black', zorder=21,
        bbox=dict(facecolor='white', alpha=0.9, edgecolor='none', boxstyle='round,pad=0.2'))

# DIFUSIÓN POR GRAVEDAD
z_diff = 11
arrow_props_diff = dict(arrowstyle="->", color=COLOR_B_FIELD, lw=2.0, connectionstyle="arc3,rad=-0.15", zorder=z_diff)

ax.annotate("", xy=(x_max_graph - 2.0, y_E + 0.5), xytext=(x_equator + 1.5, y_F + 0.5), arrowprops=arrow_props_diff)
arrow_props_diff['connectionstyle'] = "arc3,rad=0.15"
ax.annotate("", xy=(x_min_graph + 2.0, y_E + 0.5), xytext=(x_equator - 1.5, y_F + 0.5), arrowprops=arrow_props_diff)

ax.text(x_equator, y_F + 0.8, "Difusión por Gravedad",
        ha='center', va='bottom', fontsize=14, fontweight='bold', color=COLOR_B_FIELD, zorder=z_diff+1)

# --- 5. EXPORTACIÓN ---
plt.tight_layout()

filename_base = 'Figura_2_1_Geofisica_EIA_EfectoFuente_Peru'
plt.savefig(filename_base + '.pdf', format='pdf', bbox_inches='tight')
plt.savefig(filename_base + '.png', format='png', bbox_inches='tight', dpi=300)

print(f"¡Imagen de la Figura 2.1 (sin encabezado/pie) generada con éxito! Archivos creados: {filename_base}.pdf, {filename_base}.png")