import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['text.color'] = '#000000'

fig, ax = plt.subplots(figsize=(6.5, 1.8))
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('#F8F9FA')
ax.axis('off')

ax.set_xlim(0, 22)
ax.set_ylim(0, 3.5)

# Paleta Verde
COLOR_B, BORDE_B = '#E8F8F5', '#117864'
BLOCK_H, START_X, END_X = 1.15, 1.0, 21.0
TOTAL_W = END_X - START_X

def draw_block(ax, x, y, w, h, bg_color, edge_color, title, subtitle):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08",
                                  facecolor=bg_color, edgecolor=edge_color, linewidth=1.2, zorder=3)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h*0.58, title, ha='center', va='center', fontsize=7.5, fontweight='bold', zorder=4)
    ax.text(x + w/2, y + h*0.28, subtitle, ha='center', va='center', fontsize=5.8, fontweight='bold', color='#2C3E50', zorder=4)

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color='#000000', lw=1.4, mutation_scale=9), zorder=2)

# Renderizado
ax.text(START_X, 2.0, "b) Stacked LSTM (Profunda)", fontsize=8.0, fontweight='bold', ha='left', va='bottom')
blocks_b = [("Input", "(70, 9)"), ("LSTM\n128", "(seq → seq)"), ("Dropout", "p = 0.2"), ("LSTM\n64", "(seq → vec)"), ("Dropout", "p = 0.2"), ("Dense\n32", "(ReLU)"), ("Output", "Linear")]

w_b = 2.0  
spacing_b = (TOTAL_W - (len(blocks_b) * w_b)) / (len(blocks_b) - 1)
current_x = START_X

for i, (title, sub) in enumerate(blocks_b):
    draw_block(ax, current_x, 0.5, w_b, BLOCK_H, COLOR_B, BORDE_B, title, sub)
    if i < len(blocks_b) - 1:
        draw_arrow(ax, current_x + w_b, 0.5 + BLOCK_H/2, current_x + w_b + spacing_b, 0.5 + BLOCK_H/2)
    current_x += w_b + spacing_b

plt.tight_layout()
plt.savefig('Arquitectura_B_Stacked_LSTM.png', format='png', bbox_inches='tight', pad_inches=0.02, dpi=300)
plt.show()