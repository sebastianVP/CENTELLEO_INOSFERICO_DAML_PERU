import os
from graphviz import Digraph

# Crear la carpeta 'img' si no existe
output_dir = 'img'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Función auxiliar para crear un grafo base con estilo uniforme
def crear_grafo_base(nombre, titulo):
    dot = Digraph(nombre)
    # Configuración para flujo vertical (Top-to-Bottom) y nodos proporcionados
    dot.attr(rankdir='TB', nodesep='0.5', ranksep='0.5')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightgrey',
             fontname='Helvetica', fixedsize='true', width='2.5', height='1.2')
    dot.attr('edge', fontname='Helvetica')
    # Título del gráfico
    dot.attr(label=titulo, labelloc='t', fontsize='14', fontname='Helvetica-Bold')
    return dot

# ==========================================
# Diagrama 1: Arquitectura 1: LSTM Simple (Baseline)
# ==========================================
titulo1 = "Arquitectura 1: LSTM Simple (Baseline)\n~23,000 parámetros"
dot1 = crear_grafo_base('LSTM_Simple', titulo1)

# Definir nodos con detalles de la imagen 1
dot1.node('In1', 'Input\n\n60 timesteps\n9 features')
dot1.node('L1', 'LSTM\n\n64 units, tanh')
dot1.node('D1', 'Dropout\n\n0.2')
dot1.node('Out1', 'Dense\n\nhorizon, linear')

# Definir aristas
dot1.edge('In1', 'L1')
dot1.edge('L1', 'D1')
dot1.edge('D1', 'Out1')

# Renderizar imagen 1
dot1.render(os.path.join(output_dir, 'arquitectura1_lstm_simple'), format='png', cleanup=True)
print("Generado: arquitectura1_lstm_simple.png")


# ==========================================
# Diagrama 2: Arquitectura 2: LSTM Stacked (Apilada)
# ==========================================
titulo2 = "Arquitectura 2: LSTM Stacked (Apilada)\n~67,500 parámetros"
dot2 = crear_grafo_base('LSTM_Stacked', titulo2)

# Definir nodos con detalles de la imagen 2
dot2.node('In2', 'Input\n\n60 timesteps\n9 features')
dot2.node('L2_1', 'LSTM\n\n128 units\nreturn_sequences=True')
dot2.node('Drop2', 'Dropout\n\n64\nReLU')
dot2.node('Out2', 'Dense\n\n64\nRU')

# Definir aristas
dot2.edge('In2', 'L2_1')
dot2.edge('L2_1', 'Drop2')
dot2.edge('Drop2', 'Out2')

# Renderizar imagen 2
dot2.render(os.path.join(output_dir, 'arquitectura2_lstm_stacked'), format='png', cleanup=True)
print("Generado: arquitectura2_lstm_stacked.png")


# ==========================================
# Diagrama 3: Arquitectura 3: LSTM Bidireccional
# ==========================================
titulo3 = "Arquitectura 3: LSTM Bidireccional\n~45,800 parámetros"
dot3 = crear_grafo_base('LSTM_Bidireccional', titulo3)

# Definir nodos con detalles de la imagen 3
dot3.node('In3', 'Input\n\n60 timesteps\n9 features')
dot3.node('Conv', 'Conv1D\n\n32 filters\nkernel size\nReLU')
dot3.node('BiL1', 'Bidirectional LSTM\n\n64 units')
dot3.node('BN', 'BatchNormalization')
dot3.node('Drop3', 'Dropout\n\n0.3')
dot3.node('BiL2', 'Bidirectional LSTM\n\n32 units')
dot3.node('Out3', 'Dense Output\n\n(linear)')

# Definir aristas secuenciales
dot3.edge('In3', 'Conv')
dot3.edge('Conv', 'BiL1')
dot3.edge('BiL1', 'BN')
dot3.edge('BN', 'Drop3')
dot3.edge('Drop3', 'BiL2')
dot3.edge('BiL2', 'Out3')

# Renderizar imagen 3
dot3.render(os.path.join(output_dir, 'arquitectura3_lstm_bidireccional'), format='png', cleanup=True)
print("Generado: arquitectura3_lstm_bidireccional.png")

print(f"\n¡Proceso completado! Las 3 imágenes se han guardado en la carpeta '{output_dir}'.")