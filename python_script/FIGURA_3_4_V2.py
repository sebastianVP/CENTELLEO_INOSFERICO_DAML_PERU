import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuración de alta calidad para impresión académica
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'

def draw_academic_box(ax, x, y, width, height, title, body, bg_color, text_color='black'):
    """
    Dibuja un bloque metodológico perfectamente alineado y libre de distorsión.
    x, y: Esquina inferior izquierda del bloque.
    """
    # 1. Sombra geométrica sutil
    shadow = patches.Rectangle(
        (x + 0.12, y - 0.12), width, height,
        linewidth=0, facecolor='#cccccc', alpha=0.5, zorder=1
    )
    ax.add_patch(shadow)

    # 2. Caja Principal Rectangular (Estilo académico formal)
    rect = patches.Rectangle(
        (x, y), width, height,
        linewidth=2.0, edgecolor='#2C3E50', facecolor=bg_color, zorder=2
    )
    ax.add_patch(rect)

    # 3. Título del bloque (Centrado en el área superior del recuadro)
    ax.text(
        x + width / 2, y + height - 0.45, title,
        ha='center', va='center', fontsize=13, fontweight='bold', color=text_color, zorder=3
    )

    # 4. Línea divisoria interna
    ax.plot(
        [x + 0.4, x + width - 0.4], [y + height - 0.75, y + height - 0.75],
        color=text_color, alpha=0.25, lw=1.2, zorder=3
    )

    # 5. Viñetas / Contenido (Alineación izquierda con margen de seguridad)
    ax.text(
        x + 0.5, y + height - 0.95, body,
        ha='left', va='top', fontsize=11.5, color=text_color, linespacing=1.5, zorder=3
    )

def draw_flow_arrow(ax, start_xy, end_xy):
    """ Dibuja una flecha conectora sólida y recta entre bloques. """
    ax.annotate(
        "", xy=end_xy, xytext=start_xy,
        arrowprops=dict(arrowstyle="-|>,head_width=0.5,head_length=0.7", lw=2.5, color='#34495E'),
        zorder=1
    )

# =========================================================================
# LIENZO CONTROLADO (Proporciones simétricas perfectas para A4)
# =========================================================================
fig, ax = plt.subplots(figsize=(10, 16))
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')

# Al hacer xlim y ylim proporcionales a figsize, se elimina el 100% de la distorsión
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.axis('off')

# Título General del Diagrama
ax.text(5, 15.4, "DIAGRAMA DE FLUJO METODOLÓGICO",
        ha='center', va='center', fontsize=16, fontweight='bold', color='#1A1A1A')

# =========================================================================
# UBICACIÓN PRECISA DE LOS BLOQUES (Coordenadas X, Y absolutas)
# =========================================================================
box_x = 0.5
box_w = 9.0

# BLOQUE 1: Datos de Entrada
txt_1 = ("• Series temporales: S4, TEC, ROTI, Kp, Dst, AE, F10.7\n"
         "• Frecuencia de muestreo: 1 minuto  |  Periodo: Escala mensual")
draw_academic_box(ax, x=box_x, y=13.3, width=box_w, height=1.5,
                  title="DATOS DE ENTRADA (CSV)", body=txt_1,
                  bg_color="#455A64", text_color="white")

draw_flow_arrow(ax, start_xy=(5, 13.3), end_xy=(5, 12.6))

# BLOQUE 2: Fase 1
txt_2 = ("1. Carga masiva y validación (remoción activa de registros corruptos)\n"
         "2. Análisis exploratorio de datos y filtrado inicial de ruido\n"
         "3. Ingeniería de características avanzadas (Feature Engineering)\n"
         "4. División estricta del dataset: Entrenamiento (70%) / Val (15%) / Test (15%)\n"
         "5. Normalización escalar de características mediante MinMax Scaler")
draw_academic_box(ax, x=box_x, y=9.8, width=box_w, height=2.8,
                  title="FASE 1: PREPROCESAMIENTO", body=txt_2,
                  bg_color="#D4E6F1")

draw_flow_arrow(ax, start_xy=(5, 9.8), end_xy=(5, 9.1))

# BLOQUE 3: Fase 2
txt_3 = ("• Ventanas temporales (Windowing): Entrada (60 min) → Salida (20 min)\n"
         "• Arquitectura del modelo: Red Bi-LSTM con capas de Batch Normalization\n"
         "• Función de pérdida optimizada: Algoritmo Weighted Focal MSE\n"
         "• Tratamiento de desbalanceo severo: Técnica matemática de Oversampling\n"
         "• Control de entrenamiento: Optimizador Adam + Criterio de Early Stopping")
draw_academic_box(ax, x=box_x, y=6.3, width=box_w, height=2.8,
                  title="FASE 2: MODELAMIENTO MULTI-STEP", body=txt_3,
                  bg_color="#D5F5E3")

draw_flow_arrow(ax, start_xy=(5, 6.3), end_xy=(5, 5.6))

# BLOQUE 4: Fase 3
txt_4 = ("• Generación de predicción iterativa sobre el conjunto aislado de Test\n"
         "• Inversión de escala (Desnormalización para recuperar valores reales de S4)\n"
         "• Métricas de error estadístico global: Evaluación de RMSE y MAE\n"
         "• Evaluación especializada en picos de centelleo ionosférico: Event-RMSE\n"
         "• Comparativa de desempeño (Benchmark) frente a arquitecturas base")
draw_academic_box(ax, x=box_x, y=2.8, width=box_w, height=2.8,
                  title="FASE 3: EVALUACIÓN Y VALIDACIÓN", body=txt_4,
                  bg_color="#FDEBD0")

draw_flow_arrow(ax, start_xy=(5, 2.8), end_xy=(5, 2.1))

# BLOQUE 5: Salidas
txt_5 = ("• Modelo predictivo final completamente entrenado, guardado y validado\n"
         "• Matriz completa de métricas de desempeño y error predictivo\n"
         "• Gráficas vectoriales comparativas de la predicción temporal del índice S4\n"
         "• Reporte técnico integral estructurado de resultados metodológicos")
draw_academic_box(ax, x=box_x, y=0.3, width=box_w, height=1.8,
                  title="SALIDAS DEL SISTEMA", body=txt_5,
                  bg_color="#EBDEF0")

# =========================================================================
# EXPORTACIÓN DE CALIDAD VECTORIAL E IMAGEN
# =========================================================================
plt.tight_layout()

# El archivo .pdf es el formato ideal para LaTeX o Word porque no pierde resolución al ampliarse
plt.savefig("Diagrama_Metodologia_Academico.pdf", bbox_inches='tight', dpi=300)
plt.savefig("Diagrama_Metodologia_Academico.png", bbox_inches='tight', dpi=300)

plt.show()