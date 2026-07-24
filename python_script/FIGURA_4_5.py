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

plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.facecolor'] = academic_autumn['academic_bg']
plt.rcParams['axes.edgecolor'] = academic_autumn['grid_grey']
plt.rcParams['axes.labelcolor'] = academic_autumn['action_blue']
plt.rcParams['xtick.color'] = academic_autumn['grid_grey']
plt.rcParams['ytick.color'] = academic_autumn['grid_grey']

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

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.patch.set_facecolor(academic_autumn['academic_bg'])

    # =========================================================================
    # PANEL A: HEATMAP
    # =========================================================================
    cmap_heat = LinearSegmentedColormap.from_list('heat', ['white', academic_autumn['warning_orange'], academic_autumn['danger_red']])
    
    sns.heatmap(rmse_data, annot=True, fmt=".3f", cmap=cmap_heat, ax=ax1,
                xticklabels=[f"{h} min" for h in horizons],
                yticklabels=lookbacks,
                annot_kws={"size": 11, "weight": "bold"},
                cbar_kws={'label': 'RMSE (Eventos S4 > 0.6)'},
                linewidths=1, linecolor=academic_autumn['grid_grey'])
    
    # Resaltar la celda de Lookback 70 a los 10 minutos (fila índice 2, col índice 1)
    ax1.add_patch(plt.Rectangle((1, 2), 1, 1, fill=False, edgecolor=academic_autumn['warning_orange'], lw=4, clip_on=False))

    ax1.set_xlabel('Horizonte Predictivo (minutos)', fontsize=12, fontweight='bold', labelpad=10)
    ax1.set_ylabel('Ventana de Observación - Lookback (minutos)', fontsize=12, fontweight='bold', labelpad=10)
    ax1.set_title('a) Heatmap de Error Predictivo', fontsize=12, fontweight='bold', color=academic_autumn['action_blue'])

    # =========================================================================
    # PANEL B: GRÁFICO DE LÍNEAS (DEGRADACIÓN Y PUNTO ÓPTIMO)
    # =========================================================================
    ax2.set_facecolor('white')
    
    colors = sns.color_palette("Blues_d", len(lookbacks))
    markers = ['o', 's', '^', 'D', 'v', 'P']
    
    for i in range(len(lookbacks)):
        # Resaltamos visualmente SÓLO el lookback de 70 min
        if lookbacks[i] == 70:
            lw = 3.0 
            alpha = 1.0 
            color = academic_autumn['warning_orange']
            zorder = 5 # Traer al frente
        else:
            lw = 1.5 
            alpha = 0.4 # Atenuar el resto
            color = colors[i]
            zorder = 2
            
        ax2.plot(horizons, rmse_data[i], marker=markers[i], linewidth=lw, alpha=alpha, 
                 color=color, label=f'Lookback {lookbacks[i]} min', markersize=7, zorder=zorder)

    # Línea vertical marcando el límite de 10 min
    ax2.axvline(x=10, color=academic_autumn['danger_red'], linestyle='--', linewidth=2.5, zorder=1)
    
    # Sombreado para las zonas de confianza e incertidumbre
    ax2.axvspan(5, 10, facecolor=academic_autumn['action_blue'], alpha=0.1)
    ax2.axvspan(10, 30, facecolor=academic_autumn['danger_red'], alpha=0.05)

    # Textos de las zonas
    ax2.text(7.5, 0.35, 'Zona de Confianza', color=academic_autumn['action_blue'], 
             fontsize=10, fontweight='bold', ha='center', va='top')
    ax2.text(20, 0.35, 'Alta Incertidumbre', color=academic_autumn['danger_red'], 
             fontsize=10, fontweight='bold', ha='center', va='top')
    
    # Anotación específica para el punto óptimo (Lookback 70 a 10 mins -> 0.285)
    ax2.annotate('Mínimo Global\n(RMSE = 0.285)', 
                 xy=(10, 0.285), 
                 xytext=(13, 0.275),
                 arrowprops=dict(facecolor=academic_autumn['warning_orange'], edgecolor=academic_autumn['warning_orange'], shrink=0.05, width=1.5, headwidth=7),
                 fontsize=10, fontweight='bold', color=academic_autumn['warning_orange'], zorder=10)

    ax2.set_xlabel('Horizonte Predictivo (minutos)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('RMSE (Eventos S4 > 0.6)', fontsize=12, fontweight='bold')
    ax2.set_title('b) Degradación y Punto Óptimo (Lookback 70)', fontsize=12, fontweight='bold', color=academic_autumn['action_blue'])
    ax2.set_xticks(horizons)
    ax2.set_xticklabels([f"{h}" for h in horizons], fontweight='bold')
    ax2.set_ylim(0.24, 0.36)
    ax2.grid(True, linestyle=':', alpha=0.6)
    
    ax2.legend(title='Ventana (Lookback)', loc='lower right', fontsize=9, title_fontsize=10, framealpha=0.9)

    plt.tight_layout()
    plt.savefig(output_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(output_png, bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_figura_4_5_lookback_70('figura_4_5_horizonte_L70.pdf', 'figura_4_5_horizonte_L70.png')