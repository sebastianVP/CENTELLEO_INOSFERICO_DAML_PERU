import matplotlib.pyplot as plt
import numpy as np

# Configuración estética Academic Autumn
academic_colors = {
    'simple': '#95A5A6',      # Gris neutro
    'stacked': '#D68910',     # Naranja (Ganador/Alerta)
    'bidir': '#34495E',       # Azul oscuro
    'bg': '#FCF3CF',          # Crema académico
    'grid': '#5D6D7E'
}

plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'

def generate_figura_4_3_rmse_comparison(output_pdf, output_png):
    # Datos de la tabla
    modelos = ['LSTM Simple', 'Stacked LSTM', 'Bidireccional']
    rmse_global = [0.073358, 0.077312, 0.088282]
    rmse_eventos = [0.264439, 0.249589, 0.252970] # Stacked es el menor aquí

    x = np.arange(len(modelos))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor(academic_colors['bg'])

    # Barras
    rects1 = ax.bar(x - width/2, rmse_global, width, label='RMSE Global (Promedio)', 
                    color=academic_colors['bidir'], alpha=0.7)
    rects2 = ax.bar(x + width/2, rmse_eventos, width, label='RMSE Eventos Críticos (>0.6)', 
                    color=[academic_colors['simple'], academic_colors['stacked'], academic_colors['simple']])

    # Etiquetas y Estilo
    ax.set_ylabel('Error Cuadrático Medio (RMSE)', fontsize=12, fontweight='bold', color=academic_colors['bidir'])
    ax.set_xticks(x)
    ax.set_xticklabels(modelos, fontsize=11, fontweight='bold')
    ax.legend(loc='upper left', frameon=True, facecolor='white')
    
    # Añadir texto "Año 2025" sutilmente
    ax.text(0.98, 0.02, 'Benchmark DAML-Peru 2025', transform=ax.transAxes, 
            ha='right', va='bottom', fontsize=9, color=academic_colors['grid'], alpha=0.6)

    # Anotación de "Arquitectura Ganadora" sobre Stacked LSTM
    ganador_idx = 1
    ax.annotate('ARQUITECTURA\nGANADORA', 
                xy=(ganador_idx + width/2, rmse_eventos[ganador_idx]), 
                xytext=(0, 20), 
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=10, fontweight='bold', color=academic_colors['stacked'],
                bbox=dict(boxstyle='round,pad=0.5', fc='white', ec=academic_colors['stacked'], lw=2),
                arrowprops=dict(arrowstyle='->', color=academic_colors['stacked'], lw=2))

    # Etiquetas de valor sobre las barras de eventos
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.4f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

    autolabel(rects2)

    ax.grid(axis='y', linestyle='--', alpha=0.5, color=academic_colors['grid'])
    ax.set_ylim(0, 0.35) # Espacio para la etiqueta del ganador

    plt.tight_layout()
    plt.savefig(output_pdf, bbox_inches='tight')
    plt.savefig(output_png, bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    generate_figura_4_3_rmse_comparison('figura_4_3_rmse.pdf', 'figura_4_3_rmse.png')