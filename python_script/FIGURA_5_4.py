import graphviz

def generar_diagrama_mlops_grande():
    # Configuración principal del gráfico
    dot = graphviz.Digraph(
        'Estrategia_MLOps_Grande', 
        graph_attr={
            'rankdir': 'TB',       # De arriba a abajo
            'splines': 'ortho',    
            'nodesep': '0.5',      # Aumentamos un poco la separación para que las cajas más grandes no choquen
            'ranksep': '0.6',      
            'dpi': '300',          # Mantenemos alta resolución
            'compound': 'true',    
            'fontname': 'Helvetica'
        }
    )
    
    # ==========================================
    # 1. ESTILOS GLOBALES (MÁS GRANDES)
    # ==========================================
    # Aumentamos fontsize de 11 a 14 y el margen interno para hacer las cajas más grandes
    dot.attr('node', shape='box', style='rounded,filled', fontname='Helvetica', 
             fontsize='14', margin='0.3,0.2') 
    
    # Aumentamos fontsize de las flechas de 10 a 12
    dot.attr('edge', fontname='Helvetica', fontsize='12', color='#555555')

    # ==========================================
    # CLÚSTER 1: ENTORNO CLOUD
    # ==========================================
    with dot.subgraph(name='cluster_cloud') as c:
        # Aumentamos el fontsize del título del clúster de 12 a 16
        c.attr(label='Entorno de Entrenamiento Cloud (Alta Demanda)', 
               style='filled', fillcolor='#eaf2f8', color='#2980b9', 
               fontcolor='#154360', fontsize='16', fontweight='bold')
        
        c.node('C_HW', 'Hardware:\nGoogle Colab Pro\nGPU NVIDIA T4', shape='component', fillcolor='#aed6f1')
        
        with c.subgraph() as s:
            s.attr(rank='same')
            c.node('C_Train', 'Entrenamiento Anual\ny Optimización de\nHiperparámetros', fillcolor='#d4e6f1')
            c.node('C_FineTune', 'Protocolo Mensual:\nReentrenamiento (Fine-Tuning)\ncon Nueva Climatología', fillcolor='#d4e6f1')
        
        c.edge('C_HW', 'C_Train', style='dashed')
        c.edge('C_HW', 'C_FineTune', style='dashed')

    # ==========================================
    # ARTEFACTO INTERMEDIO
    # ==========================================
    dot.node('A_Model', 'Pesos Sinápticos\nActualizados (.h5 / .keras)', shape='cylinder', fillcolor='#fcf3cf', color='#d4ac0d')

    # ==========================================
    # CLÚSTER 2: ENTORNO LOCAL
    # ==========================================
    with dot.subgraph(name='cluster_local') as c:
        # Título del clúster más grande (16)
        c.attr(label='Entorno de Producción Local (Inferencia)', 
               style='filled', fillcolor='#e9f7ef', color='#27ae60', 
               fontcolor='#145a32', fontsize='16', fontweight='bold')
        
        with c.subgraph() as s:
            s.attr(rank='same')
            c.node('L_HW', 'Hardware Local:\nIntel Core i7 (13Gen)\n32 GB RAM DDR4', shape='component', fillcolor='#a9dfbf')
            c.node('L_Cron', 'Orquestador:\nTareas Temporizadas\n(Cron Jobs)', shape='tab', fillcolor='#d5f5e3')
            c.node('L_Data', 'Paquetes de Datos\n(Ingesta al Minuto)', shape='folder', fillcolor='#d5f5e3')
        
        c.node('L_Infer', 'Script Principal:\n05_Inference_Pipeline.py', shape='note', fillcolor='#d5f5e3')
        c.node('L_Dash', 'Latencia < 2 seg.\nPredicción Actualizada', fillcolor='#abebc6', fontcolor='black')
        
        c.edge('L_Cron', 'L_Infer', label=' Dispara minuto\n a minuto')
        c.edge('L_Data', 'L_Infer', label=' Flujo I/O')
        c.edge('L_HW', 'L_Infer', style='dashed')
        c.edge('L_Infer', 'L_Dash')

    # ==========================================
    # CONEXIONES GLOBALES
    # ==========================================
    dot.edge('C_Train', 'A_Model')
    dot.edge('C_FineTune', 'A_Model')
    
    # Textos de flechas importantes con fuente en negrita
    dot.edge('A_Model', 'L_Infer', label=' Despliegue de\n Actualización', fontcolor='#d35400', color='#d35400', style='bold')
    
    dot.edge('L_Data', 'C_FineTune', label=' Acumulación de historial\n para reentrenamiento mensual', 
             style='dotted', color='#8e44ad', fontcolor='#8e44ad', constraint='false')

    # ==========================================
    # EXPORTACIÓN
    # ==========================================
    nombre_archivo = 'Figura_5_4_Estrategia_MLOps_Grande'
    
    dot.format = 'png'
    dot.render(f'{nombre_archivo}', cleanup=True)
    
    dot.format = 'pdf'
    dot.render(f'{nombre_archivo}', cleanup=True)

    print(f"¡Diagrama MLOps actualizado (tamaño de letra y cajas ampliado)!")
    print(f"- {nombre_archivo}.png")
    print(f"- {nombre_archivo}.pdf")

if __name__ == "__main__":
    generar_diagrama_mlops_grande()