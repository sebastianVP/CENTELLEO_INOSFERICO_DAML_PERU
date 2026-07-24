import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'

def generar_flujograma_entrenamiento(output_pdf: str, output_png: str) -> None:
    fig, ax = plt.subplots(figsize=(14, 13))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')
    ax.axis('off')
    
    # Sistema de coordenadas 0-100 para facilitar el posicionamiento
    ax.set_xlim(0, 100)
    ax.set_ylim(-15, 110)

    # =========================================================================
    # FUNCIONES AUXILIARES DE DIBUJO
    # =========================================================================
    def draw_box(x, y, w, h, text, bg_color, edge_color, font_size=11, font_weight='bold'):
        """Dibuja un rectángulo con bordes redondeados y texto centrado."""
        ax.add_patch(patches.FancyBboxPatch(
            (x - w/2, y - h/2), w, h,
            boxstyle="round,pad=0.5", facecolor=bg_color, edgecolor=edge_color, 
            linewidth=2.0, zorder=3
        ))
        ax.text(x, y, text, ha='center', va='center', fontsize=font_size,
                fontweight=font_weight, color='#1A2530', zorder=4, linespacing=1.6)

    def draw_diamond(x, y, w, h, text, bg_color='#FDEBD0', edge_color='#E67E22'):
        """Dibuja un rombo de decisión."""
        verts = [(x, y+h/2), (x+w/2, y), (x, y-h/2), (x-w/2, y)]
        poly = patches.Polygon(verts, facecolor=bg_color, edgecolor=edge_color, 
                               linewidth=2.0, zorder=3)
        ax.add_patch(poly)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, 
                fontweight='bold', color='#1A2530', zorder=4, linespacing=1.4)

    def draw_path(points, color='#2C3E50', lw=2.0, linestyle='-', label=None, label_pos=None, rot=0):
        """Dibuja una línea ortogonal con una flecha al final."""
        if len(points) > 2:
            x_coords = [p[0] for p in points[:-1]]
            y_coords = [p[1] for p in points[:-1]]
            ax.plot(x_coords, y_coords, color=color, lw=lw, linestyle=linestyle, zorder=2)
        
        x_pen, y_pen = points[-2]
        x_last, y_last = points[-1]
        
        # Segmento final con flecha
        ax.annotate('', xy=(x_last, y_last), xytext=(x_pen, y_pen),
                    arrowprops=dict(arrowstyle='->', color=color, lw=lw, 
                                    mutation_scale=20, linestyle=linestyle), zorder=2)
        
        if label and label_pos:
            ax.text(label_pos[0], label_pos[1], label, ha='center', va='center', 
                    fontsize=10, fontweight='bold', color=color, rotation=rot,
                    bbox=dict(facecolor='#ffffff', edgecolor='none', alpha=0.9, pad=1), zorder=5)

    # =========================================================================
    # FONDO Y TÍTULO
    # =========================================================================
    # Título principal
    ax.text(50, 105, "Flujo de Entrenamiento, Validación y Control Algorítmico", 
            ha='center', va='center', fontsize=16, fontweight='bold', color='#ffffff',
            bbox=dict(facecolor='#2C3E50', edgecolor='none', boxstyle='round,pad=0.6'), zorder=5)

    # Caja de fondo para el "Ciclo por Época"
    ax.add_patch(patches.FancyBboxPatch(
        (15, 29), 70, 61,  # x_izq, y_inf, ancho, alto
        boxstyle="round,pad=1.0", facecolor='#F8F9F9', edgecolor='#BDC3C7', 
        linewidth=2.0, linestyle='--', zorder=1
    ))
    ax.text(17, 88, "Bucle Interno (Por cada Época)", fontsize=12, 
            fontweight='bold', color='#7F8C8D', zorder=2, style='italic')

    # =========================================================================
    # NODOS (CAJAS Y ROMBOS)
    # =========================================================================
    # Paleta de colores
    C_START = ('#D5F5E3', '#27AE60')  # Verde
    C_MODEL = ('#D6EAF8', '#2980B9')  # Azul
    C_LOSS  = ('#FDEDEC', '#E74C3C')  # Rojo (Para destacar la penalización)
    C_OPT   = ('#E8DAEF', '#8E44AD')  # Morado
    C_CALL  = ('#FCF3CF', '#F1C40F')  # Amarillo (Control)
    
    draw_box(50, 96, 35, 6, "Inicio del Entrenamiento\n(Carga de Datos y Pesos)", *C_START)
    
    draw_box(50, 81, 45, 7, "Paso Hacia Adelante (Forward Pass)\nRed LSTM genera predicciones de S4", *C_MODEL)
    
    draw_box(50, 66, 60, 9, 
             "Función de Costo: Weighted Focal Loss\n"
             r"Penalización a errores severos: $\gamma=2.0$" + "\n"
             r"Ponderación asimétrica: $\alpha=50.0$ (si $S4 > 0.6$)", *C_LOSS)
    
    draw_box(50, 51, 45, 7, "Retropropagación y Optimización\n(Optimizador Adam)", *C_OPT)
    
    draw_box(50, 36, 45, 7, "Fase de Validación\n(Evaluación de Pérdida en Val_Loss)", *C_MODEL)
    
    draw_box(26, 22, 38, 7.5, "ReduceLROnPlateau\n¿Pérdida estancada?\nReduce Learning Rate", *C_CALL)
    draw_box(74, 22, 38, 7.5, "Early Stopping\nMonitor: Val_Loss\n(Paciencia = 15 épocas)", *C_CALL)
    
    draw_diamond(74, 8, 18, 8, "¿Sin mejora\nen 15\népocas?")
    
    draw_box(74, -7, 35, 6, "Fin del Entrenamiento\n(Restaura el mejor modelo)", *C_START)

    # =========================================================================
    # RUTAS Y FLECHAS
    # =========================================================================
    # Flujo principal central
    draw_path([(50, 93), (50, 84.5)])          # Start -> Forward
    draw_path([(50, 77.5), (50, 70.5)])        # Forward -> Loss
    draw_path([(50, 61.5), (50, 54.5)])        # Loss -> Optimizador
    draw_path([(50, 47.5), (50, 39.5)])        # Optimizador -> Val

    # División hacia los Callbacks
    draw_path([(50, 32.5), (50, 29), (26, 29), (26, 25.75)])  # Val -> ReduceLR
    draw_path([(50, 32.5), (50, 29), (74, 29), (74, 25.75)])  # Val -> EarlyStop

    # Control de Early Stopping
    draw_path([(74, 18.25), (74, 12)])         # EarlyStop -> Diamond
    draw_path([(74, 4), (74, -4)], label="Sí", label_pos=(74, 0)) # Diamond -> End

    # Bucle de retorno (Siguiente Época)
    draw_path([(83, 8), (95, 8), (95, 81), (72.5, 81)], 
              linestyle='--', label="No (Continuar)", label_pos=(96.5, 45), rot=-90)

    # Bucle de actualización de Learning Rate
    draw_path([(7, 22), (4, 22), (4, 51), (27.5, 51)], 
              linestyle='--', color='#D35400', label="Ajusta\nLearning\nRate", label_pos=(4, 38))

    # =========================================================================
    # RENDERIZADO Y GUARDADO
    # =========================================================================
    plt.tight_layout()
    plt.savefig(output_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(output_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Diagrama de Flujo guardado como: '{output_pdf}' y '{output_png}'")


if __name__ == "__main__":
    generar_flujograma_entrenamiento(
        'FIGURA_3_5_Flujo_Entrenamiento.pdf',
        'FIGURA_3_5_Flujo_Entrenamiento.png'
    )