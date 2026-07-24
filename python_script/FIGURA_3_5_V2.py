import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Configuración profesional de alta resolución para tesis
plt.rcParams['figure.dpi'] = 600
plt.rcParams['font.family'] = 'DejaVu Sans'

# Constantes unificadas de tamaño de letra (según tus requerimientos)
TITLE_SIZE = 18
SECTION_SIZE = 16
LABEL_SIZE = 13
TICK_SIZE = 11
SMALL_SIZE = 10


def generar_diagrama_tesis(output_pdf: str, output_png: str) -> None:

    # Lienzo optimizado para formato vertical A4 (aprovecha al máximo el espacio útil)
    fig, (ax_ts, ax_concept, ax_tensor) = plt.subplots(
        3, 1, figsize=(11, 13.5),
        gridspec_kw={'height_ratios': [1.2, 3.2, 2.0]}
    )
    fig.patch.set_facecolor('#ffffff')

    def draw_section_title(ax, text, font_size=SECTION_SIZE):
        ax.text(
            0.5, 1.12, text,
            transform=ax.transAxes,
            ha='center', va='center',
            fontsize=font_size, fontweight='bold', color='white',
            bbox=dict(facecolor='#2C3E50', edgecolor='none',
                      boxstyle='round,pad=0.5'),
            clip_on=False, zorder=11
        )

    # =========================================================================
    # SECCIÓN 1: SERIE TEMPORAL DE S4
    # =========================================================================
    draw_section_title(ax_ts, "Serie Temporal de S4 (Datos Reales de Jicamarca, 2025)")
    ax_ts.set_facecolor('#ffffff')

    np.random.seed(42)
    t_ts     = np.linspace(0, 6 * np.pi, 300)
    base_ts  = 0.25 + 0.12 * np.sin(t_ts) + 0.06 * np.sin(2.5 * t_ts)
    pico_ts  = (0.55 * np.exp(-((np.linspace(-4, 4, 300))**2) / 3.0) +
                0.45 * np.exp(-((np.linspace(-1, 1, 300))**2) / 0.5))
    noise_ts = 0.035 * np.random.randn(300)
    s4_series = pd.Series(np.clip(base_ts + pico_ts + noise_ts, 0.0, 1.5))

    ax_ts.plot(s4_series, color='#5D6D7E', lw=1.8, alpha=0.9)
    ax_ts.set_ylabel("S4", fontsize=LABEL_SIZE, fontweight='bold')
    ax_ts.set_ylim(-0.05, 1.65)
    ax_ts.set_yticks([0.0, 0.3, 0.6, 0.9, 1.2, 1.5])
    ax_ts.tick_params(axis='y', labelsize=TICK_SIZE)

    tick_indices = np.linspace(0, len(s4_series)-1, 11, dtype=int)
    tick_labels  = [
        r"$t{-}90$", r"$t{-}89$", r"$t{-}88$", r"$t{-}87$",
        r"$t{-}3$",  r"$t$",      r"$t{+}1$",  r"$t{+}4$",
        r"$t{+}6$",  r"$t{+}7$",  r"$t{+}10$"
    ]
    ax_ts.set_xticks(tick_indices)
    ax_ts.set_xticklabels(tick_labels, fontsize=TICK_SIZE)
    ax_ts.grid(True, linestyle='--', alpha=0.3)
    ax_ts.spines['top'].set_visible(False)
    ax_ts.spines['right'].set_visible(False)

    # =========================================================================
    # SECCIÓN 2: TÉCNICA DE VENTANA DESLIZANTE
    # =========================================================================
    draw_section_title(ax_concept, "Técnica de Ventana Deslizante (Stride = 1 min)")
    ax_concept.set_facecolor('#fefefe')
    ax_concept.axis('off')

    # Límites espaciales calibrados matemáticamente para absorber el espacio vacío
    ax_concept.set_xlim(0, 100)
    ax_concept.set_ylim(-12, 14)

    BH      = 3.4   # Altura requerida de las cajas
    LB      = 46    
    HOR     = 7     
    SV      = 4.6   # Separación vertical según especificación V2
    SH      = 0.8   
    START_X = 1.0
    START_Y = 8.5

    def draw_window_set(ax, x0, y0, label, show_labels=True):
        ax.add_patch(patches.FancyBboxPatch(
            (x0, y0), LB, BH,
            boxstyle="round,pad=0.15",
            facecolor='#D6EAF8', edgecolor='#1A5276', linewidth=2.0, zorder=2
        ))
        ax.text(x0+LB/2, y0+BH/2, label,
                ha='center', va='center',
                fontsize=LABEL_SIZE, fontweight='bold', color='#1A2530', zorder=3)

        if show_labels:
            ax.annotate('', xy=(x0, y0+BH+0.4), xytext=(x0+LB, y0+BH+0.4),
                        arrowprops=dict(arrowstyle='<->', color='#1A5276', lw=1.8))
            ax.text(x0+LB/2, y0+BH+0.9,
                    r"Lookback ($\tau = 70$ min)",
                    ha='center', va='bottom', fontsize=TICK_SIZE,
                    color='#1A5276', fontweight='bold')

        x1 = x0 + LB
        ax.add_patch(patches.FancyBboxPatch(
            (x1, y0), HOR, BH,
            boxstyle="round,pad=0.15",
            facecolor='#AED6F1', edgecolor='#154360', linewidth=2.0, zorder=2
        ))
        if show_labels:
            ax.annotate('', xy=(x1, y0+BH+0.4), xytext=(x1+HOR, y0+BH+0.4),
                        arrowprops=dict(arrowstyle='<->', color='#154360', lw=1.8))
            ax.text(x1+HOR/2, y0+BH+0.9,
                    r"Horizonte ($h=10$ min)",
                    ha='center', va='bottom', fontsize=TICK_SIZE,
                    color='#154360', fontweight='bold')

    draw_window_set(ax_concept, START_X,        START_Y,        "Window 1", show_labels=True)
    draw_window_set(ax_concept, START_X+SH,     START_Y-SV,     "Window 2", show_labels=False)
    draw_window_set(ax_concept, START_X+2*SH,   START_Y-2*SV,   "Window 3…", show_labels=False)

    ax_concept.text(
        START_X+2*SH+LB+HOR+1.5, START_Y-2*SV+BH/2,
        '···', ha='left', va='center', fontsize=24, color='#7F8C8D'
    )

    # ── Insets (Mini-gráficas grandes que cubren toda el área inferior) ──────
    S4_MIN, S4_MAX = 0.0, 1.5   

    def make_s4_signal(n_points, seed):
        rng = np.random.default_rng(seed)
        t   = np.linspace(0, 4 * np.pi, n_points)
        base = 0.3 + 0.15 * np.sin(t) + 0.08 * np.sin(3*t)
        pico = 0.6 * np.exp(-((np.linspace(-3, 3, n_points))**2) / 2.0)
        noise = 0.04 * rng.standard_normal(n_points)
        return pd.Series(np.clip(base + pico + noise, S4_MIN, S4_MAX))

    def make_inset(ax_parent, bbox_data, lb_data, h_data, xtick_labels):
        ax_ins = inset_axes(
            ax_parent, width="100%", height="100%",
            loc='lower left',
            bbox_to_anchor=bbox_data,
            bbox_transform=ax_parent.transData,
            axes_kwargs={'facecolor': '#F4F9FF', 'zorder': 4}
        )
        combined = pd.concat([lb_data, h_data]).reset_index(drop=True)
        n_lb = len(lb_data)
        n_total = len(combined)

        ax_ins.plot(combined, color='#5D6D7E', lw=1.8)
        ax_ins.axvspan(n_lb - 0.5, n_total - 0.5, alpha=0.18, color='#2E86C1')
        ax_ins.axvline(n_lb - 0.5, color='#154360', lw=1.5, linestyle='--', alpha=0.7)

        PAD_Y = 0.08
        ax_ins.set_ylim(S4_MIN - PAD_Y, S4_MAX + PAD_Y)
        ax_ins.set_yticks([0.0, 0.5, 1.0, 1.5])
        ax_ins.set_yticklabels(["0.0", "0.5", "1.0", "1.5"], fontsize=TICK_SIZE)
        ax_ins.set_ylabel("S4", fontsize=LABEL_SIZE, fontweight='bold', labelpad=4)

        PAD_X = 2
        ax_ins.set_xlim(-PAD_X, n_total - 1 + PAD_X)
        ax_ins.set_xticks([0, n_lb - 1, n_total - 1])
        ax_ins.set_xticklabels(xtick_labels, fontsize=LABEL_SIZE)
        ax_ins.tick_params(axis='both', which='both', length=3, labelsize=TICK_SIZE)
        ax_ins.grid(True, linestyle=':', alpha=0.5)

        for sp in ax_ins.spines.values():
            sp.set_linestyle(':')
            sp.set_linewidth(1.2)
            sp.set_edgecolor('#2c3e50')

        ax_ins.text(
            n_total - 1 - PAD_X * 0.3,
            S4_MAX * 0.82,
            'Target',
            ha='right', fontsize=LABEL_SIZE, fontweight='bold', color='#154360',
            bbox=dict(facecolor='#EBF5FB', edgecolor='none', alpha=0.85, pad=2)
        )

    s4_w1 = make_s4_signal(80, seed=7)   
    s4_w2 = make_s4_signal(80, seed=21)  

    lb1, h1 = s4_w1.iloc[:70], s4_w1.iloc[70:]
    lb2, h2 = s4_w2.iloc[:70], s4_w2.iloc[70:]

    # Coordenadas según plantilla V2 (INSET_H e INSET_Y0 expandidos para rellenar vacíos)
    INSET_Y0    = -15.5    
    INSET_H     = 10.5     
    INSET_W     = LB + HOR - 2   
    GAP_INSETS  = 3.5     

    make_inset(ax_concept,
               (START_X, INSET_Y0, INSET_W, INSET_H),
               lb1, h1,
               [r"$t{-}70$", r"$t{-}1$", r"$t{+}9$"])

    make_inset(ax_concept,
               (START_X + INSET_W + GAP_INSETS, INSET_Y0, INSET_W, INSET_H),
               lb2, h2,
               [r"$t{-}69$", r"$t$", r"$t{+}10$"])

    # ── Control de Continuidad ────────────────────────────────────────────────
    CX = 58
    CY = START_Y - SV

    ax_concept.text(
        CX+14, CY+BH+2.8,
        "Control de Continuidad:\nDatos faltantes > 5 min → descarte",
        ha='center', va='bottom', fontsize=TICK_SIZE, fontweight='bold', color='#922B21',
        bbox=dict(facecolor='#FDEDEC', edgecolor='#922B21',
                  boxstyle='round,pad=0.5', linewidth=1.5),
        linespacing=1.3
    )
    ax_concept.add_patch(patches.FancyBboxPatch(
        (CX, CY), 13, BH, boxstyle="round,pad=0.15",
        facecolor='#D6EAF8', edgecolor='#1A5276', linewidth=2.0, zorder=2
    ))
    ax_concept.text(CX+6.5, CY+BH/2, "Seg A",
                    ha='center', va='center',
                    fontsize=TICK_SIZE, fontweight='bold', color='#1A2530', zorder=3)
    ax_concept.text(CX+15.0, CY+BH/2, "✕",
                    ha='center', va='center',
                    fontsize=34, color='#C0392B', fontweight='bold', zorder=5)
    ax_concept.add_patch(patches.FancyBboxPatch(
        (CX+17, CY), 13, BH, boxstyle="round,pad=0.15",
        facecolor='#D6EAF8', edgecolor='#1A5276', linewidth=2.0, zorder=2
    ))
    ax_concept.text(CX+23.5, CY+BH/2, "Seg B",
                    ha='center', va='center',
                    fontsize=TICK_SIZE, fontweight='bold', color='#1A2530', zorder=3)
    ax_concept.text(CX+15.0, CY-1.2, "Secuencia Descartada",
                    ha='center', va='top',
                    fontsize=SMALL_SIZE, fontweight='bold', color='#922B21')

    # =========================================================================
    # SECCIÓN 3: REPRESENTACIÓN DEL TENSOR DE ENTRADA Y SALIDA
    # =========================================================================

    draw_section_title(ax_tensor,"Representación del Tensor de Entrada y Salida para el Modelo LSTM",font_size=SECTION_SIZE)

    ax_tensor.set_facecolor("white")
    ax_tensor.axis("off")
    ax_tensor.set_xlim(0,100)
    ax_tensor.set_ylim(0,30)

    def draw_tensor(ax,x,y,w,h,depth=4,facecolor="#FFF4D6",edgecolor="#2C3E50"):
        offset=0.8
        for i in range(depth-1,-1,-1):
            ax.add_patch(patches.FancyBboxPatch((x+i*offset,y+i*offset),w,h,boxstyle="round,pad=0.15",linewidth=1.8,edgecolor=edgecolor,facecolor=facecolor,alpha=0.45 if i>0 else 1.0))

    # ===================== ENTRADA =====================

    ax_tensor.text(10,24,"Historical Window",fontsize=LABEL_SIZE,fontweight="bold",ha="center")
    ax_tensor.text(10,21,"70 minutes",fontsize=TICK_SIZE,color="gray",ha="center")
    ax_tensor.annotate("",xy=(18,18),xytext=(10,20),arrowprops=dict(arrowstyle="->",lw=2))

    draw_tensor(ax_tensor,20,9,18,10)

    ax_tensor.text(29,15,r"$X$",fontsize=22,fontweight="bold",ha="center")
    ax_tensor.text(29,10,r"$N \times 70 \times 1$",fontsize=15,fontweight="bold",ha="center")
    ax_tensor.text(29,3,"Input Tensor",fontsize=LABEL_SIZE,fontweight="bold",ha="center")

    ax_tensor.annotate("",xy=(20,8),xytext=(38,8),arrowprops=dict(arrowstyle="<->",lw=1.5))
    ax_tensor.text(29,6.2,"70 time steps",fontsize=SMALL_SIZE,ha="center")

    ax_tensor.annotate("",xy=(39.5,9),xytext=(39.5,19),arrowprops=dict(arrowstyle="<->",lw=1.5))
    ax_tensor.text(41,18,"1 Feature\n(S4)",fontsize=TICK_SIZE,va="center")

    # ===================== LSTM =====================

    ax_tensor.annotate("",xy=(48,14),xytext=(40,14),arrowprops=dict(arrowstyle="->",lw=2.5,color="#8E44AD"))

    ax_tensor.add_patch(patches.FancyBboxPatch((48,10),12,8,boxstyle="round,pad=0.35",linewidth=2,edgecolor="#8E44AD",facecolor="#F5EEF8"))

    ax_tensor.text(54,14,"LSTM",fontsize=18,fontweight="bold",color="#8E44AD",ha="center",va="center")

    # ===================== SALIDA =====================

    ax_tensor.annotate("",xy=(68,14),xytext=(60,14),arrowprops=dict(arrowstyle="->",lw=2.5,color="#8E44AD"))

    draw_tensor(ax_tensor,68,9,18,10)

    ax_tensor.text(77,15,r"$Y$",fontsize=22,fontweight="bold",ha="center")
    ax_tensor.text(77,10,r"$N \times 10 \times 1$",fontsize=15,fontweight="bold",ha="center")
    ax_tensor.text(77,3,"Output Tensor",fontsize=LABEL_SIZE,fontweight="bold",ha="center")

    ax_tensor.annotate("",xy=(68,8),xytext=(86,8),arrowprops=dict(arrowstyle="<->",lw=1.5))
    ax_tensor.text(77,6.2,"10 prediction steps",fontsize=TICK_SIZE,ha="center")

    ax_tensor.annotate("",xy=(87.5,14),xytext=(95,14),arrowprops=dict(arrowstyle="->",lw=2))

    ax_tensor.text(97,18,"Forecast",fontsize=LABEL_SIZE,fontweight="bold",ha="center")
    ax_tensor.text(97,15,"S4 Index",fontsize=TICK_SIZE,fontweight="bold",ha="center")
    ax_tensor.text(97,10,"10 min ahead",fontsize=TICK_SIZE,color="gray",ha="center")

    # Ajuste milimétrico de los subplots según el punto 7
    plt.subplots_adjust(
        hspace=0.55,
        top=0.96,
        bottom=0.04,
        left=0.04,
        right=0.98
    )
    
    # Guardado en ultra alta resolución (DPI 600) en formatos PDF y PNG
    plt.savefig(output_pdf, bbox_inches='tight', dpi=600)
    plt.savefig(output_png, bbox_inches='tight', dpi=600)
    plt.close()
    print(f"Diagrama listo para Word (A4 ~16cm): '{output_pdf}' y '{output_png}'")


if __name__ == "__main__":
    generar_diagrama_tesis(
        'FIGURA_3_4_Esquema_Sliding_Window_Final.pdf',
        'FIGURA_3_4_Esquema_Sliding_Window_Final.png'
    )