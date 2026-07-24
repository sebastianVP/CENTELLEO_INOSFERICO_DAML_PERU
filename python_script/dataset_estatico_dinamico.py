import os
from graphviz import Digraph

# 1. Preparación de carpeta
folder_path = 'img'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 2. Configuración del grafo
dot = Digraph('Pipeline_Procesamiento', comment='Pipeline de Datos a Modelo')
dot.attr(rankdir='TB', nodesep='0.5', ranksep='0.6')
dot.attr('node', fontname='Arial', fontsize='10', shape='box', style='filled')

# --- FASE 1: INSTANTE DEL DATASET (PREPARACIÓN) ---
with dot.subgraph(name='cluster_dataset') as c:
    c.attr(label='FASE 1: PREPARACIÓN DEL DATASET (Instante Estático)', 
           style='dotted', fontname='Arial Bold')
    
    c.node('P1', 'cargar_dataset()\n- Conversión Datetime\n- Orden Cronológico', fillcolor='#D6EAF8')
    c.node('P2', 'analizar_eventos_cintilacion()\n- Reporte Mensual\n- Stats de Actividad', fillcolor='#D6EAF8')
    c.node('P3', 'agregar_caracteristicas_temporales()\n- Encoding Cíclico (Sin/Cos)', fillcolor='#AED6F1')
    c.node('P4', 'dividir_estratificado_por_dias()\n- Balanceo de picos\n- Separación Train/Val/Test', fillcolor='#85C1E9')
    
    c.edge('P1', 'P2')
    c.edge('P2', 'P3')
    c.edge('P3', 'P4')

# --- FASE 2: TRABAJO CON EL DATASET (MODELADO) ---
with dot.subgraph(name='cluster_model') as c:
    c.attr(label='FASE 2: TRABAJO CON EL DATASET (Instante Dinámico)', 
           style='dotted', fontname='Arial Bold')
    
    c.node('M1', 'normalizar_sets()\n- MinMaxScaler (Fit en Train)\n- Transform en Val/Test', fillcolor='#D5F5E3')
    c.node('M2', 'construir_modelo_lstm_multistep()\n- Encoder Bidireccional\n- Weighted Focal Loss', fillcolor='#ABEBC6')
    c.node('M3', 'entrenar_modelo_multistep()\n- EarlyStopping\n- ReduceLROnPlateau', fillcolor='#58D68D')
    c.node('M4', 'evaluar_predicciones_multistep()\n- Desnormalización\n- RMSE por Horizonte (t+1..t+10)', fillcolor='#28B463')
    
    c.edge('M1', 'M2')
    c.edge('M2', 'M3')
    c.edge('M3', 'M4')

# Conexión entre fases
dot.edge('P4', 'M1', label='Datasets Listos')

# 3. Renderizado
output_path = os.path.join(folder_path, 'pipeline_detalle_procesamiento')
dot.render(output_path, format='png', cleanup=True)

print(f"✅ Diagrama de pipeline generado en: {output_path}.png")