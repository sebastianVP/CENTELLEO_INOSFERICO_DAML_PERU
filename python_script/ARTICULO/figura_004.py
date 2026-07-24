import numpy as np
import matplotlib.pyplot as plt

def generar_grafico4_loss(y_true=0.8, alpha=2.0, beta=50.0, umbral_s4=0.6, output_path="Figura4_Weighted_Focal_Loss_IEEE.png"):
    """
    Genera el Gráfico 4 optimizado para IEEE:
    - Sin título principal.
    - Leyenda en la parte inferior derecha.
    - Tipografía ampliada un 25% para máxima legibilidad.
    - Cuadro de Valor Real ajustado a la derecha y más compacto.
    """
    # 1. Configuración de Estilo IEEE
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['mathtext.fontset'] = 'stix'
    
    # Rango de predicción y_pred
    y_pred = np.linspace(0.001, 0.999, 500)
    
    # 2. CÁLCULO DE FUNCIONES DE PÉRDIDA
    loss_mse = (y_true - y_pred) ** 2
    error_abs = np.abs(y_true - y_pred)
    w_i = np.where(y_true >= umbral_s4, beta, 1.0)
    loss_wfl = w_i * (error_abs ** alpha) * loss_mse
    
    # Paleta de Colores
    color_mse = '#243B55'    # Azul oscuro
    color_wfl = '#E63946'    # Rojo carmesí
    color_box = '#FFEBEE'
    color_border = '#B71C1C'

    # 3. CONSTRUCCIÓN DE LA FIGURA
    fig, ax = plt.subplots(figsize=(9.0, 5.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # Curvas principales
    ax.plot(y_pred, loss_mse, label=r'MSE Convencional: $\mathcal{L}_{MSE} = (y - \hat{y})^2$', 
            color=color_mse, linestyle='--', linewidth=2.2, zorder=2)
    ax.plot(y_pred, loss_wfl, label=r'Weighted Focal Loss (Propuesta): $\mathcal{L}_{WFL} = \beta \cdot |y - \hat{y}|^\alpha \cdot (y - \hat{y})^2$', 
            color=color_wfl, linestyle='-', linewidth=2.8, zorder=3)

    # Sombreado Zona Crítica (y_pred < umbral_s4)
    ax.axvspan(0.0, umbral_s4, color='#FDEDEC', alpha=0.45, zorder=1)
    ax.axvline(x=umbral_s4, color=color_border, linestyle=':', linewidth=2.0, zorder=4)

    # Línea vertical Valor Real (y_true = 0.8)
    ax.axvline(x=y_true, color='#27AE60', linestyle='-', linewidth=2.2, zorder=4)

    # 4. ELEMENTOS DE TEXTO
    
    # A) Etiqueta Zona de Subestimación Crítica (Esquina superior izquierda)
    ax.text(0.30, 21.0, 'ZONA DE SUBESTIMACIÓN CRÍTICA\n(Falsos Negativos Operacionales)', 
            ha='center', va='center', color=color_border, fontsize=11.9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFFFF', edgecolor=color_border, lw=0.9, alpha=0.95))

    # B) Etiqueta Valor Real (Desplazada a la DERECHA de la línea verde y más pequeña)
    ax.text(y_true + 0.005, 16.5, f'Valor Real ($y_{{true}} = {y_true}$)\n[Evento Severo]', 
            ha='left', va='center', color='#1E8449', fontsize=10.0, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#E8F8F5', edgecolor='#27AE60', lw=1.0, alpha=0.95))

    # C) Anotación con flecha sobre la curva WFL (y_pred ~ 0.22)
    idx_sub = 75  # y_pred ~ 0.22
    ax.annotate(
        f'Penalización Severa ($\mathbf{{\\beta={beta}}}$)\nEvita el sesgo conservador\nen eventos raros',
        xy=(y_pred[idx_sub], loss_wfl[idx_sub]), 
        xytext=(y_pred[idx_sub] + 0.12, loss_wfl[idx_sub] + 3.8),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.15", color=color_border, lw=1.6),
        fontsize=11.25, fontweight='bold', color=color_border,
        bbox=dict(boxstyle="round,pad=0.4", facecolor=color_box, edgecolor=color_border, lw=1.0, alpha=0.95)
    )

    # 5. FORMATO DE EJES Y LEYENDA (+25%)
    ax.set_xlabel("Predicción del Modelo ($\hat{y} = S_4$ Predicho)", fontsize=13.1, fontweight='bold', labelpad=8)
    ax.set_ylabel("Magnitud del Error / Penalización ($\mathcal{L}$)", fontsize=13.1, fontweight='bold', labelpad=8)
    
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-0.5, 24.0)
    
    ax.grid(True, which="both", ls=":", alpha=0.4, color='#888888')
    ax.tick_params(axis='both', which='major', labelsize=11.9)
    
    # Leyenda ubicada en la parte INFERIOR DERECHA
    ax.legend(loc='lower right', bbox_to_anchor=(0.98, 0.15), fontsize=11.5, framealpha=0.95, edgecolor='#CCCCCC')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.show()
    print(f"✅ Gráfico 4 con cuadro ajustado guardado exitosamente en: {output_path}")

# Ejecutar script
generar_grafico4_loss()