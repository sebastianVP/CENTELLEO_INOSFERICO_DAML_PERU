import matplotlib.pyplot as plt
import numpy as np

# Configuración profesional de alta resolución para tesis de maestría
plt.rcParams['figure.dpi'] = 600
plt.rcParams['font.family'] = 'DejaVu Sans'

# --- CONSTANTES DE FUENTE INCREMENTADAS UN 25% EXTRA PARA MÁXIMA VISIBILIDAD ---
PANEL_TITLE_SIZE = 19  # Antes 15 (~25% inc.)
LABEL_SIZE = 16.5      # Antes 13 (~25% inc.)
TICK_SIZE = 14.5       # Antes 11.5 (~25% inc.)
VALUE_SIZE = 14        # Antes 11 (~25% inc.)


def generar_figura_4_1_sin_superposicion(output_pdf: str, output_png: str) -> None:
    # ➔ SOLUCIÓN: Incremento del tamaño de la figura en un 25% para dar soporte a las fuentes grandes
    # Pasamos de figsize=(15, 6.5) a (18.75, 8.2)
    fig, (ax_bar, ax_donut) = plt.subplots(1, 2, figsize=(18.75, 8.2), gridspec_kw={'width_ratios': [1.35, 1]})
    fig.patch.set_facecolor('#ffffff')
    
    # =========================================================================
    # PANEL IZQUIERDO: DISTRIBUCIÓN ESTACIONAL (FUENTES +25%)
    # =========================================================================
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Set', 'Oct', 'Nov', 'Dic']
    dias_eventos = [5, 14, 12, 3, 0, 0, 0, 2, 15, 18, 4, 1]
    tasas_actividad = [16.1, 50.0, 38.7, 10.0, 0.0, 0.0, 0.0, 6.4, 50.0, 58.0, 13.3, 3.2]
    
    colores_barras = ['#2980B9' if d >= 10 else '#AED6F1' for d in dias_eventos]
    
    bars = ax_bar.bar(meses, dias_eventos, color=colores_barras, edgecolor='#154360', linewidth=1.8, zorder=3)
    ax_bar.set_title("Actividad Mensual de Eventos Extremos ($S4 \geq 0.6$)", fontsize=PANEL_TITLE_SIZE, fontweight='bold', pad=20, color='#2C3E50')
    ax_bar.set_ylabel("Días con Eventos Registrados", fontsize=LABEL_SIZE, fontweight='bold', color='#154360')
    ax_bar.set_ylim(0, 22)
    ax_bar.tick_params(axis='x', labelsize=TICK_SIZE)
    ax_bar.tick_params(axis='y', labelsize=TICK_SIZE)
    ax_bar.grid(axis='y', linestyle='--', alpha=0.4, zorder=0)
    ax_bar.spines['top'].set_visible(False)
    
    # Valores numéricos sobre las barras aumentados
    for bar in bars:
        yval = bar.get_height()
        if yval > 0:
            ax_bar.text(bar.get_x() + bar.get_width()/2, yval + 0.4, int(yval), 
                        ha='center', va='bottom', fontsize=VALUE_SIZE, fontweight='bold', color='#154360')

    ax_line = ax_bar.twinx()
    line_plot = ax_line.plot(meses, tasas_actividad, color='#E74C3C', marker='o', linestyle='-', 
                             linewidth=3.8, markersize=10, zorder=4, label='Tasa de Actividad (%)')
    ax_line.set_ylabel("Tasa de Actividad Mensual (%)", fontsize=LABEL_SIZE, fontweight='bold', color='#E74C3C', rotation=270, labelpad=28)
    ax_line.set_ylim(-5, 70) 
    ax_line.spines['top'].set_visible(False)
    ax_line.spines['right'].set_color('#E74C3C')
    ax_line.tick_params(axis='y', colors='#E74C3C', labelsize=TICK_SIZE)
    
    # Leyenda con tamaño incrementado un 25% y un poco más abajo para evitar colisiones
    ax_bar.plot([], [], color='#2980B9', label='Días con Eventos', linewidth=7) 
    lines, labels = ax_bar.get_legend_handles_labels()
    lines2, labels2 = ax_line.get_legend_handles_labels()
    ax_bar.legend(lines + lines2, labels + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False, fontsize=TICK_SIZE)

    # =========================================================================
    # PANEL DERECHO: GRÁFICO DE ANILLO (FUENTES +25%)
    # =========================================================================
    clases = ['Calma / Leve\n($S4 < 0.3$)', 'Moderado\n($0.3 \leq S4 < 0.6$)', 'Extremo\n($S4 \geq 0.6$)']
    porcentajes = [94.50, 5.22, 0.28]
    colores_donut = ['#D6EAF8', '#F5B041', '#C0392B']
    explode = (0.02, 0.06, 0.18) 
    
    ax_donut.set_title("Proporción de Clases (Desbalance Severo)", fontsize=PANEL_TITLE_SIZE, fontweight='bold', pad=20, color='#2C3E50')
    
    wedges, texts = ax_donut.pie(
        porcentajes, 
        explode=explode, 
        colors=colores_donut, 
        startangle=160, 
        wedgeprops=dict(width=0.4, edgecolor='w', linewidth=3.0)
    )
    
    bbox_props = dict(boxstyle="square,pad=0.5", fc="w", ec="k", lw=0.9)
    kw = dict(arrowprops=dict(arrowstyle="-", lw=1.5), bbox=bbox_props, zorder=0, va="center")
    
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        
        # ➔ Ajuste de dispersión geométrica para que la letra grande no se encime
        x_text = 1.45 * np.sign(x)
        y_text = 1.35 * y
        
        if i == 1: 
            y_text += 0.30 
            x_text = 1.65 * np.sign(x)
        elif i == 2: 
            y_text -= 0.55 
            x_text = 1.55 * np.sign(x)
        
        if i == 2:
            bbox_props_ext = dict(boxstyle="round,pad=0.6", fc="#FDEDEC", ec="#C0392B", lw=2.0)
            ax_donut.annotate(f"{clases[i]}\n{porcentajes[i]}%", xy=(x, y), xytext=(x_text, y_text),
                              horizontalalignment=horizontalalignment, **{**kw, 'bbox': bbox_props_ext},
                              fontsize=TICK_SIZE, fontweight='bold', color='#C0392B')
        else:
            ax_donut.annotate(f"{clases[i]}\n{porcentajes[i]}%", xy=(x, y), xytext=(x_text, y_text),
                              horizontalalignment=horizontalalignment, **kw,
                              fontsize=TICK_SIZE, fontweight='bold')

    # Ajuste del círculo interno central y su texto integrado (+25%)
    centro = plt.Circle((0,0), 0.55, fc='white')
    ax_donut.add_artist(centro)
    ax_donut.text(0, 0, "Total:\n100%", ha='center', va='center', fontsize=PANEL_TITLE_SIZE, fontweight='bold', color='#34495E')

    # =========================================================================
    # RECALIBRACIÓN DE MÁRGENES PARA LA NUEVA ESCALA
    # =========================================================================
    plt.subplots_adjust(
        top=0.90,       # Mayor espacio en la parte superior para títulos de 19pt
        bottom=0.15,    # Más holgura en la base para absorber la leyenda grande
        left=0.06,      
        right=0.92,     # Mayor espacio a la derecha para las etiquetas desplazadas del donut
        wspace=0.42     # Mayor espacio de separación entre los dos subplots
    )
    
    # Guardado directo a resolución de imprenta (600 DPI)
    plt.savefig(output_pdf, bbox_inches='tight', dpi=600)
    plt.savefig(output_png, bbox_inches='tight', dpi=600)
    plt.close()
    
    print(f"Modificación completada con éxito. Archivos escalados listos.")


if __name__ == "__main__":
    generar_figura_4_1_sin_superposicion(
        'FIGURA_4_1_Distribucion_Desbalance_Escalado.pdf',
        'FIGURA_4_1_Distribucion_Desbalance_Escalado.png'
    )