import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import datetime

# =========================================================================
# CONFIGURACIÓN ACADÉMICA
# =========================================================================
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'  # Tipografía limpia y estándar

def generar_figura_ciclo_solar(output_file_pdf, output_file_png):
    """
    Genera una gráfica histórica de manchas solares justificando el período
    de estudio 2023-2025 para la tesis DAML PERÚ, contrastando el Ciclo
    Solar 25 con los anteriores.
    """
    
    # URL oficial de SILSO Monthly Total Sunspot Number V2.0
    url = "https://www.sidc.be/silso/DATA/SN_m_tot_v2.0.txt"
    # Columnas SILSO: Año, Mes, Año_decimal, SSN_crudo, SSN_suavizado, std, obs, marker
    colnames = ['year', 'month', 'decimal_year', 'raw_ssn', 'smoothed_ssn', 'std', 'obs', 'marker']

    print("Intentando descargar datos solares actualizados desde SILSO...")
    try:
        df = pd.read_csv(url, sep='\s+', names=colnames, na_values=[-1.0])
        # Crear columna de fecha para graficar
        df['date'] = pd.to_datetime({'year': df['year'], 'month': df['month'], 'day': 1})
        datos_reales = True
    except Exception as e:
        print(f"Error al descargar datos: {e}. Se generará una gráfica simulada.")
        datos_reales = False

    # --- Generación de Gráfico ---
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#fefefe')

    if datos_reales:
        # 1. Datos crudos mensuales (ruido ligero)
        ax.plot(df['date'], df['raw_ssn'], color='#3498DB', alpha=0.3, label='Número Mensual Crudo', lw=1)
        # 2. Tendencia Suavizada (Media móvil 13 meses oficial o recalculada)
        ax.plot(df['date'], df['smoothed_ssn'], color='#21618C', label='Tendencia Suavizada (SILSO 13-meses)', lw=3)
    else:
        # Contingencia: Datos Simulados Representativos
        fechas = pd.date_range(start='1990-01-01', end='2026-06-01', freq='M')
        # Simulación de 3 ciclos con pico creciente en C25
        s4_sim = 10 + 120*np.exp(-((fechas.year - 2000)**2)/20) + \
                 90*np.exp(-((fechas.year - 2014)**2)/25) + \
                 160*np.exp(-((fechas.year - 2024.5)**2)/6) + 15*np.random.rand(len(fechas))
        smoothed_sim = pd.Series(s4_sim).rolling(window=13, center=True).mean()
        ax.plot(fechas, s4_sim, color='#3498DB', alpha=0.3, lw=1)
        ax.plot(fechas, smoothed_sim, color='#21618C', lw=3, label='Tendencia Simulada (C23-C25)')

    # --- Delimitación de Ciclos Solares ---
    # Mínimos oficiales NOAA: C24: Dic 2008 / C25: Dic 2019
    # Mínimo C23 (SILSO aprox): May 1996
    ciclos = [
        {'name': 'Ciclo 23', 'start': datetime.datetime(1996, 5, 1)},
        {'name': 'Ciclo 24', 'start': datetime.datetime(2008, 12, 1)},
        {'name': 'Ciclo 25 (Fase Máxima Actual)', 'start': datetime.datetime(2019, 12, 1)},
    ]

    for ciclo in ciclos:
        ax.axvline(ciclo['start'], color='black', linestyle=':', lw=1.5, alpha=0.6)
        # Añadir nombre del ciclo
        ax.text(ciclo['start'] + datetime.timedelta(days=200), ax.get_ylim()[1] * 0.9, ciclo['name'],
                fontsize=11, fontweight='bold', ha='left', va='top', rotation=90)

    # =========================================================================
    # DELIMITACIÓN TEMPORAL DE LA MUESTRA DE ESTUDIO (2023-2025)
    # =================================================════════════════════════
    start_study = datetime.datetime(2023, 1, 1)
    end_study = datetime.datetime(2025, 12, 31)

    # Resaltar la banda temporal del período 2023-2025
    ax.axvspan(start_study, end_study, color='#C0392B', alpha=0.25, zorder=0, label='Muestra de Estudio DAML (2023-2025)')

    # ➔ Justificación Annotation box (Caja de Texto con flecha)
    # Colocar la flecha en la fase máxima
    ax.annotate(
        "Justificación del Período:\n"
        "1. Coincidencia con la Fase Máxima del Ciclo 25\n"
        "2. Maximización de ocurrencia de Burbujas de Plasma\n"
        "3. Captura de eventos de Centelleo Severo para Validación",
        xy=(datetime.datetime(2024, 6, 1), 150), # Punta de la flecha
        xytext=(datetime.datetime(1996, 1, 1), 220), # Posición de la caja
        arrowprops=dict(arrowstyle="->,head_width=0.5,head_length=0.8", color='#C0392B', lw=2),
        fontsize=11, fontweight='bold', color='#ffffff',
        bbox=dict(facecolor='#C0392B', edgecolor='#943126', alpha=0.9, boxstyle='round,pad=0.5')
    )

    # =========================================================================
    # FORMATO ACADÉMICO FINAL (Español)
    # =========================================================================
    #ax.set_title("Figura 3.2: Contexto Histórico del Número de Manchas Solares\ny Delimitación de la Muestra de Estudio (2023-2025)", fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel("Número Mensual Total de Manchas Solares (Monthly SSN)", fontsize=13, fontweight='bold')
    ax.set_xlabel("Año", fontsize=13, fontweight='bold')

    # Configuración de Ejes
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_ylim(0, 260)
    # Mostrar desde 1990 para dar contexto a los ciclos modernos
    ax.set_xlim(datetime.datetime(1990, 1, 1), datetime.datetime(2026, 7, 1))

    # Formatear Eje X
    ax.xaxis.set_major_locator(plt.MaxNLocator(15))
    
    # Leyenda
    ax.legend(loc='upper right', fontsize=11, framealpha=0.95)

    # Exportación segura
    plt.tight_layout()
    plt.savefig(output_file_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(output_file_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Archivos guardados correctamente:\n- {output_file_pdf}\n- {output_file_png}")

if __name__ == "__main__":
    generar_figura_ciclo_solar(
        "Figura_3_2_Contexto_Ciclo_Solar.pdf", 
        "Figura_3_2_Contexto_Ciclo_Solar.png"
    )