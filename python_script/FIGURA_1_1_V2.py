import os
import graphviz

def generar_diagrama_pipeline_tesis_mejorado():
    # --- CONFIGURACIÓN DE LA CARPETA DE DESTINO ---
    nombre_carpeta = 'graficos_tesis'
    
    # Si la carpeta no existe, la crea automáticamente
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)

    # Inicializar el diagrama
    dot = graphviz.Digraph('Pipeline_Macro', comment='Macro Pipeline Diagram')
    dot.attr(rankdir='TB', compound='true') 

    # --- CONTROL DE TAMAÑO PARA HOJA A4 y ESPACIADO ---
    # size="ancho,alto!" restringe el tamaño máximo en pulgadas. 
    # 7.5 x 9.5 pulgadas deja espacio ideal para los márgenes de la hoja y la descripción inferior.
    dot.attr(size='7.5,9.5!', ratio='fill')
    dot.attr(nodesep='0.5', ranksep='0.5')

    # --- ESTILOS GLOBALES ---
    dot.attr('node', shape='box', style='filled,rounded', 
             color='#2c3e50', fontname='Arial', fontsize='13', 
             margin='0.25,0.15')
    
    dot.attr('edge', color='#7f8c8d', fontname='Arial', fontsize='11', 
             arrowsize='0.9', penwidth='1.3')

    # --- CLUSTER 1: FUENTES DE DATOS ---
    with dot.subgraph(name='cluster_inputs') as c:
        c.attr(label='1. Fuentes de Datos', style='dashed', color='#7f8c8d', 
               fontsize='14', fontname='Arial', margin='15')
        c.attr('node', fillcolor='#e8f5e9')
        
        c.node('DataLocal', 
               '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="3">'
               '  <TR><TD><FONT POINT-SIZE="15"><B>Datos Locales (IGP/LISN)</B></FONT></TD></TR>'
               '  <TR><TD><FONT POINT-SIZE="12">Estaciones Perú</FONT></TD></TR>'
               '  <TR><TD><FONT POINT-SIZE="12">• Índice S4 (Target)</FONT></TD></TR>'
               '</TABLE>>')
        
        c.node('DataGlobal', 
               '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="3">'
               '  <TR><TD><FONT POINT-SIZE="15"><B>Datos Globales (NASA/NOAA)</B></FONT></TD></TR>'
               '  <TR><TD><FONT POINT-SIZE="12">Parámetros Geofísicos/Solares</FONT></TD></TR>'
               '  <TR><TD><FONT POINT-SIZE="12">• TEC, ROTI, Kp, Dst, f10.7</FONT></TD></TR>'
               '</TABLE>>')
               
    with dot.subgraph() as s:
        s.attr(rank='same')
        s.node('DataLocal')
        s.node('DataGlobal')

    # --- CLUSTER 2: PREPROCESAMIENTO ---
    dot.node('Preproc', 
             '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="3">'
             '  <TR><TD><FONT POINT-SIZE="15"><B>Preprocesamiento y Sincronización</B></FONT></TD></TR>'
             '  <TR><TD><FONT POINT-SIZE="12">• Limpieza y Sincronización temporal</FONT></TD></TR>'
             '  <TR><TD><FONT POINT-SIZE="12">• Agregación (Worst-Case Scenario)</FONT></TD></TR>'
             '</TABLE>>', fillcolor='#e3f2fd')

    dot.node('FeatEng', 
             '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="3">'
             '  <TR><TD><FONT POINT-SIZE="15"><B>Ingeniería de Características</B></FONT></TD></TR>'
             '  <TR><TD><FONT POINT-SIZE="12">• <I>Cod. Cíclica Temporal (Sin/Cos)</I></FONT></TD></TR>'
             '  <TR><TD><FONT POINT-SIZE="12">• Normalización Min-Max</FONT></TD></TR>'
             '</TABLE>>', fillcolor='#e3f2fd')

    # --- CLUSTER 3: NÚCLEO PREDICTIVO ---
    with dot.subgraph(name='cluster_model') as c:
        c.attr(label='2. Núcleo Predictivo Deep Learning', style='filled', color='#fff3e0', 
               fontsize='14', fontname='Arial', margin='15')
        c.attr('node', fillcolor='white')
        
        c.node('InputTensor', '<<FONT POINT-SIZE="14"><B>Tensor de Entrada</B></FONT><BR/><FONT POINT-SIZE="12">[70 min de Historia]</FONT>>')
        
        c.node('LSTM_Core', 
               '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="3">'
               '  <TR><TD><FONT POINT-SIZE="15"><B>Modelo Stacked LSTM</B></FONT></TD></TR>'
               '  <TR><TD><FONT POINT-SIZE="12">Extracción Jerárquica de Features</FONT></TD></TR>'
               '  <TR><TD><FONT COLOR="#d35400" POINT-SIZE="12"><B>Optimizador: Focal Loss</B></FONT></TD></TR>'
               '</TABLE>>', shape='component')
               
        c.node('OutputDense', '<<FONT POINT-SIZE="14"><B>Capa Dense</B></FONT><BR/><FONT POINT-SIZE="12">(Salida Vectorial)</FONT>>')
        
        c.edge('InputTensor', 'LSTM_Core')
        c.edge('LSTM_Core', 'OutputDense')

    # --- CLUSTER 4: SALIDA Y ALERTA ---
    dot.node('PredictVector', '<<FONT POINT-SIZE="14"><B>Vector de Predicción</B></FONT><BR/><FONT POINT-SIZE="12">(Horizonte 10 min)</FONT>>', fillcolor='#ffecb3')
    
    dot.node('Alert', 
             '<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="1">'
             '  <TR><TD><FONT POINT-SIZE="15"><B>Generación de Alerta</B></FONT></TD></TR>'
             '  <TR><TD><FONT POINT-SIZE="12">Umbral: <B>[ S4 ≥ 0.6 ]</B></FONT></TD></TR>'
             '</TABLE>>', shape='parallelogram', fillcolor='#ffcdd2', margin='0.05,0.05')

    # CONEXIONES
    dot.edge('DataLocal', 'Preproc')
    dot.edge('DataGlobal', 'Preproc')
    dot.edge('Preproc', 'FeatEng')
    dot.edge('FeatEng', 'InputTensor')
    dot.edge('OutputDense', 'PredictVector')
    dot.edge('PredictVector', 'Alert')

    # RENDERIZADO
    nombre_base = 'figura_macro_pipeline_optimizado'
    ruta_completa = os.path.join(nombre_carpeta, nombre_base)
    
    dot.render(ruta_completa, format='pdf', cleanup=True)
    dot.render(ruta_completa, format='png', cleanup=True)
    
    print(f"¡Hecho! El diagrama se auto-ajustará para entrar en una hoja A4 dejando el espacio inferior libre.")

if __name__ == "__main__":
    generar_diagrama_pipeline_tesis_mejorado()