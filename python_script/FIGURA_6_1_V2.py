import matplotlib.pyplot as plt
import numpy as np

# --- Definición de Funciones Conceptuales ---
x = np.linspace(0, 60, 200)

# 1. Confiabilidad Predictiva (Azul)
y1_confiabilidad = np.exp(-0.035 * x)

# 2. Valor Operativo Preventivo (Naranja)
y2_valor_operativo = 1 - np.exp(-0.06 * x)

# --- Configuración del Gráfico (Lienzo optimizado para fuentes +20% extra) ---
fig, ax1 = plt.subplots(figsize=(13.5, 8.5), dpi=600)
ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

# --- Constantes Tipográficas (Incremento del 20% adicional sobre la anterior) ---
FONT_SIZE_LABEL = 19.5       
FONT_SIZE_AXIS = 16.0        
FONT_SIZE_BOX = 16.0         
FONT_SIZE_LEGEND = 16.0      

# --- Graficar en el Primer Eje (ax1 - Izquierdo) ---
color1 = 'tab:blue'
ax1.set_xlabel('Tiempo de anticipación / Horizonte temporal (minutos)', fontsize=FONT_SIZE_LABEL, labelpad=15)
ax1.set_ylabel('Confiabilidad Predictiva / Precisión (Normalizada)', color='black', fontsize=FONT_SIZE_LABEL, labelpad=15)
ax1.plot(x, y1_confiabilidad, color=color1, linewidth=3.0, label='Confiabilidad Predictiva')
ax1.tick_params(axis='both', labelcolor='black', labelsize=FONT_SIZE_AXIS)

ax1.set_ylim(0, 1.05)
y1_ticks = np.arange(0, 1.1, 0.2)
ax1.set_yticks(y1_ticks)
ax1.set_yticklabels([f'{int(tick*100)}%' for tick in y1_ticks])

# --- Graficar en el Segundo Eje (ax2 - Derecho) ---
ax2 = ax1.twinx()
color2 = 'tab:orange'
ax2.set_ylabel('Valor Operativo Preventivo / Tiempo de Reacción (Normalizado)', color='black', fontsize=FONT_SIZE_LABEL, labelpad=22)
ax2.plot(x, y2_valor_operativo, color=color2, linewidth=3.0, label='Valor Operativo Preventivo')
ax2.tick_params(axis='y', labelcolor='black', labelsize=FONT_SIZE_AXIS)

ax2.set_ylim(0, 1.05)

# 6 etiquetas para 6 ticks
op_categories = ["Muy Bajo", "Bajo", "Medio-Bajo", "Medio", "Medio-Alto", "Alto"]
ax2.set_yticks(y1_ticks)
ax2.set_yticklabels(op_categories)

# --- Anotaciones y 'Sweet Spot' ---
# 1. Línea vertical del punto dulce
punto_dulce_x = 10
ax1.axvline(x=punto_dulce_x, color='grey', linestyle='--', linewidth=2.0, alpha=0.8)

# 2. Pequeñas flechas indicando las intersecciones exactas
y1_interseccion = np.exp(-0.035 * punto_dulce_x)
ax1.annotate('', xy=(punto_dulce_x, y1_interseccion), xytext=(punto_dulce_x + 2, y1_interseccion - 0.05),
            arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->', alpha=0.5))

y2_interseccion = 1 - np.exp(-0.06 * punto_dulce_x)
ax2.annotate('', xy=(punto_dulce_x, y2_interseccion), xytext=(punto_dulce_x + 2, y2_interseccion - 0.05),
            arrowprops=dict(facecolor='black', edgecolor='black', arrowstyle='->', alpha=0.5))

# 3. CAJA DE TEXTO REUBICADA HACIA ABAJO PARA DEJAR ESPACIO A LA LEYENDA CENTRAL
text_content = "PUNTO DULCE (SWEET SPOT): 10 MINUTOS\nConfiabilidad óptima (≈75%) con Tiempo de Reacción útil (≈55%)"

# Se baja la coordenada 'y' de la caja de texto a 0.22 para liberar el centro a la leyenda
ax1.annotate(
    text_content, 
    xy=(14.5, 0.58),           # Destino de la flecha verde
    xytext=(34.5, 0.22),       # Ubicación de la caja de texto ajustada
    ha='center', va='center',
    fontsize=FONT_SIZE_BOX, fontweight='bold', color='black',
    bbox=dict(boxstyle='round,pad=0.8', facecolor='#a9dfbf', edgecolor='#27ae60', alpha=0.8, linewidth=1.8),
    arrowprops=dict(arrowstyle='->', color='#27ae60', lw=2.5)
)

# --- Leyendas ---
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

# ➔ CORRECCIÓN: Leyenda movida exactamente al centro vertical (bbox_to_anchor=(0.5, 0.55))
ax1.legend(lines1 + lines2, labels1 + labels2, loc='center', bbox_to_anchor=(0.5, 0.55), frameon=True, fontsize=FONT_SIZE_LEGEND)

plt.tight_layout()

# --- GUARDAR EN MÁXIMA RESOLUCIÓN ---
nombre_archivo = 'Figura_6_1_TradeOff_Robust'
plt.savefig(f'{nombre_archivo}.png', dpi=600, bbox_inches='tight', facecolor='white')
plt.savefig(f'{nombre_archivo}.pdf', bbox_inches='tight', facecolor='white')
print(f"¡Gráfico exportado exitosamente con la leyenda integrada en el centro!")
print(f"- {nombre_archivo}.png")
print(f"- {nombre_archivo}.pdf")

plt.show()