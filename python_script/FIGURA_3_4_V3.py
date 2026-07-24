import matplotlib.pyplot as plt
import matplotlib.patches as patches
import textwrap

# Configuración profesional de renderizado para tesis académicas
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'


def clean_text_wrap(text, max_chars=55):
    """
    Divide las líneas largas manteniendo la sangría y la estética
    de las viñetas (•) y las numeraciones (1.).
    """
    wrapped_lines = []
    for line in text.split('\n'):
        if not line.strip():
            continue
        if line.startswith('•') or (line[0].isdigit() and line[1] == '.'):
            prefix = "• " if line.startswith('•') else line[:3]
            content = line[2:] if line.startswith('•') else line[3:]
            wrapped = textwrap.wrap(content, width=max_chars - 4)
            if wrapped:
                wrapped_lines.append(prefix + wrapped[0])
                for w in wrapped[1:]:
                    wrapped_lines.append("    " + w)  # Sangría de alineación
        else:
            wrapped_lines.extend(textwrap.wrap(line, width=max_chars))
    return wrapped_lines


def draw_proportional_box(fig, ax, title, body_text, y_top, bg_color, text_color='black'):
    """
    Dibuja una caja cuyo alto se calcula MIDIENDO el texto realmente
    renderizado (con el renderer de matplotlib), en vez de asumir una
    altura fija por línea. Así el cuadro siempre queda del tamaño exacto
    que necesita el contenido, y el texto nunca se sale del recuadro.
    Devuelve el límite inferior (y_bottom) de la caja.
    """
    x_left = 10
    width = 80
    x_right = x_left + width
    body_x = 14
    available_width = (x_right - 2) - body_x  # margen derecho de 2 unidades

    title_y = y_top - 2.2
    body_y = y_top - 5.2

    # --- 1. Ajustamos el ancho de envoltura (max_chars) hasta que el texto
    #         quepa horizontalmente dentro de la caja, midiendo de verdad ---
    max_chars = 58
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    inv = ax.transData.inverted()

    while max_chars > 20:
        lines = clean_text_wrap(body_text, max_chars=max_chars)
        body_str = '\n'.join(lines)

        body_txt = ax.text(
            body_x, body_y, body_str,
            ha='left', va='top', fontsize=10.5, color=text_color,
            linespacing=1.4, zorder=2
        )
        fig.canvas.draw()
        bbox_disp = body_txt.get_window_extent(renderer=renderer)
        bbox_data = bbox_disp.transformed(inv)
        text_width = bbox_data.x1 - bbox_data.x0

        if text_width <= available_width:
            break
        body_txt.remove()
        max_chars -= 2
    else:
        lines = clean_text_wrap(body_text, max_chars=max_chars)
        body_str = '\n'.join(lines)
        body_txt = ax.text(
            body_x, body_y, body_str,
            ha='left', va='top', fontsize=10.5, color=text_color,
            linespacing=1.4, zorder=2
        )
        fig.canvas.draw()

    # --- 2. Colocamos el título ---
    title_txt = ax.text(
        50, title_y, title,
        ha='center', va='top', fontsize=12.5, fontweight='bold',
        color=text_color, zorder=2
    )
    fig.canvas.draw()

    # --- 3. Medimos la extensión vertical REAL de título y cuerpo ---
    title_bbox = title_txt.get_window_extent(renderer=renderer).transformed(inv)
    body_bbox = body_txt.get_window_extent(renderer=renderer).transformed(inv)

    lowest_y = min(title_bbox.y0, body_bbox.y0)

    padding_bottom = 2.2
    y_bottom = lowest_y - padding_bottom
    box_height = y_top - y_bottom

    # --- 4. Dibujamos la caja contenedora del tamaño exacto medido ---
    rect = patches.FancyBboxPatch(
        (x_left, y_bottom), width, box_height,
        boxstyle="round,pad=0",
        linewidth=2.0, edgecolor="#2C3E50", facecolor=bg_color, zorder=1
    )
    ax.add_patch(rect)

    return y_bottom


def draw_perfect_arrow(ax, y_start, y_end):
    """ Dibuja una flecha recta que une los bloques sin tocar sus bordes """
    ax.annotate(
        "", xy=(50, y_end), xytext=(50, y_start),
        arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.6", lw=2.5, color='#34495E'),
        zorder=1
    )


# =========================================================================
# CONFIGURACIÓN DEL LIENZO PROPORCIONAL (Formato vertical de alta calidad)
# =========================================================================
fig, ax = plt.subplots(figsize=(9, 15))
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')

# Límites provisionales; se recalculan al final según el contenido real
ax.set_xlim(0, 100)
ax.set_ylim(0, 120)
ax.axis('off')

# Título Principal del Diagrama
#main_title = ax.text(50, 116, "DIAGRAMA DE FLUJO METODOLÓGICO",
#                      ha='center', va='center', fontsize=16, fontweight='bold', color='#1A1A1A')

# =========================================================================
# DEFINICIÓN DE CONTENIDOS (Identificación completa de cajas y textos)
# =========================================================================
blocks = [
    {
        "title": "DATOS DE ENTRADA (CSV)",
        "body": "• Series: S4, TEC, ROTI, Kp, Dst, AE, F10.7\n• Frecuencia: 1 minuto  |  Periodo: meses",
        "bg": "#455A64", "text": "white"
    },
    {
        "title": "FASE 1: PREPROCESAMIENTO",
        "body": "1. Carga y validación de registros (eliminación de datos corruptos)\n2. Análisis exploratorio y filtrado inicial\n3. Ingeniería de características (Feature Engineering)\n4. División de conjuntos (Training 70% / Validation 15% / Test 15%)\n5. Normalización MinMax",
        "bg": "#D4E6F1", "text": "black"
    },
    {
        "title": "FASE 2: MODELAMIENTO MULTI-STEP",
        "body": "• Windowing: Tamaño de entrada (70 min) → Salida (10 min)\n• Arquitectura: Red Stacked-LSTM con Batch Normalization\n• Función de pérdida: Weighted Focal MSE\n• Estrategia de balanceo: Técnica de Oversampling\n• Optimización: Optimizador Adam + Early Stopping",
        "bg": "#D5F5E3", "text": "black"
    },
    {
        "title": "FASE 3: EVALUACIÓN Y VALIDACIÓN",
        "body": "• Predicción iterativa sobre el conjunto de datos de Test\n• Inversión de escala (Desnormalización de los datos)\n• Métricas de error globales: RMSE, MAE\n• Evaluación especializada en picos: Event-RMSE\n• Comparativa de desempeño (Benchmark) contra modelos base",
        "bg": "#FDEBD0", "text": "black"
    },
    {
        "title": "SALIDAS DEL SISTEMA",
        "body": "• Modelo predictivo entrenado y validado\n• Métricas de desempeño finales\n• Gráficas comparativas de predicción de S4\n• Reporte integral de resultados",
        "bg": "#EBDEF0", "text": "black"
    }
]

# =========================================================================
# EJECUCIÓN DEL MOTOR DE APILAMIENTO METODOLÓGICO (EVITA SOBREPOSICIÓN)
# =========================================================================
current_y = 111.0  # Punto de inicio superior en el lienzo
arrow_gap = 3.5    # Separación fija vertical reservada exclusivamente para cada flecha

for i, block in enumerate(blocks):
    # Dibuja la caja y calcula dinámicamente dónde termina su borde inferior (next_y)
    next_y = draw_proportional_box(
        fig, ax, title=block["title"], body_text=block["body"],
        y_top=current_y, bg_color=block["bg"], text_color=block["text"]
    )

    # Si no es la última caja, dibuja la flecha hacia abajo y actualiza el "techo" de la siguiente
    if i < len(blocks) - 1:
        draw_perfect_arrow(ax, y_start=next_y, y_end=next_y - arrow_gap)
        current_y = next_y - arrow_gap  # La siguiente caja comienza exactamente donde termina la flecha
    else:
        current_y = next_y

# --- Recortamos el lienzo verticalmente para que no sobre espacio en blanco ---
final_bottom = current_y - 2
ax.set_ylim(final_bottom, 120)

# Ajuste automático final de los márgenes del lienzo
plt.tight_layout()

# Guardado en formato vectorial (.pdf) de alta calidad para impresión y (.png) para revisión
plt.savefig("Metodologia_Proporcional_Final.pdf", bbox_inches='tight', dpi=300)
plt.savefig("Metodologia_Proporcional_Final.png", bbox_inches='tight', dpi=300)

plt.show()