import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuración de alta calidad para impresión A4
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['text.color'] = '#000000'

# Dimensiones optimizadas para una sola fila (más angosta verticalmente: 6.5 x 1.8)
fig, ax = plt.subplots(figsize=(6.5, 1.8))
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('#F8F9FA')
ax.axis('off')

ax.set_xlim(0, 22)
ax.set_ylim(0, 3.5)

# Paleta Azul
COLOR_A, BORDE_A = '#D6EAF8', '#1F618D'
BLOCK_H, START_X, END_X = 1.15, 1.0, 21.0
TOTAL_W = END_X - START_X

def draw_block(ax, x, y, w, h, bg_color, edge_color, title, subtitle):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                  facecolor=bg_color, edgecolor=edge_color, linewidth=1.2, zorder=3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h*0.58, title, ha='center', va='center', fontsize=8.5, fontweight='bold', zorder=4)
    ax.text(x + w/2, y + h*0.28, subtitle, ha='center', va='center', fontsize=6.5, fontweight='bold', color='#2C3E50', zorder=4)

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4, mutation_scale=9), zorder=2)

# Renderizado
ax.text(START_X, 2.0, "a) LSTM Simple Optimizada", fontsize=8.0, fontweight='bold', ha='left', va='bottom')
blocks_a = [("Input", "(70, 9)"), ("LSTM\n64", "(seq → vec)"), ("Dropout", "p = 0.2"), ("Dense\n32", "(ReLU)"), ("Output", "Linear")]

w_a = 2.6  
spacing_a = (TOTAL_W - (len(blocks_a) * w_a)) / (len(blocks_a) - 1)
current_x = START_X

for i, (title, sub) in enumerate(blocks_a):
    draw_block(ax, current_x, 0.5, w_a, BLOCK_H, COLOR_A, BORDE_A, title, sub)
    if i < len(blocks_a) - 1:
        draw_arrow(ax, current_x + w_a, 0.5 + BLOCK_H/2, current_x + w_a + spacing_a, 0.5 + BLOCK_H/2)
    current_x += w_a + spacing_a

plt.tight_layout()
plt.savefig('Arquitectura_A_LSTM_Simple.png', format='png', bbox_inches='tight', pad_inches=0.02, dpi=300)
plt.show()