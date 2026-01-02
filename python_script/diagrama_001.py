import graphviz
import os

# 1. Crear carpeta de salida
output_dir = 'img'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. Configuración del Grafo
dot = graphviz.Digraph('Diagrama_Tesis_Final', comment='Flujo de Desarrollo S4', format='png')
dot.attr(rankdir='TB', size='12', nodesep='0.5', ranksep='0.8')
dot.attr('node', fontname='Arial', fontsize='10', style='filled', shape='box', border='1')

# --- FASE I: ADQUISICIÓN Y FUENTES ---
with dot.subgraph(name='cluster_fuentes') as c:
    c.attr(label='Fase I: Adquisicion de Datos (Fuentes Externas)', style='dashed', color='blue')
    c.node('LISN', 'LISN (Parámetro S4)\n8 Estaciones (Jicamarca, Huancayo,\nPiura, Cuzco, Pucallpa, Ayacucho,\nTacna, Iquitos)', shape='cylinder', fillcolor='#E1F5FE')
    c.node('NOAA', 'NOAA GloTEC (TEC)\nParámetros: TEC, ROTEC, ROTI', shape='cylinder', fillcolor='#E1F5FE')
    c.node('NASA', 'NASA OMNIWEB\nVariables: B, SW, Kp, Dst,\nAp, f10.7, AE', shape='cylinder', fillcolor='#E1F5FE')

# --- FASE II: PROCESAMIENTO INICIAL ---
with dot.subgraph(name='cluster_proc') as c:
    c.attr(label='Fase II: Pre-procesamiento y Limpieza', color='orange')
    c.node('S_S4', 'Scripts Python:\ndescargaDATOSANUAL.py\ndescomprimirDATOS.py\ngenerarDATASET.py', fillcolor='#FFF9C4')
    c.node('S_TEC', 'Notebook:\nTEC_IGP_2025.ipynb', fillcolor='#FFF9C4')
    c.node('S_MAX', 'Notebook:\nS1_{ESTACION}_S4_LSTM.ipynb\n(Extraccion de Maximos Diarios)', fillcolor='#FFF9C4')

# --- FASE III: INTEGRACIÓN (PUNTO CRÍTICO) ---
dot.node('INTEG', 'Integracion Multivariable\nS4_MAESTRIA_INTEGRACION_02092025.ipynb\n(Resolucion 1 min)', shape='component', fillcolor='#C8E6C9')
dot.node('CSV', 'Dataset Maestro:\ndf_FINAL_{estacion}.csv', shape='note', fillcolor='#DCEDC8')

# --- FASE IV: MODELADO PREDICTIVO (3 MODELOS) ---
with dot.subgraph(name='cluster_modelos') as c:
    c.attr(label='Fase IV: Modelado Predictivo (Deep Learning)\nN3_S4_MAESTRIA_23122025.ipynb', color='red', style='bold')
    c.node('M1', '1. Arquitectura LSTM Simple\n(Vanilla LSTM)', fillcolor='#FFECB3')
    c.node('M2', '2. Arquitectura LSTM Profunda\n(Stacked LSTM)', fillcolor='#FFE082')
    c.node('M3', '3. Arquitectura LSTM Bidireccional\n(Bi-LSTM)', fillcolor='#FFD54F')

# --- RESULTADO FINAL ---
dot.node('RES', 'Pronostico de Centelleo S4\ny Mitigacion de Perturbaciones', shape='doubleoctagon', fillcolor='#FFCCBC')

# CONEXIONES
dot.edge('LISN', 'S_S4')
dot.edge('S_S4', 'S_MAX')
dot.edge('S_MAX', 'INTEG')
dot.edge('NOAA', 'S_TEC')
dot.edge('S_TEC', 'INTEG')
dot.edge('NASA', 'INTEG')
dot.edge('INTEG', 'CSV')
dot.edge('CSV', 'M1')
dot.edge('CSV', 'M2')
dot.edge('CSV', 'M3')
dot.edge('M1', 'RES')
dot.edge('M2', 'RES')
dot.edge('M3', 'RES')

# Guardar
file_path = os.path.join(output_dir, 'diagrama_tesis_maestria_v2')
dot.render(file_path, format='png', cleanup=True)

print(f"Diagrama generado en: {file_path}.png")
