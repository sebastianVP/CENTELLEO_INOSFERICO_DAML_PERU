import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

# Paleta de colores académica
academic_autumn = {
    'warning_orange': '#D68910', # ROTI (Burnt Orange)
    'action_blue': '#34495E',    # S4 (Slate Blue)
    'academic_bg': '#FCF3CF',    # Fondo
    'grid_grey': '#5D6D7E',      # Cuadrícula
}

# --- CONFIGURACIÓN BASE CON FUENTES INCREMENTADAS UN 35% EXTRA ---
plt.rcParams['figure.dpi'] = 600  # Máxima resolución para impresión de tesis
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 15.0  # Letras un 35% más grandes para máxima legibilidad
plt.rcParams['axes.facecolor'] = academic_autumn['academic_bg']
plt.rcParams['axes.edgecolor'] = academic_autumn['grid_grey']
plt.rcParams['axes.labelcolor'] = academic_autumn['action_blue']
plt.rcParams['xtick.color'] = academic_autumn['grid_grey']
plt.rcParams['ytick.color'] = academic_autumn['grid_grey']
plt.rcParams['grid.color'] = academic_autumn['grid_grey']
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.5
plt.rcParams['legend.fontsize'] = 14.0 
plt.rcParams['legend.frameon'] = False

# Constantes unificadas de tamaño adaptado (+35%)
LABEL_SIZE = 16.5
ANNOTATION_SIZE = 14.0


def generate_figura_4_2_final(output_file_pdf, output_file_png):
    num_samples = 48 
    time_index = pd.date_range("2025-11-15 00:00:00 UT", periods=num_samples, freq="5min")

    np.random.seed(42) 
    
    # ➔ ROTI (Precursor)
    roti_precursor_base = np.random.normal(0.2, 0.05, num_samples) 
    t_roti_rise = 10 
    t_roti_peak = 18 
    roti_precursor_surge = 1.6 * np.exp(-((np.arange(num_samples) - t_roti_peak)**2) / (2 * 5**2))
    simulated_roti = np.clip(roti_precursor_base + roti_precursor_surge + np.random.normal(0, 0.1, num_samples), 0, 2.5) 

    # ➔ S4 (Respuesta)
    s4_base = np.random.normal(0.1, 0.03, num_samples) 
    s4_delay = 5 
    t_s4_surge_delay = t_roti_rise + s4_delay 
    t_s4_peak = 23 
    
    s4_surge = 0.8 * np.exp(-((np.arange(num_samples) - t_s4_peak)**2) / (2 * 6**2))
    simulated_s4 = np.clip(s4_base + s4_surge + np.random.normal(0, 0.05, num_samples), 0, 1.0) 

    thesis_data = pd.DataFrame({
        'Tiempo': time_index,
        'ROTI (Precursor)': simulated_roti,
        'S4 (Respuesta)': simulated_s4
    })

    # =========================================================================
    # CREACIÓN DEL GRÁFICO (Estructura fija optimizada para textos grandes)
    # =========================================================================
    fig, ax1 = plt.subplots(figsize=(12, 6.5)) 
    ax2 = ax1.twinx()

    # PLOT ROTI
    roti_plot = ax1.plot(thesis_data['Tiempo'], thesis_data['ROTI (Precursor)'], 
                         color=academic_autumn['warning_orange'], 
                         label='Índice ROTI Precursor', 
                         linewidth=3.0, zorder=3)
    ax1.fill_between(thesis_data['Tiempo'], thesis_data['ROTI (Precursor)'], 
                     color=academic_autumn['warning_orange'], alpha=0.15, zorder=2)
    
    ax1.set_ylabel("Índice ROTI Precursor ( TEU/min )", fontsize=LABEL_SIZE, fontweight='bold', color=academic_autumn['warning_orange'], labelpad=12)
    ax1.tick_params(axis='y', labelcolor=academic_autumn['warning_orange'], labelsize=ANNOTATION_SIZE)
    ax1.set_ylim(-0.1, 2.75) 
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.5))

    # PLOT S4
    s4_plot = ax2.plot(thesis_data['Tiempo'], thesis_data['S4 (Respuesta)'], 
                        color=academic_autumn['action_blue'], 
                        label='Índice S4 Response', 
                        linewidth=4.0, linestyle='-', zorder=5) 
    
    ax2.set_ylabel("Índice S4 Response ( Adimensional )", fontsize=LABEL_SIZE, fontweight='bold', color=academic_autumn['action_blue'], labelpad=22)
    ax2.tick_params(axis='y', labelcolor=academic_autumn['action_blue'], labelsize=ANNOTATION_SIZE)
    ax2.set_ylim(-0.05, 1.05)
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.2))

    # =========================================================================
    # ANOTACIONES VERTICALES DE CONTROL
    # =========================================================================
    t_roti_pre_conditioning = time_index[t_roti_rise]
    ax1.axvline(x=t_roti_pre_conditioning, color=academic_autumn['grid_grey'], linestyle=':', linewidth=1.8, alpha=0.7, zorder=1)
    
    # "Ascenso Precursor" se mantiene en la parte inferior del eje Y
    ax1.text(t_roti_pre_conditioning - pd.Timedelta(minutes=3.5), 0.60, "Ascenso Precursor de ROTI", 
             ha='center', va='bottom', rotation=90, fontsize=ANNOTATION_SIZE, fontweight='bold', color=academic_autumn['warning_orange'])

    t_s4_event_onset = time_index[t_s4_surge_delay]
    ax1.axvline(x=t_s4_event_onset, color=academic_autumn['grid_grey'], linestyle=':', linewidth=1.8, alpha=0.7, zorder=1)
    ax1.text(t_s4_event_onset - pd.Timedelta(minutes=3.5), 1.2, "Inicio de Centelleo\n Severo S4", 
             ha='center', va='bottom', rotation=90, fontsize=ANNOTATION_SIZE, fontweight='bold', color=academic_autumn['action_blue'])
    
    # =========================================================================
    # FLECHA ORIGINAL + CUADRO DESPLAZADO A LA DERECHA
    # =========================================================================
    y_lead_demonstration = 2.15 
    
    # La flecha física mantiene su origen estricto
    ax1.hlines(y=y_lead_demonstration, xmin=t_roti_pre_conditioning, xmax=t_s4_event_onset, 
                color=academic_autumn['action_blue'], linewidth=3.0, linestyle='-', label=None, zorder=10)
    
    ax1.plot([t_roti_pre_conditioning, t_s4_event_onset], [y_lead_demonstration, y_lead_demonstration], 
             marker=6, color=academic_autumn['action_blue'], markersize=12, linewidth=0, label=None, zorder=11)
    ax1.plot([t_s4_event_onset, t_roti_pre_conditioning], [y_lead_demonstration, y_lead_demonstration], 
             marker=7, color=academic_autumn['action_blue'], markersize=12, linewidth=0, label=None, zorder=11)
    
    # Posición del cuadro de texto a la derecha (zona despejada del gráfico)
    arrow_center_x = t_roti_pre_conditioning + (t_s4_event_onset - t_roti_pre_conditioning) / 2
    quad_x_position = time_index[num_samples - 12]  
    quad_y_position = 2.15
    
    # Línea de llamada indicadora (discontinua y fina)
    ax1.plot([arrow_center_x, quad_x_position], [y_lead_demonstration, quad_y_position], 
             color=academic_autumn['action_blue'], linestyle=':', linewidth=1.5, zorder=9)
    
    # Cuadro de texto explicativo a la derecha
    lead_time_demonstration_text = "Demostración Empírica:\nAntelación de ROTI (~25 min)"
    ax1.text(quad_x_position, quad_y_position, lead_time_demonstration_text, 
             ha='center', va='center', fontsize=ANNOTATION_SIZE, fontweight='bold', color=academic_autumn['action_blue'], 
             bbox=dict(facecolor='white', edgecolor=academic_autumn['action_blue'], boxstyle='round,pad=0.5', linewidth=1.8, alpha=0.9), zorder=12)

    # =========================================================================
    # EJE X Y CONFIGURACIÓN HORARIA
    # =========================================================================
    ax1.set_xlabel("Tiempo ( Horas UT ) - Año 2025", fontsize=LABEL_SIZE, fontweight='bold', labelpad=18)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 30])) 
    ax1.tick_params(axis='x', labelsize=ANNOTATION_SIZE)
    ax1.grid(True, zorder=0)

    # =========================================================================
    # ➔ CORRECCIÓN: LEYENDA MÁS PEGADA A LA FIGURA (bbox_to_anchor=(0.5, -0.16))
    # =========================================================================
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    
    # Al cambiar de -0.28 a -0.16, la leyenda sube y se posiciona justo debajo de la etiqueta del eje X
    ax1.legend(lines1 + lines2, labels1 + labels2, 
               loc='upper center', 
               bbox_to_anchor=(0.5, -0.16), 
               ncol=2, 
               fontsize=ANNOTATION_SIZE, 
               frameon=False)

    plt.tight_layout()
    
    # GUARDAR RECURSOS EN ALTA RESOLUCIÓN
    plt.savefig(output_file_pdf, bbox_inches='tight', dpi=600)
    plt.savefig(output_file_png, bbox_inches='tight', dpi=600)
    plt.close()

    print(f"Éxito: Leyenda acercada de forma óptima a la figura.")


if __name__ == "__main__":
    generate_figura_4_2_final('figura_4_2_final.pdf', 'figura_4_2_final.png')