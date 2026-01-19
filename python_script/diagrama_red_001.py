import os
from graphviz import Digraph

# 1. Crear la carpeta 'img' si no existe
folder_path = 'img'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 2. Crear el objeto Digraph
dot = Digraph('LSTM_Simple_Architecture', comment='Arquitectura 1: LSTM Simple')

# 3. Configuración de proporciones y estilo global
dot.attr(rankdir='LR', size='12,5!', ratio='fill') # Tamaño fijo y proporcionado
dot.attr('node', 
         shape='rectangle', 
         style='filled', 
         fillcolor='#F9F9F9', 
         fontname='Segoe UI, Arial',
         fontsize='11',
         width='2.2',    # Ancho uniforme para todos los nodos
         height='1.2',   # Alto uniforme para todos los nodos
         fixedsize='true') # Fuerza a que los nodos respeten el ancho/alto definido

# Título del diagrama
dot.attr(labelloc='t', label='Arquitectura 1: LSTM Simple (Baseline)\n\n', fontsize='16')

# 4. Definición de los Nodos (Nombres técnicos precisos)
dot.node('Input', 'INPUT LAYER\n\n60 Timesteps\n9 Features')
dot.node('LSTM', 'LSTM LAYER\n\n64 Units\nActivation: Tanh')
dot.node('Dropout', 'DROPOUT\n\nRate: 0.2')
dot.node('Dense', 'DENSE (OUTPUT)\n\n10 Horizon\nActivation: Linear')

# 5. Definición de las Conexiones con estilo de flecha
dot.edge('Input', 'LSTM', penwidth='1.5')
dot.edge('LSTM', 'Dropout', penwidth='1.5')
dot.edge('Dropout', 'Dense', penwidth='1.5')

# 6. Renderizar y guardar en la carpeta /img
# El nombre del archivo incluirá la ruta de la carpeta
output_filename = os.path.join(folder_path, 'diagrama_lstm_simple')
dot.render(output_filename, format='png', cleanup=True)

print(f"✅ Proceso completado. El diagrama se guardó en: {output_filename}.png")