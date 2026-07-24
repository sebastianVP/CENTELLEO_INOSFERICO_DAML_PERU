import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generar_tacometro_s4(valor_s4_ejemplo=0.45):
    """
    Genera un gráfico de tacómetro para el riesgo del índice S4.
    valor_s4_ejemplo: Valor donde apuntará la aguja (por defecto 0.45).
    """
    # Configuración inicial del lienzo
    fig, ax = plt.subplots(figsize=(9, 5))
    
    # ==========================================
    # LÓGICA DE MAPEO A GRADOS (0 a 180)
    # ==========================================
    radio_exterior = 1.0
    ancho_arco = 0.35
    
    # 1. Zona Verde (0.0 a 0.3) -> (180° a 126°)
    w_verde = patches.Wedge(
        (0,0), radio_exterior, 126, 180, width=ancho_arco, 
        facecolor='#2ecc71', edgecolor='white', linewidth=2
    )
    
    # 2. Zona Amarilla (0.3 a 0.6) -> (126° a 72°)
    w_amarillo = patches.Wedge(
        (0,0), radio_exterior, 72, 126, width=ancho_arco, 
        facecolor='#f1c40f', edgecolor='white', linewidth=2
    )
    
    # 3. Zona Roja (0.6 a 1.0+) -> (72° a 0°)
    w_rojo = patches.Wedge(
        (0,0), radio_exterior, 0, 72, width=ancho_arco, 
        facecolor='#e74c3c', edgecolor='white', linewidth=2
    )

    # Añadir los arcos
    ax.add_patch(w_verde)
    ax.add_patch(w_amarillo)
    ax.add_patch(w_rojo)

    # ==========================================
    # ETIQUETAS DE LOS UMBRALES MATEMÁTICOS
    # ==========================================
    r_texto = 1.15 
    umbrales = {'0.0': 180, '0.3': 126, '0.6': 72, '1.0+': 0}
    
    for texto, angulo in umbrales.items():
        x = np.cos(np.radians(angulo)) * r_texto
        y = np.sin(np.radians(angulo)) * r_texto
        ax.text(x, y, texto, ha='center', va='center', fontsize=12, fontweight='bold', color='#333333')

    # ==========================================
    # AGUJA INDICADORA (MOTOR PREDICTIVO)
    # ==========================================
    valor_clamp = min(valor_s4_ejemplo, 1.0)
    angulo_aguja = 180 - (valor_clamp / 1.0) * 180
    angulo_rad = np.radians(angulo_aguja)
    
    x_flecha = np.cos(angulo_rad) * (radio_exterior - 0.1)
    y_flecha = np.sin(angulo_rad) * (radio_exterior - 0.1)
    
    # Flecha
    ax.annotate('', xy=(x_flecha, y_flecha), xytext=(0, 0),
                arrowprops=dict(arrowstyle='wedge,tail_width=0.4', facecolor='#2c3e50', shrinkA=0))
    
    # Centro (Pivote)
    ax.add_patch(patches.Circle((0,0), 0.08, facecolor='#2c3e50', zorder=10))

    # ==========================================
    # LEYENDAS Y TEXTOS OPERATIVOS
    # ==========================================
    ax.text(0, 0.35, f'max(S4_pred) = {valor_s4_ejemplo}', ha='center', va='center', 
            fontsize=13, fontweight='bold', color='#2c3e50',
            bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.4', alpha=0.9))

    ax.text(-0.8, -0.2, 'Estado Verde\n< 0.3\n(Nominal)', ha='center', va='top', fontsize=11, color='#27ae60', fontweight='bold')
    ax.text(0, -0.2, 'Estado Amarillo\n[0.3, 0.6)\n(Precaución)', ha='center', va='top', fontsize=11, color='#d35400', fontweight='bold')
    ax.text(0.8, -0.2, 'Estado Rojo\n$\geq$ 0.6\n(Alerta Crítica)', ha='center', va='top', fontsize=11, color='#c0392b', fontweight='bold')

    plt.title('Tacómetro de Evaluación de Riesgo Operativo (Índice S4)', y=1.05, fontsize=14, fontweight='bold')
    
    # ==========================================
    # CORRECCIÓN DE ENCUADRE (LÍMITES VISUALES)
    # ==========================================
    # Forzamos los límites de la "cámara" para asegurar que los arcos y textos sean visibles
    ax.set_xlim(-1.4, 1.4)
    ax.set_ylim(-0.5, 1.4)
    ax.set_aspect('equal') # Mantiene la proporción para que no se vea ovalado
    ax.axis('off')         # Ocultamos las líneas del plano cartesiano
    
    # ==========================================
    # EXPORTACIÓN
    # ==========================================
    nombre_archivo = 'Figura_5_2_Tacometro_Riesgo'
    plt.savefig(f'{nombre_archivo}.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig(f'{nombre_archivo}.pdf', bbox_inches='tight', facecolor='white')
    
    print(f"¡Gráfico generado exitosamente y centrado!")
    print(f"- {nombre_archivo}.png")
    print(f"- {nombre_archivo}.pdf")
    
    plt.show()

if __name__ == "__main__":
    generar_tacometro_s4(valor_s4_ejemplo=0.45)