import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 1. CONFIGURACIÓN INICIAL ---
plt.rcParams['figure.dpi'] = 300
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')
ax.set_facecolor('#FFFFFF')

# Fuentes principales
font_title = {'family': 'sans-serif', 'weight': 'bold', 'size': 18}
font_math_large = {'family': 'sans-serif', 'weight': 'bold', 'size': 16}
font_gate_title = {'family': 'sans-serif', 'weight': 'bold', 'size': 12}
font_equation = {'family': 'sans-serif', 'size': 12}

# --- 2. TÍTULOS Y LEYENDAS ---
ax.text(8, 8.5, "Figura 2.3. Arquitectura interna y compuertas matemáticas de una celda LSTM.", 
        ha='center', va='center', color='black', **font_title)
ax.plot([1, 15], [8.0, 8.0], color='#BDC3C7', linewidth=2) # Línea separadora

# --- 3. LÍMITES DE LA CELDA LSTM ---
# Dibujamos un cuadro grande que representa el interior de la neurona
cell_box = patches.Rectangle((2.5, 1.5), 11, 5.5, linewidth=2.5, edgecolor='#34495E', 
                             facecolor='#F8F9F9', linestyle='--', zorder=1)
ax.add_patch(cell_box)
ax.text(8, 6.7, "INTERIOR DE LA CELDA LSTM", ha='center', va='center', 
        color='#7F8C8D', fontsize=16, fontweight='bold', zorder=2)

# --- 4. FLUJOS PRINCIPALES DE MEMORIA (Líneas horizontales) ---

# A. Estado Celular (Memoria a Largo Plazo) - Línea superior
ax.annotate('', xy=(15.5, 5.5), xytext=(0.5, 5.5), arrowprops=dict(arrowstyle="->", lw=3.5, color='#2980B9'))
ax.text(0.4, 5.5, r'$c_{t-1}$', ha='right', va='center', color='#2980B9', **font_math_large)
ax.text(15.6, 5.5, r'$c_t$', ha='left', va='center', color='#2980B9', **font_math_large)
ax.text(0.4, 5.8, 'Estado Celular (Largo Plazo)', ha='left', va='bottom', color='#2980B9', fontsize=11, fontweight='bold')

# B. Estado Oculto (Memoria a Corto Plazo) - Línea inferior
ax.annotate('', xy=(15.5, 2.5), xytext=(0.5, 2.5), arrowprops=dict(arrowstyle="->", lw=3.5, color='#C0392B'))
ax.text(0.4, 2.5, r'$h_{t-1}$', ha='right', va='center', color='#C0392B', **font_math_large)
ax.text(15.6, 2.5, r'$h_t$', ha='left', va='center', color='#C0392B', **font_math_large)
ax.text(0.4, 2.1, 'Estado Oculto (Corto Plazo)', ha='left', va='top', color='#C0392B', fontsize=11, fontweight='bold')

# C. Vector de Entrada Actual (Sube desde abajo)
ax.annotate('', xy=(3.5, 2.3), xytext=(3.5, 0.5), arrowprops=dict(arrowstyle="->", lw=3.5, color='#27AE60'))
ax.text(3.5, 0.2, r'$x_t$', ha='center', va='top', color='#27AE60', **font_math_large)
ax.text(3.5, -0.2, 'Entrada Actual', ha='center', va='top', color='#27AE60', fontsize=11, fontweight='bold')

# Punto de concatenación [h_{t-1}, x_t]
ax.plot(3.5, 2.5, marker='o', markersize=8, color='black', zorder=5)

# --- 5. COMPUERTAS (GATES) MATEMÁTICAS ---
gates = [
    {'x': 4.5, 'y': 3.5, 'title': 'Compuerta\nde Olvido\n(Forget)', 'sym': r'$\sigma$', 'eq': r'$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$', 'color': '#FAD7A1'},
    {'x': 7.0, 'y': 3.5, 'title': 'Compuerta\nde Entrada\n(Input)', 'sym': r'$\sigma$', 'eq': r'$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$', 'color': '#AED6F1'},
    {'x': 9.5, 'y': 3.5, 'title': 'Estado\nCandidato\n(Cell)', 'sym': r'$\tanh$', 'eq': r'$\tilde{c}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c)$', 'color': '#A9DFBF'},
    {'x': 12.0, 'y': 3.5, 'title': 'Compuerta\nde Salida\n(Output)', 'sym': r'$\sigma$', 'eq': r'$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$', 'color': '#D7BDE2'}
]

for g in gates:
    # Flecha subiendo desde h_{t-1} hacia la compuerta
    ax.annotate('', xy=(g['x'], g['y'] - 0.5), xytext=(g['x'], 2.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='black'))
    
    # Caja de la compuerta
    gate_box = patches.Rectangle((g['x'] - 1.0, g['y'] - 0.6), 2.0, 1.2, linewidth=1.5, edgecolor='black', facecolor=g['color'], zorder=3)
    ax.add_patch(gate_box)
    
    # Textos de la compuerta
    ax.text(g['x'], g['y'] + 0.1, g['title'], ha='center', va='center', color='black', **font_gate_title)
    
    # Ecuación correspondiente debajo del bloque principal de h_t para limpieza
    ax.text(g['x'], 1.0, g['eq'], ha='center', va='center', bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'), **font_equation)

# --- 6. OPERADORES PUNTUALES Y CONEXIONES SUPERIORES ---
def draw_op(x, y, symbol, bg_color):
    circle = patches.Circle((x, y), 0.3, linewidth=1.5, edgecolor='black', facecolor=bg_color, zorder=4)
    ax.add_patch(circle)
    ax.text(x, y, symbol, ha='center', va='center', fontsize=16, fontweight='bold', zorder=5)

# Operador de Olvido (Multiplicación en la línea C_t)
draw_op(4.5, 5.5, r'$\times$', '#FAD7A1')
ax.annotate('', xy=(4.5, 5.2), xytext=(4.5, 4.1), arrowprops=dict(arrowstyle="->", lw=1.5, color='black')) # Sube desde Forget Gate

# Operador de Entrada (Multiplicación entre Input y Candidato)
draw_op(8.25, 4.5, r'$\times$', '#AED6F1')
ax.annotate('', xy=(8.1, 4.3), xytext=(7.0, 4.1), arrowprops=dict(arrowstyle="->", lw=1.5, color='black')) # Desde Input
ax.annotate('', xy=(8.4, 4.3), xytext=(9.5, 4.1), arrowprops=dict(arrowstyle="->", lw=1.5, color='black')) # Desde Candidato

# Operador de Actualización de C_t (Suma en la línea C_t)
draw_op(8.25, 5.5, r'$+$', '#D5F5E3')
ax.annotate('', xy=(8.25, 5.2), xytext=(8.25, 4.8), arrowprops=dict(arrowstyle="->", lw=1.5, color='black')) # Sube desde la multiplicación

# Ecuación de C_t
ax.text(8.25, 6.2, r'$c_t = f_t \times c_{t-1} + i_t \times \tilde{c}_t$', ha='center', va='center', 
        bbox=dict(facecolor='white', edgecolor='#2980B9', boxstyle='round,pad=0.3'), fontsize=13, color='#2980B9', fontweight='bold')

# Operador de Salida h_t
draw_op(13.5, 4.5, r'$\tanh$', '#FFFFFF') # Tanh del estado celular actual
ax.annotate('', xy=(13.5, 4.8), xytext=(13.5, 5.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='black')) # Baja desde C_t

draw_op(13.5, 3.5, r'$\times$', '#D7BDE2') # Multiplicación final
ax.annotate('', xy=(13.5, 3.8), xytext=(13.5, 4.2), arrowprops=dict(arrowstyle="->", lw=1.5, color='black')) # Baja desde Tanh
ax.annotate('', xy=(13.2, 3.5), xytext=(12.0, 3.5), arrowprops=dict(arrowstyle="->", lw=1.5, color='black')) # Viene de Output Gate
ax.annotate('', xy=(13.5, 2.5), xytext=(13.5, 3.2), arrowprops=dict(arrowstyle="->", lw=2.0, color='#C0392B')) # Inyecta a la línea h_t

# Ecuación de h_t
ax.text(14.0, 4.5, r'$h_t = o_t \times \tanh(c_t)$', ha='left', va='center', 
        bbox=dict(facecolor='white', edgecolor='#C0392B', boxstyle='round,pad=0.3'), fontsize=13, color='#C0392B', fontweight='bold')

# --- 7. EXPORTACIÓN ---
plt.tight_layout()
# Comento plt.show() para evitar la advertencia en tu terminal WSL
# plt.show() 

plt.savefig('Figura_2_3_LSTM_Celda_Arquitectura.pdf', format='pdf', bbox_inches='tight')
plt.savefig('Figura_2_3_LSTM_Celda_Arquitectura.png', format='png', bbox_inches='tight', dpi=300)

print("¡Imágenes generadas con éxito! Revisa la carpeta.")