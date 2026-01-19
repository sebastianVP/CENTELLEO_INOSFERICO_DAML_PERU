import os
from graphviz import Digraph

# 1. Preparación de carpeta
folder_path = 'img'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 2. Crear el grafo principal con dirección Top-to-Bottom (TB)
dot = Digraph('LSTM_Vertical_Comparison', comment='Comparativa Vertical de Arquitecturas')
dot.attr(rankdir='TB', nodesep='0.8', ranksep='1.0')
dot.attr('node', shape='rectangle', style='filled', fillcolor='#FDFDFD', 
         fontname='Arial', fontsize='10', width='2.2', height='1.0', fixedsize='true')

# --- ARQUITECTURA 1: SIMPLE (SUPERIOR) ---
with dot.subgraph(name='cluster_0') as c:
    # Etiqueta con características técnicas
    c.attr(label='ARQUITECTURA 1: LSTM SIMPLE (BASELINE)\n'
                 '• Modelo base con ~23,000 parámetros\n'
                 '• Una sola capa recurrente\n'
                 '• Ideal para establecer rendimiento de referencia', 
           fontname='Arial Bold', fontsize='12', color='blue', labelloc='t')
    
    c.node('A1_In', 'INPUT\n60 Timesteps\n9 Features')
    c.node('A1_LSTM', 'LSTM\n64 Units\n(tanh)')
    c.node('A1_Drop', 'DROPOUT\n0.2')
    c.node('A1_Out', 'DENSE\nHorizon\n(linear)')
    
    c.edge('A1_In', 'A1_LSTM')
    c.edge('A1_LSTM', 'A1_Drop')
    c.edge('A1_Drop', 'A1_Out')

# --- ARQUITECTURA 2: STACKED (INFERIOR) ---
with dot.subgraph(name='cluster_1') as c:
    # Etiqueta con características técnicas
    c.attr(label='ARQUITECTURA 2: LSTM STACKED (APILADA)\n'
                 '• ~67,500 parámetros\n'
                 '• Aprendizaje jerárquico: capas de bajo nivel y contexto abstracto\n'
                 '• Mayor capacidad de representación para patrones complejos', 
           fontname='Arial Bold', fontsize='12', color='darkgreen', labelloc='t')
    
    c.node('A2_In', 'INPUT\n60 Timesteps\n9 Features')
    c.node('A2_LSTM', 'LSTM\n128 Units\n(Return Seq: True)')
    c.node('A2_Drop', 'DROPOUT / ACT\n64 Units\n(ReLU)')
    c.node('A2_Out', 'DENSE\n64 Units\n(RU)')
    
    c.edge('A2_In', 'A2_LSTM')
    c.edge('A2_LSTM', 'A2_Drop')
    c.edge('A2_Drop', 'A2_Out')

# Flecha invisible para forzar que el cluster_0 esté estrictamente arriba del cluster_1
dot.edge('A1_Out', 'A2_In', style='invis')

# 3. Renderizado
output_path = os.path.join(folder_path, 'arquitecturas_vertical')
dot.render(output_path, format='png', cleanup=True)

print(f"✅ Figura vertical generada en: {output_path}.png")