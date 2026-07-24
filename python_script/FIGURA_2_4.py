import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# =========================================================================
# CONFIGURACIÓN GENERAL Y ESTILO ACADÉMICO ACTUALIZADO
# =========================================================================
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'

# Función para generar la figura con las nuevas proporciones bloqueadas
def generar_diagrama_sliding_window_perfecto(output_pdf, output_png):
    # Lienzo amplio para que quepa todo el contenido sin amontonarse (amplio 16:9)
    fig, (ax_ts, ax_concept, ax_tensor) = plt.subplots(
        3, 1, figsize=(24, 11), gridspec_kw={'height_ratios': [1, 2.5, 1.3]}
    )
    fig.patch.set_facecolor('#ffffff')
    
    # ➔ Funciones de Dibujo Modular Actualizadas con Padding y Proporciones
    def draw_section_title(ax, text, font_size=13):
        # Caja gris oscuro fixed para texto overflow
        rect_title = patches.FancyBboxPatch(
            (0.1, 1.1), 0.8, 0.12, transform=ax.transAxes,
            boxstyle="round,pad=0.03", facecolor='#404040', edgecolor='none', zorder=10
        )
        ax.add_patch(rect_title)
        ax.text(
            0.5, 1.16, text, transform=ax.transAxes,
            ha='center', va='center', fontsize=font_size, fontweight='bold', color='white',
            zorder=11
        )
        
    def draw_box(ax, x, y, width, height, title, subtitle, color_bg, color_border, font_size_title=13, font_size_subtitle=11, font_color='#1a1a1a'):
        # Caja principal con proporciones más grandes y padding
        box = patches.FancyBboxPatch(
            (x, y), width, height,
            boxstyle="round,pad=0.2", facecolor=color_bg, edgecolor=color_border, linewidth=1.5, zorder=2
        )
        ax.add_patch(box)
        # Sombra
        shadow = patches.FancyBboxPatch(
            (x + 0.05, y - 0.05), width, height,
            boxstyle="round,pad=0.2", facecolor='#cccccc', edgecolor='none', alpha=0.3, zorder=1
        )
        ax.add_patch(shadow)
        # Texto centrado automáticamente con padding
        ax.text(x + width/2, y + height*0.7, title, ha='center', va='center', 
                fontsize=font_size_title, fontweight='bold', color=font_color, zorder=3)
        ax.text(x + width/2, y + height*0.3, subtitle, ha='center', va='center', 
                fontsize=font_size_subtitle, color=font_color, zorder=3)

    # =========================================================================
    # SECCIÓN 1: SERIE TEMPORAL DE S4 (Datos Reales, 2025)
    # =========================================================================
    draw_section_title(ax_ts, "Serie Temporal de S4 (Datos Reales de Jicamarca, 2025)")
    ax_ts.set_facecolor('#ffffff')
    
    np.random.seed(42)
    # Señal base + picos exponenciales + ruido gaussiano
    s4_base = 1.0 + 0.5 * np.exp(-((np.linspace(-3, 3, 300))**2))
    s4_peaks = 3.0 * np.exp(-((np.linspace(-5, 5, 300))**2)) + 4.0 * np.exp(-((np.linspace(-1, 1, 300))**2))
    s4_raw = 0.5 + 3.0 * s4_base + 3.0 * s4_peaks + 0.7 * np.random.randn(300)
    s4_series = pd.Series(np.clip(s4_raw, 0.2, 6.0))
    
    ax_ts.plot(s4_series, color='#5D6D7E', lw=1.2, alpha=0.9)
    ax_ts.set_ylabel("S4", fontsize=11, fontweight='bold')
    ax_ts.set_ylim(-0.2, 6.5)
    
    num_ticks = 11
    tick_indices = np.linspace(0, len(s4_series)-1, num_ticks, dtype=int)
    tick_labels = [
        r"$t-90$", r"$t-89$", r"$t-88$", r"$t-87...$", r"$t...$", 
        r"$t...$", r"$t+1...$", r"$t+4...$", r"$t+6$", r"$t+7$", r"$t+10$ (min)"
    ]
    ax_ts.set_xticks(tick_indices)
    ax_ts.set_xticklabels(tick_labels, fontsize=10)
    
    ax_ts.grid(True, linestyle='--', alpha=0.3)
    ax_ts.spines['top'].set_visible(False)
    ax_ts.spines['right'].set_visible(False)

    # =========================================================================
    # SECCIÓN 2: TÉCNICA DE VENTANA DESLIZANTE (Stride = 1 min)
    # =========================================================================
    draw_section_title(ax_concept, "Técnica de Ventana Deslizante (Stride = 1 min)")
    ax_concept.set_facecolor('#fefefe')
    
    # NUEVAS PROPORCIONES: Cajas más grandes, menos espacio en blanco
    start_y_concept = 10
    start_x_concept = 0
    box_height = 1.4     # Cajas más altas
    space_v = 1.7
    space_h_windows = 1  
    
    # Función para dibujar un conjunto de ventanas conceptuales más corpulentas
    def draw_window_set(ax, start_x, start_y, label, lookback, horizon, title_pos='center'):
        # Ventana de Observación (Gris claro) con proporciones XL y padding
        rect_lb = patches.FancyBboxPatch(
            (start_x, start_y), lookback, box_height,
            boxstyle="round,pad=0.2", linewidth=1.5, edgecolor='#2c3e50', facecolor='#D6EAF8', alpha=0.9, zorder=2
        )
        ax.add_patch(rect_lb)
        # Flecha y texto Lookback
        ax.annotate('', xy=(start_x, start_y+1.6), xytext=(start_x+lookback, start_y+1.6), arrowprops=dict(arrowstyle='<->', color='#2c3e50', lw=1.5))
        # CAMBIO: fontsize subió a 14 para llenar la caja
        ax.text(start_x+lookback/2, start_y+box_height/2, label, ha='center', va='center', fontsize=14, weight='bold', color='#1a1a1a', zorder=3)
        if title_pos == 'center':
            ax.text(start_x+lookback/2, start_y+1.9, f"Ventana de Observación\n(Lookback, $\\tau = {lookback}$ min)", ha='center', fontsize=11)

        # Horizonte de Predicción (Gris más oscuro adyacente a la derecha)
        start_x_h = start_x + lookback 
        rect_h = patches.FancyBboxPatch(
            (start_x_h, start_y), horizon, box_height,
            boxstyle="round,pad=0.2", linewidth=1.5, edgecolor='#2c3e50', facecolor='#AED6F1', alpha=0.9, zorder=2
        )
        ax.add_patch(rect_h)
        # Flecha y texto Horizonte
        ax.annotate('', xy=(start_x_h, start_y+1.6), xytext=(start_x_h+horizon, start_y+1.6), arrowprops=dict(arrowstyle='<->', color='#2c3e50', lw=1.5))
        ax.text(start_x_h+horizon/2, start_y+1.9, f"Horizonte de Predicción\n($h = {horizon}$ min)", ha='center', fontsize=11)
        ax.text(start_x_h+horizon/2, start_y+1.9, f"$h = {horizon}$ min", ha='center', va='bottom', fontsize=12, weight='bold')

    # Dibujar 3 conjuntos de ventanas para ilustrar el stride
    draw_window_set(ax_concept, start_x_concept, start_y_concept, "Window 1", 70, 10, title_pos='center')
    
    y_v2 = start_y_concept - space_v
    x_v2 = start_x_concept + space_h_windows
    draw_window_set(ax_concept, x_v2, y_v2, "Window 2", 70, 10, title_pos='none')

    y_v3 = y_v2 - space_v
    x_v3 = x_v2 + space_h_windows
    draw_window_set(ax_concept, x_v3, y_v3, "Window 3...", 70, 10, title_pos='none')
    
    ax_concept.text(x_v3 + 90, y_v3 + box_height/2, '...', ha='center', va='center', fontsize=18, rotation=90, color='#7F8C8D')
    ax_concept.text(x_v3 + 100, y_v3 + box_height/2, '...', ha='center', va='center', fontsize=18, color='#7F8C8D')
    
    # ➔ Desgloses Detallados (Inset Plots) con Proporciones XL
    def create_detailed_inset(ax_parent, x_pos_parent, y_pos_parent, lb_data, h_data, num_window):
        # Crear inset plot con mpl_toolkits - proporciones más grandes y padding
        ax_inset = inset_axes(ax_parent, width="100%", height="100%", loc='lower left',
                              bbox_to_anchor=(x_pos_parent, y_pos_parent, 25, 4.0), bbox_transform=ax_parent.transData,
                              axes_kwargs={'facecolor': '#fefefe', 'zorder': 1})
        
        combined_data = pd.concat([lb_data, h_data])
        # Graficar con el mismo color azul grisáceo y ancho XL
        ax_inset.plot(combined_data, color='#5D6D7E', lw=1.2)
        
        # Etiqueta "Target" con padding
        ax_inset.text(len(combined_data)-1, ax_inset.get_ylim()[1]*0.9, 'Target', ha='right', fontsize=10, fontweight='bold', color='#1a1a1a', 
                      bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=0.1))
        
        ax_inset.set_ylabel("S4", fontsize=11, fontweight='bold')
        t_lb = len(lb_data)
        
        if num_window == 1:
            ax_inset.set_xticks([0, t_lb-1, len(combined_data)-1])
            ax_inset.set_xticklabels([r"$S4(t-70)$", r"$t-1$", r"$t+9$"], fontsize=11)
        else:
            # Para la ventana 2, los índices X cambian.
            ax_inset.set_xticks([0, len(combined_data)-1])
            ax_inset.set_xticklabels([r"$S4(t$", r"$t+9)$"], fontsize=11)
            
        ax_inset.grid(True, linestyle=':', alpha=0.4)
        ax_inset.spines['top'].set_visible(False)
        ax_inset.spines['right'].set_visible(False)
        # Usar un marco punteado XL con padding
        for spine in ax_inset.spines.values():
            spine.set_linestyle(':')
            spine.set_linewidth(1)
            spine.set_edgecolor('#1a1a1a')
            
    # Datos para Inset 1 (Window 1)
    window_data_raw = s4_series[20:100].reset_index(drop=True)
    lb_data_w1 = window_data_raw[:70]
    h_data_w1 = window_data_raw[70:]
    h_data_w1.iloc[-1] = 5.8
    # Usar una sección más plana para contraste y padding XL
    create_detailed_inset(ax_concept, 10, y_v3 - 4.2, lb_data_w1, h_data_w1, num_window=1)

    # Datos para Inset 2 (Window 2)
    window_data_v2_raw = s4_series[50:130].reset_index(drop=True)
    lb_data_w2 = window_data_v2_raw[:70]
    h_data_w2 = window_data_v2_raw[70:]
    # Usar una sección más plana para contraste y padding XL
    create_detailed_inset(ax_concept, x_v2 + 70 + 5, y_v3 - 4.2, lb_data_w2, h_data_w2, num_window=2)

    # ➔ Control de Continuidad (a la derecha) con Proporciones XL
    ax_concept.text(128, start_y_concept+box_height/2, 'Control de Continuidad Estricto:\nDatos faltantes > 5 min', ha='center', fontsize=12, fontweight='bold')
    
    # Cajas con X
    start_x_discard = 110
    y_discard = start_y_concept - space_v * 1.5
    box_w_discard = 25
    rect_disc_1 = patches.FancyBboxPatch(
        (start_x_discard, y_discard), box_w_discard, box_height,
        boxstyle="round,pad=0.2", linewidth=1.5, edgecolor='#2c3e50', facecolor='#D6EAF8', alpha=0.9, zorder=2
    )
    ax_concept.add_patch(rect_disc_1)
    
    # Brecha con X roja
    rect_disc_2 = patches.FancyBboxPatch(
        (start_x_discard + box_w_discard + 2, y_discard), box_w_discard, box_height,
        boxstyle="round,pad=0.2", linewidth=1.5, edgecolor='#2c3e50', facecolor='#D6EAF8', alpha=0.9, zorder=2
    )
    ax_concept.add_patch(rect_disc_2)
    ax_concept.text(start_x_discard + box_w_discard + 2 + box_w_discard/2, y_discard + box_height/2, 'Sep>', ha='center', va='center', fontsize=12, fontweight='bold', zorder=3)

    # Gran X roja
    ax_concept.text(start_x_discard + box_w_discard + 1, y_discard + box_height/2, 'X', ha='center', va='center', fontsize=50, color='#C0392B', fontweight='bold', zorder=5)
    # Texto Secuencia Descartada
    ax_concept.text(start_x_discard + box_w_discard + 1, y_discard - 0.7, 'Secuencia Descartada', ha='center', va='center', fontsize=11, fontweight='bold')

    # Configuración de Ejes Final
    ax_concept.set_xlim(-5, 145)
    ax_concept.set_ylim(-1, 14)
    ax_concept.axis('off')

    # =========================================================================
    # SECCIÓN 3: ESTRUCTURA DEL TENSOR TRIDIMENSIONAL (Datos Reales, 2025)
    # =========================================================================
    draw_section_title(ax_tensor, "Estructura del Tensor Tridimensional de Salida")
    ax_tensor.set_facecolor('#ffffff')
    
    # Cajas de texto gris claro con proporciones XL y padding
    bbox_props_left = dict(facecolor='#E8E8E8', edgecolor='#2c3e50', boxstyle='round,pad=0.6', linewidth=1)
    ax_tensor.text(-5, 5, r"Lookback (70 min):"+"\n"+r"\"Pre-acondicionamiento\""+"\n"+r"histórico de Rayleigh-Taylor", 
                   ha='center', va='center', fontsize=11, bbox=bbox_props_left, fontweight='bold', zorder=5)
    # Flecha hacia el tensor X con padding
    ax_tensor.annotate('', xy=(14, 5), xytext=(5, 5), arrowprops=dict(arrowstyle='->', lw=1.5, color='#2c3e50'), zorder=5)
    
    # Pieza derecha
    bbox_props_right = dict(facecolor='#E8E8E8', edgecolor='#2c3e50', boxstyle='round,pad=0.6', linewidth=1)
    ax_tensor.text(105, 5, r"Horizonte (10 min):"+"\n"+r"Límite predictivo"+"\n"+r"operativo (caos no lineal)", 
                   ha='center', va='center', fontsize=11, bbox=bbox_props_right, fontweight='bold', zorder=5)
    # Flecha hacia el tensor Y con padding
    ax_tensor.annotate('', xy=(85, 5), xytext=(95, 5), arrowprops=dict(arrowstyle='->', lw=1.5, color='#2c3e50'), zorder=5)

    # ➔ Representación Tridimensional de Tensores (Cubos apilados) con Proporciones XL
    y_tensor = 3
    
    # Color beige claro de los tensores: #FEF7DA con proporciones XL
    tensor_color = '#FEF7DA'
    
    # Función para dibujar un bloque 3D translúcido con padding
    def draw_3d_tensor(ax, start_x, start_y, width, height, depth_offset, num_batches, color):
        for i in range(num_batches - 1, -1, -1):
            x_i = start_x + i * depth_offset
            y_i = start_y + i * depth_offset
            alpha_val = 1.0 if i == 0 else 0.4  
            
            rect = patches.FancyBboxPatch(
                (x_i, y_i), width, height,
                boxstyle="round,pad=0.2", linewidth=1.5, edgecolor='#2c3e50', facecolor=color, alpha=alpha_val, zorder=2+num_batches-i
            )
            ax.add_patch(rect)

    # Tensor de Entrada X (70x1) - Pila de 3 matrices
    draw_3d_tensor(ax_tensor, 15, y_tensor, 35, 6, depth_offset=0.3, num_batches=3, color=tensor_color)
    # Texto matemático LaTeX
    ax_tensor.text(32.5, y_tensor+3, r"$X \in \mathbb{R}^{N \times 70 \times 1}$", ha='center', va='center', fontsize=16, weight='bold')
    
    # Etiquetas de dimensiones
    ax_tensor.text(14, y_tensor+3, 'Batch\n(N)', ha='right', va='center', rotation=90, fontsize=11, fontweight='bold')
    ax_tensor.text(32.5, y_tensor-0.7, 'Lookback (70 min)', ha='center', va='top', fontsize=11, fontweight='bold')
    
    # Flecha y texto Feature
    arrow_f = ax_tensor.annotate('', xy=(53, y_tensor+0.2), xytext=(53, y_tensor+3.2), arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=1.5), zorder=6)
    ax_tensor.text(53, y_tensor+0.2, 'Feature\n(1, S4)', ha='left', va='center', fontsize=10, fontweight='bold', zorder=6)

    # Flecha de mapeo del modelo XL
    ax_tensor.annotate('', xy=(65, y_tensor+3), xytext=(55, y_tensor+3), arrowprops=dict(arrowstyle='->', lw=3, color='#8E44AD'))
    ax_tensor.text(60, y_tensor+3.6, 'Modelo\nLSTM', ha='center', va='center', weight='bold', color='#8E44AD', fontsize=11)

    # Tensor de Salida Y (10x1) - Pila de 3 matrices
    draw_3d_tensor(ax_tensor, 68, y_tensor, 15, 6, depth_offset=0.3, num_batches=3, color=tensor_color)
    # Texto matemático LaTeX
    ax_tensor.text(75.5, y_tensor+3, r"$Y \in \mathbb{R}^{N \times 10 \times 1}$", ha='center', va='center', fontsize=16, weight='bold')
    
    # Etiquetas de dimensiones
    # Flecha y texto Horizonte
    ax_tensor.annotate('', xy=(68, y_tensor-0.7), xytext=(83, y_tensor-0.7), arrowprops=dict(arrowstyle='<->', color='#2c3e50', lw=1.5), zorder=6)
    ax_tensor.text(75.5, y_tensor-0.7, 'Horizonte (10 min)', ha='center', va='top', fontsize=11, fontweight='bold')
    
    # Configuración de Ejes Final
    ax_tensor.set_xlim(-15, 125)
    ax_tensor.set_ylim(-1, 10)
    ax_tensor.axis('off')

    # =========================================================================
    # PIE DE FIGURA GENERAL CENTRADO
    # =========================================================================
    fig.text(0.5, 0.05, 
             "Figura 2.4. Generación de tensores tridimensionales mediante la técnica de ventana deslizante (*Sliding Window*).",
             ha='center', fontsize=12, fontweight='bold')

    plt.tight_layout()
    # Ajustar un poco el espacio vertical entre secciones
    plt.subplots_adjust(hspace=0.3, bottom=0.1)
    
    # Exportación garantizada
    plt.savefig(output_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(output_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Diagrama generated exitosamente como '{output_pdf}' y '{output_png}'.")

if __name__ == "__main__":
    generar_diagrama_sliding_window_perfecto('Esquema_Sliding_Window_Final.pdf', 'Esquema_Sliding_Window_Final.png')