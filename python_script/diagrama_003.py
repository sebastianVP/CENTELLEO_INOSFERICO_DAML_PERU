import graphviz
import os

# 1. Crear carpeta de salida
output_dir = 'img'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. Configuración del Grafo (Estética del Original con Contenido Completo)
dot = graphviz.Digraph('Diagrama_Tesis_Final_Maestria', comment='Flujo de Desarrollo S4', format='png')
# Se mantiene el ranksep amplio para el flujo general y nodesep del original
dot.attr(rankdir='TB', size='12', nodesep='0.5', ranksep='0.8')
# Letras GRANDES y bordes marcados como en el original
dot.attr('node', fontname='Arial Bold', fontsize='12', style='filled', shape='box', border='1', penwidth='1.5')
dot.attr('edge', penwidth='1.5', arrowsize='1.2')

# --- FASE I: ADQUISICIÓN Y FUENTES (Contenido Original Íntegro) ---
with dot.subgraph(name='cluster_fuentes') as c:
    c.attr(label='Fase I: Adquisicion de Datos (Fuentes Externas)', style='dashed', color='blue', fontname='Arial Bold', fontsize='14')
    c.node('LISN', 'LISN (Parámetro S4)\n8 Estaciones (Jicamarca, Huancayo,\nPiura, Cuzco, Pucallpa, Ayacucho,\nTacna, Iquitos)', shape='cylinder', fillcolor='#E1F5FE')
    c.node('NOAA', 'NOAA GloTEC (TEC)\nParámetros: TEC, ROTEC, ROTI', shape='cylinder', fillcolor='#E1F5FE')
    c.node('NASA', 'NASA OMNIWEB\nVariables: B, SW, Kp, Dst,\nAp, f10.7, AE', shape='cylinder', fillcolor='#E1F5FE')

# --- FASE II: PROCESAMIENTO INICIAL (Contenido Original Íntegro) ---
with dot.subgraph(name='cluster_proc') as c:
    c.attr(label='Fase II: Pre-procesamiento y Limpieza', color='orange', fontname='Arial Bold', fontsize='14')
    c.node('S_S4', 'Scripts Python:\ndescargaDATOSANUAL.py\ndescomprimirDATOS.py\ngenerarDATASET.py', fillcolor='#FFF9C4')
    c.node('S_TEC', 'Notebook:\nTEC_IGP_2025.ipynb', fillcolor='#FFF9C4')
    c.node('S_MAX', 'Notebook:\nS1_{ESTACION}_S4_LSTM.ipynb\n(Extraccion de Maximos Diarios)', fillcolor='#FFF9C4')

# --- FASE III: INTEGRACIÓN (Contenido Original Íntegro) ---
dot.node('INTEG', 'Integracion Multivariable\nS4_MAESTRIA_INTEGRACION_02092025.ipynb\n(Resolucion 1 min)', shape='component', fillcolor='#C8E6C9')
dot.node('CSV', 'Dataset Maestro:\ndf_FINAL_{estacion}.csv', shape='note', fillcolor='#DCEDC8')

# --- FASE IV: INGENIERÍA DE FEATURES Y VENTANEO (NUEVO - COMPACTO) ---
with dot.subgraph(name='cluster_fe') as c:
    c.attr(label='Fase IV: Ingenieria de Features y Ventaneo Temporal', color='purple', style='bold', fontname='Arial Bold', fontsize='14')
    # Ajuste para flechas pequeñas
    c.attr(ranksep='0.3') 
    c.node('F1', '1. Limpieza y Reordenamiento\nIndice temporal y eliminacion\nde columnas auxiliares', fillcolor='#E1BEE7')
    c.node('F2', '2. Division Estratificada\n(umbral_s4=0.6)\nAsegura tormentas en Train, Val y Test', fillcolor='#E1BEE7')
    c.node('F3', '3. Escalado Preservando Indices\nNormalizacion de datos', fillcolor='#E1BEE7')
    c.node('F4', '4. Generador LSTM Multistep\nLookback=60, Horizon=10', shape='component', fillcolor='#CE93D8')
    
    # Conexiones internas cortas
    c.edge('F1', 'F2')
    c.edge('F2', 'F3')
    c.edge('F3', 'F4')

# --- FASE V: MODELADO PREDICTIVO (3 MODELOS - CONTENIDO NUEVO) ---
with dot.subgraph(name='cluster_modelos') as c:
    c.attr(label='Fase V: Modelado Predictivo (Deep Learning)\nN3_S4_MAESTRIA_23122025.ipynb', color='red', style='bold', fontname='Arial Bold', fontsize='14')
    c.node('M1', '1. Arquitectura LSTM Simple\n(Vanilla LSTM)', fillcolor='#FFECB3')
    c.node('M2', '2. Arquitectura LSTM Profunda\n(Stacked LSTM)', fillcolor='#FFE082')
    c.node('M3', '3. Arquitectura LSTM Bidireccional\n(Bi-LSTM)', fillcolor='#FFD54F')

# --- RESULTADO FINAL ---
dot.node('RES', 'Pronostico de Centelleo S4\n(Secuencia de 20 min futuros)', shape='doubleoctagon', fillcolor='#FFCCBC')

# CONEXIONES GENERALES (Igual al flujo original)
dot.edge('LISN', 'S_S4')
dot.edge('S_S4', 'S_MAX')
dot.edge('S_MAX', 'INTEG')
dot.edge('NOAA', 'S_TEC')
dot.edge('S_TEC', 'INTEG')
dot.edge('NASA', 'INTEG')
dot.edge('INTEG', 'CSV')
dot.edge('CSV', 'F1')
dot.edge('F4', 'M1', label=' Tensores X, y')
dot.edge('F4', 'M2')
dot.edge('F4', 'M3')
dot.edge('M1', 'RES')
dot.edge('M2', 'RES')
dot.edge('M3', 'RES')

# Guardar
file_path = os.path.join(output_dir, 'diagrama_tesis_final_maestria_v5')
dot.render(file_path, format='png', cleanup=True)

print(f"Diagrama final generado en: {file_path}.png")
