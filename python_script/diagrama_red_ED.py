import os
from graphviz import Digraph

# 1. Configuración de carpeta
folder_path = 'img'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 2. Inicializar el grafo
# Usamos rankdir='TB' para que el flujo principal sea de arriba a abajo
dot = Digraph('LSTM_Detailed_Flow', comment='Esquema Lookback-Horizon')
dot.attr(rankdir='TB', nodesep='0.8', ranksep='0.6')
dot.attr('node', fontname='Arial', fontsize='10')

# --- BLOQUE SUPERIOR: REPRESENTACIÓN DEL LOOKBACK (60 min) ---
with dot.subgraph(name='cluster_lookback') as c:
    c.attr(label='PASO 1: ENTRADA DE DATOS (Lookback: 60 min)', 
           style='filled', fillcolor='#EBF5FB', fontname='Arial Bold')
    
    # Nodos creados con etiquetas HTML para simular tablas de datos
    c.node('LB_60', '''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
          <TR><TD BGCOLOR="#D5D8DC"><B>t - 60</B></TD></TR>
          <TR><TD>9 Features</TD></TR>
          <TR><TD>Timestep: 0</TD></TR>
        </TABLE>>''', shape='none')
    
    c.node('LB_30', '''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
          <TR><TD BGCOLOR="#D5D8DC"><B>t - 30</B></TD></TR>
          <TR><TD>9 Features</TD></TR>
          <TR><TD>Timestep: 30</TD></TR>
        </TABLE>>''', shape='none')

    c.node('LB_0', '''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
          <TR><TD BGCOLOR="#AED6F1"><B>t (Actual)</B></TD></TR>
          <TR><TD>9 Features</TD></TR>
          <TR><TD>Timestep: 59</TD></TR>
        </TABLE>>''', shape='none')

    c.edge('LB_60', 'LB_30', label='... 30 min ...')
    c.edge('LB_30', 'LB_0', label='... 30 min ...')

# --- BLOQUE CENTRAL: PROCESAMIENTO (Encoder - Contexto) ---
# Forzamos que estos nodos estén alineados horizontalmente
with dot.subgraph() as s:
    s.attr(rank='same')
    s.node('Encoder', 'LSTM ENCODER\n(Capa Recurrente)', 
           shape='box3d', style='filled', fillcolor='#D6EAF8', width='2.0')
    s.node('Context', 'VECTOR DE CONTEXTO\n(Espacio Latente)', 
           shape='ellipse', style='filled', fillcolor='#D5F5E3')

# --- BLOQUE INFERIOR: PREDICCIÓN (Horizonte: 10 min) ---
with dot.subgraph(name='cluster_horizon') as c:
    c.attr(label='PASO 2: SALIDA DE PREDICCIÓN (Horizonte: 10 min)', 
           style='filled', fillcolor='#FDEDEC', fontname='Arial Bold')
    
    c.node('H_1', '''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
          <TR><TD BGCOLOR="#FADBD8"><B>t + 1</B></TD></TR>
          <TR><TD>1 Output (S4)</TD></TR>
        </TABLE>>''', shape='none')
    
    c.node('H_10', '''<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">
          <TR><TD BGCOLOR="#FADBD8"><B>t + 10</B></TD></TR>
          <TR><TD>1 Output (S4)</TD></TR>
        </TABLE>>''', shape='none')

    c.edge('H_1', 'H_10', label='... 10 min ...', style='dashed')

# --- CONEXIONES ENTRE BLOQUES ---
dot.edge('LB_0', 'Encoder')
dot.edge('Encoder', 'Context')
dot.edge('Context', 'H_1', label='Decoder Step')

# 3. Guardar y Renderizar
output_file = os.path.join(folder_path, 'diagrama_secuencial_proporcionado')
dot.render(output_file, format='png', cleanup=True)

print(f"✅ Esquema generado en: {output_file}.png")