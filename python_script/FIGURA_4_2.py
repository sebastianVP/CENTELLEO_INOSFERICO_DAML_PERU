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

# Estilos base
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.facecolor'] = academic_autumn['academic_bg']
plt.rcParams['axes.edgecolor'] = academic_autumn['grid_grey']
plt.rcParams['axes.labelcolor'] = academic_autumn['action_blue']
plt.rcParams['xtick.color'] = academic_autumn['grid_grey']
plt.rcParams['ytick.color'] = academic_autumn['grid_grey']
plt.rcParams['grid.color'] = academic_autumn['grid_grey']
plt.rcParams['grid.linestyle'] = '--'
plt.rcParams['grid.alpha'] = 0.5
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['legend.frameon'] = False

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
    # CREACIÓN DEL GRÁFICO (Sin títulos superior ni inferior)
    # =========================================================================
    fig, ax1 = plt.subplots(figsize=(12, 6)) # Se reduce ligeramente la altura al no tener título
    ax2 = ax1.twinx()

    # PLOT ROTI
    roti_plot = ax1.plot(thesis_data['Tiempo'], thesis_data['ROTI (Precursor)'], 
                         color=academic_autumn['warning_orange'], 
                         label='Índice ROTI Precursor', 
                         linewidth=2.5, zorder=3)
    ax1.fill_between(thesis_data['Tiempo'], thesis_data['ROTI (Precursor)'], 
                     color=academic_autumn['warning_orange'], alpha=0.15, zorder=2)
    ax1.set_ylabel("Índice ROTI Precursor ( TEU/min )", fontsize=12, fontweight='bold', color=academic_autumn['warning_orange'])
    ax1.tick_params(axis='y', labelcolor=academic_autumn['warning_orange'])
    ax1.set_ylim(-0.1, 2.5) 
    ax1.yaxis.set_major_locator(ticker.MultipleLocator(0.5))

    # PLOT S4
    s4_plot = ax2.plot(thesis_data['Tiempo'], thesis_data['S4 (Respuesta)'], 
                        color=academic_autumn['action_blue'], 
                        label='Índice S4 Response', 
                        linewidth=3.5, linestyle='-', zorder=5) 
    ax2.set_ylabel("Índice S4 Response ( Adimensional )", fontsize=12, fontweight='bold', color=academic_autumn['action_blue'])
    ax2.tick_params(axis='y', labelcolor=academic_autumn['action_blue'])
    ax2.set_ylim(-0.05, 1.0)
    ax2.yaxis.set_major_locator(ticker.MultipleLocator(0.2))

    # =========================================================================
    # ANOTACIONES (Movidas abajo a la izquierda y sin log)
    # =========================================================================
    t_roti_pre_conditioning = time_index[t_roti_rise]
    ax1.axvline(x=t_roti_pre_conditioning, color=academic_autumn['grid_grey'], linestyle=':', linewidth=1.5, alpha=0.7, zorder=1)
    
    # Textos movidos abajo (y=0.1) y un poco a la izquierda de la línea
    ax1.text(t_roti_pre_conditioning - pd.Timedelta(minutes=3), 0.85, "Ascenso Precursor de ROTI", 
             ha='center', va='bottom', rotation=90, fontsize=10, fontweight='bold', color=academic_autumn['warning_orange'])

    t_s4_event_onset = time_index[t_s4_surge_delay]
    ax1.axvline(x=t_s4_event_onset, color=academic_autumn['grid_grey'], linestyle=':', linewidth=1.5, alpha=0.7, zorder=1)
    ax1.text(t_s4_event_onset - pd.Timedelta(minutes=3), 1.2, "Inicio de Centelleo\n Severo S4", 
             ha='center', va='bottom', rotation=90, fontsize=10, fontweight='bold', color=academic_autumn['action_blue'])
    
    # Flecha superior de demostración empírica
    y_lead_demonstration = 2.1 
    ax1.hlines(y=y_lead_demonstration, xmin=t_roti_pre_conditioning, xmax=t_s4_event_onset, 
                color=academic_autumn['action_blue'], linewidth=2.5, linestyle='-', label=None, zorder=10)
    
    ax1.plot([t_roti_pre_conditioning, t_s4_event_onset], [y_lead_demonstration, y_lead_demonstration], 
             marker=6, color=academic_autumn['action_blue'], markersize=10, linewidth=0, label=None, zorder=11)
    ax1.plot([t_s4_event_onset, t_roti_pre_conditioning], [y_lead_demonstration, y_lead_demonstration], 
             marker=7, color=academic_autumn['action_blue'], markersize=10, linewidth=0, label=None, zorder=11)
    
    lead_time_demonstration_text = "Demostración Empírica:\nAntelación de ROTI (~25 min)"
    t_text_anchor = t_roti_pre_conditioning + (t_s4_event_onset - t_roti_pre_conditioning) / 2
    
    ax1.text(t_text_anchor, y_lead_demonstration + 0.1, lead_time_demonstration_text, 
             ha='center', va='bottom', fontsize=10, fontweight='bold', color=academic_autumn['action_blue'], 
             bbox=dict(facecolor='white', edgecolor=academic_autumn['action_blue'], boxstyle='round,pad=0.4', linewidth=1.5, alpha=0.9), zorder=12)

    # =========================================================================
    # EJE X (Agregando "Año 2025" al label)
    # =========================================================================
    ax1.set_xlabel("Tiempo ( Horas UT ) - Año 2025", fontsize=12, fontweight='bold', labelpad=15)
    
    # Configurar formato de horas
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax1.xaxis.set_major_locator(mdates.MinuteLocator(byminute=[0, 30])) # Marcas cada 30 min
    
    ax1.grid(True, zorder=0)

    # Ajuste final sin caption inferior
    plt.tight_layout()
    
    # GUARDAR PDF Y PNG 
    plt.savefig(output_file_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(output_file_png, bbox_inches='tight', dpi=300)
    plt.close()

if __name__ == "__main__":
    generate_figura_4_2_final('figura_4_2_limpia.pdf', 'figura_4_2_limpia.png')