import matplotlib
# matplotlib.use('Agg')  # Activar si se ejecuta en servidores sin interfaz gráfica
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 1. CONFIGURACIÓN PARA HOJA A4 ---
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['text.color'] = '#000000'

# Ajustamos el lienzo para acomodar las cuatro líneas con comodidad
fig, ax = plt.subplots(figsize=(6.5, 5.2))
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('#F8F9FA')
ax.axis('off')

# Límites fijados del lienzo
X_MAX = 22.0
ax.set_xlim(0, X_MAX)
ax.set_ylim(0, 13)

# --- 2. PALETA DE COLORES DE ALTO CONTRASTE ---
COLOR_A = '#D6EAF8'  # Azul
BORDE_A = '#1F618D'
COLOR_B = '#E8F8F5'  # Verde
BORDE_B = '#117864'
COLOR_C = '#FDEDEC'  # Rosado
BORDE_C = '#922B21'

# --- 3. FUNCIONES DE DIBUJO CON FUENTES GRANDES ---
def draw_block(ax, x, y, w, h, bg_color, edge_color, title, subtitle, font_title_sz=7.5, font_sub_sz=5.8):
    rect = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=0.08",
        facecolor=bg_color, edgecolor=edge_color, linewidth=1.2, zorder=3
    )
    ax.add_patch(rect)
    
    # Textos legibles y grandes
    ax.text(x + w/2, y + h*0.58, title, ha='center', va='center', 
            fontsize=font_title_sz, fontweight='bold', color='#000000', zorder=4)
    ax.text(x + w/2, y + h*0.28, subtitle, ha='center', va='center', 
            fontsize=font_sub_sz, fontweight='bold', color='#2C3E50', zorder=4)

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4, 
                                mutation_scale=9), zorder=2)

# --- 4. CONSTANTES DE GEOMETRÍA ---
BLOCK_H = 1.15   # Alto de bloque
START_X = 1.0    # Margen izquierdo absoluto
END_X   = 21.0   # Margen derecho absoluto
TOTAL_W = END_X - START_X

# --- 5. RENDERIZADO DE LAS ARQUITECTURAS ---

# =========================================================================
# ARQUITECTURA A) 5 bloques
# =========================================================================
Y_A = 10.2
ax.text(START_X, Y_A + BLOCK_H + 0.15, "a) LSTM Simple Optimizada", fontsize=7.5, fontweight='bold', ha='left', va='bottom')
blocks_a = [("Input", "(70, 9)"), ("LSTM\n64", "(seq → vec)"), ("Dropout", "p = 0.2"), ("Dense\n32", "(ReLU)"), ("Output", "Linear")]

w_a = 2.6  
spacing_a = (TOTAL_W - (len(blocks_a) * w_a)) / (len(blocks_a) - 1)
current_x = START_X
for i, (title, sub) in enumerate(blocks_a):
    draw_block(ax, current_x, Y_A, w_a, BLOCK_H, COLOR_A, BORDE_A, title, sub, font_title_sz=8.0, font_sub_sz=6.2)
    if i < len(blocks_a) - 1:
        draw_arrow(ax, current_x + w_a, Y_A + BLOCK_H/2, current_x + w_a + spacing_a, Y_A + BLOCK_H/2)
    current_x += w_a + spacing_a

# =========================================================================
# ARQUITECTURA B) 7 bloques
# =========================================================================
Y_B = 7.2
ax.text(START_X, Y_B + BLOCK_H + 0.15, "b) Stacked LSTM (Profunda)", fontsize=7.5, fontweight='bold', ha='left', va='bottom')
blocks_b = [("Input", "(70, 9)"), ("LSTM\n128", "(seq → seq)"), ("Dropout", "p = 0.2"), ("LSTM\n64", "(seq → vec)"), ("Dropout", "p = 0.2"), ("Dense\n32", "(ReLU)"), ("Output", "Linear")]

w_b = 2.0  
spacing_b = (TOTAL_W - (len(blocks_b) * w_b)) / (len(blocks_b) - 1)
current_x = START_X
for i, (title, sub) in enumerate(blocks_b):
    draw_block(ax, current_x, Y_B, w_b, BLOCK_H, COLOR_B, BORDE_B, title, sub, font_title_sz=7.5, font_sub_sz=5.8)
    if i < len(blocks_b) - 1:
        draw_arrow(ax, current_x + w_b, Y_B + BLOCK_H/2, current_x + w_b + spacing_b, Y_B + BLOCK_H/2)
    current_x += w_b + spacing_b

# =========================================================================
# ARQUITECTURA C) 10 bloques -> Conexión secuencial en forma de "S" corregida
# =========================================================================
Y_C1 = 3.8  # Fila superior de C
Y_C2 = 1.0  # Fila inferior de C
ax.text(START_X, Y_C1 + BLOCK_H + 0.15, "c) Bidirectional LSTM (BiLSTM)", fontsize=7.5, fontweight='bold', ha='left', va='bottom')

blocks_c1 = [("Input", "(70, 9)"), ("BiLSTM\n128", "(seq → seq)"), ("BatchNorm", ""), ("Dropout", "p = 0.3"), ("BiLSTM\n64", "(seq → vec)")]
blocks_c2 = [("BatchNorm", ""), ("Dropout", "p = 0.3"), ("Dense\n128", "(ReLU)"), ("Dense\n64", "(ReLU)"), ("Output", "Linear")]

w_c = 2.6  
spacing_c = (TOTAL_W - (5 * w_c)) / (5 - 1) 

# Primera línea de C (Input -> ... -> BiLSTM 64)
current_x = START_X
for i, (title, sub) in enumerate(blocks_c1):
    draw_block(ax, current_x, Y_C1, w_c, BLOCK_H, COLOR_C, BORDE_C, title, sub, font_title_sz=8.0, font_sub_sz=6.2)
    if i < len(blocks_c1) - 1:
        draw_arrow(ax, current_x + w_c, Y_C1 + BLOCK_H/2, current_x + w_c + spacing_c, Y_C1 + BLOCK_H/2)
    else:
        # CAMBIO CORREGIDO: Línea limpia escalonada (ortogonal) desde BiLSTM 64 hasta el BatchNorm inferior
        # Baja verticalmente, viaja en horizontal hacia el inicio y baja al centro de BatchNorm.
        x_start = current_x + w_c / 2
        y_start = Y_C1
        x_end = START_X + w_c / 2
        y_end = Y_C2 + BLOCK_H
        
        # Trayecto en 3 segmentos limpios
        y_mid = (y_start + y_end) / 2
        ax.plot([x_start, x_start], [y_start, y_mid], color='#000000', lw=1.4, zorder=2) # Baja
        ax.plot([x_start, x_end], [y_mid, y_mid], color='#000000', lw=1.4, zorder=2)     # Va a la izquierda
        # Tramo final con la punta de flecha apuntando hacia abajo al centro del bloque inferior
        ax.annotate('', xy=(x_end, y_end), xytext=(x_end, y_mid),
                    arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4, mutation_scale=9), zorder=2)
        
    current_x += w_c + spacing_c

# Segunda línea de C (BatchNorm -> ... -> Output)
current_x = START_X
for i, (title, sub) in enumerate(blocks_c2):
    draw_block(ax, current_x, Y_C2, w_c, BLOCK_H, COLOR_C, BORDE_C, title, sub, font_title_sz=8.0, font_sub_sz=6.2)
    if i < len(blocks_c2) - 1:
        draw_arrow(ax, current_x + w_c, Y_C2 + BLOCK_H/2, current_x + w_c + spacing_c, Y_C2 + BLOCK_H/2)
    current_x += w_c + spacing_c

# --- 6. EXPORTACIÓN PROFESIONAL ---
plt.tight_layout()

filename = 'Figura_2_4_Comparativa_Multilinea_Corregida'
plt.savefig(filename + '.pdf', format='pdf', bbox_inches='tight', pad_inches=0.02)
plt.savefig(filename + '.png', format='png', bbox_inches='tight', pad_inches=0.02, dpi=300)

print(f"Diagrama con flujo corregido e hiper-legible generado con éxito: {filename}.png")