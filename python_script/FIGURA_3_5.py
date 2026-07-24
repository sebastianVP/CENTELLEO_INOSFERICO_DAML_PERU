import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'


def generar_diagrama(output_pdf: str, output_png: str) -> None:

    # ➔ CAMBIO 1: Reducción del figsize y los ratios para compensar el recorte del panel central
    fig, (ax_ts, ax_concept, ax_tensor) = plt.subplots(
        3, 1, figsize=(20, 11.5),
        gridspec_kw={'height_ratios': [1.2, 2.6, 1.8]}
    )
    fig.patch.set_facecolor('#ffffff')

    # ── Título de sección ─────────────────────────────────────────────────────
    def draw_section_title(ax, text, font_size=13):
        ax.text(
            0.5, 1.08, text,
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

    ax_ts.plot(s4_series, color='#5D6D7E', lw=1.5, alpha=0.9)
    ax_ts.set_ylabel("S4", fontsize=13, fontweight='bold')
    ax_ts.set_ylim(-0.05, 1.65)
    ax_ts.set_yticks([0.0, 0.3, 0.6, 0.9, 1.2, 1.5])
    ax_ts.tick_params(axis='y', labelsize=11)

    tick_indices = np.linspace(0, len(s4_series)-1, 11, dtype=int)
    tick_labels  = [
        r"$t{-}90$", r"$t{-}89$", r"$t{-}88$", r"$t{-}87$",
        r"$t{-}3$",  r"$t$",      r"$t{+}1$",  r"$t{+}4$",
        r"$t{+}6$",  r"$t{+}7$",  r"$t{+}10$"
    ]
    ax_ts.set_xticks(tick_indices)
    ax_ts.set_xticklabels(tick_labels, fontsize=12)
    ax_ts.grid(True, linestyle='--', alpha=0.3)
    ax_ts.spines['top'].set_visible(False)
    ax_ts.spines['right'].set_visible(False)

    # =========================================================================
    # SECCIÓN 2: TÉCNICA DE VENTANA DESLIZANTE
    # =========================================================================
    draw_section_title(ax_concept, "Técnica de Ventana Deslizante (Stride = 1 min)")
    ax_concept.set_facecolor('#fefefe')
    ax_concept.axis('off')

    # ➔ CAMBIO 2: Límite inferior subido (de -10 a -4) para cortar el espacio vacío de abajo
    ax_concept.set_xlim(0, 100)
    ax_concept.set_ylim(-6, 16)

    BH      = 1.8   
    LB      = 46    
    HOR     = 7     
    SV      = 3.2   
    SH      = 0.7   
    START_X = 1.0
    START_Y = 10.0

    def draw_window_set(ax, x0, y0, label, show_labels=True):
        ax.add_patch(patches.FancyBboxPatch(
            (x0, y0), LB, BH,
            boxstyle="round,pad=0.12",
            facecolor='#D6EAF8', edgecolor='#1A5276', linewidth=2.0, zorder=2
        ))
        ax.text(x0+LB/2, y0+BH/2, label,
                ha='center', va='center',
                fontsize=13, fontweight='bold', color='#1A2530', zorder=3)

        if show_labels:
            ax.annotate('', xy=(x0, y0+BH+0.4), xytext=(x0+LB, y0+BH+0.4),
                        arrowprops=dict(arrowstyle='<->', color='#1A5276', lw=1.6))
            ax.text(x0+LB/2, y0+BH+0.85,
                    r"Lookback ($\tau = 70$ min)",
                    ha='center', va='bottom', fontsize=11,
                    color='#1A5276', fontweight='bold')

        x1 = x0 + LB
        ax.add_patch(patches.FancyBboxPatch(
            (x1, y0), HOR, BH,
            boxstyle="round,pad=0.12",
            facecolor='#AED6F1', edgecolor='#154360', linewidth=2.0, zorder=2
        ))
        if show_labels:
            ax.annotate('', xy=(x1, y0+BH+0.4), xytext=(x1+HOR, y0+BH+0.4),
                        arrowprops=dict(arrowstyle='<->', color='#154360', lw=1.6))
            ax.text(x1+HOR/2, y0+BH+0.85,
                    r"Horizonte ($h=10$ min)",
                    ha='center', va='bottom', fontsize=11,
                    color='#154360', fontweight='bold')

    draw_window_set(ax_concept, START_X,        START_Y,        "Window 1", show_labels=True)
    draw_window_set(ax_concept, START_X+SH,     START_Y-SV,     "Window 2", show_labels=False)
    draw_window_set(ax_concept, START_X+2*SH,   START_Y-2*SV,   "Window 3…", show_labels=False)

    ax_concept.text(
        START_X+2*SH+LB+HOR+0.8, START_Y-2*SV+BH/2,
        '···', ha='left', va='center', fontsize=20, color='#7F8C8D'
    )

    # ── Insets (mini-gráficas) ────────────────────────────────────────────────
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

        ax_ins.plot(combined, color='#5D6D7E', lw=1.3)
        ax_ins.axvspan(n_lb - 0.5, n_total - 0.5, alpha=0.18, color='#2E86C1')
        ax_ins.axvline(n_lb - 0.5, color='#154360', lw=1.0, linestyle='--', alpha=0.7)

        PAD_Y = 0.08
        ax_ins.set_ylim(S4_MIN - PAD_Y, S4_MAX + PAD_Y)
        ax_ins.set_yticks([0.0, 0.5, 1.0, 1.5])
        ax_ins.set_yticklabels(["0.0", "0.5", "1.0", "1.5"], fontsize=8.5)
        ax_ins.set_ylabel("S4", fontsize=10, fontweight='bold', labelpad=4)

        PAD_X = 2
        ax_ins.set_xlim(-PAD_X, n_total - 1 + PAD_X)
        ax_ins.set_xticks([0, n_lb - 1, n_total - 1])
        ax_ins.set_xticklabels(xtick_labels, fontsize=9.5)
        ax_ins.tick_params(axis='both', which='both', length=3, labelsize=9)

        ax_ins.grid(True, linestyle=':', alpha=0.4)

        for sp in ax_ins.spines.values():
            sp.set_linestyle(':')
            sp.set_linewidth(1.0)
            sp.set_edgecolor('#2c3e50')

        ax_ins.text(
            n_total - 1 - PAD_X * 0.3,
            S4_MAX * 0.88,
            'Target',
            ha='right', fontsize=9, fontweight='bold', color='#154360',
            bbox=dict(facecolor='#EBF5FB', edgecolor='none', alpha=0.85, pad=2)
        )

    s4_w1 = make_s4_signal(80, seed=7)   
    s4_w2 = make_s4_signal(80, seed=21)  

    lb1, h1 = s4_w1.iloc[:70], s4_w1.iloc[70:]
    lb2, h2 = s4_w2.iloc[:70], s4_w2.iloc[70:]

    # ➔ CAMBIO 3: Insets colocados más arriba (de -9.5 a -3.5) para pegarlos a Window 3
    INSET_Y0    = -3.5    
    INSET_H     = 5.8     
    INSET_W     = LB + HOR - 1   
    GAP_INSETS  = 2.5     

    make_inset(ax_concept,
               (START_X, INSET_Y0, INSET_W, INSET_H),
               lb1, h1,
               [r"$t{-}70$", r"$t{-}1$", r"$t{+}9$"])

    make_inset(ax_concept,
               (START_X + INSET_W + GAP_INSETS, INSET_Y0, INSET_W, INSET_H),
               lb2, h2,
               [r"$t{-}69$", r"$t$", r"$t{+}10$"])

    # ── Control de Continuidad ────────────────────────────────────────────────
    CX = 59
    CY = START_Y - SV

    ax_concept.text(
        CX+14, CY+BH+2.5,
        "Control de Continuidad:\nDatos faltantes > 5 min → descarte",
        ha='center', va='bottom', fontsize=11, fontweight='bold', color='#922B21',
        bbox=dict(facecolor='#FDEDEC', edgecolor='#922B21',
                  boxstyle='round,pad=0.5', linewidth=1.5)
    )
    ax_concept.add_patch(patches.FancyBboxPatch(
        (CX, CY), 12, BH, boxstyle="round,pad=0.12",
        facecolor='#D6EAF8', edgecolor='#1A5276', linewidth=1.8, zorder=2
    ))
    ax_concept.text(CX+6, CY+BH/2, "Seg A",
                    ha='center', va='center',
                    fontsize=12, fontweight='bold', color='#1A2530', zorder=3)
    ax_concept.text(CX+13.2, CY+BH/2, "✕",
                    ha='center', va='center',
                    fontsize=32, color='#C0392B', fontweight='bold', zorder=5)
    ax_concept.add_patch(patches.FancyBboxPatch(
        (CX+15, CY), 12, BH, boxstyle="round,pad=0.12",
        facecolor='#D6EAF8', edgecolor='#1A5276', linewidth=1.8, zorder=2
    ))
    ax_concept.text(CX+21, CY+BH/2, "Seg B",
                    ha='center', va='center',
                    fontsize=12, fontweight='bold', color='#1A2530', zorder=3)
    ax_concept.text(CX+13.5, CY-1.0, "Secuencia Descartada",
                    ha='center', va='top',
                    fontsize=10, fontweight='bold', color='#922B21')

    # =========================================================================
    # SECCIÓN 3: TENSOR TRIDIMENSIONAL
    # =========================================================================
    draw_section_title(ax_tensor, "Estructura del Tensor Tridimensional de Salida")
    ax_tensor.set_facecolor('#ffffff')
    ax_tensor.axis('off')
    ax_tensor.set_xlim(-22, 132)
    ax_tensor.set_ylim(0, 12)

    def draw_3d_tensor(ax, x0, y0, w, h, n=3, color='#FEF7DA'):
        d = 0.4
        for i in range(n-1, -1, -1):
            alpha = 1.0 if i == 0 else 0.45
            ax.add_patch(patches.FancyBboxPatch(
                (x0+i*d, y0+i*d), w, h,
                boxstyle="round,pad=0.15",
                facecolor=color, edgecolor='#2c3e50',
                linewidth=1.6, alpha=alpha, zorder=2+n-i
            ))

    ax_tensor.text(
        -8, 6,
        "Lookback (70 min)\n\"Pre-acondicionamiento\"\nhistórico Rayleigh-Taylor",
        ha='center', va='center', fontsize=16, fontweight='bold',
        linespacing=1.8,
        bbox=dict(facecolor='#EBF5FB', edgecolor='#2c3e50',
                  boxstyle='round,pad=1.8', linewidth=2.5)
    )
    ax_tensor.annotate('', xy=(15, 6), xytext=(8, 6),
                        arrowprops=dict(arrowstyle='->', lw=2.2, color='#2c3e50'))

    draw_3d_tensor(ax_tensor, 16, 2.5, 38, 7, color='#FEF7DA')
    ax_tensor.text(33, 6, r"$X \in \mathbb{R}^{N \times 70 \times 1}$",
                   ha='center', va='center', fontsize=16, fontweight='bold')
    ax_tensor.text(13, 9, "Batch\n(N)",
                   ha='right', va='center', fontsize=11, fontweight='bold', rotation=90)
    ax_tensor.text(30, 2.0, "Lookback (70 min)",
                   ha='center', va='top', fontsize=11, fontweight='bold')
    ax_tensor.annotate('', xy=(53.5, 3.0), xytext=(53.5, 6.5),
                        arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=1.5))
    ax_tensor.text(54, 2.8, "Feature\n(1, S4)",
                   ha='left', va='top', fontsize=10, fontweight='bold')

    ax_tensor.annotate('', xy=(68, 6), xytext=(57, 6),
                        arrowprops=dict(arrowstyle='->', lw=3.0, color='#8E44AD'))
    ax_tensor.text(62.5, 7.5, "Modelo\nLSTM",
                   ha='center', va='center',
                   fontweight='bold', color='#8E44AD', fontsize=12)

    draw_3d_tensor(ax_tensor, 69, 2.5, 18, 7, color='#FEF7DA')
    ax_tensor.text(78, 6, r"$Y \in \mathbb{R}^{N \times 10 \times 1}$",
                   ha='center', va='center', fontsize=15, fontweight='bold')
    ax_tensor.annotate('', xy=(69, 2.0), xytext=(88, 2.0),
                        arrowprops=dict(arrowstyle='<->', color='#2c3e50', lw=1.5))
    ax_tensor.text(78.5, 1.5, "Horizonte (10 min)",
                   ha='center', va='top', fontsize=11, fontweight='bold')

    ax_tensor.annotate('', xy=(97, 6), xytext=(90, 6),
                        arrowprops=dict(arrowstyle='->', lw=2.2, color='#2c3e50'))
    ax_tensor.text(
        112, 6,
        "Horizonte (10 min)\nLímite predictivo\noperativo (caos no lineal)",
        ha='center', va='center', fontsize=16, fontweight='bold',
        linespacing=1.8,
        bbox=dict(facecolor='#EBF5FB', edgecolor='#2c3e50',
                  boxstyle='round,pad=1.8', linewidth=2.5)
    )

# ➔ CAMBIO: Se aumentó hspace de 0.08 a 0.35 para separar los gráficos y dar espacio a los títulos
    plt.subplots_adjust(hspace=0.35, top=0.95, bottom=0.05, left=0.05, right=0.98)
    plt.savefig(output_pdf, bbox_inches='tight', dpi=300)
    plt.savefig(output_png, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Guardado: '{output_pdf}' y '{output_png}'")


if __name__ == "__main__":
    generar_diagrama(
        'FIGURA_3_4_Esquema_Sliding_Window_Final.pdf',
        'FIGURA_3_4_Esquema_Sliding_Window_Final.png'
    )