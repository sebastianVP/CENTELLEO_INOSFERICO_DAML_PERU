import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# ------------------------------------------------------------
# 1. Configuración Estilo IEEE (Fuentes Grandes y Nítidas)
# ------------------------------------------------------------
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['font.weight'] = 'bold'

# Dimensiones del lienzo más ajustadas
fig, ax = plt.subplots(figsize=(13.5, 4.2), facecolor='#FFFFFF')
ax.set_xlim(0, 13.5)
ax.set_ylim(2.0, 6.2) # Límites verticales estrictos para eliminar espacios en blanco
ax.axis('off')

# ------------------------------------------------------------
# 2. Funciones de Dibujo Ajustadas
# ------------------------------------------------------------
def draw_card(x, y, w, h, bg_color, border_color, title="", title_color="#000000"):
    shadow = FancyBboxPatch((x + 0.04, y - 0.04), w, h, boxstyle="round,pad=0.10", 
                            fc='#EAEDED', ec='none', zorder=1)
    ax.add_patch(shadow)
    
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.10", 
                         fc=bg_color, ec=border_color, lw=1.8, zorder=2)
    ax.add_patch(box)
    
    if title:
        ax.text(x + w/2, y + h - 0.30, title, ha='center', va='center', 
                fontsize=11.5, weight='bold', color=title_color, zorder=3)

def draw_badge_arrow(x1, y1, x2, y2, tensor_str):
    arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='->', 
                            mutation_scale=16, color='#34495E', lw=2.0, zorder=4)
    ax.add_patch(arrow)
    
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    txt = ax.text(mid_x, mid_y + 0.32, tensor_str, fontsize=9.5, weight='bold', 
                  ha='center', va='center', color='#1A252C', zorder=6)
    txt.set_bbox(dict(facecolor='#FFFFFF', alpha=1.0, edgecolor='#90A4AE', 
                      boxstyle='round,pad=0.25'))

# ------------------------------------------------------------
# 3. CONSTRUCCIÓN DE LA ARQUITECTURA (Cajas más grandes y centradas)
# ------------------------------------------------------------

# --- 1. ENTRADA ---
draw_card(0.2, 2.2, 2.1, 3.8, "#EBF5FB", "#2980B9", "ENTRADA", "#1B4F72")
ax.text(1.25, 4.9, "Tensor $X_t$", ha='center', va='center', fontsize=12.5, weight='bold', color='#1B4F72')
ax.text(1.25, 3.55, "• Ventana: 70 min\n• Features ($F$)\n• Batch ($B = 64$)\n─────────────\nHistorial Ionosférico", 
        ha='center', va='center', fontsize=9.5, color='#283747', linespacing=1.35, zorder=3)

draw_badge_arrow(2.35, 4.1, 3.05, 4.1, r"$\mathbf{R}^{B \times 70 \times F}$")

# --- 2. CAPA RECURRENTE 1 ---
draw_card(3.1, 2.2, 2.4, 3.8, "#E8F8F5", "#117A65", "LSTM LAYER 1", "#0E6251")
ax.text(4.3, 4.9, "128 Neuronas", ha='center', va='center', fontsize=12.0, weight='bold', color='#0E6251')
ax.text(4.3, 3.55, "return_sequences = True\n─────────────\n+ Batch Norm\n+ Dropout (0.2)\n─────────────\nPatrones locales", 
        ha='center', va='center', fontsize=9.2, color='#145A32', linespacing=1.35, zorder=3)

draw_badge_arrow(5.55, 4.1, 6.25, 4.1, r"$\mathbf{R}^{B \times 70 \times 128}$")

# --- 3. CAPA RECURRENTE 2 ---
draw_card(6.3, 2.2, 2.4, 3.8, "#FEF9E7", "#D4AC0D", "LSTM LAYER 2", "#7D6608")
ax.text(7.5, 4.9, "64 Neuronas", ha='center', va='center', fontsize=12.0, weight='bold', color='#7D6608')
ax.text(7.5, 3.55, "return_sequences = False\n─────────────\n+ Batch Norm\n+ Dropout (0.2)\n─────────────\nResumen de estado", 
        ha='center', va='center', fontsize=9.2, color='#7D6608', linespacing=1.35, zorder=3)

draw_badge_arrow(8.75, 4.1, 9.45, 4.1, r"$\mathbf{R}^{B \times 64}$")

# --- 4. DECODER ---
draw_card(9.5, 2.2, 2.1, 3.8, "#F4ECF7", "#8E44AD", "DECODER", "#4A235A")
ax.text(10.55, 4.85, "Dense (128)", ha='center', va='center', fontsize=10.5, weight='bold', color='#4A235A')
ax.text(10.55, 4.25, "Act: ReLU\nDropout (0.2)", ha='center', va='center', fontsize=9.0, color='#5B2C6F')
ax.text(10.55, 3.15, "Dense (10)", ha='center', va='center', fontsize=10.5, weight='bold', color='#4A235A')
ax.text(10.55, 2.65, "Act: Linear", ha='center', va='center', fontsize=9.0, color='#5B2C6F')

draw_badge_arrow(11.65, 4.1, 12.15, 4.1, r"$\mathbf{R}^{B \times 10}$")

# --- 5. SALIDA / PRONÓSTICO ---
draw_card(12.2, 2.2, 1.1, 3.8, "#FDEDEC", "#CB4335", "SALIDA", "#78281F")
ax.text(12.75, 4.75, r"$\hat{Y}_t$", ha='center', va='center', fontsize=13.0, weight='bold', color='#78281F')
ax.text(12.75, 3.5, "Forecast\nMulti-paso\n─────────\n+1 a +10\nminutos\n($S_4$)", 
        ha='center', va='center', fontsize=8.8, color='#922B21', linespacing=1.3, zorder=3)

# Guardar figura ultra-ajustada sin bordes blancos excesivos
plt.savefig("Figura2_Arquitectura_Stacked_LSTM_Optimizado.png", dpi=300, bbox_inches='tight', pad_inches=0.01, facecolor='#FFFFFF')
plt.show()