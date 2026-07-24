import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# Configuración estética Academic Autumn
academic_autumn = {
    'warning_orange': '#D68910', # Falsos/Eventos
    'action_blue': '#34495E',    # Correctos/Calma
    'academic_bg': '#FCF3CF',    # Fondo
    'grid_grey': '#5D6D7E',      # Cuadrícula
    'light_blue': '#85C1E9',
    'light_orange': '#F5B041'
}

# --- CONFIGURACIÓN DE FUENTES EXTRAS GRANDES (INCREMENTO PROPORCIONAL) ---
plt.rcParams['figure.dpi'] = 600  # Máxima calidad de impresión para tesis
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 14.5  # Base global aumentada
plt.rcParams['axes.facecolor'] = academic_autumn['academic_bg']
plt.rcParams['axes.edgecolor'] = academic_autumn['grid_grey']
plt.rcParams['axes.labelcolor'] = academic_autumn['action_blue']
plt.rcParams['xtick.color'] = academic_autumn['grid_grey']
plt.rcParams['ytick.color'] = academic_autumn['grid_grey']

# Constantes unificadas para legibilidad robusta
FONT_SIZE_TITLE = 16.5
FONT_SIZE_LABEL = 14.5
FONT_SIZE_AXIS = 13.5
FONT_SIZE_TEXT_INSIDE = 12.0

def generate_figura_4_4_evaluacion_mejorada(output_pdf, output_png):
    # --- 1. PREPARACIÓN DE DATOS ---
    TP = 546
    FN = 194
    FP = 4878
    total_points = 257200
    TN = total_points - TP - FN - FP

    np.random.seed(42)
    # Generación de muestras representativas para el gráfico de dispersión
    tn_actual = np.random.normal(0.2, 0.12, 8000)
    tn_pred = tn_actual + np.random.normal(0, 0.1, 8000)
    tn_mask = (tn_actual < 0.6) & (tn_pred < 0.6)
    tn_actual, tn_pred = tn_actual[tn_mask], tn_pred[tn_mask]

    fp_actual = np.random.normal(0.45, 0.08, 1000)
    fp_pred = np.random.normal(0.7, 0.1, 1000)
    fp_mask = (fp_actual < 0.6) & (fp_pred >= 0.6)
    fp_actual, fp_pred = fp_actual[fp_mask][:500], fp_pred[fp_mask][:500]

    fn_actual = np.random.normal(0.7, 0.1, 500)
    fn_pred = np.random.normal(0.4, 0.1, 500)
    fn_mask = (fn_actual >= 0.6) & (fn_pred < 0.6)
    fn_actual, fn_pred = fn_actual[fn_mask][:150], fn_pred[fn_mask][:150]

    tp_actual = np.random.normal(0.8, 0.15, 1000)
    tp_pred = tp_actual + np.random.normal(0, 0.15, 1000)
    tp_mask = (tp_actual >= 0.6) & (tp_pred >= 0.6)
    tp_actual, tp_pred = tp_actual[tp_mask][:400], tp_pred[tp_mask][:400]

    x_scatter = np.concatenate([tn_actual, fp_actual, fn_actual, tp_actual])
    y_scatter = np.concatenate([tn_pred, fp_pred, fn_pred, tp_pred])
    
    colors = ['#BDC3C7']*len(tn_actual) + [academic_autumn['warning_orange']]*len(fp_actual) + \
             ['#E74C3C']*len(fn_actual) + [academic_autumn['action_blue']]*len(tp_actual)

    # --- 2. CREACIÓN DE LA FIGURA (Mantiene proporciones originales externas) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor(academic_autumn['academic_bg'])

    # --- GRÁFICO 1: SCATTER PLOT ---
    ax1.set_facecolor('white')
    # Se aumenta el tamaño de los puntos de s=15 a s=35 para rellenar visualmente el espacio interno
    ax1.scatter(x_scatter, y_scatter, c=colors, alpha=0.4, s=35, edgecolors='none')
    ax1.axvline(x=0.6, color=academic_autumn['grid_grey'], linestyle='--', linewidth=2.2)
    ax1.axhline(y=0.6, color=academic_autumn['grid_grey'], linestyle='--', linewidth=2.2)
    
    # Textos de los cuadrantes con fuentes escaladas
    ax1.text(0.05, 1.12, 'Falsas Alarmas (FP)', color=academic_autumn['warning_orange'], fontweight='bold', fontsize=FONT_SIZE_TEXT_INSIDE)
    ax1.text(0.65, 1.12, 'Aciertos Tormenta (TP)', color=academic_autumn['action_blue'], fontweight='bold', fontsize=FONT_SIZE_TEXT_INSIDE)
    ax1.text(0.05, 0.05, 'Calma Correcta (TN)', color='#7F8C8D', fontweight='bold', fontsize=FONT_SIZE_TEXT_INSIDE)
    ax1.text(0.65, 0.05, 'Fugas (FN)', color='#E74C3C', fontweight='bold', fontsize=FONT_SIZE_TEXT_INSIDE)

    ax1.set_xlabel('Índice S4 Real (Observado)', fontsize=FONT_SIZE_LABEL, fontweight='bold', labelpad=10)
    ax1.set_ylabel('Índice S4 Predicho (Modelo WFL)', fontsize=FONT_SIZE_LABEL, fontweight='bold', labelpad=10)
    ax1.set_title('a) Dispersión Predictiva', fontsize=FONT_SIZE_TITLE, fontweight='bold', color=academic_autumn['action_blue'], pad=12)
    ax1.set_xlim(0, 1.2)
    ax1.set_ylim(0, 1.2)
    ax1.tick_params(axis='both', labelsize=FONT_SIZE_AXIS)
    ax1.grid(True, linestyle=':', alpha=0.6)

    # --- GRÁFICO 2: MATRIZ DE CONFUSIÓN ---
    cm = np.array([[TN, FP], [FN, TP]])
    cmap_cm = LinearSegmentedColormap.from_list('academic_cm', ['white', academic_autumn['light_blue'], academic_autumn['action_blue']])
    
    # "size": 17 hace que los números grandes dentro de la matriz sean muy claros
    sns.heatmap(cm, annot=True, fmt="d", cmap=cmap_cm, ax=ax2, 
                annot_kws={"size": 17, "weight": "bold"}, cbar=False,
                linewidths=2.5, linecolor=academic_autumn['grid_grey'])
    
    ax2.set_xticklabels(['Calma\n(S4 $\leq$ 0.6)', 'Tormenta\n(S4 > 0.6)'], fontsize=FONT_SIZE_AXIS, fontweight='bold')
    ax2.set_yticklabels(['Calma\n(S4 $\leq$ 0.6)', 'Tormenta\n(S4 > 0.6)'], fontsize=FONT_SIZE_AXIS, fontweight='bold', va='center')
    ax2.set_xlabel('Predicción del Modelo', fontsize=FONT_SIZE_LABEL, fontweight='bold', labelpad=12)
    ax2.set_ylabel('Realidad Observada', fontsize=FONT_SIZE_LABEL, fontweight='bold', labelpad=12)
    ax2.set_title('b) Matriz de Confusión', fontsize=FONT_SIZE_TITLE, fontweight='bold', color=academic_autumn['action_blue'], pad=12)
    ax2.tick_params(axis='both', labelsize=FONT_SIZE_AXIS)

    # --- CAJA DE MÉTRICAS COMPACTA Y CERCANA ---
    metrics_text = (
        "          MÉTRICAS DEL TRADE-OFF (FOCAL LOSS)          \n"
        "───────────────────────────────────────────────────────\n"
        " ▶ Recall (Clave): 73.78%  ➔ Prioriza detectar tormentas \n"
        " ▶ Precision:      10.07%  ➔ Tolera falsas alarmas      \n"
        " ▶ F1-Score:       0.1772  ➔ Balance general del modelo "
    )
    
    props = dict(boxstyle='round,pad=0.6', facecolor='white', alpha=0.95, 
                 edgecolor=academic_autumn['warning_orange'], linewidth=2)
    
    # ➔ CORRECCIÓN: De -0.40 a -0.28 para arrastrar la leyenda mucho más cerca del gráfico b
    ax2.text(0.5, -0.28, metrics_text, transform=ax2.transAxes, fontsize=FONT_SIZE_AXIS - 0.5,
             verticalalignment='top', horizontalalignment='center', multialignment='left', 
             bbox=props, fontweight='bold', color=academic_autumn['action_blue'], fontfamily='monospace')

    plt.tight_layout()
    # ➔ CORRECCIÓN: Se reduce el ajuste de la base a 0.20 para evitar espacios vacíos innecesarios
    plt.subplots_adjust(bottom=0.20) 
    
    # GUARDAR RECURSOS EN ULTRA RESOLUCIÓN
    plt.savefig(output_pdf, bbox_inches='tight', dpi=600)
    plt.savefig(output_png, bbox_inches='tight', dpi=600)
    plt.close()

    print("Éxito: Elementos internos agrandados y cuadro de métricas aproximado correctamente.")

if __name__ == "__main__":
    generate_figura_4_4_evaluacion_mejorada('figura_4_4_matriz_focal_loss_corregida.pdf', 'figura_4_4_matriz_focal_loss_corregida.png')