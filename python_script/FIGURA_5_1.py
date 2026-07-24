import graphviz

def generar_diagrama_compacto():
    # Configuración general para un diseño más compacto (Top-to-Bottom)
    dot = graphviz.Digraph(
        'Pipeline_ETL_Compacto', 
        graph_attr={
            'rankdir': 'TB',       # Orientación de arriba hacia abajo (ideal para hojas A4/Carta)
            'splines': 'ortho',    # Líneas con ángulos rectos para un aspecto más ordenado
            'nodesep': '0.3',      # Reduce la separación horizontal entre nodos
            'ranksep': '0.5',      # Reduce la separación vertical entre niveles
            'dpi': '300',          # Alta resolución para el PNG
            'compound': 'true'     # Permite flechas lógicas entre clústeres si es necesario
        }
    )
    
    # Estilo general de los nodos y aristas con fuente un poco más compacta
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='white', 
             fontname='Helvetica', fontsize='11', margin='0.1,0.1')
    dot.attr('edge', fontname='Helvetica', fontsize='10', color='#555555')

    # ==========================================
    # FUENTES DE DATOS (Entradas crudas)
    # ==========================================
    with dot.subgraph(name='cluster_fuentes') as c:
        c.attr(label='Fuentes de Datos Asíncronas', style='dashed', color='gray', fontsize='12')
        # Colocamos las fuentes en el mismo nivel para que se alineen horizontalmente
        with c.subgraph() as s:
            s.attr(rank='same')
            s.node('N_Jicamarca', 'Jicamarca\n(S4, TEC, ROTI)', fillcolor='#fcf3cf')
            s.node('N_OMNI', 'OMNI\n(Kp, Dst, AE)', fillcolor='#fcf3cf')
            s.node('N_GNSS', 'GNSS Solar\n(f10.7)', fillcolor='#fcf3cf')

    # ==========================================
    # MÓDULO 1: INGESTA
    # ==========================================
    with dot.subgraph(name='cluster_ingesta') as c:
        c.attr(label='1. Ingesta (ETL) [pandas, requests]', style='filled', fillcolor='#ebdef0', color='#8e44ad', fontcolor='black')
        c.node('M1_Descarga', 'Descarga Automática y Limpieza')
        c.node('M1_Sync', 'Sincronización\n(Inner Join temporal por minuto)')
        c.edge('M1_Descarga', 'M1_Sync')

    # ==========================================
    # MÓDULO 2: PREPROCESAMIENTO
    # ==========================================
    with dot.subgraph(name='cluster_preproc') as c:
        c.attr(label='2. Preprocesamiento [scikit-learn, numpy]', style='filled', fillcolor='#d4e6f1', color='#2980b9', fontcolor='black')
        c.node('M2_CodTemp', 'Codificación Temporal\n-> 9 Predictoras')
        c.node('M2_Escalamiento', 'Normalización MinMax [0, 1]')
        c.node('M2_Ventanas', 'Ventaneo (Sliding Windows)\nGeneración de Tensores')
        c.edge('M2_CodTemp', 'M2_Escalamiento')
        c.edge('M2_Escalamiento', 'M2_Ventanas')

    # ==========================================
    # MÓDULO 3: NÚCLEO PREDICTIVO
    # ==========================================
    with dot.subgraph(name='cluster_nucleo') as c:
        c.attr(label='3. Núcleo Predictivo [TensorFlow, Keras]', style='filled', fillcolor='#d5f5e3', color='#27ae60', fontcolor='black')
        c.node('M3_Modelo', 'Modelo Stacked LSTM', shape='cylinder')
        c.node('M3_Inferencia', 'Inferencia Vectorial Multi-Step')
        c.edge('M3_Modelo', 'M3_Inferencia')

    # ==========================================
    # MÓDULO 4: VISUALIZACIÓN
    # ==========================================
    with dot.subgraph(name='cluster_vis') as c:
        c.attr(label='4. Visualización [matplotlib, seaborn]', style='filled', fillcolor='#fdebd0', color='#f39c12', fontcolor='black')
        c.node('M4_Inversa', 'Inversa de Escalamiento')
        c.node('M4_Dashboard', 'Dashboard:\nUmbrales y Trayectorias', shape='note')
        c.edge('M4_Inversa', 'M4_Dashboard')

    # ==========================================
    # CONEXIONES ENTRE MÓDULOS (Flujo de Datos)
    # ==========================================
    # Agrupamos las salidas de las fuentes hacia un solo punto para no cruzar tantas líneas
    dot.edge('N_Jicamarca', 'M1_Descarga')
    dot.edge('N_OMNI', 'M1_Descarga')
    dot.edge('N_GNSS', 'M1_Descarga')

    # Transiciones con etiquetas claras
    dot.edge('M1_Sync', 'M2_CodTemp', label=' Datos Crudos\n Sincronizados')
    dot.edge('M2_Ventanas', 'M3_Modelo', label=' Tensor 3D: (Batch_Size, 70, 9)', fontcolor='blue')
    dot.edge('M3_Inferencia', 'M4_Inversa', label=' Vector Predictivo (t+1, ..., t+10)', fontcolor='red')

    # ==========================================
    # EXPORTACIÓN A MÚLTIPLES FORMATOS
    # ==========================================
    nombre_archivo = 'Figura_5_1_Arquitectura_Sistema'
    
    # 1. Generar y guardar como PNG
    dot.format = 'png'
    dot.render(f'{nombre_archivo}_img', cleanup=True)
    
    # 2. Generar y guardar como PDF
    dot.format = 'pdf'
    dot.render(f'{nombre_archivo}_doc', cleanup=True)

    print(f"¡Listo! Se han generado los archivos de alta resolución:")
    print(f"- {nombre_archivo}_img.png")
    print(f"- {nombre_archivo}_doc.pdf")

if __name__ == "__main__":
    generar_diagrama_compacto()