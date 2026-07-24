import numpy as np
import matplotlib.pyplot as plt

def generar_grafico_focal_loss_dividido(output_pdf, output_png):
    # Configuración de alta calidad
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    y_pred = np.linspace(0, 1, 200)
    gamma = 2.0
    omega_severo = 50.0  
    omega_calma = 1.0    
    
    # Datos Evento Severo (y_true = 0.9)
    y_true_sev = 0.9
    mse_sev = (y_true_sev - y_pred)**2
    wfl_sev = ((y_true_sev - y_pred)**2) * ((1 + np.abs(y_true_sev - y_pred))**gamma) * omega_severo

    # Datos Evento Calma (y_true = 0.2)
    y_true_calm = 0.2
    mse_calm = (y_true_calm - y_pred)**2
    wfl_calm = ((y_true_calm - y_pred)**2) * ((1 + np.abs(y_true_calm - y_pred))**gamma) * omega_calma

    # --- Creación de la figura con 2 subgráficos (1 fila, 2 columnas) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    fig.patch.set_facecolor('#ffffff')

    # =========================================================================
    # PANEL A: EVENTO SEVERO (ESCALA GRANDE)
    # =========================================================================
    ax1.set_facecolor('#f8f9f9')
    ax1.plot(y_pred, wfl_sev, color='#C0392B', lw=3, label=r'WFL ($\omega=50$)')
    ax1.plot(y_pred, mse_sev, color='#E6B0AA', lw=3, linestyle='--', label='MSE Tradicional')
    
    ax1.axvline(x=0.9, color='#C0392B', linestyle=':', lw=2, label='Valor Real ($y_{true}=0.9$)')
    ax1.axvspan(0.0, 0.5, facecolor='#FDEDEC', alpha=0.6, zorder=0)
    ax1.text(0.25, 80, 'Zona de Subestimación\n(Falso Negativo)', ha='center', va='center', color='#922B21', fontsize=11, weight='bold')

    ax1.set_title("A) Escenario de Tormenta Severa", fontsize=14, weight='bold', pad=10)
    ax1.set_xlabel('Predicción del Modelo ($\hat{y}$)', fontsize=12)
    ax1.set_ylabel('Castigo (Valor de la Función de Pérdida)', fontsize=12)
    ax1.set_ylim(-5, 160)
    ax1.set_xlim(0, 1)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='upper center', fontsize=11)

    # =========================================================================
    # PANEL B: ESTADO DE CALMA (ZOOM EN LA ESCALA)
    # =========================================================================
    ax2.set_facecolor('#f8f9f9')
    ax2.plot(y_pred, wfl_calm, color='#27AE60', lw=3, label=r'WFL ($\omega=1$)')
    ax2.plot(y_pred, mse_calm, color='#7DCEA0', lw=3, linestyle='--', label='MSE Tradicional')
    
    ax2.axvline(x=0.2, color='#27AE60', linestyle=':', lw=2, label='Valor Real ($y_{true}=0.2$)')

    ax2.set_title("B) Escenario de Calma Nominal", fontsize=14, weight='bold', pad=10)
    ax2.set_xlabel('Predicción del Modelo ($\hat{y}$)', fontsize=12)
    # IMPORTANTE: Escala mucho menor para poder ver las curvas
    ax2.set_ylim(-0.1, 2.5) 
    ax2.set_xlim(0, 1)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(loc='upper right', fontsize=11)
    
    # Anotación para explicar la diferencia
    ax2.annotate("WFL mantiene errores \nbajo control.", 
                 xy=(0.8, 1.3), xytext=(0.45, 1.8),
                 arrowprops=dict(arrowstyle="->", color='#27AE60'),
                 fontsize=10, bbox=dict(facecolor='white', edgecolor='#7DCEA0', pad=3))

    # Título general
    #fig.suptitle("Figura 2.6: Comportamiento asimétrico de WFL vs MSE", fontsize=16, weight='bold', y=1.05)

    # Exportación
    plt.tight_layout()
    plt.savefig(output_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(output_png, bbox_inches='tight', dpi=300)
    plt.close()

generar_grafico_focal_loss_dividido("Figura_2_6_WFL_Dividido.pdf", "Figura_2_6_WFL_Dividido.png")