import numpy as np
import matplotlib.pyplot as plt

def generar_grafico_focal_loss_dividido(output_pdf, output_png):
    # =========================================================================
    # 1. CONFIGURACIÓN DE ALTA LEGIBILIDAD PARA HOJA A4 (MITAD DE PÁGINA)
    # =========================================================================
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['text.color'] = '#000000'
    
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

    # --- Lienzo compacto en pulgadas (Fuerza a que las letras se vean grandes) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 3.2))
    fig.patch.set_facecolor('#ffffff')

    # =========================================================================
    # PANEL A: EVENTO SEVERO (ESCALA GRANDE)
    # =========================================================================
    ax1.set_facecolor('#f8f9f9')
    ax1.plot(y_pred, wfl_sev, color='#C0392B', lw=1.8, label=r'WFL ($\omega=50$)')
    ax1.plot(y_pred, mse_sev, color='#E6B0AA', lw=1.6, linestyle='--', label='MSE Tradicional')
    
    ax1.axvline(x=0.9, color='#C0392B', linestyle=':', lw=1.2, label='Valor Real ($y_{true}=0.9$)')
    ax1.axvspan(0.0, 0.5, facecolor='#FDEDEC', alpha=0.6, zorder=0)
    
    # Texto de zona significativamente más grande y posicionado estratégicamente
    ax1.text(0.25, 80, 'Zona de\nSubestimación\n(Falso Negativo)', ha='center', va='center', 
             color='#922B21', fontsize=6.8, weight='bold')

    ax1.set_title("Escenario de Tormenta Severa", fontsize=7.8, weight='bold', pad=8)
    ax1.set_xlabel('Predicción del Modelo ($\hat{y}$)', fontsize=7.0, weight='bold')
    ax1.set_ylabel('Castigo (Valor de Pérdida)', fontsize=7.0, weight='bold')
    ax1.set_ylim(-5, 160)
    ax1.set_xlim(0, 1)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.legend(loc='upper center', fontsize=5.8, framealpha=0.9)
    ax1.tick_params(axis='both', which='major', labelsize=6.2)

    # =========================================================================
    # PANEL B: ESTADO DE CALMA (ZOOM EN LA ESCALA)
    # =========================================================================
    ax2.set_facecolor('#f8f9f9')
    ax2.plot(y_pred, wfl_calm, color='#27AE60', lw=1.8, label=r'WFL ($\omega=1$)')
    ax2.plot(y_pred, mse_calm, color='#7DCEA0', lw=1.6, linestyle='--', label='MSE Tradicional')
    
    ax2.axvline(x=0.2, color='#27AE60', linestyle=':', lw=1.2, label='Valor Real ($y_{true}=0.2$)')

    ax2.set_title("Escenario de Calma Nominal", fontsize=7.8, weight='bold', pad=8)
    ax2.set_xlabel('Predicción del Modelo ($\hat{y}$)', fontsize=7.0, weight='bold')
    ax2.set_ylim(-0.1, 2.5) 
    ax2.set_xlim(0, 1)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(loc='upper right', fontsize=5.8, framealpha=0.9)
    ax2.tick_params(axis='both', which='major', labelsize=6.2)
    
    # Anotación interna corregida con texto más visible y adaptado al espacio
    ax2.annotate("WFL mantiene\nerrores bajo\ncontrol.", 
                 xy=(0.8, 1.2), xytext=(0.42, 1.6),
                 arrowprops=dict(arrowstyle="->", color='#27AE60', lw=0.8),
                 fontsize=6.2, weight='bold', bbox=dict(facecolor='white', edgecolor='#7DCEA0', pad=1.5, alpha=0.9))

    # =========================================================================
    # EXPORTACIÓN OPTIMIZADA
    # =========================================================================
    plt.tight_layout()
    plt.savefig(output_pdf, bbox_inches='tight', pad_inches=0.02)
    plt.savefig(output_png, bbox_inches='tight', pad_inches=0.02, dpi=300)
    plt.close()

# Ejecutar la función
generar_grafico_focal_loss_dividido("Figura_2_6_WFL_Dividido.pdf", "Figura_2_6_WFL_Dividido.png")
print("¡Figura 2.6 de alto impacto y letras masivas generada con éxito!")

# =========================================================================
# DESCRIPCIÓN FORMAL PARA LA LEYENDA DE LA TESIS (Cuerpo del Documento)
# =========================================================================
#
# Figura 2.6: Comportamiento asimétrico de la función de pérdida Weighted Focal 
# Loss (WFL) en comparación con el Mean Squared Error (MSE) tradicional. El panel 
# izquierdo ilustra el escenario de tormenta severa ($y_{true}=0.9$), donde la 
# subestimación del centelleo (zona de falsos negativos) es severamente penalizada 
# mediante el factor de peso $\omega=50$, forzando al modelo a priorizar estos 
# eventos críticos. Por el contrario, el panel derecho muestra el escenario de 
# calma nominal ($y_{true}=0.2$), donde el castigo se atenúa de forma dinámica 
# ($\omega=1$) para evitar que los gradientes de ruido de fondo dominen el 
# aprendizaje, manteniendo los errores residuales bajo control matemático estable.
#
# Fuente: Elaboración propia.
# =========================================================================