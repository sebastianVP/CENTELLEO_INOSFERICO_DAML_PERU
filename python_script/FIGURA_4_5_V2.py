import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Configuración estética Academic Autumn
academic_autumn = {
    'warning_orange': '#D68910', 
    'action_blue': '#34495E',    
    'academic_bg': '#FCF3CF',    
    'grid_grey': '#5D6D7E',      
    'light_orange': '#FAD7A1',
    'danger_red': '#E74C3C'
}

# --- CONFIGURACIÓN DE FUENTES EXTRAS GRANDES (INCREMENTO ADICIONAL DEL 20%) ---
plt.rcParams['figure.dpi'] = 600  # Máxima resolución académica para impresión
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 17.5  # Base global aumentada un 20% adicional (Antes 14.5)
plt.rcParams['axes.facecolor'] = academic_autumn['academic_bg']
plt.rcParams['axes.edgecolor'] = academic_autumn['grid_grey']
plt.rcParams['axes.labelcolor'] = academic_autumn['action_blue']
plt.rcParams['xtick.color'] = academic_autumn['grid_grey']
plt.rcParams['ytick.color'] = academic_autumn['grid_grey']

# Constantes unificadas del escalado proporcional (+20% respecto al anterior)
FONT_SIZE_TITLE = 20.0       
FONT_SIZE_LABEL = 18.5       
FONT_SIZE_AXIS = 16.5        
FONT_SIZE_LEGEND = 14.5      
FONT_SIZE_TEXT_INSIDE = 15.5  

def generate_figura_4_5_lookback_70(output_pdf, output_png):
    # Datos de la tabla proporcionada
    horizons = [5, 10, 15, 20, 30]
    lookbacks = [50, 60, 70, 80, 90, 100]
    
    rmse_data = np.array([
        [0.282, 0.299, 0.335, 0.334, 0.340],
        [0.263, 0.307, 0.315, 0.332, 0.333],
        [0.324, 0.285, 0.316, 0.346, 0.339],
        [0.253, 0.300, 0.296, 0.349, 0.340],
        [0.261, 0.290, 0.318, 0.335, 0.338],
        [0.265, 0.316, 0.310, 0.335, 0.320]
    ])

    # Lienzo optimizado para albergar texto de gran escala
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(17.5, 7.5)) 
    fig.patch.set_facecolor(academic_autumn['academic_bg'])

    # =========================================================================
    # PANEL A: HEATMAP
    # =========================================================================
    cmap_heat = LinearSegmentedColormap.from_list('heat', ['white', academic_autumn['warning_orange'], academic_autumn['danger_red']])
    
    sns.heatmap(rmse_data, annot=True, fmt=".3f", cmap=cmap_heat, ax=ax1,
                xticklabels=[f"{h} min" for h in horizons],
                yticklabels=lookbacks,
                annot_kws={"size": FONT_SIZE_TEXT_INSIDE, "weight": "bold"},
                cbar_kws={'label': 'RMSE (Eventos S4 > 0.6)', 'pad': 0.05},
                linewidths=1.5, linecolor=academic_autumn['grid_grey'])
    
    # Ajustar tamaño de fuente de las etiquetas de la barra de color (+20%)
    ax1.collections[0].colorbar.set_label('RMSE (Eventos S4 > 0.6)', fontsize=FONT_SIZE_LABEL, fontweight='bold', labelpad=15)
    ax1.collections[0].colorbar.ax.tick_params(labelsize=FONT_SIZE_AXIS)

    # Resaltar la celda de Lookback 70 a los 10 minutos (fila índice 2, col índice 1)
    ax1.add_patch(plt.Rectangle((1, 2), 1, 1, fill=False, edgecolor=academic_autumn['warning_orange'], lw=4, clip_on=False))

    ax1.set_xlabel('Horizonte Predictivo (minutos)', fontsize=FONT_SIZE_LABEL, fontweight='bold', labelpad=15)
    ax1.set_ylabel('Ventana de Observación - Lookback (minutos)', fontsize=FONT_SIZE_LABEL, fontweight='bold', labelpad=15)
    ax1.set_title('a) Heatmap de Error Predictivo', fontsize=FONT_SIZE_TITLE, fontweight='bold', color=academic_autumn['action_blue'], pad=15)
    ax1.tick_params(axis='both', labelsize=FONT_SIZE_AXIS)

    # =========================================================================
    # PANEL B: GRÁFICO DE LÍNEAS
    # =========================================================================
    ax2.set_facecolor('white')
    
    colors = sns.color_palette("Blues_d", len(lookbacks))
    markers = ['o', 's', '^', 'D', 'v', 'P']
    
    for i in range(len(lookbacks)):
        if lookbacks[i] == 70:
            lw = 4.0 
            alpha = 1.0 
            color = academic_autumn['warning_orange']
            zorder = 5
        else:
            lw = 2.0 
            alpha = 0.4 
            color = colors[i]
            zorder = 2
            
        ax2.plot(horizons, rmse_data[i], marker=markers[i], linewidth=lw, alpha=alpha, 
                 color=color, label=f'Lookback {lookbacks[i]} min', markersize=9, zorder=zorder)

    # Línea vertical marcando el límite de 10 min
    ax2.axvline(x=10, color=academic_autumn['danger_red'], linestyle='--', linewidth=2.5, zorder=1)
    
    # Sombreado para las zonas
    ax2.axvspan(5, 10, facecolor=academic_autumn['action_blue'], alpha=0.1)
    ax2.axvspan(10, 30, facecolor=academic_autumn['danger_red'], alpha=0.05)

    # Textos de las zonas (Reposicionados para no chocar con el borde superior debido al +20%)
    ax2.text(7.5, 0.357, 'Zona de Confianza', color=academic_autumn['action_blue'], 
             fontsize=FONT_SIZE_TEXT_INSIDE - 1, fontweight='bold', ha='center', va='top')
    ax2.text(20, 0.357, 'Alta Incertidumbre', color=academic_autumn['danger_red'], 
             fontsize=FONT_SIZE_TEXT_INSIDE - 1, fontweight='bold', ha='center', va='top')
    
    # Anotación específica para el punto óptimo (Calibrada en base al tamaño de letra nuevo)
    ax2.annotate('Mínimo Global\n(RMSE = 0.285)', 
                 xy=(10, 0.285), 
                 xytext=(13.0, 0.268),
                 arrowprops=dict(facecolor=academic_autumn['warning_orange'], edgecolor=academic_autumn['warning_orange'], shrink=0.07, width=2.5, headwidth=9),
                 fontsize=FONT_SIZE_TEXT_INSIDE - 0.5, fontweight='bold', color=academic_autumn['warning_orange'], zorder=10)

    ax2.set_xlabel('Horizonte Predictivo (minutos)', fontsize=FONT_SIZE_LABEL, fontweight='bold', labelpad=15)
    ax2.set_ylabel('RMSE (Eventos S4 > 0.6)', fontsize=FONT_SIZE_LABEL, fontweight='bold', labelpad=15)
    ax2.set_title('b) Degradación y Punto Óptimo (Lookback 70)', fontsize=FONT_SIZE_TITLE, fontweight='bold', color=academic_autumn['action_blue'], pad=15)
    ax2.set_xticks(horizons)
    ax2.set_xticklabels([f"{h}" for h in horizons], fontweight='bold', fontsize=FONT_SIZE_AXIS)
    ax2.tick_params(axis='y', labelsize=FONT_SIZE_AXIS)
    ax2.set_ylim(0.24, 0.36)
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    # Leyenda adaptada al formato de fuente grande
    ax2.legend(title='Ventana (Lookback)', loc='lower right', 
               fontsize=FONT_SIZE_LEGEND, title_fontsize=FONT_SIZE_LEGEND + 1, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(output_pdf, bbox_inches='tight', dpi=600)
    plt.savefig(output_png, bbox_inches='tight', dpi=600)
    plt.close()

    print("Éxito: Todas las fuentes e indicadores han sido incrementados un 20% extra de forma limpia.")

if __name__ == "__main__":
    generate_figura_4_5_lookback_70('figura_4_5_horizonte_L70_grande.pdf', 'figura_4_5_horizonte_L70_grande.png')