import graphviz

def generar_diagrama_mlops_ligero_letra_grande():
    # Configuración de lienzo optimizada para reducir MB manteniendo la proporción de la letra
    dot = graphviz.Digraph(
        'Estrategia_MLOps_Optimizado', 
        graph_attr={
            'rankdir': 'TB',       # Flujo de arriba a abajo
            'splines': 'ortho',    
            # Volvemos a separaciones estándar para que el tamaño real de la imagen no sea gigante
            'nodesep': '0.7',      
            'ranksep': '0.9',      
            'dpi': '300',          # 300 DPI es excelente para impresión y no genera archivos pesados
            'compound': 'true',    
            'fontname': 'Helvetica'
        }
    )
    
    # ==========================================
    # 1. ESTILOS GLOBALES (FUENTES GRANDES VS CUADROS)
    # ==========================================
    # Elevamos la fuente a 24 para que destaque visualmente sobre el tamaño del cuadro.
    # El margen se mantiene controlado (0.4, 0.25) para que los cuadros no pesen de más en píxeles.
    dot.attr('node', shape='box', style='rounded,filled', fontname='Helvetica', 
             fontsize='24', margin='0.4,0.25', penwidth='2') 
    
    # Etiquetas de las flechas a un tamaño muy legible de 18
    dot.attr('edge', fontname='Helvetica', fontsize='18', color='#444444', penwidth='2')

    # ==========================================
    # CLÚSTER 1: ENTORNO CLOUD
    # ==========================================
    with dot.subgraph(name='cluster_cloud') as c:
        # Título del clúster grande (28) para mantener la jerarquía académica
        c.attr(label='Entorno de Entrenamiento Cloud (Alta Demanda)', 
               style='filled', fillcolor='#eaf2f8', color='#2980b9', penwidth='2.5',
               fontcolor='#154360', fontsize='28', fontweight='bold')
        
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
    dot.node('A_Model', 'Pesos Sinápticos\nActualizados (.h5 / .keras)', shape='cylinder', fillcolor='#fcf3cf', color='#d4ac0d', penwidth='2')

    # ==========================================
    # CLÚSTER 2: ENTORNO LOCAL
    # ==========================================
    with dot.subgraph(name='cluster_local') as c:
        # Título del bloque local a tamaño 28
        c.attr(label='Entorno de Producción Local (Inferencia)', 
               style='filled', fillcolor='#e9f7ef', color='#27ae60', penwidth='2.5',
               fontcolor='#145a32', fontsize='28', fontweight='bold')
        
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
    
    dot.edge('A_Model', 'L_Infer', label=' Despliegue de\n Actualización', fontcolor='#d35400', color='#d35400', style='bold', penwidth='2.5')
    
    dot.edge('L_Data', 'C_FineTune', label=' Acumulación de historial\n para reentrenamiento mensual', 
             style='dotted', color='#8e44ad', fontcolor='#8e44ad', constraint='false', penwidth='2')

    # ==========================================
    # EXPORTACIÓN OPTIMIZADA EN ESPACIO
    # ==========================================
    nombre_archivo = 'Figura_5_4_MLOps_Ligero'
    
    try:
        # Guardar PNG (Ahora pesará una fracción de megabyte y mantendrá las letras grandes)
        dot.format = 'png'
        dot.render(f'{nombre_archivo}', cleanup=True)
        
        # Guardar PDF (¡Ultra recomendado para la tesis! Pesa poquísimo por ser vectorial y nunca se pixela)
        dot.format = 'pdf'
        dot.render(f'{nombre_archivo}', cleanup=True)

        print(f"¡Éxito! Gráfico optimizado generado.")
        print(f" - Resultado: Letras visualmente grandes y legibles.")
        print(f" - Peso del archivo: Reducido drásticamente (Ideal para que tu PDF final de tesis no sea pesado).")
        print(f"Archivos listos:")
        print(f" ➔ {nombre_archivo}.png")
        print(f" ➔ {nombre_archivo}.pdf")
    except Exception as e:
        print(f"Error al exportar: {e}")

if __name__ == "__main__":
    generar_diagrama_mlops_ligero_letra_grande()