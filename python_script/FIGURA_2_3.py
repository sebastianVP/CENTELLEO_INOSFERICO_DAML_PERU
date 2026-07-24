import graphviz

def generar_diagrama_lstm_academico():
    dot = graphviz.Digraph('LSTM_Academico', format='png')
    dot.attr(rankdir='LR', size='10,6', bgcolor='transparent')
    
    # --- Configuración Estilo Académico ---
    # Usamos formas cuadradas para las capas de activación y círculos para las operaciones puntuales
    dot.attr('node', fontname='Times New Roman', fontsize='12')
    
    # Nodos de Entrada y Estado (Variables LaTeX)
    dot.attr('node', shape='none', style='')
    dot.node('x_t', '<<i>x<SUB>t</SUB></i>>')
    dot.node('c_prev', '<<i>c<SUB>t-1</SUB></i>>')
    dot.node('h_prev', '<<i>h<SUB>t-1</SUB></i>>')
    
    dot.node('c_curr', '<<i>c<SUB>t</SUB></i>>')
    dot.node('h_curr', '<<i>h<SUB>t</SUB></i>>')
    dot.node('h_curr_top', '<<i>h<SUB>t</SUB></i>>') # Salida superior

    # --- Compuertas y Activaciones (Cajas Amarillas en la imagen) ---
    dot.attr('node', shape='square', style='filled', fillcolor='#FFFDE7', color='#9E9E9E', width='0.5', height='0.5')
    dot.node('gate_2', 'σ\n(2)') # Compuerta de Olvido
    dot.node('gate_1', 'σ\n(1)') # Compuerta de Entrada
    dot.node('act_tanh', 'tanh')   # Candidato a Celda
    dot.node('gate_3', 'σ\n(3)') # Compuerta de Salida

    # --- Operaciones Puntuales (Círculos Rosados) ---
    dot.attr('node', shape='circle', style='filled', fillcolor='#FCE4EC', color='#9E9E9E', width='0.4', height='0.4')
    dot.node('op_mul1', '×') # Olvido x Memoria
    dot.node('op_mul2', '×') # Entrada x Candidato
    dot.node('op_add', '+')   # Actualización Memoria
    dot.node('op_tanh_out', 'tanh') # Tanh final
    dot.node('op_mul3', '×') # Salida x Tanh final

    # --- Conexiones (El Flujo de Información) ---
    dot.attr('edge', color='black', penwidth='1')

    # 1. Flujo del Estado de Celda (La autopista superior c(t-1) -> c(t))
    dot.edge('c_prev', 'op_mul1')
    dot.edge('op_mul1', 'op_add')
    dot.edge('op_add', 'c_curr')

    # 2. Flujo de Entrada (Concatenación de x(t) y h(t-1))
    dot.edge('x_t', 'gate_2')
    dot.edge('x_t', 'gate_1')
    dot.edge('x_t', 'act_tanh')
    dot.edge('x_t', 'gate_3')
    
    dot.edge('h_prev', 'gate_2')
    dot.edge('h_prev', 'gate_1')
    dot.edge('h_prev', 'act_tanh')
    dot.edge('h_prev', 'gate_3')

    # 3. Lógica de las Compuertas
    # Compuerta de Olvido (f_t)
    dot.edge('gate_2', 'op_mul1')
    
    # Compuerta de Entrada e Candidato
    dot.edge('gate_1', 'op_mul2')
    dot.edge('act_tanh', 'op_mul2')
    
    # Actualización de la Memoria
    dot.edge('op_mul2', 'op_add')

    # 4. Generación del Nuevo Estado Oculto (h_t)
    dot.edge('op_add', 'op_tanh_out') # Memoria entra a tanh
    dot.edge('gate_3', 'op_mul3')       # Salida de la compuerta de salida
    dot.edge('op_tanh_out', 'op_mul3')  # Tanh de la memoria
    
    # Salidas del Estado Oculto
    dot.edge('op_mul3', 'h_curr')
    dot.edge('op_mul3', 'h_curr_top')

    # Renderizado y Visualización
    dot.render('LSTM_Celda_Academica_Figura_2_3', view=True)

if __name__ == "__main__":
    generar_diagrama_lstm_academico()