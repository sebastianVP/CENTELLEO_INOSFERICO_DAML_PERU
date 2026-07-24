import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuración profesional de alta resolución para tesis de maestría
plt.rcParams['figure.dpi'] = 600
plt.rcParams['font.family'] = 'DejaVu Sans'

# --- CONSTANTES DE FUENTE AGRESIVAS PARA MÁXIMA LEGIBILIDAD EN HOJA A4 ---
TITLE_SIZE = 20
SECTION_SIZE = 16
LABEL_SIZE = 14
TICK_SIZE = 13
SMALL_SIZE = 12


def generar_flujograma_entrenamiento(output_pdf: str, output_png: str) -> None:
    # Dimensiones equilibradas para que al reducirse a 16cm en Word, la letra mantenga escala real de libro
    fig, ax = plt.subplots(figsize=(14, 13.5))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.axis('off')
    
    # Sistema de coordenadas extendido hacia los márgenes laterales para absorber textos gigantes
    ax.set_xlim(-8, 108)
    ax.set_ylim(-15, 110)

    # =========================================================================
    # FUNCIONES AUXILIARES DE DIBUJO (OPTIMIZADAS PARA FUENTES GRANDES)
    # =========================================================================
    def draw_box(x, y, w, h, text, bg_color, edge_color, font_size=LABEL_SIZE):
        """Dibuja un rectángulo con bordes redondeados y texto gigante centrado."""
        ax.add_patch(patches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.7", facecolor=bg_color, edgecolor=edge_color, 
            linewidth=2.5, zorder=3
        ))
        ax.text(x, y, text, ha='center', va='center', fontsize=font_size,
                fontweight='bold', color='#1A2530', zorder=4, linespacing=1.5)

    def draw_diamond(x, y, w, h, text, bg_color='#FDEBD0', edge_color='#E67E22'):
        """Dibuja un rombo de decisión adaptado para texto de alta visibilidad."""
        verts = [(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)]
        poly = patches.Polygon(verts, facecolor=bg_color, edgecolor=edge_color, 
                               linewidth=2.5, zorder=3)
        ax.add_patch(poly)
        ax.text(x, y, text, ha='center', va='center', fontsize=SMALL_SIZE, 
                fontweight='bold', color='#1A2530', zorder=4, linespacing=1.4)

    def draw_path(points, color='#2C3E50', lw=2.5, linestyle='-', label=None, label_pos=None, rot=0):
        """Dibuja líneas de flujo con flechas robustas y visibles en impresión."""
        if len(points) > 2:
            x_coords = [p[0] for p in points[:-1]]
            y_coords = [p[1] for p in points[:-1]]
            ax.plot(x_coords, y_coords, color=color, lw=lw, linestyle=linestyle, zorder=2)
        
        x_pen, y_pen = points[-2]
        x_last, y_last = points[-1]
        
        # Flechas de escala incrementada (mutation_scale=26)
        ax.annotate('', xy=(x_last, y_last), xytext=(x_pen, y_pen),
                    arrowprops=dict(arrowstyle='->', color=color, lw=lw, 
                                    mutation_scale=26, linestyle=linestyle), zorder=2)
        
        if label and label_pos:
            ax.text(label_pos[0], label_pos[1], label, ha='center', va='center', 
                    fontsize=TICK_SIZE, fontweight='bold', color=color, rotation=rot,
                    bbox=dict(facecolor='#ffffff', edgecolor='none', alpha=0.9, pad=15), zorder=5)

    # =========================================================================
    # FONDO Y TÍTULO
    # =========================================================================
    ax.text(50, 105, "Flujo de Entrenamiento, Validación y Control Algorítmico", 
            ha='center', va='center', fontsize=TITLE_SIZE, fontweight='bold', color='#ffffff',
            bbox=dict(facecolor='#2C3E50', edgecolor='none', boxstyle='round,pad=0.7'), zorder=5)

    # Contenedor del bucle por Época (ajustado para dar espacio a las fuentes)
    ax.add_patch(patches.FancyBboxPatch(
        (10, 29), 80, 61,  
        boxstyle="round,pad=1.2", facecolor='#F8F9F9', edgecolor='#BDC3C7', 
        linewidth=2.2, linestyle='--', zorder=1
    ))
    ax.text(12, 88.5, "Bucle Interno (Por cada Época)", fontsize=SECTION_SIZE, 
            fontweight='bold', color='#7F8C8D', zorder=2, style='italic')

    # =========================================================================
    # NODOS (ANCHO EXPANDIDO PARA EVITAR DESBORDES DE TEXTO LARGO)
    # =========================================================================
    C_START = ('#D5F5E3', '#27AE60')  
    C_MODEL = ('#D6EAF8', '#2980B9')  
    C_LOSS  = ('#FDEDEC', '#E74C3C')  
    C_OPT   = ('#E8DAEF', '#8E44AD')  
    C_CALL  = ('#FCF3CF', '#F1C40F')  
    
    # Se incrementaron los anchos (w) significativamente para albergar la letra de 14pt
    draw_box(50, 96, 48, 6.2, "Inicio del Entrenamiento\n(Carga de Datos y Pesos)", *C_START)
    
    draw_box(50, 81, 58, 7.2, "Paso Hacia Adelante (Forward Pass)\nRed LSTM genera predicciones de S4", *C_MODEL)
    
    draw_box(50, 66, 74, 9.5, 
             "Función de Costo: Weighted Focal Loss\n"
             r"Penalización a errores severos: $\gamma=2.0$" + "\n"
             r"Ponderación asimétrica: $\alpha=50.0$ (si $S4 > 0.6$)", *C_LOSS)
    
    draw_box(50, 51, 58, 7.2, "Retropropagación y Optimización\n(Optimizador Adam)", *C_OPT)
    
    draw_box(50, 36, 58, 7.2, "Fase de Validación\n(Evaluación de Pérdida en Val_Loss)", *C_MODEL)
    
    # Callbacks en paralelo (Reducción de anchos y re-centrado para dejar aire en los costados)
    draw_box(26, 22, 42, 7.8, "ReduceLROnPlateau\n¿Pérdida estancada?\nReduce Learning Rate", *C_CALL)
    draw_box(74, 22, 42, 7.8, "Early Stopping\nMonitor: Val_Loss\n(Paciencia = 15 épocas)", *C_CALL)
    
    # Rombo de decisión ensanchado para albergar perfectamente el texto de 12pt
    draw_diamond(74, 6.5, 25, 9.5, "¿Sin mejora\nen 15\népocas?")
    
    draw_box(74, -8, 48, 6.2, "Fin del Entrenamiento\n(Restaura el mejor modelo)", *C_START)

    # =========================================================================
    # RUTAS Y FLECHAS (CALIBRACIÓN ANTISOLAPAMIENTO)
    # =========================================================================
    # Canal central
    draw_path([(50, 93), (50, 84.6)])          
    draw_path([(50, 77.4), (50, 70.8)])        
    draw_path([(50, 61.3), (50, 54.6)])        
    draw_path([(50, 47.4), (50, 39.6)])        

    # Conexiones a Callbacks
    draw_path([(50, 32.4), (50, 29), (26, 29), (26, 25.9)])  
    draw_path([(50, 32.4), (50, 29), (74, 29), (74, 25.9)])  

    # Control de Parada Temprana
    draw_path([(74, 18.1), (74, 11.3)])       
    draw_path([(74, 1.8), (74, -4.9)], label="Sí", label_pos=(74, -1.5)) 

    # Bucle de retorno (Siguiente Época) - Desplazado a X=99 para evitar colisiones
    draw_path([(86.5, 6.5), (99, 6.5), (99, 81), (79, 81)], 
              linestyle='--', label="No (Continuar)", label_pos=(101.5, 44), rot=-90)

    # Bucle adaptativo de Learning Rate - Retirado a X = 1.5 para el texto de la flecha
    draw_path([(5, 22), (1.5, 22), (1.5, 51), (21, 51)], 
              linestyle='--', color='#D35400', label="Ajusta\nLearning\nRate", label_pos=(1.5, 36.5))

    # =========================================================================
    # EXPORTACIÓN DE ALTA CALIDAD DE EDICIÓN
    # =========================================================================
    plt.subplots_adjust(
        hspace=0.55,
        top=0.96,
        bottom=0.04,
        left=0.04,
        right=0.98
    )
    
    plt.savefig(output_pdf, bbox_inches='tight', dpi=600)
    plt.savefig(output_png, bbox_inches='tight', dpi=600)
    plt.close()
    print(f"Completado con éxito: Fuentes ultra legibles para impresión A4 guardadas.")


if __name__ == "__main__":
    generar_flujograma_entrenamiento(
        'FIGURA_3_5_Flujo_Entrenamiento.pdf',
        'FIGURA_3_5_Flujo_Entrenamiento.png'
    )