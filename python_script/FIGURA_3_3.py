import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generar_diagrama_embudo(output_pdf, output_png):
    # Configuración de alta calidad
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['font.family'] = 'DejaVu Sans'

    fig, ax = plt.subplots(figsize=(10, 14))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # =========================================================================
    # FONDO: SILUETA DE EMBUDO (FUNNEL)
    # =========================================================================
    # Polígono que simula el embudo (más ancho arriba, más estrecho abajo)
    funnel_points = [
        [0.5, 12], [9.5, 12],   # Tope ancho
        [7.0, 7],               # Reducción media derecha
        [6.5, 2],               # Tubo inferior derecho
        [3.5, 2],               # Tubo inferior izquierdo
        [3.0, 7]                # Reducción media izquierda
    ]
    funnel = patches.Polygon(funnel_points, closed=True, fill=True, color='#EBF5FB', zorder=0)
    ax.add_patch(funnel)
    
    # Borde del embudo
    funnel_edge = patches.Polygon(funnel_points, closed=True, fill=False, edgecolor='#AED6F1', lw=3, zorder=1)
    ax.add_patch(funnel_edge)

    # =========================================================================
    # FUNCIONES AUXILIARES PARA CAJAS Y FLECHAS
    # =========================================================================
    def draw_step(y, width, height, title, desc, color_bg, color_border, font_color='#1a1a1a'):
        x_center = 5.0
        x_left = x_center - (width / 2)
        y_bottom = y - (height / 2)
        
        # Sombra
        ax.add_patch(patches.FancyBboxPatch(
            (x_left + 0.1, y_bottom - 0.1), width, height,
            boxstyle="round,pad=0.2", facecolor='#cccccc', edgecolor='none', alpha=0.4, zorder=2
        ))
        
        # Caja principal
        box = patches.FancyBboxPatch(
            (x_left, y_bottom), width, height,
            boxstyle="round,pad=0.2", facecolor=color_bg, edgecolor=color_border, lw=2, zorder=3
        )
        ax.add_patch(box)
        
        # Textos
        ax.text(x_center, y + 0.25, title, ha='center', va='center', fontsize=13, weight='bold', color=font_color, zorder=4)
        ax.text(x_center, y - 0.25, desc, ha='center', va='center', fontsize=11, color=font_color, zorder=4)

    def draw_arrow(y_start, y_end):
        ax.annotate("", xy=(5.0, y_end), xytext=(5.0, y_start),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.6,head_length=0.8", color='#34495E', lw=3),
                    zorder=2)

    # =========================================================================
    # CONSTRUCCIÓN DE LOS PASOS DEL EMBUDO
    # =========================================================================
    
    # 1. Extracción (Caja ancha)
    draw_step(11, 7.5, 1.4, 
              "1. Datos Crudos GNSS (Logs ISMR)", 
              "Lectura masiva de archivos de la estación Jicamarca.\n(Millones de registros multiconstelación)", 
              "#D4E6F1", "#2471A3")
    
    draw_arrow(10.3, 9.2)

    # 2. Limpieza
    draw_step(8.5, 6.5, 1.4, 
              "2. Limpieza y Curación de Datos", 
              "Eliminación de registros corruptos, imputación de\nvalores faltantes (NaNs) y sincronización temporal.", 
              "#A9CCE3", "#1F618D")

    draw_arrow(7.8, 6.7)

    # 3. Filtro de Elevación (Punto crítico - Resaltado en Rojo/Naranja)
    draw_step(6.0, 5.5, 1.5, 
              "3. Máscara de Elevación ($> 30^\circ$)", 
              "Filtrado espacial riguroso.\nRechazo de señales con efecto Multipath y\nruido troposférico en el horizonte.", 
              "#FADBD8", "#C0392B", font_color='#641E16')
    
    # Etiqueta lateral explicando por qué se eliminan datos aquí
    ax.text(7.9, 6.0, "Descarte del ~35%\nde los datos\n(Basura espacial)", 
            ha='left', va='center', color='#C0392B', fontsize=10, weight='bold',
            bbox=dict(facecolor='#FDEDEC', edgecolor='#C0392B', pad=0.3, boxstyle="larrow,pad=0.3"))

    draw_arrow(5.25, 4.2)

    # 4. Agregación Operativa
    draw_step(3.5, 4.8, 1.4, 
              "4. Estrategia de Agregación Operativa", 
              "Cálculo del valor máximo del índice $S_4$ por minuto\nentre todos los satélites visibles y filtrados.", 
              "#A3E4D7", "#117A65")

    draw_arrow(2.8, 1.7)

    # 5. Estructuración
    draw_step(1.0, 4.0, 1.4, 
              "5. Dataset Final Estructurado", 
              "Matrices secuenciales ($70 \\times 9$) listas\npara el entrenamiento Deep Learning.", 
              "#D5F5E3", "#1E8449")

    # =========================================================================
    # FORMATO Y EXPORTACIÓN
    # =========================================================================
    #ax.set_title("Figura 3.3: Embudo de preprocesamiento de datos y aplicación\nde la estrategia operativa de agregación", 
    #              fontsize=15, weight='bold', pad=20, color='#1a1a1a')
    
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.5, 13)
    ax.axis('off') # Ocultar ejes

    plt.tight_layout()
    plt.savefig(output_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(output_png, bbox_inches='tight', dpi=300)
    plt.close()

# Ejecución
generar_diagrama_embudo("Figura_3_3_Embudo_Preprocesamiento.pdf", "Figura_3_3_Embudo_Preprocesamiento.png")
print("¡Diagrama de embudo generado con éxito!")