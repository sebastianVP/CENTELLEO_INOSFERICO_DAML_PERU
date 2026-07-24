import matplotlib.pyplot as plt
import numpy as np

# Configuración profesional de alta resolución para tesis de maestría
plt.rcParams['figure.dpi'] = 600
plt.rcParams['font.family'] = 'DejaVu Sans'

# --- CONSTANTES DE FUENTE MAXIMIZADAS A NIVEL ULTRA-GIGANTE ---
PANEL_TITLE_SIZE = 30  # Títulos principales de cada panel
LABEL_SIZE = 26        # Etiquetas de los ejes (Días, Tasa, etc.)
TICK_SIZE = 22         # Meses, números de los ejes y textos de leyendas
VALUE_SIZE = 20        # Valores numéricos sobre las barras


def generar_figura_4_1_sin_superposicion(output_pdf: str, output_png: str) -> None:
    # Ajustamos las dimensiones generales incrementando la altura para acomodar textos más grandes
    fig, (ax_bar, ax_donut) = plt.subplots(1, 2, figsize=(23.5, 10.0), gridspec_kw={'width_ratios': [1.35, 1]})
    fig.patch.set_facecolor('#ffffff')
    
    # =========================================================================
    # PANEL IZQUIERDO: DISTRIBUCIÓN ESTACIONAL
    # =========================================================================
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Set', 'Oct', 'Nov', 'Dic']
    dias_eventos = [5, 14, 12, 3, 0, 0, 0, 2, 15, 18, 4, 1]
    tasas_actividad = [16.1, 50.0, 38.7, 10.0, 0.0, 0.0, 0.0, 6.4, 50.0, 58.0, 13.3, 3.2]
    
    colores_barras = ['#2980B9' if d >= 10 else '#AED6F1' for d in dias_eventos]
    
    bars = ax_bar.bar(meses, dias_eventos, color=colores_barras, edgecolor='#154360', linewidth=2.5, zorder=3)
    ax_bar.set_title("Actividad Mensual de Eventos Extremos ($S4 \geq 0.6$)", fontsize=PANEL_TITLE_SIZE, fontweight='bold', pad=25, color='#2C3E50')
    ax_bar.set_ylabel("Días con Eventos Registrados", fontsize=LABEL_SIZE, fontweight='bold', color='#154360', labelpad=15)
    ax_bar.set_ylim(0, 22)  # Ajustado a 22 para que el número '18' no toque el borde del recuadro con fuente 20
    ax_bar.tick_params(axis='x', labelsize=TICK_SIZE, pad=10)
    ax_bar.tick_params(axis='y', labelsize=TICK_SIZE)
    ax_bar.grid(axis='y', linestyle='--', alpha=0.4, zorder=0)
    ax_bar.spines['top'].set_visible(False)
    
    for bar in bars:
        yval = bar.get_height()
        if yval > 0:
            ax_bar.text(bar.get_x() + bar.get_width()/2, yval + 0.4, int(yval), 
                        ha='center', va='bottom', fontsize=VALUE_SIZE, fontweight='bold', color='#154360')

    ax_line = ax_bar.twinx()
    line_plot = ax_line.plot(meses, tasas_actividad, color='#E74C3C', marker='o', linestyle='-', 
                             linewidth=5.0, markersize=13, zorder=4, label='Tasa de Actividad (%)')
    ax_line.set_ylabel("Tasa de Actividad Mensual (%)", fontsize=LABEL_SIZE, fontweight='bold', color='#E74C3C', rotation=270, labelpad=45)
    ax_line.set_ylim(-5, 75) 
    ax_line.spines['top'].set_visible(False)
    ax_line.spines['right'].set_color('#E74C3C')
    ax_line.tick_params(axis='y', colors='#E74C3C', labelsize=TICK_SIZE)
    
    ax_bar.plot([], [], color='#2980B9', label='Días con Eventos', linewidth=10) 
    lines, labels = ax_bar.get_legend_handles_labels()
    lines2, labels2 = ax_line.get_legend_handles_labels()
    
    # Leyenda muy pegada al gráfico (bbox_to_anchor 0.5, -0.16)
    ax_bar.legend(lines + lines2, labels + labels2, loc='upper center', bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False, fontsize=TICK_SIZE)

    # =========================================================================
    # PANEL DERECHO: GRÁFICO DE ANILLO (PROPORCIÓN DE CLASES)
    # =========================================================================
    clases = ['Calma / Leve\n($S4 < 0.3$)', 'Moderado\n($0.3 \leq S4 < 0.6$)', 'Extremo\n($S4 \geq 0.6$)']
    porcentajes = [94.50, 5.22, 0.28]
    colores_donut = ['#D6EAF8', '#F5B041', '#C0392B']
    explode = (0.02, 0.06, 0.18) 
    
    ax_donut.set_title("Proporción de Clases (Desbalance Severo)", fontsize=PANEL_TITLE_SIZE, fontweight='bold', pad=25, color='#2C3E50')
    
    wedges, texts = ax_donut.pie(
        porcentajes, 
        explode=explode, 
        colors=colores_donut, 
        startangle=160, 
        wedgeprops=dict(width=0.4, edgecolor='w', linewidth=4.5)
    )
    
    bbox_props = dict(boxstyle="square,pad=0.7", fc="w", ec="k", lw=1.5)
    kw = dict(arrowprops=dict(arrowstyle="-", lw=2.2), bbox=bbox_props, zorder=0, va="center")
    
    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        
        # Posiciones base para los textos
        x_text = 1.50 * np.sign(x)
        y_text = 1.40 * y
        
        # Mantener el bloque "Moderado" muy pegado pero tolerando la fuente gigante
        if i == 1: 
            y_text += 0.15    
            x_text = 1.35 * np.sign(x)  
        elif i == 2: 
            y_text -= 0.72
            x_text = 1.60 * np.sign(x)
        
        if i == 2:
            bbox_props_ext = dict(boxstyle="round,pad=0.8", fc="#FDEDEC", ec="#C0392B", lw=2.8)
            ax_donut.annotate(f"{clases[i]}\n{porcentajes[i]}%", xy=(x, y), xytext=(x_text, y_text),
                              horizontalalignment=horizontalalignment, **{**kw, 'bbox': bbox_props_ext},
                              fontsize=TICK_SIZE, fontweight='bold', color='#C0392B')
        else:
            ax_donut.annotate(f"{clases[i]}\n{porcentajes[i]}%", xy=(x, y), xytext=(x_text, y_text),
                              horizontalalignment=horizontalalignment, **kw,
                              fontsize=TICK_SIZE, fontweight='bold')

    centro = plt.Circle((0,0), 0.55, fc='white')
    ax_donut.add_artist(centro)
    ax_donut.text(0, 0, "Total:\n100%", ha='center', va='center', fontsize=PANEL_TITLE_SIZE, fontweight='bold', color='#34495E')

    # =========================================================================
    # RECALIBRACIÓN GEOMÉTRICA DE BORDES Y PARÁMETROS DE POSICIÓN
    # =========================================================================
    plt.subplots_adjust(
        top=0.85,       
        bottom=0.22,    
        left=0.08,      
        right=0.90,     
        wspace=0.62     
    )
    
    # Desplazamiento sutil del bloque derecho hacia abajo para compensar los títulos masivos
    pos = ax_donut.get_position()
    ax_donut.set_position([pos.x0, pos.y0 - 0.03, pos.width, pos.height])
    
    # Guardado directo de calidad de publicación
    plt.savefig(output_pdf, bbox_inches='tight', dpi=600)
    plt.savefig(output_png, bbox_inches='tight', dpi=600)
    plt.close()
    
    print(f"Modificación completada: Fuentes escaladas a tamaño gigante sin perder las compactaciones.")


if __name__ == "__main__":
    generar_figura_4_1_sin_superposicion(
        'FIGURA_4_1_Distribucion_Desbalance_Gigante.pdf',
        'FIGURA_4_1_Distribucion_Desbalance_Gigante.png'
    )