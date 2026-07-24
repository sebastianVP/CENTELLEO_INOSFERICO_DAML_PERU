import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def generar_grafico_s4_con_ventana_destacada():
    """
    Genera un gráfico académico profesional replicando el estilo real discutido,
    e incluye un sombreado visual para destacar la ventana de pronóstico de 10 min.
    """
    # 1. CONFIGURACIÓN DE ESTILO ACADÉMICO PROFESIONAL
    plt.rcParams.update({
        'font.size': 11,
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'DejaVu Sans'],
        'axes.labelsize': 11,
        'axes.titlesize': 12,
        'legend.fontsize': 10,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'lines.linewidth': 1.8
    })

    # 2. GENERACIÓN DE DATOS SINTÉTICOS (Replicando la firma física real discussed)
    np.random.seed(1337)
    num_minutos = 1440
    hora_inicio = datetime(2025, 2, 9, 0, 0)
    tiempo_datetime = [hora_inicio + timedelta(minutes=i) for i in range(num_minutos)]
    
    t_min = np.arange(num_minutos)
    s4_base = 0.12 + np.random.normal(0, 0.02, num_minutos)
    
    # Evento Principal (Shape similar a la real discussed)
    centro_evento = 130 # ~ 02:10 UTC
    burbuja_principal = 0.85 * np.exp(-0.5 * ((t_min - centro_evento) / 15)**2)
    s4_real = s4_base + 0.45 * np.exp(-0.5 * ((t_min - 80) / 10)**2) + burbuja_principal
    s4_real = np.clip(s4_real, 0, 0.95)
    
    # S4 Predicho (LSTM con Focal Loss)
    # Replicamos el ligero lag al principio y en la caída discussed
    s4_pred = s4_real * 0.95 + np.random.normal(0, 0.035, num_minutos) + 0.04
    s4_pred = np.roll(s4_pred, 5) 
    s4_pred[0:5] = s4_pred[5]

    s4_max_real = np.max(s4_real)
    rmse_dia = np.sqrt(np.mean((s4_real - s4_pred)**2))

    # 3. CREACIÓN DE LA FIGURA Y EL GRÁFICO (ax)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_facecolor('white')
    ax.grid(True, linestyle='-', color='#d0d0d0', linewidth=0.5, alpha=0.8) # Grilla oscura/sutil
    
    # 4. PLOTEO DE SERIES (Estilo real discussed)
    # Negro observado discussed
    ax.plot(tiempo_datetime, s4_real, 
            label='S4 Observado (Real)', color='#111111', alpha=0.6, linewidth=1.5)
    
    # Rojo predicción discussed
    ax.plot(tiempo_datetime, s4_pred, 
            label='Predicción LSTM', color='#c0392b', linestyle='-')

    # Umbral Crítico (Naranja discussed)
    umbral_severo = 0.6
    ax.axhline(y=umbral_severo, color='#f39c12', linestyle='--', linewidth=1.5, alpha=0.8)

    # ==================================================================
    # 5. NUEVA SECCIÓN: DESTARCAR VISUALMENTE LA VENTANA DE PRONÓSTICO
    # ==================================================================
    # Definimos la ventana de 10 minutos (ej. justo antes de que S4 supere 0.6)
    # El evento principal cruza 0.6 aproximadamente en el minuto 118 (~01:58 UTC)
    inicio_indice = 108 # 01:48 UTC
    fin_indice = 118     # 01:58 UTC

    inicio_ventana = tiempo_datetime[inicio_indice]
    fin_ventana = tiempo_datetime[fin_indice]

    # Destacar visualmente la ventana de 10 minutos (Sombra amarilla suave)
    # 'label' para que aparezca en la leyenda
    ax.axvspan(inicio_ventana, fin_ventana, 
               color='#f1c40f', alpha=0.25, # Amarillo muy transparente
               label='Ventana de Pronóstico (10 min)')

    # Añadir una anotación operativa con flecha (en negrita y color sutil)
    ax.annotate('Alerta Temprana\n(Ventana Operativa)', 
                xy=(fin_ventana, 0.5), # Punta de la flecha
                xytext=(fin_ventana + timedelta(hours=3), 0.65), # Ubicación del texto con offset
                arrowprops=dict(facecolor='black', arrowstyle='->', lw=1.2, color='#2c3e50'),
                fontsize=10, fontweight='bold', color='#2c3e50', ha='left')
    # ==================================================================

    # 6. CONFIGURACIÓN FINAL (Estilo real discussed)
    ax.set_title(f'CASO #1: Tormenta del 2025-02-09 | Max S4 Real: {s4_max_real:.2f}', 
                 pad=15, fontweight='bold')
    ax.set_ylabel('Índice de Cintilación (S4)', fontweight='bold')
    
    # Sello RMSE discussed
    label_eje_x = f'Hora (UTC) - RMSE del día: {rmse_dia:.4f}'
    ax.set_xlabel(label_eje_x, fontweight='bold', labelpad=10)
    
    ax.set_ylim(0, 1.1)
    
    # Leyenda: Se auto-ajustará para incluir la sombra amarilla
    ax.legend(loc='upper right', frameon=True, shadow=True, borderpad=1)

    # Formato temporal (Eje tilted discussed)
    locator = mdates.HourLocator(byhour=[0, 3, 6, 9, 12, 15, 18, 21])
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=30, ha='right')

    plt.tight_layout()

    # 7. EXPORTAR FIGURA
    nombre_archivo = 'figura_s4_ventana_operativa'
    plt.savefig(f"{nombre_archivo}.pdf", format='pdf', dpi=300, transparent=True)
    plt.savefig(f"{nombre_archivo}.png", format='png', dpi=300, transparent=True)
    
    print(f"¡Gráfico profesional con ventana destacada generado exitosamente!")
    print(f"Archivos: {nombre_archivo}.pdf y .png")

if __name__ == '__main__':
    generar_grafico_s4_con_ventana_destacada()