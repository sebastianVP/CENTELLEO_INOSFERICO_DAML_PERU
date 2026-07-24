import matplotlib
#matplotlib.use('Agg')  # Backend sin pantalla, 100% consistente
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.path import Path

# ════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN PARA MITAD DE PÁGINA A4 (Ajuste Real de Impresión)
# ════════════════════════════════════════════════════════════════════════
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['text.color'] = '#000000'

# CAMBIO CRÍTICO: Figsize optimizado para el ancho de caja de una tesis A4 (aprox 6.2 x 4.2 pulgadas)
fig = plt.figure(figsize=(6.2, 4.2), facecolor='#F8F9FA')
ax  = fig.add_axes([0, 0, 1, 1])
ax.set_facecolor('#F8F9FA')
ax.axis('off')

# Mantenemos las proporciones internas del plano cartesiano original
ax.set_xlim(0, 60)
ax.set_ylim(0, 33)

# ════════════════════════════════════════════════════════════════════════
# PALETA DE COLORES DE ALTO CONTRASTE
# ════════════════════════════════════════════════════════════════════════
PANEL_COLORS = ['#1A6FA3', '#D4720A', '#B52B27']
GRAY_DARK    = '#000000'  
GRAY_MED     = '#1C2833'  
WHITE        = '#FFFFFF'

# ════════════════════════════════════════════════════════════════════════
# CONSTANTES DE LAYOUT
# ════════════════════════════════════════════════════════════════════════
PANEL_W       = 17.5
PANEL_H       = 26.5      # Ajustado levemente para dar espacio al pie
PANEL_Y       = 3.8
PANEL_XS      = [1.0, 21.5, 42.0]
HEADER_H      = 2.8
CONTENT_Y_TOP = PANEL_Y + PANEL_H - HEADER_H
CONTENT_Y_BOT = PANEL_Y

DRAW_TOP = CONTENT_Y_TOP - 0.3
DRAW_BOT = PANEL_Y + 5.5
DRAW_H   = DRAW_TOP - DRAW_BOT

TITLES = [
    'a) Estado Inicial y Perturbación',
    'b) Campo de Polarización ($E_p$)',
    'c) Burbuja de Plasma y Centelleo',
]
SUBTITLES = [
    'Régimen post-puesta del sol',
    'Acumulación de cargas',
    'Fase no lineal',
]

# ════════════════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ════════════════════════════════════════════════════════════════════════
def fancy_rect(ax, x, y, w, h, color, radius=0.5, alpha=1.0, lw=1.2, ec=None, zorder=2):
    ec = ec or color
    ax.add_patch(patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=color, edgecolor=ec, linewidth=lw, alpha=alpha, zorder=zorder))

def arrow(ax, x1, y1, x2, y2, color='#C0392B', lw=1.5, zorder=6, ms=12):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
        arrowprops=dict(arrowstyle='->', color=color, lw=lw, mutation_scale=ms),
        zorder=zorder)

# ════════════════════════════════════════════════════════════════════════
# ESTRUCTURA COMÚN DE PANELES
# ════════════════════════════════════════════════════════════════════════
for i, (px, color) in enumerate(zip(PANEL_XS, PANEL_COLORS)):
    ax.add_patch(patches.FancyBboxPatch(
        (px+0.25, PANEL_Y-0.25), PANEL_W, PANEL_H,
        boxstyle="round,pad=0,rounding_size=0.6",
        facecolor='#BDC3C7', edgecolor='none', zorder=1, alpha=0.4))
    fancy_rect(ax, px, PANEL_Y, PANEL_W, PANEL_H,
               WHITE, radius=0.6, ec=color, lw=1.5, zorder=2)
    fancy_rect(ax, px, CONTENT_Y_TOP, PANEL_W, HEADER_H,
               color, radius=0.6, zorder=3)
    ax.add_patch(patches.Rectangle(
        (px, CONTENT_Y_TOP), PANEL_W, HEADER_H-0.5,
        facecolor=color, zorder=3))
    
    # CAMBIO: Tamaños de fuente balanceados para escala real A4 (Legible sin lupa)
    ax.text(px + PANEL_W/2, CONTENT_Y_TOP + HEADER_H*0.70,
            TITLES[i], color='white', ha='center', va='center',
            fontsize=6.5, fontweight='bold', zorder=8)
    ax.text(px + PANEL_W/2, CONTENT_Y_TOP + HEADER_H*0.30,
            SUBTITLES[i], color='white', ha='center', va='center',
            fontsize=5.2, alpha=0.95, zorder=8)

# ════════════════════════════════════════════════════════════════════════
# PANEL 0 — Estado Inicial y Perturbación
# ════════════════════════════════════════════════════════════════════════
px  = PANEL_XS[0]
col = PANEL_COLORS[0]
pw  = PANEL_W
mid_y = (DRAW_TOP + DRAW_BOT) / 2

ax.add_patch(patches.Rectangle(
    (px+0.2, mid_y), pw-0.4, DRAW_TOP - mid_y,
    facecolor='#D6EAF8', alpha=0.65, zorder=3))
ax.text(px + pw/2, mid_y + (DRAW_TOP - mid_y)/2 + 0.4,
        'Región F (Plasma Denso)',
        ha='center', va='center', color='#0A3256', fontsize=5.5, fontweight='bold', zorder=5,
        bbox=dict(facecolor='white', alpha=0.85, edgecolor='none', boxstyle='round,pad=0.15'))

ax.add_patch(patches.Rectangle(
    (px+0.2, DRAW_BOT), pw-0.4, mid_y - DRAW_BOT,
    facecolor='#EBF5FB', alpha=0.35, zorder=3))
ax.text(px + pw/2, DRAW_BOT + (mid_y - DRAW_BOT)/2 + 0.4,
        'Región E (Plasma Menos Denso)',
        ha='center', va='center', color='#2C3E50', fontsize=5.5, fontweight='bold', zorder=5,
        bbox=dict(facecolor='white', alpha=0.85, edgecolor='none', boxstyle='round,pad=0.15'))

t0   = np.linspace(px+0.2, px+pw-0.2, 300)
amp0 = DRAW_H * 0.06
y_w0 = mid_y + amp0 * np.sin(2*np.pi*(t0 - px - 0.2) / (pw - 0.4))
ax.plot(t0, y_w0, color=col, lw=1.2, ls='--', zorder=6, alpha=0.9)
ax.text(px + pw/2, mid_y - amp0 - 0.3,
        'Interfaz ondulada (perturbación)',
        ha='center', va='top', color='#0E3A5A', fontsize=5.0, style='italic', zorder=6)

gx     = px + pw - 1.5
gy_top = DRAW_TOP - 1.25
gy_bot = gy_top - 2.2
arrow(ax, gx, gy_top, gx, gy_bot, color='#B32B1A', lw=1.5, ms=10)
ax.text(gx, gy_top + 0.1, r'$\vec{g}$', ha='center', va='bottom', color='#B32B1A',
        fontsize=8.0, fontweight='bold', fontfamily='serif', style='italic', zorder=6)

bx, by = px + 1.5, DRAW_TOP - 1.5
ax.add_patch(patches.Circle((bx, by), 0.45, facecolor='white', edgecolor='#000000', lw=1.0, zorder=6))
ax.plot(bx, by, 'o', ms=2.5, color='#000000', zorder=7)
ax.text(bx, by - 0.6, r'$\vec{B}$', ha='center', va='top', color='#000000',
        fontsize=7.0, fontfamily='serif', style='italic', zorder=6)

arrow(ax, px+2.5, mid_y+0.3, px+2.5, mid_y+2.5, color='#000000', lw=1.0, ms=9)
ax.text(px+3.3, mid_y+1.7, r'$\nabla n_e$', ha='left', va='center', color='#000000',
        fontsize=7.0, fontfamily='serif', style='italic', zorder=6)

bullets0 = [
    '• Régimen nocturno, post-sunset',
    '• Región F densa sobre E ligera',
    '• Gradiente invertido: ∇nₑ↑',
    '• Perturbación en la interfaz',
]
for j, b in enumerate(bullets0):
    ax.text(px+0.5, PANEL_Y+5.1 - j*1.1, b, ha='left', va='top', color=GRAY_DARK, fontsize=5.4, zorder=5)

# ════════════════════════════════════════════════════════════════════════
# PANEL 1 — Campo de Polarización
# ════════════════════════════════════════════════════════════════════════
px  = PANEL_XS[1]
col = PANEL_COLORS[1]
pw  = PANEL_W
mid_y = (DRAW_TOP + DRAW_BOT) / 2

ax.add_patch(patches.Rectangle(
    (px+0.2, mid_y), pw-0.4, DRAW_TOP - mid_y, facecolor='#FEF5E7', alpha=0.5, zorder=3))
ax.add_patch(patches.Rectangle(
    (px+0.2, DRAW_BOT), pw-0.4, mid_y - DRAW_BOT, facecolor='#FDFEFE', alpha=0.3, zorder=3))

t1   = np.linspace(px+0.2, px+pw-0.2, 300)
amp1 = DRAW_H * 0.15
y_w1 = mid_y + amp1 * np.sin(2*np.pi*(t1 - px - 0.2) / (pw - 0.4))
ax.plot(t1, y_w1, color=col, lw=1.5, zorder=6)

cx_p, cy_p = px + pw*0.28, mid_y + amp1
cx_n, cy_n = px + pw*0.72, mid_y - amp1

ax.add_patch(patches.Circle((cx_p, cy_p), 0.65, facecolor='white', edgecolor='#E74C3C', lw=1.2, zorder=8))
ax.text(cx_p, cy_p, '+', ha='center', va='center', color='#E74C3C', fontsize=8.5, fontweight='bold', zorder=9)

ax.add_patch(patches.Circle((cx_n, cy_n), 0.65, facecolor='white', edgecolor='#2980B9', lw=1.2, zorder=8))
ax.text(cx_n, cy_n, '−', ha='center', va='center', color='#2980B9', fontsize=9.0, fontweight='bold', zorder=9)

arrow(ax, cx_p, cy_p - 0.75, cx_n, cy_n + 0.75, color='#000000', lw=1.2, ms=10)
ax.text((cx_p+cx_n)/2 + 0.5, (cy_p+cy_n)/2 + 0.5, r'$\vec{E}_p$', ha='left', va='center', color='#000000',
        fontsize=8.0, fontfamily='serif', style='italic', zorder=9)

for dx in [px+2.0, px+pw-2.0]:
    arrow(ax, dx, mid_y - amp1 - 0.9, dx, mid_y - amp1 + 0.5, color='#7E4105', lw=1.2, ms=9)
ax.text(px + pw/2, mid_y - amp1 - 0.8, r'Deriva $\vec{E}_p \times \vec{B}$',
        ha='center', va='top', color='#7E4105', fontsize=5.2, style='italic', zorder=6, fontweight='bold')

bullets1 = [
    '• Cargas acumuladas en la onda',
    '• Campo Ep normal a la interfaz',
    '• Ep × B acelera la inestabilidad',
    '• Crestas caen, valles ascienden',
]
for j, b in enumerate(bullets1):
    ax.text(px+0.5, PANEL_Y+5.1 - j*1.1, b, ha='left', va='top', color=GRAY_DARK, fontsize=5.4, zorder=5)

# ════════════════════════════════════════════════════════════════════════
# PANEL 2 — Burbuja de Plasma y Centelleo GNSS
# ════════════════════════════════════════════════════════════════════════
px  = PANEL_XS[2]
col = PANEL_COLORS[2]
pw  = PANEL_W

ax.add_patch(patches.Rectangle(
    (px+0.2, DRAW_BOT), pw-0.4, DRAW_TOP - DRAW_BOT, facecolor='#FDEDEC', alpha=0.25, zorder=3))

bub_cx  = px + pw/2
bub_bot = DRAW_BOT + 1.0
bub_top = DRAW_BOT + DRAW_H * 0.72
bub_w   = pw * 0.32

bubble_path_data = [
    (Path.MOVETO,    [bub_cx - bub_w,        bub_bot]),
    (Path.CURVE4,    [bub_cx - bub_w*1.6,    bub_bot + (bub_top-bub_bot)*0.35]),
    (Path.CURVE4,    [bub_cx - bub_w*1.0,    bub_top]),
    (Path.CURVE4,    [bub_cx,                bub_top + 0.35]),
    (Path.CURVE4,    [bub_cx + bub_w*1.0,    bub_top]),
    (Path.CURVE4,    [bub_cx + bub_w*1.6,    bub_bot + (bub_top-bub_bot)*0.35]),
    (Path.CURVE4,    [bub_cx + bub_w,        bub_bot]),
    (Path.CLOSEPOLY, [bub_cx - bub_w,        bub_bot]),
]
codes_b = [c for c, v in bubble_path_data]
verts_b = [v for c, v in bubble_path_data]
ax.add_patch(patches.PathPatch(Path(verts_b, codes_b), facecolor='#FDFEFE', edgecolor=col, linewidth=1.8, zorder=7, alpha=0.95))

ax.text(bub_cx, (bub_bot + bub_top) / 2 + 0.9, 'Burbuja\n(Depleción)',
        ha='center', va='center', color=col, fontsize=6.2, fontweight='bold', zorder=9)

t2     = np.linspace(px+0.2, px+pw-0.2, 300)
y_base = bub_bot + 0.5 * np.sin(np.pi*(t2 - px - 0.2) / (pw - 0.4))
ax.plot(t2, y_base, color=col, lw=1.5, zorder=6)

arrow(ax, bub_cx, bub_top + 0.3, bub_cx, bub_top + 1.8, color=col, lw=1.5, ms=10)
ax.text(bub_cx + 0.45, bub_top + 1.2, 'Asciende', ha='left', va='center', color=col, fontsize=5.4, fontweight='bold', zorder=7)

gnss_y = bub_bot + (bub_top - bub_bot) * 0.40
seg_x  = bub_w * 0.9

ax.plot([px+0.4,         bub_cx - seg_x], [gnss_y, gnss_y], 'r--', lw=1.0, zorder=8)
ax.plot([bub_cx + seg_x, px+pw-0.4],      [gnss_y, gnss_y], 'r--', lw=1.0, zorder=8)

zig_x = [bub_cx - seg_x, bub_cx - seg_x*0.35, bub_cx + seg_x*0.35, bub_cx + seg_x]
zig_y = [gnss_y,          gnss_y + 0.65,        gnss_y - 0.65,        gnss_y]
ax.plot(zig_x, zig_y, 'r-', lw=1.3, zorder=9)

ax.text(px+0.6, gnss_y + 0.45, 'Señal GNSS', ha='left', va='bottom', color='#B52B27', fontsize=5.2, fontweight='bold', zorder=8,
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=0.5))
ax.text(px+pw-0.6, gnss_y + 0.45, '⚡ Centelleo Severo', ha='right', va='bottom', color='#B52B27', fontsize=5.2, fontweight='bold', zorder=8,
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=0.5))

bullets2 = [
    '• Fase evolutiva no lineal',
    '• Valles de baja densidad suben a F',
    '• Fuertes gradientes locales',
    '• Centelleo de ondas de radio',
]
for j, b in enumerate(bullets2):
    ax.text(px+0.5, PANEL_Y+5.1 - j*1.1+0.2, b, ha='left', va='top', color=GRAY_DARK, fontsize=5.4, zorder=5)

# ════════════════════════════════════════════════════════════════════════
# FLECHAS DE PROGRESIÓN ENTRE PANELES
# ════════════════════════════════════════════════════════════════════════
for xa, xb in [(PANEL_XS[0]+PANEL_W, PANEL_XS[1]),
               (PANEL_XS[1]+PANEL_W, PANEL_XS[2])]:
    mid_y_arr = PANEL_Y + PANEL_H / 2
    ax.annotate('', xy=(xb, mid_y_arr), xytext=(xa, mid_y_arr),
        arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=2.0, mutation_scale=15), zorder=10)

# ════════════════════════════════════════════════════════════════════════
# PIE DE FIGURA MÁS COMPACTO
# ════════════════════════════════════════════════════════════════════════
#ax.text(30, 1.3,
#        'Adaptado del mecanismo de inestabilidad Rayleigh-Taylor ionosférica (RTI).\n'
#        'El gradiente invertido evoluciona exponencialmente generando burbujas de plasma macroscópicas.',
#        ha='center', va='center', color='#000000', fontsize=5.6, style='italic', fontweight='bold', zorder=5)

# ════════════════════════════════════════════════════════════════════════
# EXPORTACIÓN PERFECTA PARA WORD / LATEX (Sin bordes blancos sobrantes)
# ════════════════════════════════════════════════════════════════════════
plt.show()
fig.savefig('Figura_2_2_RTI_Mechanism.pdf', format='pdf', dpi=300,
            facecolor='#F8F9FA', edgecolor='none', bbox_inches='tight', pad_inches=0.02)

fig.savefig('Figura_2_2_RTI_Mechanism.png', format='png', dpi=300,
            facecolor='#F8F9FA', edgecolor='none', bbox_inches='tight', pad_inches=0.02)

print("¡Listo! Tu imagen tiene ahora el tamaño exacto y real para mitad de página A4 sin distorsión.")