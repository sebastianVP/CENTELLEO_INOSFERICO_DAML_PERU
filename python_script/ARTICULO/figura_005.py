import numpy as np
import matplotlib.pyplot as plt

def generar_grafico5_benchmark(output_path="Figura5_Benchmark_Arquitecturas_IEEE.png"):
    """
    Genera el Gráfico 5 de comparación de arquitecturas bajo condiciones de tormenta.
    Ajuste de posiciones para evitar superposición entre leyenda y cajas de texto.
    """
    # 1. Configuración de Estilo IEEE
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['mathtext.fontset'] = 'stix'

    # 2. DATOS DE LA TABLA (Condiciones de Tormenta)
    modelos = ['Simple', 'Stacked', 'Bidireccional']
    
    # Métricas
    rmse_global  = [0.101910, 0.076372, 0.104356]
    rmse_eventos = [0.165522, 0.159016, 0.150833]

    # 3. CONFIGURACIÓN DE EJES Y ANCHOS
    x = np.arange(len(modelos))  # Posiciones: Simple, Stacked, Bidireccional
    width = 0.28                  # Ancho de las barras

    # Paleta de colores inspirada en la imagen de referencia
    color_global  = '#95A5A6'    # Gris Pizarra
    color_eventos = '#8E44AD'    # Púrpura profundo

    # 4. CONSTRUCCIÓN DE LA FIGURA
    fig, ax = plt.subplots(figsize=(9.0, 5.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # Creación de barras por métrica
    rects1 = ax.bar(x - width/2, rmse_global, width, label='RMSE Global', 
                    color=color_global, edgecolor='none', zorder=3)
    rects2 = ax.bar(x + width/2, rmse_eventos, width, label='RMSE Eventos ($S_4 > 0.6$)', 
                    color=color_eventos, edgecolor='none', zorder=3)

    # 5. ETIQUETAS SOBRE BARRAS (4 decimales para rigor técnico)
    def agregar_valores(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.4f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=10.0, fontweight='bold', color='#2C3E50')

    agregar_valores(rects1)
    agregar_valores(rects2)

    # 6. ANOTACIONES DE CONTEXTO TÉCNICO (Sin superposiciones)

    # A) Destacar la superioridad del Stacked en RMSE Global (Abajo a la izquierda de la barra)
    ax.annotate(
        'Mejor Desempeño\nGlobal (Menor Error)',
        xy=(1 - width/2, 0.076372),
        xytext=(1 - width/2 - 0.35, 0.035),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.2", color='#2C3E50', lw=1.4),
        fontsize=10.0, fontweight='bold', color='#2C3E50',
        bbox=dict(boxstyle="round,pad=0.35", facecolor='#F2F4F4', edgecolor='#95A5A6', lw=0.9, alpha=0.95),
        ha='center'
    )

    # B) Contexto: Diferencia no considerable en Eventos (Ubicada en la zona superior derecha, limpia)
    ax.annotate(
        'Desempeño similar en eventos\n($\Delta \mathrm{RMSE} \leq 0.0147$)',
        xy=(1 + width/2, 0.159016),
        xytext=(1 + width/2 + 0.35, 0.192),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.15", color='#8E44AD', lw=1.3),
        fontsize=10.0, fontweight='bold', color='#512E5F',
        bbox=dict(boxstyle="round,pad=0.35", facecolor='#F5EEF8', edgecolor='#8E44AD', lw=0.9, alpha=0.95),
        ha='center'
    )

    # 7. FORMATO GENERAL (+25% tamaño de fuentes)
    ax.set_xlabel("Arquitectura del Modelo", fontsize=13.1, fontweight='bold', labelpad=8)
    ax.set_ylabel("RMSE (Unidades $S_4$)", fontsize=13.1, fontweight='bold', labelpad=8)
    
    ax.set_xticks(x)
    ax.set_xticklabels(modelos, fontsize=12.5, fontweight='bold')
    
    ax.set_ylim(0.0, 0.225)  # Espacio vertical ampliado para evitar colisiones
    ax.grid(True, axis='y', ls=":", alpha=0.35, color='#BDC3C7', zorder=0)
    ax.tick_params(axis='both', which='major', labelsize=11.9)

    # Leyenda en la ESQUINA SUPERIOR IZQUIERDA (Zona despejada)
    ax.legend(title='Métrica', loc='upper left', title_fontsize=11.5, fontsize=11.2, framealpha=0.95, edgecolor='#CCCCCC')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.show()
    print(f"✅ Gráfico 5 sin superposiciones guardado exitosamente en: {output_path}")

# Ejecutar script
generar_grafico5_benchmark()