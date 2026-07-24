import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['text.color'] = '#000000'

# Dimensiones verticales adaptadas para sus dos filas internas (6.5 x 3.2)
fig, ax = plt.subplots(figsize=(6.5, 3.2))
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('#F8F9FA')
ax.axis('off')

ax.set_xlim(0, 22)
ax.set_ylim(0, 5.2)

# Paleta Rosada
COLOR_C, BORDE_C = '#FDEDEC', '#922B21'
BLOCK_H, START_X, END_X = 1.15, 1.0, 21.0
TOTAL_W = END_X - START_X

def draw_block(ax, x, y, w, h, bg_color, edge_color, title, subtitle):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                  facecolor=bg_color, edgecolor=edge_color, linewidth=1.2, zorder=3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h*0.58, title, ha='center', va='center', fontsize=8.0, fontweight='bold', zorder=4)
    ax.text(x + w/2, y + h*0.28, subtitle, ha='center', va='center', fontsize=6.2, fontweight='bold', color='#2C3E50', zorder=4)

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4, mutation_scale=9), zorder=2)

# Coordenadas de las dos filas
Y_C1, Y_C2 = 2.4, 0.4
ax.text(START_X, Y_C1 + BLOCK_H + 0.15, "c) Bidirectional LSTM (BiLSTM)", fontsize=8.0, fontweight='bold', ha='left', va='bottom')

blocks_c1 = [("Input", "(70, 9)"), ("BiLSTM\n128", "(seq → seq)"), ("BatchNorm", ""), ("Dropout", "p = 0.3"), ("BiLSTM\n64", "(seq → vec)")]
blocks_c2 = [("BatchNorm", ""), ("Dropout", "p = 0.3"), ("Dense\n128", "(ReLU)"), ("Dense\n64", "(ReLU)"), ("Output", "Linear")]

w_c = 2.6  
spacing_c = (TOTAL_W - (5 * w_c)) / (5 - 1)

# Fila 1
current_x = START_X
for i, (title, sub) in enumerate(blocks_c1):
    draw_block(ax, current_x, Y_C1, w_c, BLOCK_H, COLOR_C, BORDE_C, title, sub)
    if i < len(blocks_c1) - 1:
        draw_arrow(ax, current_x + w_c, Y_C1 + BLOCK_H/2, current_x + w_c + spacing_c, Y_C1 + BLOCK_H/2)
    else:
        # Conexión ortogonal limpia hacia la fila inferior
        x_start, y_start = current_x + w_c / 2, Y_C1
        x_end, y_end = START_X + w_c / 2, Y_C2 + BLOCK_H
        y_mid = (y_start + y_end) / 2
        ax.plot([x_start, x_start], [y_start, y_mid], color='#000000', lw=1.4, zorder=2)
        ax.plot([x_start, x_end], [y_mid, y_mid], color='#000000', lw=1.4, zorder=2)
        ax.annotate('', xy=(x_end, y_end), xytext=(x_end, y_mid),
                    arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4, mutation_scale=9), zorder=2)
    current_x += w_c + spacing_c

# Fila 2
current_x = START_X
for i, (title, sub) in enumerate(blocks_c2):
    draw_block(ax, current_x, Y_C2, w_c, BLOCK_H, COLOR_C, BORDE_C, title, sub)
    if i < len(blocks_c2) - 1:
        draw_arrow(ax, current_x + w_c, Y_C2 + BLOCK_H/2, current_x + w_c + spacing_c, Y_C2 + BLOCK_H/2)
    current_x += w_c + spacing_c

plt.tight_layout()
plt.savefig('Arquitectura_C_BiLSTM.png', format='png', bbox_inches='tight', pad_inches=0.02, dpi=300)
plt.show()