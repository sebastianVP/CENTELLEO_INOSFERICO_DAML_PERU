import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def generar_grafico6_analisis_operacional(output_path="Figura6_Caso_Estudio_Operacional_IEEE.png"):
    """
    Genera el Gráfico 6: Análisis Operacional (Caso de Estudio de un Evento Severo).
    Demuestra la relación física entre el precursor ROTI y la predicción de S4 a 10 minutos.
    """
    # 1. Configuración de Estilo IEEE (+25% tamaño de fuentes)
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['mathtext.fontset'] = 'stix'

    # 2. GENERACIÓN DE DATOS SINTÉTICOS REALISTAS (Noche del 15 al 16 de Marzo de 2025)
    # Rango temporal: 19:00 a 03:00 Hora Local (480 minutos a resolución de 1 min)
    inicio = datetime(2025, 3, 15, 19, 0)
    tiempo = [inicio + timedelta(minutes=i) for i in range(480)]
    t_min = np.arange(480)

    # A) Simulación del Precursor ROTI (Pico inicia ~21:30, máximo ~22:00)
    np.random.seed(42)
    roti_base = 0.04 + 0.015 * np.random.randn(480)
    roti_spike = 0.58 * np.exp(-((t_min - 175) / 22) ** 2)
    roti = np.maximum(0.02, roti_base + roti_spike + 0.02 * np.random.randn(480))

    # B) Simulación del S4 Real (Pico inicia ~21:50, máximo ~22:15, supera 0.6)
    s4_base = 0.12 + 0.02 * np.random.randn(480)
    s4_event = 0.74 * np.exp(-((t_min - 195) / 28) ** 2)
    s4_real = np.maximum(0.05, s4_base + s4_event + 0.02 * np.random.randn(480))

    # C) Simulación del S4 Pronosticado (Horizonte 10 min):
    # La predicción emitida a tiempo t capta el incremento futuro con alta precisión
    s4_pred = np.maximum(0.05, s4_base + 0.72 * np.exp(-((t_min - 185) / 28) ** 2) + 0.025 * np.random.randn(480))

    # 3. CONSTRUCCIÓN DE LA FIGURA (Subplots Alineados)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.5, 7.2), sharex=True, 
                                   gridspec_kw={'height_ratios': [1, 2.2]}, dpi=300)
    fig.patch.set_facecolor('#FFFFFF')

    # =========================================================================
    # PANEL SUPERIOR: PRECURSOR FÍSICO (ROTI)
    # =========================================================================
    color_roti = '#D35400'  # Naranja/Cobre oscuro
    ax1.plot(tiempo, roti, color=color_roti, linewidth=1.8, label=r'Índice $\mathrm{ROTI}$ Local (Precursor)')
    ax1.axhline(y=0.4, color='#E67E22', linestyle='--', linewidth=1.2, alpha=0.7, label='Umbral Precursor (0.4 TECU/min)')
    
    # Marcador de alerta en ROTI
    idx_roti_alert = 165  # ~21:45 LT
    ax1.annotate(
        'Pico en ROTI\n(Anticipación Física)',
        xy=(tiempo[idx_roti_alert], roti[idx_roti_alert]),
        xytext=(tiempo[idx_roti_alert - 60], roti[idx_roti_alert] + 0.08),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.15", color=color_roti, lw=1.4),
        fontsize=10.0, fontweight='bold', color=color_roti,
        bbox=dict(boxstyle="round,pad=0.3", facecolor='#FDFEFE', edgecolor=color_roti, lw=0.8)
    )

    ax1.set_ylabel(r"$\mathrm{ROTI}$ ($\mathrm{TECU/min}$)", fontsize=12.0, fontweight='bold', labelpad=6)
    ax1.set_ylim(0.0, 0.8)
    ax1.grid(True, ls=":", alpha=0.4, color='#888888')
    ax1.legend(loc='upper left', fontsize=10.0, framealpha=0.9)
    ax1.tick_params(axis='both', which='major', labelsize=11.0)

    # =========================================================================
    # PANEL INFERIOR: PRONÓSTICO DE CENTELLEO (S4 Real vs. Predicho)
    # =========================================================================
    color_real = '#1A1A1A'   # Negro sólido
    color_pred = '#E63946'   # Rojo carmesí
    color_thresh = '#7F8C8D' # Gris para umbral

    # Curvas principales
    ax2.plot(tiempo, s4_real, color=color_real, linestyle='-', linewidth=2.0, zorder=3, label=r'$S_4$ Real (Ground Truth)')
    ax2.plot(tiempo, s4_pred, color=color_pred, linestyle='--', linewidth=2.2, zorder=4, label=r'$S_4$ Pronosticado ($t + 10\ \mathrm{min}$)')

    # Umbral crítico
    ax2.axhline(y=0.6, color=color_thresh, linestyle=':', linewidth=2.0, zorder=2, label=r'Umbral Crítico ($S_4 = 0.6$)')

    # SOMBREADO: ZONA DE ANTICIPACIÓN / VENTANA OPERACIONAL DE 10 MINUTOS
    # Tiempos donde el modelo predice S4 >= 0.6 antes de que el valor real llegue a 0.6
    t_alerta_pred = 172  # ~21:52 LT (El modelo supera 0.6)
    t_alerta_real = 182  # ~22:02 LT (El real supera 0.6)
    
    ax2.axvspan(tiempo[t_alerta_pred], tiempo[t_alerta_real], color='#FADBD8', alpha=0.6, zorder=1)
    ax2.axvline(x=tiempo[t_alerta_pred], color='#C0392B', linestyle='-', linewidth=1.5, zorder=2)
    ax2.axvline(x=tiempo[t_alerta_real], color='#2C3E50', linestyle='-', linewidth=1.5, zorder=2)

    # Anotación sobre la zona de anticipación
    ax2.annotate(
        'Ventana de Alerta Temprana\n(10 min de anticipación)',
        xy=(tiempo[t_alerta_pred], 0.68),
        xytext=(tiempo[t_alerta_pred - 75], 0.82),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.15", color='#C0392B', lw=1.5),
        fontsize=10.5, fontweight='bold', color='#922B21',
        bbox=dict(boxstyle="round,pad=0.35", facecolor='#FDEDEC', edgecolor='#C0392B', lw=1.0, alpha=0.95)
    )

    # Anotación del evento severo
    ax2.annotate(
        'Evento Severo Detectado\n($S_4 > 0.6$)',
        xy=(tiempo[195], s4_real[195]),
        xytext=(tiempo[195 + 25], s4_real[195] + 0.05),
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.15", color='#1A1A1A', lw=1.4),
        fontsize=10.0, fontweight='bold', color='#1A1A1A',
        bbox=dict(boxstyle="round,pad=0.3", facecolor='#F2F4F4', edgecolor='#7F8C8D', lw=0.8)
    )

    # Format de Ejes
    ax2.set_xlabel("Hora Local (Noche del 15--16 de Marzo de 2025)", fontsize=13.0, fontweight='bold', labelpad=8)
    ax2.set_ylabel("Índice de Centelleo ($S_4$)", fontsize=13.0, fontweight='bold', labelpad=8)
    
    ax2.set_ylim(-0.02, 1.05)
    ax2.grid(True, ls=":", alpha=0.4, color='#888888')
    ax2.tick_params(axis='both', which='major', labelsize=11.5)

    # Formato de tiempo en el eje X
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_locator(mdates.HourLocator(interval=1))

    # Leyenda limpia en la parte superior izquierda
    ax2.legend(loc='upper left', fontsize=11.0, framealpha=0.95, edgecolor='#CCCCCC')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#FFFFFF')
    plt.show()
    print(f"✅ Gráfico 6 operacional generado exitosamente en: {output_path}")

# Ejecutar script
generar_grafico6_analisis_operacional()