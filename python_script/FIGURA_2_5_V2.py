import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generar_figura_multistep(output_pdf, output_png):
    # =========================================================================
    # 1. CONFIGURACIÓN DE IMPRESIÓN ALTA VISIBILIDAD (MITAD PÁGINA A4)
    # =========================================================================
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.weight'] = 'bold'
    plt.rcParams['text.color'] = '#000000'

    # Dimensiones físicas controladas
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.5, 5.0), gridspec_kw={'height_ratios': [1.2, 1.0]})
    fig.patch.set_facecolor('#ffffff')

    # Ampliamos ligeramente el límite derecho (de 20 a 30) para dar espacio al desplazamiento
    x_min, x_max = -75, 30
    
    # =========================================================================
    # PANEL SUPERIOR: REPRESENTACIÓN TEMPORAL DE LA SEÑAL (S4)
    # =========================================================================
    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(-0.15, 1.35) # Más aire vertical para las etiquetas grandes
    ax1.axvline(x=0, color='#C0392B', linestyle='--', lw=1.4, zorder=1) # Línea t=0
    
    # Simulación de Datos
    np.random.seed(42)  
    t_past = np.linspace(-70, -1, 70)
    s4_past = 0.1 + 0.04 * np.random.randn(70) + 0.8 * np.exp(-((t_past - 4)**2) / 100)
    s4_past = np.clip(s4_past, 0.05, 1.0)
    ax1.plot(t_past, s4_past, color='#2980B9', lw=1.4, alpha=0.8, label='Datos Históricos Observados')
    
    t_fut = np.linspace(0, 9, 10)
    s4_fut = 0.1 + 0.8 * np.exp(-((t_fut - 4)**2) / 100)
    ax1.plot(t_fut, s4_fut, color='#27AE60', lw=2.2, label='Trayectoria Pronosticada')
    ax1.scatter(t_fut, s4_fut, color='#27AE60', s=16, zorder=5) 
    
    # Áreas sombreadas temporales
    ax1.axvspan(-70, -1, facecolor='#EBF5FB', alpha=0.5, zorder=0)
    ax1.axvspan(0, 9, facecolor='#EAFAF1', alpha=0.5, zorder=0)

    # ANOTACIONES DE FASES (¡Letras mucho más grandes!)
    ax1.annotate('Ataque', xy=(1.5, 0.7), xytext=(-16, 0.95),
                 arrowprops=dict(arrowstyle="->", color='#5D6D7E', lw=1.0), fontsize=7.5, weight='bold')
    ax1.annotate('Pico', xy=(4, 0.9), xytext=(-1, 1.18),
                 arrowprops=dict(arrowstyle="->", color='#5D6D7E', lw=1.0), fontsize=7.5, weight='bold')
    ax1.annotate('Decaimiento', xy=(7, 0.6), xytext=(12, 0.90),
                 arrowprops=dict(arrowstyle="->", color='#5D6D7E', lw=1.0), fontsize=7.5, weight='bold')

    ax1.set_ylabel("Índice de Centelleo ($S_4$)", fontsize=8.5, weight='bold')
    ax1.legend(loc='upper left', fontsize=6.8, framealpha=0.9)
    ax1.grid(True, linestyle=':', alpha=0.5)
    
    # Ventanas Temporales inferiores aumentadas
    ax1.text(-35, -0.02, 'Ventana de Observación\n(Pasado: 70 min)', ha='center', va='top', fontsize=7.5, color='#1F618D', weight='bold')
    ax1.text(4.5, -0.02, 'Horizonte Predictivo\n(Futuro: 10 min)', ha='center', va='top', fontsize=7.5, color='#1E743B', weight='bold')
    
    ax1.tick_params(axis='both', which='major', labelsize=7.0)

    # =========================================================================
    # PANEL INFERIOR: ESTRUCTURA MATEMÁTICA DE LOS TENSORES
    # =========================================================================
    ax2.set_xlim(x_min, x_max)
    ax2.set_ylim(-3.5, 11)
    ax2.axvline(x=0, color='#C0392B', linestyle='--', lw=1.4, zorder=1)
    
    # Texto divisor temporal central (Agrandado)
    ax2.text(0, 10.5, 'Tiempo Actual ($t$)', color='#C0392B', ha='center', va='center', weight='bold', fontsize=8.0, 
             bbox=dict(facecolor='white', edgecolor='none', pad=1))

    # 1. Matriz de Entrada (X)
    rect_in = patches.Rectangle((-70, 0), 69, 9, linewidth=1.5, edgecolor='#1A5276', facecolor='#D6EAF8', zorder=2)
    ax2.add_patch(rect_in)
    
    for i in range(1, 9):
        ax2.plot([-70, -1], [i, i], color='#A9CCE3', lw=0.7, zorder=2)
    
    # Letras internas aumentadas a 8.0 puntos
    ax2.text(-35.5, 4.5, "Matriz de Entrada Histórica ($X_t$)\n$X_t \in \mathbb{R}^{70 \\times 9}$", 
             ha='center', va='center', fontsize=8.0, weight='bold', color='#1A5276',
             bbox=dict(facecolor='#D6EAF8', edgecolor='none', alpha=0.9, pad=1))
    
    ax2.text(-72.0, 4.5, "9 Características (Features)", ha='right', va='center', fontsize=7.5, rotation=90, weight='bold')
    ax2.text(-35.5, -1.2, "70 Pasos de Tiempo ($t-70$ a $t-1$)", ha='center', va='top', fontsize=7.5, weight='bold')

    # 2. MODELO SEQ2SEQ (Desplazado a la derecha en X=5.5 para no tapar la línea de tiempo t)
    X_MODELO = 5.5
    ax2.annotate("", xy=(X_MODELO + 2.0, 4.5), xytext=(-0.5, 4.5),
                 arrowprops=dict(arrowstyle="->,head_length=0.5,head_width=0.3", color='#34495E', lw=2.0))
    ax2.text(X_MODELO, 5.2, "Modelo\nSeq2Seq", ha='center', va='bottom', fontsize=8.0, weight='bold', color='#34495E',
             bbox=dict(facecolor='#ffffff', edgecolor='none', pad=1, alpha=0.9))

    # 3. VECTOR DE SALIDA (Y) (Desplazado a la derecha, comenzando en X=11 para airear el diseño)
    X_OUTPUT_START = 11.0
    rect_out = patches.Rectangle((X_OUTPUT_START, 4), 10, 1, linewidth=1.5, edgecolor='#1E8449', facecolor='#D5F5E3', zorder=2)
    ax2.add_patch(rect_out)
    
    for i in range(1, 10):
        ax2.plot([X_OUTPUT_START + i, X_OUTPUT_START + i], [4, 5], color='#A3E4D7', lw=0.7, zorder=2)

    # Títulos del vector con fuentes de tamaño 8.0 y 7.5 (Muy visibles)
    ax2.text(X_OUTPUT_START + 5.0, 7.2, "Vector de Salida ($Y_t$)\n$Y_t \in \mathbb{R}^{10 \\times 1}$", 
             ha='center', va='center', fontsize=8.0, weight='bold', color='#1E8449')
    ax2.text(X_OUTPUT_START + 5.0, 2.5, "10 Pasos\n($t$ a $t+9$)", ha='center', va='top', fontsize=7.5, weight='bold')
    ax2.text(X_OUTPUT_START + 10.8, 4.5, "1 Objetivo\n(Target $S_4$)", ha='left', va='center', fontsize=7.5, weight='bold')

    ax2.axis('off') 

    # =========================================================================
    # EXPORTACIÓN SÍNCRONA A4
    # =========================================================================
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.28)
    
    plt.savefig(output_pdf, bbox_inches='tight', dpi=300, facecolor='#ffffff', pad_inches=0.02)
    plt.savefig(output_png, bbox_inches='tight', dpi=300, facecolor='#ffffff', pad_inches=0.02)
    plt.close()

# Ejecutar la función
generar_figura_multistep("Figura_2_5_MultiStep_Sequence.pdf", "Figura_2_5_MultiStep_Sequence.png")
print("¡Figura 2.5 corregida con texto ampliado y flujo desplazado generada con éxito!")

# =========================================================================
# DESCRIPCIÓN FORMAL PARA LA LEYENDA DE LA TESIS (Cuerpo del Documento)
# =========================================================================
#
# Figura 2.5: Esquema estructural del mapeo Sequence-to-Sequence (Seq2Seq) 
# para el pronóstico multietapa (Multi-Step) del índice de centelleo S4. 
# En la sección superior se presenta el comportamiento fenomenológico temporal 
# de la señal afectado por una burbuja de plasma ecuatorial (EPB), delimitando 
# la ventana de observación histórica (70 minutos previos) frente al horizonte 
# predictivo futuro (10 minutos del vector objetivo, caracterizado por sus etapas 
# de ataque, pico y decaimiento). En la sección inferior se detalla la correspondencia 
# algebraica de los tensores dentro de la arquitectura de la red neuronal, donde la 
# matriz de entrada Xt (dimensión 70x9) recopila la dinámica temporal de las 9 
# variables predictoras exógenas y endógenas, la cual es procesada de forma compacta 
# por el modelo para proyectar directamente el vector multi-step Yt (dimensión 10x1) 
# correspondiente a la trayectoria univariada del índice S4.
#
# Fuente: Elaboración propia.
# =========================================================================