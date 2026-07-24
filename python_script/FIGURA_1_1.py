import graphviz

def generar_diagrama_pipeline_tesis_compacto():
    # rankdir='TB' (Top to Bottom) para un diseño vertical
    dot = graphviz.Digraph('Pipeline_Macro', comment='Macro Pipeline Diagram')
    dot.attr(rankdir='TB', compound='true') 

    # ESTILOS GLOBALES - Reducidos a la mitad
    # Bajamos el fontsize de 15 a 10, y los márgenes de 0.3 a 0.1
    dot.attr('node', shape='box', style='filled,rounded', 
             color='#2c3e50', fontname='Arial', fontsize='10', 
             margin='0.1,0.1')
    
    # Bajamos el tamaño de la flecha y el texto de la conexión
    dot.attr('edge', color='#7f8c8d', fontname='Arial', fontsize='9', 
             arrowsize='0.7', penwidth='1.0')

    # --- CLUSTER 1: FUENTES DE DATOS ---
    with dot.subgraph(name='cluster_inputs') as c:
        c.attr(label='1. Fuentes de Datos', style='dashed', color='#7f8c8d', fontsize='10', fontname='Arial', margin='10')
        c.attr('node', fillcolor='#e8f5e9')
        
        c.node('DataLocal', 
               '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="1">'
               '  <TR><TD><FONT POINT-SIZE="11"><B>Datos Locales (IGP/LISN)</B></FONT></TD></TR>'
               '  <TR><TD>Estaciones Perú</TD></TR>'  # CAMBIO APLICADO AQUÍ
               '  <TR><TD>• Índice S4 (Target)</TD></TR>'
               '</TABLE>>')
        
        c.node('DataGlobal', 
               '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="1">'
               '  <TR><TD><FONT POINT-SIZE="11"><B>Datos Globales (NASA/NOAA)</B></FONT></TD></TR>'
               '  <TR><TD>Parámetros Geofísicos/Solares</TD></TR>'
               '  <TR><TD>• TEC, ROTI, Kp, Dst, f10.7</TD></TR>'
               '</TABLE>>')
               
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('DataLocal')
        s.node('DataGlobal')

    # --- CLUSTER 2: PREPROCESAMIENTO ---
    dot.node('Preproc', 
             '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="1">'
             '  <TR><TD><FONT POINT-SIZE="11"><B>Preprocesamiento y Sincronización</B></FONT></TD></TR>'
             '  <TR><TD>• Limpieza y Sincronización temporal</TD></TR>'
             '  <TR><TD>• Agregación (Worst-Case Scenario)</TD></TR>'
             '</TABLE>>', fillcolor='#e3f2fd')

    dot.node('FeatEng', 
             '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="1">'
             '  <TR><TD><FONT POINT-SIZE="11"><B>Ingeniería de Características</B></FONT></TD></TR>'
             '  <TR><TD>• <I>Cod. Cíclica Temporal (Sin/Cos)</I></TD></TR>'
             '  <TR><TD>• Normalización Min-Max</TD></TR>'
             '</TABLE>>', fillcolor='#e3f2fd')

    # --- CLUSTER 3: NÚCLEO PREDICTIVO ---
    with dot.subgraph(name='cluster_model') as c:
        c.attr(label='2. Núcleo Predictivo Deep Learning', style='filled', color='#fff3e0', fontsize='10', fontname='Arial', margin='10')
        c.attr('node', fillcolor='white')
        
        c.node('InputTensor', '<<B>Tensor de Entrada</B><BR/>[70 min de Historia]>')
        
        c.node('LSTM_Core', 
               '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="1">'
               '  <TR><TD><FONT POINT-SIZE="11"><B>Modelo Stacked LSTM</B></FONT></TD></TR>'
               '  <TR><TD>Extracción Jerárquica de Features</TD></TR>'
               '  <TR><TD><FONT COLOR="#d35400"><B>Optimizador: Focal Loss</B></FONT></TD></TR>'
               '</TABLE>>', shape='component')
               
        c.node('OutputDense', '<<B>Capa Dense</B><BR/>(Salida Vectorial)>')
        
        c.edge('InputTensor', 'LSTM_Core')
        c.edge('LSTM_Core', 'OutputDense')

    # --- CLUSTER 4: SALIDA Y ALERTA ---
    dot.node('PredictVector', '<<B>Vector de Predicción</B><BR/>(Horizonte 10 min)>', fillcolor='#ffecb3')
    
    # AJUSTE DE TAMAÑO EN LA ALERTA (Márgenes mínimos y textos un poco más cortos)
    dot.node('Alert', 
             '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">'
             '  <TR><TD><FONT POINT-SIZE="11"><B>Generación de Alerta</B></FONT></TD></TR>'
             '  <TR><TD>Verificación Umbral</TD></TR>'
             '  <TR><TD><B>[ S4 ≥ 0.6 ]</B></TD></TR>'
             '</TABLE>>', shape='parallelogram', fillcolor='#ffcdd2', margin='0.05,0.05')

    # CONEXIONES
    dot.edge('DataLocal', 'Preproc')
    dot.edge('DataGlobal', 'Preproc')
    dot.edge('Preproc', 'FeatEng')
    dot.edge('FeatEng', 'InputTensor')
    dot.edge('OutputDense', 'PredictVector')
    dot.edge('PredictVector', 'Alert')

    # RENDERIZADO
    nombre_archivo = 'figura_macro_pipeline_mitad'
    dot.render(nombre_archivo, format='pdf', cleanup=True)
    dot.render(nombre_archivo, format='png', cleanup=True)
    
    print("¡Diagrama a la mitad de tamaño, corregido y generado exitosamente!")

if __name__ == "__main__":
    generar_diagrama_pipeline_tesis_compacto()