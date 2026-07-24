import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generar_figura_multistep(output_pdf, output_png):
    # Configuración de alta calidad
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['font.family'] = 'DejaVu Sans'

    # Crear figura con 2 subgráficos (Señal temporal arriba, Estructura de tensores abajo)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 9), gridspec_kw={'height_ratios': [1.3, 1]})
    fig.patch.set_facecolor('#ffffff')

    # Eje X común
    x_min, x_max = -75, 20
    
    # =========================================================================
    # PANEL SUPERIOR: REPRESENTACIÓN TEMPORAL DE LA SEÑAL (S4)
    # =========================================================================
    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(-0.1, 1.2)
    ax1.axvline(x=0, color='#C0392B', linestyle='--', lw=2, zorder=1) # Línea t=0
    
    # 1. Simulación de la "Historia" (70 minutos, ruido + inicio de burbuja)
    t_past = np.linspace(-70, -1, 70)
    # Señal base con ruido que empieza a subir al final (Fase de ataque)
    s4_past = 0.1 + 0.05 * np.random.randn(70) + 0.8 * np.exp(-((t_past - 4)**2) / 100)
    s4_past = np.clip(s4_past, 0.05, 1.0)
    ax1.plot(t_past, s4_past, color='#2980B9', lw=1.5, alpha=0.8, label='Datos Históricos Observados')
    
    # 2. Simulación de la "Predicción" (10 minutos, curva suave)
    t_fut = np.linspace(0, 9, 10)
    # Continúa subiendo, alcanza el pico y decae
    s4_fut = 0.1 + 0.8 * np.exp(-((t_fut - 4)**2) / 100)
    ax1.plot(t_fut, s4_fut, color='#27AE60', lw=3, label='Trayectoria Vectorial Pronosticada')
    ax1.scatter(t_fut, s4_fut, color='#27AE60', s=40, zorder=5) # Puntos discretos
    
    # Áreas sombreadas para separar pasado y futuro
    ax1.axvspan(-70, -1, facecolor='#EBF5FB', alpha=0.5, zorder=0)
    ax1.axvspan(0, 9, facecolor='#EAFAF1', alpha=0.5, zorder=0)

    # Anotaciones de fases en la predicción
    ax1.annotate('Ataque', xy=(1.5, 0.7), xytext=(-8, 0.9),
                 arrowprops=dict(arrowstyle="->", color='#5D6D7E'), fontsize=10, weight='bold')
    ax1.annotate('Pico / Sostenimiento', xy=(4, 0.9), xytext=(2, 1.05),
                 arrowprops=dict(arrowstyle="->", color='#5D6D7E'), fontsize=10, weight='bold')
    ax1.annotate('Decaimiento', xy=(7, 0.6), xytext=(11, 0.8),
                 arrowprops=dict(arrowstyle="->", color='#5D6D7E'), fontsize=10, weight='bold')

    ax1.set_ylabel("Índice de Centelleo ($S_4$)", fontsize=12, weight='bold')
    ax1.set_title("A) Fenomenología: Evolución temporal de una burbuja de plasma", fontsize=14, weight='bold', loc='left', pad=10)
    ax1.legend(loc='upper left', fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.6)
    
    # Anotaciones de tiempo (Eje X)
    ax1.text(-35, -0.25, 'Ventana de Observación (Pasado: 70 min)', ha='center', fontsize=11, color='#2980B9', weight='bold')
    ax1.text(4.5, -0.25, 'Horizonte Predictivo\n(Futuro: 10 min)', ha='center', fontsize=11, color='#27AE60', weight='bold')

    # =========================================================================
    # PANEL INFERIOR: ESTRUCTURA MATEMÁTICA DE LOS TENSORES
    # =========================================================================
    ax2.set_xlim(x_min, x_max)
    ax2.set_ylim(-2, 11)
    ax2.axvline(x=0, color='#C0392B', linestyle='--', lw=2, zorder=1)
    
    # Texto separador temporal
    ax2.text(0, 10.5, 'Tiempo Actual ($t$)', color='#C0392B', ha='center', va='center', weight='bold', fontsize=12, bbox=dict(facecolor='white', edgecolor='none', pad=1))

    # 1. MATRIZ DE ENTRADA (X)
    # Dibujamos un bloque ancho (70 t-steps) y alto (9 features)
    rect_in = patches.Rectangle((-70, 0), 69, 9, linewidth=2, edgecolor='#1A5276', facecolor='#D6EAF8', zorder=2)
    ax2.add_patch(rect_in)
    
    # Líneas decorativas internas para simular filas (features)
    for i in range(1, 9):
        ax2.plot([-70, -1], [i, i], color='#A9CCE3', lw=1, zorder=2)
    
    # Etiquetas de la matriz
    ax2.text(-35.5, 4.5, "Matriz de Entrada Histórica ($X_t$)\n$X_t \in \mathbb{R}^{70 \\times 9}$", 
             ha='center', va='center', fontsize=12, weight='bold', color='#1A5276',
             bbox=dict(facecolor='#D6EAF8', edgecolor='none', alpha=0.9))
    ax2.text(-71, 4.5, "9 Características\n(Features)", ha='right', va='center', fontsize=10, rotation=90)
    ax2.text(-35.5, -1, "70 Pasos de Tiempo ($t-70$ a $t-1$)", ha='center', va='center', fontsize=10)

    # 2. FLECHA DEL MODELO
    ax2.annotate("", xy=(0, 4.5), xytext=(-1, 4.5),
                 arrowprops=dict(arrowstyle="->,head_length=0.8,head_width=0.5", color='#34495E', lw=3))
    ax2.text(-0.5, 5.5, "Modelo\nSeq2Seq", ha='center', va='center', fontsize=11, weight='bold', color='#34495E')

    # 3. VECTOR DE SALIDA (Y)
    # Dibujamos un bloque estrecho (10 t-steps) y bajo (1 target: S4)
    rect_out = patches.Rectangle((0, 4), 9, 1, linewidth=2, edgecolor='#1E8449', facecolor='#D5F5E3', zorder=2)
    ax2.add_patch(rect_out)
    
    # Líneas decorativas internas para simular columnas (pasos de tiempo pronosticados)
    for i in range(1, 9):
        ax2.plot([i, i], [4, 5], color='#A3E4D7', lw=1, zorder=2)

    # Etiquetas del vector
    ax2.text(4.5, 6, "Vector de Salida ($Y_t$)\n$Y_t \in \mathbb{R}^{10 \\times 1}$", 
             ha='center', va='center', fontsize=12, weight='bold', color='#1E8449')
    ax2.text(4.5, 3, "10 Pasos de Tiempo\n($t$ a $t+9$)", ha='center', va='center', fontsize=10)
    ax2.text(9.5, 4.5, "1 Objetivo\n(Target $S_4$)", ha='left', va='center', fontsize=10)

    ax2.set_title("B) Arquitectura de Tensores: Mapeo Sequence-to-Sequence (Multi-Step)", fontsize=14, weight='bold', loc='left', pad=10)
    ax2.axis('off') # Ocultar ejes para la parte de diagrama estructural

    # =========================================================================
    # EXPORTACIÓN
    # =========================================================================
    plt.tight_layout()
    # Ajustar un poco el espacio entre los dos paneles
    plt.subplots_adjust(hspace=0.4)
    
    plt.savefig(output_pdf, bbox_inches='tight', dpi=300, facecolor='#ffffff')
    plt.savefig(output_png, bbox_inches='tight', dpi=300, facecolor='#ffffff')
    plt.close()

# Ejecutar la función
generar_figura_multistep("Figura_2_5_MultiStep_Sequence.pdf", "Figura_2_5_MultiStep_Sequence.png")
print("¡Figura 2.5 generada con éxito como PDF y PNG!")