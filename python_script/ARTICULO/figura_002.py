import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, BoxStyle

# ------------------------------------------------------------
# 1. Configuración Estilo IEEE / Paper de Alto Impacto
# ------------------------------------------------------------
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['font.weight'] = 'bold'

fig, ax = plt.subplots(figsize=(14.0, 6.2), facecolor='#FFFFFF')
ax.set_xlim(0, 14)
ax.set_ylim(0, 8.5)
ax.axis('off')

# ------------------------------------------------------------
# 2. Funciones de Dibujo Avanzadas
# ------------------------------------------------------------
def draw_card(x, y, w, h, bg_color, border_color, title="", title_color="#000000"):
    """Dibuja una tarjeta con estilo moderno y encabezado."""
    # Sombra sutil tras la caja
    shadow = FancyBboxPatch((x + 0.05, y - 0.05), w, h, boxstyle="round,pad=0.15", 
                            fc='#EAEDED', ec='none', zorder=1)
    ax.add_patch(shadow)
    
    # Caja principal
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", 
                         fc=bg_color, ec=border_color, lw=1.8, zorder=2)
    ax.add_patch(box)
    
    if title:
        ax.text(x + w/2, y + h - 0.35, title, ha='center', va='center', 
                fontsize=10.5, weight='bold', color=title_color, zorder=3)

def draw_badge_arrow(x1, y1, x2, y2, tensor_str):
    """Dibuja flecha de conexión con badge flotante para el tensor."""
    # Flecha
    arrow = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle='->', 
                            mutation_scale=16, color='#34495E', lw=2.0, zorder=4)
    ax.add_patch(arrow)
    
    # Badge para el tensor
    mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
    txt = ax.text(mid_x, mid_y + 0.35, tensor_str, fontsize=8.0, weight='bold', 
                  ha='center', va='center', color='#1A252C', zorder=6)
    txt.set_bbox(dict(facecolor='#EAECEE', alpha=1.0, edgecolor='#BDC3C7', 
                      boxstyle='round,pad=0.25'))

# ------------------------------------------------------------
# 3. CONSTRUCCIÓN DE LA ARQUITECTURA
# ------------------------------------------------------------

# --- 1. INPUT TENSOR ---
draw_card(0.4, 2.8, 2.0, 3.8, "#EBF5FB", "#2980B9", "ENTRADA", "#1B4F72")
ax.text(1.4, 5.5, "Tensor $X_t$", ha='center', va='center', fontsize=11.0, weight='bold', color='#1B4F72')
ax.text(1.4, 4.2, "• Ventana: 70 min\n• Features ($F$)\n• Batch ($B = 64$)\n─────────────\nHistorial Ionosférico", 
        ha='center', va='center', fontsize=8.5, color='#283747', linespacing=1.4, zorder=3)

draw_badge_arrow(2.55, 4.7, 3.35, 4.7, r"$\mathbf{R}^{B \times 70 \times F}$")

# --- 2. CAPA RECURRENTE 1 ---
draw_card(3.4, 2.8, 2.3, 3.8, "#E8F8F5", "#117A65", "LSTM LAYER 1", "#0E6251")
ax.text(4.55, 5.5, "128 Neuronas", ha='center', va='center', fontsize=10.5, weight='bold', color='#0E6251')
ax.text(4.55, 4.2, "`return_seq = True`\n─────────────\n+ Batch Norm\n+ Dropout (0.2)\n─────────────\nExtrae patrones local", 
        ha='center', va='center', fontsize=8.2, color='#145A32', linespacing=1.35, zorder=3)

draw_badge_arrow(5.85, 4.7, 6.65, 4.7, r"$\mathbf{R}^{B \times 70 \times 128}$")

# --- 3. CAPA RECURRENTE 2 ---
draw_card(6.7, 2.8, 2.3, 3.8, "#FEF9E7", "#D4AC0D", "LSTM LAYER 2", "#7D6608")
ax.text(7.85, 5.5, "64 Neuronas", ha='center', va='center', fontsize=10.5, weight='bold', color='#7D6608')
ax.text(7.85, 4.2, "`return_seq = False`\n─────────────\n+ Batch Norm\n+ Dropout (0.2)\n─────────────\nResumen de estado", 
        ha='center', va='center', fontsize=8.2, color='#7D6608', linespacing=1.35, zorder=3)

draw_badge_arrow(9.15, 4.7, 9.95, 4.7, r"$\mathbf{R}^{B \times 64}$")

# --- 4. DECODER ---
draw_card(10.0, 2.8, 1.8, 3.8, "#F4ECF7", "#8E44AD", "DECODER", "#4A235A")
ax.text(10.9, 5.4, "Dense (128)", ha='center', va='center', fontsize=9.5, weight='bold', color='#4A235A')
ax.text(10.9, 4.8, "Act: ReLU\nDropout (0.2)", ha='center', va='center', fontsize=8.0, color='#5B2C6F')
ax.text(10.9, 3.8, "Dense (10)", ha='center', va='center', fontsize=9.5, weight='bold', color='#4A235A')
ax.text(10.9, 3.3, "Act: Linear", ha='center', va='center', fontsize=8.0, color='#5B2C6F')

draw_badge_arrow(11.95, 4.7, 12.55, 4.7, r"$\mathbf{R}^{B \times 10}$")

# --- 5. SALIDA / PRONÓSTICO ---
draw_card(12.6, 2.8, 1.1, 3.8, "#FDEDEC", "#CB4335", "SALIDA", "#78281F")
ax.text(13.15, 5.3, r"$\hat{Y}_t$", ha='center', va='center', fontsize=12.0, weight='bold', color='#78281F')
ax.text(13.15, 4.1, "Forecast\nMulti-paso\n─────────\n+1 a +10\nminutos\n($S_4$)", 
        ha='center', va='center', fontsize=8.0, color='#922B21', linespacing=1.3, zorder=3)

# ------------------------------------------------------------
# 4. TÍTULO Y PANEL DE JUSTIFICACIÓN
# ------------------------------------------------------------
ax.text(7.0, 7.8, "Arquitectura Propuesta: Stacked LSTM para Pronóstico de Centelleo Ionosférico", 
        ha='center', va='center', fontsize=12.5, weight='bold', color='#1C2833')

# Panel inferior explicativo con estética limpia
draw_card(0.4, 0.4, 13.3, 1.9, "#F8F9F9", "#B0BEC5", "", "#2C3E50")
ax.text(0.7, 1.9, "Principios de Diseño y Flujo Jerárquico:", fontsize=9.5, weight='bold', color='#2C3E50')
ax.text(0.7, 1.15, 
        "• Modulación Multiescala: La Capa 1 conserva la dimensión temporal (70, 128) para capturar dinámicas rápidas de plasma (ROTI/TEC).\n"
        "• Compresión de Estado: La Capa 2 sintetiza la historia en un vector latente de 64 dimensiones eliminando redundancia temporal.\n"
        "• Proyección Continua: El Decoder proyecta la representación abstracta directamente al horizonte de predicción futura (+10 min).",
        fontsize=8.5, color='#34495E', linespacing=1.45, va='center')

# Guardar figura en alta resolución
plt.savefig("Figura2_Arquitectura_Stacked_LSTM_Sofisticada.png", dpi=300, bbox_inches='tight', pad_inches=0.03, facecolor='#FFFFFF')
plt.show()