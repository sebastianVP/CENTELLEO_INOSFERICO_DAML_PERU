import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import datetime

# =========================================================================
# CONFIGURACIÓN ACADÉMICA Y TAMAÑOS DE FUENTE GLOBALES
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
    colnames = ['year', 'month', 'decimal_year', 'raw_ssn', 'smoothed_ssn', 'std', 'obs', 'marker']

    print("Intentando descargar datos solares actualizados desde SILSO...")
    try:
        df = pd.read_csv(url, sep='\s+', names=colnames, na_values=[-1.0])
        df['date'] = pd.to_datetime({'year': df['year'], 'month': df['month'], 'day': 1})
        datos_reales = True
    except Exception as e:
        print(f"Error al descargar datos: {e}. Se generará una gráfica simulada.")
        datos_reales = False

    # --- Generación de Gráfico ---
    fig, ax = plt.subplots(figsize=(14, 8.5)) 
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#fefefe')

    if datos_reales:
        ax.plot(df['date'], df['raw_ssn'], color='#3498DB', alpha=0.3, label='Número Mensual Crudo', lw=1.5)
        ax.plot(df['date'], df['smoothed_ssn'], color='#21618C', label='Tendencia Suavizada (13-meses)', lw=3.5)
    else:
        fechas = pd.date_range(start='1990-01-01', end='2027-01-01', freq='M')
        s4_sim = 10 + 120*np.exp(-((fechas.year - 2000)**2)/20) + \
                 90*np.exp(-((fechas.year - 2014)**2)/25) + \
                 160*np.exp(-((fechas.year - 2024.5)**2)/6) + 15*np.random.rand(len(fechas))
        smoothed_sim = pd.Series(s4_sim).rolling(window=13, center=True).mean()
        ax.plot(fechas, s4_sim, color='#3498DB', alpha=0.3, lw=1.5)
        ax.plot(fechas, smoothed_sim, color='#21618C', lw=3.5, label='Tendencia Simulada (C23-C25)')

    # --- Delimitación de Ciclos Solares ---
    ciclos = [
        {'name': 'Ciclo 23', 'start': datetime.datetime(1996, 5, 1)},
        {'name': 'Ciclo 24', 'start': datetime.datetime(2008, 12, 1)},
        {'name': 'Ciclo 25 (Fase Máxima)', 'start': datetime.datetime(2019, 12, 1)},
    ]

    for ciclo in ciclos:
        ax.axvline(ciclo['start'], color='black', linestyle=':', lw=2, alpha=0.6)
        ax.text(ciclo['start'] + datetime.timedelta(days=200), ax.get_ylim()[1] * 0.9, ciclo['name'],
                fontsize=16, fontweight='bold', ha='left', va='top', rotation=90)

    # =========================================================================
    # DELIMITACIÓN TEMPORAL DE LA MUESTRA DE ESTUDIO (2023-2025)
    # =========================================================================
    start_study = datetime.datetime(2023, 1, 1)
    end_study = datetime.datetime(2025, 12, 31)

    # Banda temporal del período 2023-2025
    ax.axvspan(start_study, end_study, color='#C0392B', alpha=0.25, zorder=0, label='Muestra de Estudio (2023-2025)')

    # Caja de justificación con texto grande y claro
    ax.annotate(
        "Justificación del Período:\n"
        "1. Coincidencia con Fase Máxima del Ciclo 25\n"
        "2. Mayor ocurrencia de Burbujas de Plasma\n"
        "3. Eventos de Centelleo Severo para Validación",
        xy=(datetime.datetime(2024, 6, 1), 150), 
        xytext=(datetime.datetime(1996, 1, 1), 220), 
        arrowprops=dict(arrowstyle="->,head_width=0.6,head_length=0.9", color='#C0392B', lw=2.5),
        fontsize=14, fontweight='bold', color='#ffffff',
        bbox=dict(facecolor='#C0392B', edgecolor='#943126', alpha=0.9, boxstyle='round,pad=0.6')
    )

    # =========================================================================
    # FORMATO ACADÉMICO FINAL
    # =========================================================================
    ax.set_ylabel("Número Mensual Total de Manchas Solares", fontsize=18, fontweight='bold', labelpad=15)
    ax.set_xlabel("Año", fontsize=18, fontweight='bold', labelpad=15)

    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_ylim(0, 260)
    
    # 1. AMPLIAR HASTA 2026: El límite llega hasta enero de 2027 para incluir todo 2026
    ax.set_xlim(datetime.datetime(1990, 1, 1), datetime.datetime(2027, 1, 1))

    # 2. CORREGIR TRASLAPE EJE X: Mostrar años cada 2 años para dar espacio
    ax.xaxis.set_major_locator(mdates.YearLocator(2)) 
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y')) 

    # 3. ROTACIÓN DE FECHAS: 45 grados para lectura perfecta en A4
    plt.xticks(rotation=45, ha='right')
    ax.tick_params(axis='both', which='major', labelsize=15)
    
    # 4. LEYENDA DENTRO DEL GRÁFICO: En la parte inferior central, en dos columnas
    ax.legend(loc='lower center', ncol=2, fontsize=14, framealpha=0.95, edgecolor='#943126', fancybox=True)

    # Exportación
    plt.tight_layout()
    plt.savefig(output_file_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(output_file_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Archivos guardados correctamente:\n- {output_file_pdf}\n- {output_file_png}")

if __name__ == "__main__":
    generar_figura_ciclo_solar(
        "Figura_3_2_Contexto_Ciclo_Solar_V3.pdf", 
        "Figura_3_2_Contexto_Ciclo_Solar_V3.png"
    )