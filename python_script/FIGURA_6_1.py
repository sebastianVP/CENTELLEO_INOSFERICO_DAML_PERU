import matplotlib.pyplot as plt
import numpy as np

# --- Definición de Funciones Conceptuales ---
x = np.linspace(0, 60, 200)

# 1. Confiabilidad Predictiva (Azul)
y1_confiabilidad = np.exp(-0.035 * x)

# 2. Valor Operativo Preventivo (Naranja)
y2_valor_operativo = 1 - np.exp(-0.06 * x)

# --- Configuración del Gráfico ---
fig, ax1 = plt.subplots(figsize=(10, 6), dpi=100)
ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

# --- Graficar en el Primer Eje (ax1 - Izquierdo) ---
color1 = 'tab:blue'
ax1.set_xlabel('Tiempo de anticipación / Horizonte temporal (minutos)', fontsize=12)
ax1.set_ylabel('Confiabilidad Predictiva / Precisión (Normalizada)', color='black', fontsize=12)
ax1.plot(x, y1_confiabilidad, color=color1, linewidth=2, label='Confiabilidad Predictiva')
ax1.tick_params(axis='y', labelcolor='black')

ax1.set_ylim(0, 1.05)
y1_ticks = np.arange(0, 1.1, 0.2)
ax1.set_yticks(y1_ticks)
ax1.set_yticklabels([f'{int(tick*100)}%' for tick in y1_ticks])

# --- Graficar en el Segundo Eje (ax2 - Derecho) ---
ax2 = ax1.twinx()
color2 = 'tab:orange'
ax2.set_ylabel('Valor Operativo Preventivo / Tiempo de Reacción (Normalizado)', color='black', fontsize=12)
ax2.plot(x, y2_valor_operativo, color=color2, linewidth=2, label='Valor Operativo Preventivo')
ax2.tick_params(axis='y', labelcolor='black')

ax2.set_ylim(0, 1.05)

# 6 etiquetas para 6 ticks
op_categories = ["Muy Bajo", "Bajo", "Medio-Bajo", "Medio", "Medio-Alto", "Alto"]
ax2.set_yticks(y1_ticks)
ax2.set_yticklabels(op_categories)

# --- Anotaciones y 'Sweet Spot' ---
# 1. Línea vertical del punto dulce
punto_dulce_x = 10
ax1.axvline(x=punto_dulce_x, color='grey', linestyle='--', linewidth=1.5, alpha=0.8)

# 2. Pequeñas flechas indicando las intersecciones exactas
y1_interseccion = np.exp(-0.035 * punto_dulce_x)
ax1.annotate('', xy=(punto_dulce_x, y1_interseccion), xytext=(punto_dulce_x + 2, y1_interseccion - 0.05),
            arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->', alpha=0.5))

y2_interseccion = 1 - np.exp(-0.06 * punto_dulce_x)
ax2.annotate('', xy=(punto_dulce_x, y2_interseccion), xytext=(punto_dulce_x + 2, y2_interseccion - 0.05),
            arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->', alpha=0.5))

# 3. CAJA DE TEXTO MOVIDA A LA DERECHA CON FLECHA INDICADORA
text_content = "PUNTO DULCE (SWEET SPOT): 10 MINUTOS\nConfiabilidad óptima (≈75%) con Tiempo de Reacción útil (≈55%)"

# Posicionamos el texto en x=35 para que quede a la derecha, libre de las curvas
ax1.annotate(
    text_content, 
    xy=(10.5, 0.58),           # A dónde apunta la flecha (cerca de la línea de 10 min)
    xytext=(35, 0.58),         # Dónde se ubica el centro de la caja de texto
    ha='center', va='center',
    fontsize=10, fontweight='bold', color='black',
    bbox=dict(boxstyle='round,pad=1', facecolor='#a9dfbf', edgecolor='#27ae60', alpha=0.8),
    arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2) # Flecha verde apuntando al sweet spot
)

# --- Leyendas ---
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

# Colocar la leyenda arriba al centro
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper center', bbox_to_anchor=(0.5, 0.95), frameon=True, fontsize=10)

plt.tight_layout()

# --- GUARDAR COMO PNG ---
nombre_archivo = 'Figura_6_1_TradeOff'
plt.savefig(f'{nombre_archivo}.png', dpi=300, bbox_inches='tight', facecolor='white')
print(f"¡Imagen guardada exitosamente como: {nombre_archivo}.png!")

# Mostrar gráfico en pantalla (opcional)
plt.show()