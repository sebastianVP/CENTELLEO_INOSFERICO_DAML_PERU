import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generar_diagrama_embudo(output_pdf, output_png):
    # Configuración de alta calidad
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['font.family'] = 'DejaVu Sans'

    # 1. Lienzo ligeramente más ancho para acomodar cajas grandes y etiqueta lateral
    fig, ax = plt.subplots(figsize=(11, 15)) 
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # =========================================================================
    # FONDO: SILUETA DE EMBUDO (FUNNEL) AMPLIADO
    # =========================================================================
    funnel_points = [
        [-0.2, 13.0], [10.2, 13.0], # Tope ancho
        [7.8, 7.5],                 # Reducción media derecha
        [7.0, 1.0],                 # Tubo inferior derecho
        [3.0, 1.0],                 # Tubo inferior izquierdo
        [2.2, 7.5]                  # Reducción media izquierda
    ]
    funnel = patches.Polygon(funnel_points, closed=True, fill=True, color='#EBF5FB', zorder=0)
    ax.add_patch(funnel)
    
    funnel_edge = patches.Polygon(funnel_points, closed=True, fill=False, edgecolor='#AED6F1', lw=3, zorder=1)
    ax.add_patch(funnel_edge)

    # =========================================================================
    # FUNCIONES AUXILIARES MEJORADAS
    # =========================================================================
    def draw_step(y, width, height, title, desc, color_bg, color_border, font_color='#1a1a1a'):
        x_center = 5.0
        x_left = x_center - (width / 2)
        y_bottom = y - (height / 2)
        
        # Sombra adaptada
        ax.add_patch(patches.FancyBboxPatch(
            (x_left + 0.15, y_bottom - 0.15), width, height,
            boxstyle="round,pad=0.2", facecolor='#cccccc', edgecolor='none', alpha=0.4, zorder=2
        ))
        
        # Caja principal (bordes más gruesos lw=2.5)
        box = patches.FancyBboxPatch(
            (x_left, y_bottom), width, height,
            boxstyle="round,pad=0.2", facecolor=color_bg, edgecolor=color_border, lw=2.5, zorder=3
        )
        ax.add_patch(box)
        
        # Textos: Posición relativa al nuevo tamaño de altura (TAMAÑOS AUMENTADOS: 18 y 15)
        ax.text(x_center, y + height*0.22, title, ha='center', va='center', 
                fontsize=18, weight='bold', color=font_color, zorder=4)
        ax.text(x_center, y - height*0.18, desc, ha='center', va='center', 
                fontsize=15, color=font_color, zorder=4, linespacing=1.4)

    def draw_arrow(y_start, y_end):
        # Flechas más gruesas y notorias
        ax.annotate("", xy=(5.0, y_end), xytext=(5.0, y_start),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.8,head_length=1.0", color='#34495E', lw=4),
                    zorder=2)

    # =========================================================================
    # CONSTRUCCIÓN DE LOS PASOS (Espaciado Y ajustado para cajas de altura 2.0)
    # =========================================================================
    
    # 1. Extracción (Caja ancha)
    draw_step(11.6, 9.0, 2.0, 
              "1. Datos Crudos GNSS (Logs ISMR)", 
              "Lectura masiva de archivos de la estación Jicamarca.\n(Millones de registros multiconstelación)", 
              "#D4E6F1", "#2471A3")
    
    draw_arrow(10.6, 9.8)

    # 2. Limpieza
    draw_step(8.8, 8.0, 2.0, 
              "2. Limpieza y Curación de Datos", 
              "Eliminación de registros corruptos, imputación\nde valores faltantes (NaNs) y sincronización temporal.", 
              "#A9CCE3", "#1F618D")

    draw_arrow(7.8, 7.0)

    # 3. Filtro de Elevación
    draw_step(6.0, 6.8, 2.0, 
              "3. Máscara de Elevación ($> 30^\circ$)", 
              "Filtrado espacial riguroso.\nRechazo de señales con efecto Multipath\ny ruido troposférico en el horizonte.", 
              "#FADBD8", "#C0392B", font_color='#641E16')
    
    # Etiqueta lateral recolocada y con fuente 14
    ax.text(8.8, 6.0, "Descarte del ~35%\nde los datos\n(Basura espacial)", 
            ha='left', va='center', color='#C0392B', fontsize=14, weight='bold', linespacing=1.3,
            bbox=dict(facecolor='#FDEDEC', edgecolor='#C0392B', pad=0.5, boxstyle="larrow,pad=0.4", lw=1.5))

    draw_arrow(5.0, 4.2)

    # 4. Agregación Operativa
    draw_step(3.2, 5.8, 2.0, 
              "4. Agregación Operativa", 
              "Cálculo del valor máximo del índice $S_4$ por minuto\nentre todos los satélites visibles y filtrados.", 
              "#A3E4D7", "#117A65")

    draw_arrow(2.2, 1.4)

    # 5. Estructuración
    draw_step(0.4, 5.0, 2.0, 
              "5. Dataset Final Estructurado", 
              "Matrices secuenciales ($70 \\times 9$)\nlistas para el entrenamiento\nde Deep Learning.", 
              "#D5F5E3", "#1E8449")

    # =========================================================================
    # FORMATO Y EXPORTACIÓN
    # =========================================================================
    
    # Expandimos el eje X para que la etiqueta lateral que agregamos no se corte
    ax.set_xlim(-0.5, 12.5) 
    ax.set_ylim(-1.0, 13.5)
    ax.axis('off') # Ocultar ejes

    plt.tight_layout()
    plt.savefig(output_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(output_png, bbox_inches='tight', dpi=300)
    plt.close()

# Ejecución
generar_diagrama_embudo("Figura_3_3_Embudo_Preprocesamiento_Mejorado.pdf", "Figura_3_3_Embudo_Preprocesamiento_Mejorado.png")
print("¡Diagrama de embudo mejorado generado con éxito!")