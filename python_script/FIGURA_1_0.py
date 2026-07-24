import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Ellipse
from matplotlib.lines import Line2D
import matplotlib.patheffects as pe
import matplotlib.gridspec as gridspec
import os

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN GENERAL
# CAMBIO 1: fondo blanco en toda la figura (antes: '#0a0e1f', azul casi negro)
# CAMBIO 2: texto por defecto en negro (antes: blanco, ilegible sobre fondo claro)
# ══════════════════════════════════════════════════════════════════════════════
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.facecolor': 'white',
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
    'text.color': 'black',
})

# CAMBIO 3: figura de mayor tamaño para que el texto no se vea diminuto
# al insertarla en el documento de tesis (antes: 14.0 x 10.5)
FIG_W, FIG_H = 16.0, 12.0

fig = plt.figure(figsize=(FIG_W, FIG_H))

gs = gridspec.GridSpec(2, 3,
                       height_ratios=[5.5, 1.0],
                       hspace=0.10, wspace=0.22,
                       left=0.02, right=0.98,
                       top=0.97, bottom=0.10)

ax  = fig.add_subplot(gs[0, :])   # panel espacial — ancho completo
ax1 = fig.add_subplot(gs[1, 0])
ax2 = fig.add_subplot(gs[1, 1])
ax3 = fig.add_subplot(gs[1, 2])

for a in [ax, ax1, ax2, ax3]:
    a.set_facecolor('white')

# ══════════════════════════════════════════════════════════════════════════════
# PALETA DE COLORES
# CAMBIO: tonos más saturados/oscuros para mantener buen contraste sobre blanco
# (los tonos pastel originales fueron pensados para fondo oscuro)
# ══════════════════════════════════════════════════════════════════════════════
C_EARTH     = '#1a6fbf'
C_IONOS     = '#4da6ff'
C_FREGION   = '#0088bb'
C_BUBBLE    = '#e05a20'
C_REFRACTED = '#cc0000'
C_CLEAN2    = '#2266aa'
C_CLEAN3    = '#2e8b57'
C_EQUATOR   = '#666666'
C_NOTE      = '#b35900'
C_REF_LINE  = '#999999'
C_BORDER    = '#1a6fbf'

# ── Fuentes ──────────────────────────────────────────────────────────────────
# CAMBIO: todos los tamaños de fuente incrementados respecto a la versión
# original para asegurar legibilidad al insertar la figura en el documento
FS_TITLE   = 16.0
FS_LABEL   = 14.0
FS_SMALL   = 13.0
FS_TINY    = 11.5
FS_PANEL   = 13.0
FS_LEGEND  = 12.5

# ══════════════════════════════════════════════════════════════════════════════
# POSICIONES
# ══════════════════════════════════════════════════════════════════════════════
sats = {
    'SAT-1': {'x': -4.2, 'y': 4.4,  'color': '#cc7a00', 'label': 'PRN-01\n(EPB)'},
    'SAT-2': {'x':  0.2, 'y': 4.6,  'color': C_CLEAN2,  'label': 'PRN-14'},
    'SAT-3': {'x':  4.4, 'y': 3.2,  'color': C_CLEAN3,  'label': 'PRN-22'},
}
rx_x, rx_y  =  0.20, -1.10
bub_cx, bub_cy = -1.55,  1.05
bub_a,  bub_b  =  0.52,  0.68

def ellipse_intersect(sat, rx, cx, cy, a, b):
    dx, dy = rx[0]-sat[0], rx[1]-sat[1]
    ox, oy = sat[0]-cx,    sat[1]-cy
    A = (dx/a)**2 + (dy/b)**2
    B = 2*((ox*dx)/a**2 + (oy*dy)/b**2)
    C = (ox/a)**2 + (oy/b)**2 - 1
    disc = B**2 - 4*A*C
    if disc < 0: return None, None
    sq = np.sqrt(disc)
    return (-B-sq)/(2*A), (-B+sq)/(2*A)

def lerp(p1, p2, t):
    return (p1[0]+t*(p2[0]-p1[0]), p1[1]+t*(p2[1]-p1[1]))

s1 = sats['SAT-1']
t_in, t_out = ellipse_intersect(
    (s1['x'], s1['y']), (rx_x, rx_y),
    bub_cx, bub_cy, bub_a, bub_b)
pt_in  = lerp((s1['x'], s1['y']), (rx_x, rx_y), t_in)
pt_out = lerp((s1['x'], s1['y']), (rx_x, rx_y), t_out)

# ══════════════════════════════════════════════════════════════════════════════
# PANEL ESPACIAL
# ══════════════════════════════════════════════════════════════════════════════
# NOTA: se elimina el campo de estrellas (puntos blancos) porque dejan de ser
# visibles sobre fondo blanco y no aportan información científica a la figura.

# Tierra
ax.add_patch(Circle((0,0), 1.0, color=C_EARTH, zorder=5, linewidth=2, ec='#0d3f73'))
for r,a in zip(np.linspace(1.0,1.18,10), np.linspace(0.18,0.0,10)):
    ax.add_patch(Circle((0,0), r, color=C_IONOS, alpha=a, zorder=4, linewidth=0))
ax.text(-0.3, 0.2, 'Tierra', ha='center', va='center',
        fontsize=FS_LABEL, fontweight='bold', color='white', zorder=6)

# Región F
theta = np.linspace(0, 2*np.pi, 360)
for r,a in zip([1.25,1.40,1.55,1.70,1.75],[0.13,0.10,0.07,0.04,0.0]):
    ax.fill(r*np.cos(theta), r*np.sin(theta), color=C_FREGION, alpha=a, zorder=2)
ax.add_patch(Circle((0,0),1.75,fill=False,ec=C_FREGION,linestyle='--',linewidth=1.5,zorder=3))
ax.add_patch(Circle((0,0),1.25,fill=False,ec=C_FREGION,linestyle=':',linewidth=1.2,zorder=3))
ax.text(-1.0, 3.30, 'Región F\n(300-600 km)',
        fontsize=FS_SMALL, color=C_FREGION, ha='center', va='center', zorder=10,
        bbox=dict(boxstyle='round,pad=0.32', fc='white', ec=C_FREGION, alpha=0.95))
ax.annotate('', xy=(1.75*np.cos(np.radians(100)), 1.75*np.sin(np.radians(100))),
            xytext=(-0.75, 3.05),
            arrowprops=dict(arrowstyle='->', color=C_FREGION, lw=1.0), zorder=9)

# Ecuador magnético
ax.plot([-5.2, 5.2], [0,0], linestyle='--', color=C_EQUATOR,
        linewidth=1.2, dashes=(6,4), zorder=4, alpha=0.85)
ax.text(-5.15, 0.12, 'Ecuador\nmagnético',
        fontsize=FS_SMALL, color=C_EQUATOR, va='bottom', ha='left', alpha=0.95)

# Burbuja de plasma
ax.add_patch(Ellipse((bub_cx,bub_cy), 2*bub_a, 2*bub_b,
                     color=C_BUBBLE, alpha=0.18, zorder=6))
ax.add_patch(Ellipse((bub_cx,bub_cy), 2*bub_a, 2*bub_b,
                     fill=False, ec=C_BUBBLE, linewidth=2.6, linestyle='--', zorder=7))
for s,a in zip([0.85,0.65,0.44,0.24],[0.05,0.07,0.11,0.15]):
    ax.add_patch(Ellipse((bub_cx,bub_cy), 2*bub_a*s, 2*bub_b*s,
                         color=C_BUBBLE, alpha=a, zorder=7))
ax.text(bub_cx-1.9, bub_cy + bub_b - 1.10,
        'Burbuja de plasma (EPB)\nDepleción de densidad electrónica',
        fontsize=FS_SMALL, color=C_BUBBLE, ha='center', va='bottom',
        fontweight='bold', zorder=11,
        bbox=dict(boxstyle='round,pad=0.32', fc='white',
                  ec=C_BUBBLE, alpha=0.97, linewidth=1.2))

# Satélites
def draw_satellite(ax, x, y, label, color):
    ax.scatter(x, y, s=260, color=color, zorder=12,
               marker='*', edgecolors='black', linewidths=0.5)
    for dy in [-0.22, 0.22]:
        ax.plot([x-0.46, x+0.46], [y+dy]*2,
                color=color, linewidth=3.8, solid_capstyle='round', zorder=11)
        ax.plot([x-0.46, x+0.46], [y+dy]*2,
                color='white', linewidth=1.6, solid_capstyle='round', zorder=12)
    ax.text(x, y+0.56, label, fontsize=FS_SMALL, color=color,
            ha='center', fontweight='bold', zorder=12,
            bbox=dict(boxstyle='round,pad=0.28', fc='white', ec=color, alpha=0.95))

for k,s in sats.items():
    draw_satellite(ax, s['x'], s['y'], s['label'], s['color'])

# Receptor
ax.scatter(rx_x, rx_y, s=180, color='black', zorder=13,
           marker='^', edgecolors=C_EARTH, linewidths=1.5)
ax.plot([rx_x, rx_x], [rx_y-0.02, rx_y-0.25],
        color='black', linewidth=2.8, zorder=13)
ax.plot([rx_x-0.22, rx_x+0.22], [rx_y-0.25]*2,
        color='black', linewidth=2.8, zorder=13)
ax.text(rx_x+0.46, rx_y+0.01,
        'Receptor GNSS\n(punto único)',
        fontsize=FS_SMALL, color='black', va='center', ha='left',
        bbox=dict(boxstyle='round,pad=0.28', fc='white', ec='black', alpha=0.95))

# ══════════════════════════════════════════════════════════════════════════════
# TRAYECTORIAS
# ══════════════════════════════════════════════════════════════════════════════
for key in ['SAT-2', 'SAT-3']:
    s = sats[key]
    ax.plot([s['x'], rx_x], [s['y'], rx_y],
            color=s['color'], linewidth=2.2, zorder=8)
    fx = s['x'] + 0.60*(rx_x - s['x'])
    fy = s['y'] + 0.60*(rx_y - s['y'])
    ax.annotate('', xy=(fx, fy),
                xytext=(fx - 0.01*(rx_x-s['x']), fy - 0.01*(rx_y-s['y'])),
                arrowprops=dict(arrowstyle='->', color=s['color'], lw=2.0), zorder=9)

# PRN-01 tramo compartido
ax.plot([s1['x'], pt_in[0]], [s1['y'], pt_in[1]],
        color='black', linewidth=2.6, zorder=9, solid_capstyle='round')
mid_wx = (s1['x'] + pt_in[0]) / 2
mid_wy = (s1['y'] + pt_in[1]) / 2
ax.text(mid_wx + 0.45, mid_wy + 0.32, 'Tramo compartido',
        fontsize=FS_TINY, color='black', ha='center', style='italic',
        bbox=dict(boxstyle='round,pad=0.20', fc='white',
                  ec='black', alpha=0.85, linewidth=0.7))

# PRN-01 dentro de la EPB — curva de trayectoria refractada
t_b  = np.linspace(0, 1, 120)
bxi  = pt_in[0]*(1-t_b) + pt_out[0]*t_b
byi  = pt_in[1]*(1-t_b) + pt_out[1]*t_b
dx_r = pt_out[0]-pt_in[0]; dy_r = pt_out[1]-pt_in[1]
ln   = np.sqrt(dx_r**2 + dy_r**2)
px, py = dy_r/ln, -dx_r/ln
bx_p = bxi + 0.40*np.sin(np.pi*t_b)*px
by_p = byi + 0.40*np.sin(np.pi*t_b)*py
ax.plot(bx_p, by_p, color=C_REFRACTED, linewidth=3.0, zorder=10)

exit_px, exit_py = bx_p[-1], by_p[-1]
ax.plot([exit_px, rx_x], [exit_py, rx_y],
        color=C_REFRACTED, linewidth=3.0, zorder=10)
ax.annotate('', xy=(rx_x, rx_y),
            xytext=(exit_px + 0.68*(rx_x-exit_px),
                    exit_py + 0.68*(rx_y-exit_py)),
            arrowprops=dict(arrowstyle='->', color=C_REFRACTED, lw=2.3), zorder=11)

# Nota de refracción
ax.text(pt_in[0] - 1.5, pt_in[1] + 0.85, 'Refracción\n(variación del índice de refracción)',
        fontsize=FS_TINY, color=C_NOTE, ha='center',
        bbox=dict(boxstyle='round,pad=0.22', fc='white', ec=C_NOTE, alpha=0.92))
ax.annotate('', xy=(pt_in[0]-0.02, pt_in[1]+0.02),
            xytext=(pt_in[0]-1.1, pt_in[1]+0.80),
            arrowprops=dict(arrowstyle='->', color=C_NOTE, lw=1.1), zorder=11)

# Nota sobre el receptor
ax.text(rx_x+0.6, rx_y - 0.55,
        'Misma posición geográfica.\n'
        'Amplitud (S4) y fase (\u03c3\u03c6) alteradas',
        fontsize=FS_SMALL, color=C_NOTE, ha='center', va='top',
        bbox=dict(boxstyle='round,pad=0.28', fc='white',
                  ec=C_NOTE, alpha=0.97, linewidth=1.2))

# Etiqueta PRN-01
ax.text(-5.10, 1.80, 'PRN-01\nSeñal afectada por la EPB',
        fontsize=FS_LABEL, color=C_REFRACTED, ha='left', va='center',
        fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.32', fc='white',
                  ec=C_REFRACTED, alpha=0.95, linewidth=1.1))
ax.annotate('', xy=(-1.90, 1.20), xytext=(-4.55, 1.56),
            arrowprops=dict(arrowstyle='->', color=C_REFRACTED, lw=1.1,
                            connectionstyle='arc3,rad=0.15'), zorder=9)

# Etiqueta señales no perturbadas
ax.text(2.10, 3.30, 'PRN-14 / PRN-22\nSeñales no perturbadas',
        fontsize=FS_LABEL, color=C_CLEAN2, ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.32', fc='white',
                  ec=C_CLEAN2, alpha=0.95, linewidth=1.1))
ax.annotate('', xy=(0.20, 2.40), xytext=(2.1, 2.90),
            arrowprops=dict(arrowstyle='->', color=C_CLEAN2, lw=1.1,
                            connectionstyle='arc3,rad=-0.15'), zorder=9)

ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-2.2, 5.8)
ax.set_aspect('equal')
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_edgecolor(C_BORDER); sp.set_linewidth(1.0)

# ══════════════════════════════════════════════════════════════════════════════
# LEYENDA
# ══════════════════════════════════════════════════════════════════════════════
legend_elements = [
    Line2D([0],[0], color='black',       lw=2.2,
           label='Tramo no afectado por la EPB (señal no perturbada)'),
    Line2D([0],[0], color=C_REFRACTED,   lw=2.2,
           label='PRN-01 — señal afectada (S4 elevado, \u03c3\u03c6 elevado)'),
    Line2D([0],[0], color=C_CLEAN2,      lw=1.8,
           label='PRN-14 — señal no perturbada'),
    Line2D([0],[0], color=C_CLEAN3,      lw=1.8,
           label='PRN-22 — señal no perturbada'),
    mpatches.Patch(fc=C_BUBBLE,  alpha=0.45, ec=C_BUBBLE,  lw=1.3, ls='--',
                   label='Burbuja de plasma (EPB)'),
    mpatches.Patch(fc=C_FREGION, alpha=0.22, ec=C_FREGION, lw=1.1, ls='--',
                   label='Región F ionosférica'),
]
leg = ax.legend(handles=legend_elements,
                loc='lower left', bbox_to_anchor=(0.0, 0.0),
                fontsize=FS_LEGEND, framealpha=0.97,
                facecolor='white', edgecolor=C_BORDER,
                labelcolor='black', handlelength=2.2,
                borderpad=0.7, labelspacing=0.55,
                title='Leyenda', title_fontsize=FS_LEGEND+1.0)
leg.get_title().set_color(C_BORDER)
leg.get_title().set_fontweight('bold')

# ══════════════════════════════════════════════════════════════════════════════
# PANELES DE SEÑAL
# ══════════════════════════════════════════════════════════════════════════════
t_sig = np.linspace(0, 4*np.pi, 500)

def signal_panel(ax_s, t, signal, color, title, subtitle,
                 show_ref=True, ref_color=C_REF_LINE):
    ax_s.set_facecolor('white')
    if show_ref:
        ax_s.plot(t, np.sin(t), color=ref_color, linewidth=1.4,
                  linestyle='--', alpha=0.70)
    ax_s.plot(t, signal, color=color, linewidth=2.2)
    ax_s.axhline(0, color='#bbbbbb', linewidth=0.8, zorder=0)
    ax_s.set_xlim(t[0], t[-1]); ax_s.set_ylim(-2.3, 2.3)
    ax_s.set_xticks([]); ax_s.set_yticks([])
    for sp in ax_s.spines.values():
        sp.set_edgecolor(color); sp.set_linewidth(1.4)
    ax_s.set_title(title, fontsize=FS_PANEL, color=color, fontweight='bold', pad=6)
    ax_s.text(0.97, 0.95, subtitle,
              transform=ax_s.transAxes, fontsize=FS_TINY-1.0,
              color=color, ha='right', va='top',
              bbox=dict(boxstyle='round,pad=0.20', fc='white', ec=color, alpha=0.92))

env = 1.0 + 0.75*np.sin(0.55*t_sig+0.5) \
          - 0.50*np.cos(1.10*t_sig+1.2) \
          + 0.25*np.sin(2.20*t_sig)
env = np.clip(env, 0.05, 2.0)
phase_noise = (0.60*np.sin(0.80*t_sig+0.3)
             + 0.35*np.sin(1.90*t_sig+2.1)
             + 0.20*np.sin(3.50*t_sig))
sig_epb = env * np.sin(t_sig + phase_noise)

signal_panel(ax1, t_sig, sig_epb,
             color=C_REFRACTED,
             title='PRN-01 — Afectado por la EPB',
             subtitle='S4 elevado / \u03c3\u03c6 elevado\nAmplitud y fase perturbadas')
ax1.annotate('Amplitud\nfluctuante',
             xy=(t_sig[100], sig_epb[100]),
             xytext=(t_sig[100]+1.5, 1.55),
             fontsize=FS_TINY-1.0, color=C_NOTE,
             arrowprops=dict(arrowstyle='->', color=C_NOTE, lw=0.9))
ax1.annotate('Desfase\nde fase',
             xy=(t_sig[320], sig_epb[320]),
             xytext=(t_sig[320]+0.6, -2.05),
             fontsize=FS_TINY-1.0, color=C_NOTE,
             arrowprops=dict(arrowstyle='->', color=C_NOTE, lw=0.9))

signal_panel(ax2, t_sig, np.sin(t_sig),
             color=C_CLEAN2,
             title='PRN-14 — Sin perturbación',
             subtitle='S4 \u2248 0 / \u03c3\u03c6 \u2248 0\nAmplitud y fase estables',
             show_ref=False)
ax2.text(0.50, 0.06, 'Amplitud constante, fase coherente',
         transform=ax2.transAxes, fontsize=FS_TINY-1.0, color=C_CLEAN2,
         ha='center', va='bottom',
         bbox=dict(boxstyle='round,pad=0.20', fc='white', ec=C_CLEAN2, alpha=0.85))

signal_panel(ax3, t_sig, np.sin(t_sig+0.35),
             color=C_CLEAN3,
             title='PRN-22 — Sin perturbación',
             subtitle='S4 \u2248 0 / \u03c3\u03c6 \u2248 0\nAmplitud y fase estables',
             show_ref=False)
ax3.text(0.50, 0.06, 'Amplitud constante, fase coherente',
         transform=ax3.transAxes, fontsize=FS_TINY-1.0, color=C_CLEAN3,
         ha='center', va='bottom',
         bbox=dict(boxstyle='round,pad=0.20', fc='white', ec=C_CLEAN3, alpha=0.85))

# ══════════════════════════════════════════════════════════════════════════════
# TÍTULO / DESCRIPCIÓN, AHORA COMO PIE DE FIGURA
# CAMBIO: se retira el título superior con recuadro de color y se reemplaza
# por un texto formal en la parte inferior de la imagen, sin recuadro
# decorativo, a modo de leyenda descriptiva de la figura.
# ══════════════════════════════════════════════════════════════════════════════
fig.text(0.50, 0.020,
         'Cintilación ionosférica GNSS producida por una burbuja de plasma ecuatorial (EPB). '
         'La señal de los tres satélites llega al mismo receptor; únicamente la señal PRN-01, '
         'al atravesar la EPB, presenta alteraciones en la amplitud (S4) y en la fase (\u03c3\u03c6).',
         ha='center', va='bottom', fontsize=FS_TITLE-2.0,
         color='black', wrap=True)

# ══════════════════════════════════════════════════════════════════════════════
# GUARDADO
# ══════════════════════════════════════════════════════════════════════════════
output_dir = r"outputs"
os.makedirs(output_dir, exist_ok=True)

for fname, kw in [
    ("plasma_bubble_final.png", dict(dpi=300)),
    ("plasma_bubble_final.pdf", dict(dpi=600)),
    ("plasma_bubble_final.svg", dict()),
]:
    plt.savefig(os.path.join(output_dir, fname),
                bbox_inches='tight', facecolor='white', **kw)

print("Guardado en:", output_dir)