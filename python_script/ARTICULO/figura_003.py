import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

def generar_grafico3_tecnico(df, target_col="S4", umbral_s4=0.6, output_path="Figura3_Desbalance_S4_IEEE.png"):
    # ============================================================
    # 1. Configuración Estética IEEE / Publication Grade
    # ============================================================
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['mathtext.fontset'] = 'stix'
    
    s4_data = df[target_col].dropna()
    n_total = len(s4_data)
    
    n_severo = (s4_data >= umbral_s4).sum()
    n_calma = n_total - n_severo
    pct_severo = (n_severo / n_total) * 100
    pct_calma = (n_calma / n_total) * 100

    # Paleta de colores técnica y elegante
    color_calma = '#243B55'   # Azul noche / Slate
    color_severo = '#E63946'  # Rojo Carmesí / Alert
    color_bg_box = '#FFEBEE'   # Fondo tenue para llamada de texto
    color_border = '#B71C1C'

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), dpi=300, gridspec_kw={'width_ratios': [1.35, 1.0]})
    fig.patch.set_facecolor('#FFFFFF')

    # ============================================================
    # PANEL A: HISTOGRAMA LOGARÍTMICO REFINADO
    # ============================================================
    counts, bins, patches = ax1.hist(s4_data, bins=45, range=(0.0, 1.0), edgecolor='white', lw=0.4, log=True)

    # Coloreado dinámico según umbral
    for bin_left, patch in zip(bins[:-1], patches):
        if bin_left >= umbral_s4 - 0.001:
            patch.set_facecolor(color_severo)
        else:
            patch.set_facecolor(color_calma)

    # Línea vertical del umbral
    ax1.axvline(x=umbral_s4, color=color_border, linestyle='--', linewidth=1.8, zorder=5)

    # Ajuste del límite superior de Y para dar espacio a la leyenda y etiquetas
    ax1.set_ylim(bottom=1, top=counts.max() * 12)

    # Anotación del Umbral (Posicionada limpiamente sin tapar datos)
    ax1.text(umbral_s4 + 0.025, counts.max() * 0.15, 
             f'Umbral Crítico\n$S_4 \geq {umbral_s4}$', 
             color=color_border, fontsize=8.5, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.35', facecolor=color_bg_box, edgecolor=color_border, lw=0.8, alpha=0.95))

    # Formato de ejes
    ax1.set_title("(A) Distribución de Frecuencia del Índice $S_4$", fontsize=10.5, fontweight='bold', pad=10, color='#1A1A1A')
    ax1.set_xlabel("Índice de Centelleo ($S_4$)", fontsize=9.5, fontweight='bold', labelpad=6)
    ax1.set_ylabel("Frecuencia de Muestras [Escala $\log_{10}$]", fontsize=9.5, fontweight='bold', labelpad=6)
    ax1.set_xlim(0.0, 1.0)
    
    ax1.grid(True, which="both", ls=":", alpha=0.35, color='#888888')
    ax1.tick_params(axis='both', which='major', labelsize=8.5)

    # Leyenda aislada en esquina superior derecha
    legend_elements = [
        Patch(facecolor=color_calma, label=f'Calma / Moderado ($S_4 < {umbral_s4}$)'),
        Patch(facecolor=color_severo, label=f'Evento Severo ($S_4 \geq {umbral_s4}$)')
    ]
    ax1.legend(handles=legend_elements, loc='upper right', fontsize=8.5, framealpha=0.95, edgecolor='#CCCCCC')

    # ============================================================
    # PANEL B: DONUT CHART TÉCNICO CON FLECHA DE PRECISIÓN
    # ============================================================
    sizes = [n_calma, n_severo]
    colors = [color_calma, color_severo]
    explode = (0, 0.18)  # Desplazar la rebanada de eventos severos

    wedges, texts, autotexts = ax2.pie(
        sizes, explode=explode, colors=colors,
        autopct='%1.2f%%', pctdistance=0.75, startangle=30,
        wedgeprops=dict(width=0.38, edgecolor='white', linewidth=1.5)
    )

    # Formato del porcentaje de la clase Calma (dentro de la dona)
    autotexts[0].set_color('white')
    autotexts[0].set_fontsize(9.5)
    autotexts[0].set_fontweight('bold')

    # Ocultar la etiqueta automática pequeña del gajo rojo para no amontonar
    autotexts[1].set_visible(False)

    # Texto central de Total de Muestras
    ax2.text(0, 0, f"Total Muestras\n$N = {n_total:,}$", ha='center', va='center', 
             fontsize=9.0, fontweight='bold', color='#1A1A1A')

    # Cálculo trigonométrico exacto de la posición del gajo rojo para la flecha
    theta = (wedges[1].theta1 + wedges[1].theta2) / 2.0
    x_slice = 0.85 * np.cos(np.deg2rad(theta))
    y_slice = 0.85 * np.sin(np.deg2rad(theta))

    # Anotación con flecha apuntando EXACTAMENTE al gajo rojo
    ax2.annotate(
        f"Eventos Severos ($S_4 \geq {umbral_s4}$)\n$N = {n_severo:,}$ ({pct_severo:.2f}%)",
        xy=(x_slice, y_slice), xytext=(0.25, -0.85),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.15", color=color_border, lw=1.3),
        fontsize=8.5, fontweight='bold', color=color_border, ha='left',
        bbox=dict(boxstyle="round,pad=0.4", facecolor=color_bg_box, edgecolor=color_border, lw=0.8)
    )

    ax2.set_title("(B) Proporción Relativa de Clases", fontsize=10.5, fontweight='bold', pad=10, color='#1A1A1A')

    # ============================================================
    # Guardado de la imagen
    # ============================================================
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.show()

# Ejecución de la función:
# generar_grafico3_tecnico(df_final, target_col="S4", umbral_s4=0.6)

# Ejemplo de uso con tu pipeline:

import os
import numpy as np
import pandas as pd

import os
ESTACION = ["JICAMARCA","HUANCAYO","PIURA","CUZCO","PUCALLPA","AYACUCHO","TACNA","IQUITOS"]
ABREVIATURA = ["jic","hyo","piu","cuz","pucall","aya","tac","iqui"]
print("El número de Estaciones GNSS del IGP en el Peru es: ",len(ESTACION))

N_ESTACION  = 0 # dependiendo del orden podemos seleccionar la ubicacion

PATH       ="/home/soporte/Documents/CENTELLEO_INOSFERICO_DAML_PERU/notebook"
filename   = f"df_max_s4_all_{ABREVIATURA[N_ESTACION]}.csv"
file_base  = os.path.join(PATH,filename)
print(file_base)
s4_param_JIC   = pd.read_csv(file_base)
s4_param_JIC.describe()
# generar_grafico3_desbalance(df_final, target_col="S4", umbral_s4=0.6)
generar_grafico3_tecnico(s4_param_JIC, target_col="S4", umbral_s4=0.6)