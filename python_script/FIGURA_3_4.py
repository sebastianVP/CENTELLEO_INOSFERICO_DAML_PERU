import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_box(ax, xy, width, height, text, color, edgecolor="black"):
    rect = patches.FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02",
        linewidth=2,
        edgecolor=edgecolor,
        facecolor=color
    )
    ax.add_patch(rect)

    ax.text(
        xy[0] + width/2,
        xy[1] + height/2,
        text,
        ha='center',
        va='center',
        fontsize=9,
        wrap=True
    )

def draw_arrow(ax, start, end):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="->", lw=1.5)
    )

fig, ax = plt.subplots(figsize=(10, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 20)
ax.axis('off')

# Título
ax.text(5, 19, "DIAGRAMA DE FLUJO METODOLÓGICO",
        ha='center', fontsize=16, fontweight='bold')

# --- BLOQUES ---

draw_box(ax, (1, 16), 8, 2,
"""
DATOS DE ENTRADA (CSV)
• Series: S4, TEC, ROTI, Kp, Dst, AE, F10.7
• Frecuencia: 1 min | Periodo: meses
""", "#5f7c8a")

draw_box(ax, (1, 12), 8, 3.5,
"""
FASE 1: PREPROCESAMIENTO
1. Carga y validación
2. Análisis exploratorio
3. Feature Engineering
4. División (70/15/15)
5. Normalización MinMax
""", "#cfe2f3")

draw_box(ax, (1, 8), 8, 3.5,
"""
FASE 2: MODELAMIENTO MULTI-STEP
• Windowing (60 → 20)
• Bi-LSTM + BatchNorm
• Weighted Focal MSE
• Oversampling
• Adam + EarlyStopping
""", "#d9ead3")

draw_box(ax, (1, 4), 8, 3.5,
"""
FASE 3: EVALUACIÓN Y VALIDACIÓN
• Predicción test
• Desnormalización
• RMSE, MAE
• Event-RMSE
• Benchmark
""", "#fce5cd")

draw_box(ax, (1, 1), 8, 2,
"""
SALIDAS DEL SISTEMA
• Modelo entrenado
• Métricas
• Gráficas
• Reporte
""", "#ead1dc")

# --- FLECHAS ---
draw_arrow(ax, (5, 16), (5, 15.5))
draw_arrow(ax, (5, 12), (5, 11.5))
draw_arrow(ax, (5, 8), (5, 7.5))
draw_arrow(ax, (5, 4), (5, 3.5))

plt.tight_layout()
plt.show()