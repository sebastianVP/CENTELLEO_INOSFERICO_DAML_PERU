
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os,gc
import tensorflow as tf # Solo si necesitas verificar GPU aquí
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Importaciones específicas de Keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Input, Bidirectional, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# Intentar importar seaborn para un mejor heatmap, si no, usamos matplotlib plano
try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False

# =============================================================================
# 1. CONFIGURACIÓN Y CONSTANTES
# =============================================================================
N_ESTACION  = 0  # 0: JICAMARCA
ESTACION    = ["JICAMARCA","HUANCAYO","PIURA","CUZCO","PUCALLPA","AYACUCHO","TACNA","IQUITOS"]

# Ajusta tu ruta según corresponda
RUTA        = "/home/soporte/Documents/CENTELLEO_INOSFERICO_DAML_PERU/notebook"
ARCHIVO     = f"df_FINAL_{ESTACION[N_ESTACION]}.csv"
# update
ARCHIVO     = "/home/soporte/Documents/pipelines_cip/INTEGRACION/integrated_dataset/dataset_integrado_jic.csv"


# Definición de Features (El orden importa para la red neuronal)
# Asegúrate de que 'S4' esté aquí si quieres usarlo como input también (autoregresivo)
FEATURES_COLS = [
    'S4', 'TEC', 'ROTI', 'Kp_Index', 'Dst_Index', 'AE_Index', 'f10.7_Index',
    'Hora_Sin', 'Hora_Cos'
]

print("="*60)
print(f"📍 ESTACIÓN: {ESTACION[N_ESTACION]}")
print(f"📂 RUTA: {RUTA}")
print(f"📄 ARCHIVO: {ARCHIVO}")
print("="*60)

# =============================================================================
# 2. FUNCIONES DE CARGA Y ANÁLISIS
# =============================================================================
def cargar_dataset(path, filename):
    """
    Carga el CSV y realiza la conversión inicial de fechas.
    """
    full_path = os.path.join(path, filename)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"No se encontró el archivo en: {full_path}")

    print(f"📂 Cargando archivo: {filename}...")
    df = pd.read_csv(full_path)

    # Conversión única y definitiva a datetime
    df["Tiempo"] = pd.to_datetime(df["Tiempo"])

    # Ordenar cronológicamente (vital para series temporales)
    df = df.sort_values("Tiempo")

    print(f"✅ Dataset cargado. Shape: {df.shape}")
    print(f"   Rango de fechas: {df['Tiempo'].min()} a {df['Tiempo'].max()}")
    return df

def analizar_eventos_cintilacion(df, umbral_s4=0.6, plot=True):
    """
    Analiza y visualiza los días con presencia de cintilación.
    No modifica el DF original permanentemente, solo reporta estadísticas.
    """
    print("\n🔍 Analizando distribución de eventos...")

    # Trabajamos con una copia ligera para no alterar el original
    df_analisis = df[["Tiempo", "S4"]].copy()
    df_analisis["Fecha"] = df_analisis["Tiempo"].dt.date

    # 1. Identificar si cada día superó el umbral
    resumen_diario = df_analisis.groupby("Fecha")["S4"].max() > umbral_s4
    resumen_diario = resumen_diario.reset_index()
    resumen_diario.columns = ["Fecha", "Evento_Cintilacion"] # True/False

    total_dias = resumen_diario["Fecha"].nunique()
    dias_con_evento = resumen_diario["Evento_Cintilacion"].sum()

    print(f"   Total de días registrados: {total_dias}")
    print(f"   Días con eventos (S4 > {umbral_s4}): {dias_con_evento}")
    print(f"   Porcentaje de actividad: {(dias_con_evento/total_dias)*100:.2f}%")

    # 2. Reporte Mensual
    df_analisis["Mes"] = df_analisis["Tiempo"].dt.to_period("M")

    # Unimos para saber qué día tuvo evento
    # Primero agrupamos por día para saber si ESE día hubo evento
    max_s4_dia = df_analisis.groupby(["Mes", "Fecha"])["S4"].max().reset_index()
    max_s4_dia["Tuvo_Evento"] = (max_s4_dia["S4"] > umbral_s4).astype(int)

    # Tabla resumen
    tabla_mensual = max_s4_dia.groupby("Mes")["Tuvo_Evento"].agg(
        Dias_Con_Cintilacion='sum',
        Total_Dias='count'
    )
    tabla_mensual["Dias_Sin_Cintilacion"] = tabla_mensual["Total_Dias"] - tabla_mensual["Dias_Con_Cintilacion"]

    print("\n📊 Resumen Mensual de Actividad:")
    print(tabla_mensual)

    # 3. Visualización (Opcional)
    if plot:
        plt.figure(figsize=(12, 5))
        # Convertimos a string para que matplotlib no haga lío con fechas
        fechas_str = resumen_diario["Fecha"].astype(str)
        valores = resumen_diario["Evento_Cintilacion"].astype(int)

        plt.bar(fechas_str, valores, color=np.where(valores==1, 'orange', 'skyblue'))
        plt.title(f"Días con Cintilación (S4 > {umbral_s4})")
        plt.ylabel("Presencia (1=Sí, 0=No)")
        plt.xticks(rotation=90, fontsize=8)

        # Mostrar solo una etiqueta cada 7 días para no saturar
        ax = plt.gca()
        for index, label in enumerate(ax.xaxis.get_ticklabels()):
            if index % 7 != 0:
                label.set_visible(False)

        plt.tight_layout()
        plt.show()

# =============================================================================
# 3. INGENIERÍA DE CARACTERÍSTICAS
# =============================================================================
def agregar_caracteristicas_temporales(df):
    """Agrega transformaciones cíclicas (Sin/Cos) de la hora."""
    print("\n⚙️ Generando características temporales...")
    minutos_dia = df["Tiempo"].dt.hour * 60 + df["Tiempo"].dt.minute
    periodo = 24 * 60 

    df["Hora_Sin"] = np.sin(2 * np.pi * minutos_dia / periodo)
    df["Hora_Cos"] = np.cos(2 * np.pi * minutos_dia / periodo)
    return df

# =============================================================================
# 3.5. DIVISIÓN ESTRATIFICADA (CORE)
# =============================================================================
def finalizar_estructura_df(df, target_col="S4"):
    """
    Limpia columnas auxiliares, reordena y establece el índice temporal.
    Esta función deja el DF listo para entrar al Generador de Ventanas.
    """
    print("\n🧹 Finalizando estructura del DataFrame...")

    # 1. Asegurar índice temporal
    if df.index.name != 'Tiempo':
        df = df.set_index('Tiempo')

    df = df.sort_index()

    # 2. Reordenar columnas: Target al final (práctica estándar)
    cols = [c for c in df.columns if c != target_col]
    cols.append(target_col)
    df = df[cols]

    # 3. Eliminar columnas que ya no sirven para el modelo numérico
    # (Ej: Fechas string, columnas categóricas, etc.)
    cols_a_borrar = ["dias", "Fecha", "Mes", "minuto_del_dia", "Cintilacion"]
    # Borramos solo si existen
    cols_existentes = [c for c in cols_a_borrar if c in df.columns]

    if cols_existentes:
        df = df.drop(columns=cols_existentes)
        print(f"   Columnas eliminadas: {cols_existentes}")

    print(f"✅ DataFrame Final Listo. Shape: {df.shape}")
    print(f"   Columnas finales: {df.columns.tolist()}")

    return df

# =============================================================================
# 4. DIVISIÓN ESTRATIFICADA (CORE)
# =============================================================================

def dividir_estratificado_por_dias(df, umbral_s4=0.6):
    """
    Divide el dataset asegurando que haya días con tormentas en Train, Val y Test.
    Mantiene la integridad interna de cada día completo.
    """
    print("\n✂️ Ejecutando división estratificada de datos...")

    # Recuperamos la fecha del índice de forma segura
    fechas_unicas = np.unique(df.index.date)
    
    # Crear un DataFrame temporal de mapeo diario para calcular máximos de S4
    temp_diario = pd.DataFrame(index=df.index)
    temp_diario['Fecha'] = df.index.date
    temp_diario['S4'] = df['S4'].values
    
    resumen_diario = temp_diario.groupby('Fecha')['S4'].max().reset_index()

    # Identificar Días Activos vs Días Quietos
    dias_activos = resumen_diario[resumen_diario['S4'] > umbral_s4]['Fecha'].values
    dias_quietos = resumen_diario[resumen_diario['S4'] <= umbral_s4]['Fecha'].values
    
    print("-------- Distribución Original de Días ------------")
    print(f"   Total Días Activos encontrados: {len(dias_activos)}")
    print(f"   Total Días Quietos encontrados: {len(dias_quietos)}")

    # Opcional: Si deseas aplicar el submuestreo de días quietos que tenías comentado:
    # dias_quietos = dias_quietos[:len(dias_activos)]

    # 2. Repartir los Días ACTIVOS (70% Train, 15% Val, 15% Test)
    activos_train, activos_temp = train_test_split(dias_activos, test_size=0.3, random_state=42)
    activos_val, activos_test = train_test_split(activos_temp, test_size=0.5, random_state=42)

    # 3. Repartir los Días QUIETOS
    quietos_train, quietos_temp = train_test_split(dias_quietos, test_size=0.3, random_state=42)
    quietos_val, quietos_test = train_test_split(quietos_temp, test_size=0.5, random_state=42)

    # 4. Combinar las listas por conjunto
    lista_dias_train = np.concatenate([activos_train, quietos_train])
    lista_dias_val = np.concatenate([activos_val, quietos_val])
    lista_dias_test = np.concatenate([activos_test, quietos_test])

    # 5. Crear los DataFrames Finales filtrando por el objeto fecha del índice
    train = df[df.index.date.astype(object) == pd.Series(df.index.date).isin(lista_dias_train).values] # Filtrado eficiente
    
    # Método alternativo ultra-seguro usando máscaras booleanas basadas en el índice
    df_dates = pd.Series(df.index.date)
    train = df[df_dates.isin(lista_dias_train).values].sort_index()
    val = df[df_dates.isin(lista_dias_val).values].sort_index()
    test = df[df_dates.isin(lista_dias_test).values].sort_index()

    return train, val, test

def auditar_division_datos(df, nombre_set, umbral_s4=0.6):
    """
    Función auxiliar para verificar que cada set tenga eventos.
    """
    if df.empty:
        print(f"⚠️ PELIGRO: El set {nombre_set} está completamente vacío.")
        return

    fechas = df.index.date
    s4_values = df['S4'].values
    df_temp = pd.DataFrame({'Fecha': fechas, 'S4': s4_values})

    dias_totales = df_temp['Fecha'].nunique()
    dias_con_evento = df_temp[df_temp['S4'] > umbral_s4]['Fecha'].nunique()

    porcentaje = (dias_con_evento / dias_totales) * 100 if dias_totales > 0 else 0

    print(f"--- AUDITORÍA: {nombre_set.upper()} ---")
    print(f"📅 Días totales: {dias_totales} | ⚡ Con Cintilación: {dias_con_evento}")
    print(f"📊 Porcentaje actividad: {porcentaje:.2f}%")
    print("✅ Set válido." if dias_con_evento > 0 else f"⚠️ PELIGRO: {nombre_set} NO tiene eventos.")
    print("-" * 40)
# =============================================================================
# 5. NORMALIZACIÓN
# =============================================================================
def escalar_preservando_indices(df_subset, scaler, cols, is_train=False):
    """
    Normaliza un DataFrame pero devuelve otro DataFrame con el mismo índice temporal.
    """
    if df_subset.empty:
        return df_subset

    # IMPORTANTE: Solo 'aprendemos' (fit) los máximos y mínimos con el set de TRAIN
    if is_train:
        scaler.fit(df_subset[cols])

    # Transformamos los datos (Matriz numpy)
    scaled_values = scaler.transform(df_subset[cols])

    # Reconstruimos el DataFrame pegándole el índice original
    df_scaled = pd.DataFrame(
        scaled_values,
        columns=cols,
        index=df_subset.index
    )

    # Añadimos la columna 'Fecha' para referencia (útil para depuración)
    # Si la columna no existe en el subset, la extraemos del índice
    if 'Fecha' in df_subset.columns:
        df_scaled['Fecha'] = df_subset['Fecha'].values
    else:
        df_scaled['Fecha'] = df_subset.index.date

    return df_scaled

def normalizar_sets(train_df, val_df, test_df, features_cols):
    """
    Aplica la normalización a los tres conjuntos de datos usando MinMaxScaler.
    """
    print("\n⚖️ Ejecutando Normalización (MinMaxScaler 0-1)...")

    # Inicializamos el escalador
    scaler = MinMaxScaler(feature_range=(0, 1))

    # 1. Normalizamos TRAIN (Aquí aprende el scaler)
    print("   -> Normalizando Train (Fit & Transform)")
    train_scaled = escalar_preservando_indices(train_df, scaler, features_cols, is_train=True)

    # 2. Normalizamos VAL y TEST (Usando lo aprendido en Train)
    print("   -> Normalizando Val (Transform only)")
    val_scaled = escalar_preservando_indices(val_df, scaler, features_cols, is_train=False)

    print("   -> Normalizando Test (Transform only)")
    test_scaled = escalar_preservando_indices(test_df, scaler, features_cols, is_train=False)

    # Verificación
    s4_min_orig = train_df['S4'].min()
    s4_max_orig = train_df['S4'].max()
    s4_min_scal = train_scaled['S4'].min()
    s4_max_scal = train_scaled['S4'].max()

    print(f"   ✅ Normalización completada.")
    print(f"   Rango S4 Original (Train): {s4_min_orig:.4f} a {s4_max_orig:.4f}")
    print(f"   Rango S4 Escalado (Train): {s4_min_scal:.4f} a {s4_max_scal:.4f}")

    return train_scaled, val_scaled, test_scaled, scaler
# =============================================================================
# 6. EJECUCIÓN DEL PIPELINE (MAIN)
# =============================================================================
if __name__ == "__main__":
    
    # 1. Cargar
    df_raw = cargar_dataset(RUTA, ARCHIVO)
    
    # 2. Análisis preliminar
    analizar_eventos_cintilacion(df_raw)
    
    # 3. Ingeniería de Features
    df_feat = agregar_caracteristicas_temporales(df_raw)
    
    # 4. Limpieza Estructural
    df_final = finalizar_estructura_df(df_feat)
    
    # 5. División Estratificada
    train_df, val_df, test_df = dividir_estratificado_por_dias(df_final)
    
    # Auditoría
    print("\n--- AUDITORÍA DE SETS ---")
    auditar_division_datos(train_df, "TRAIN")
    auditar_division_datos(val_df, "VAL")
    auditar_division_datos(test_df, "TEST")
    
    # 6. Normalización Final
    # Solo pasamos las columnas que vamos a usar en el modelo
    train_scaled, val_scaled, test_scaled, scaler = normalizar_sets(
        train_df, val_df, test_df, FEATURES_COLS
    )

    print("\n✅ PREPROCESAMIENTO FINALIZADO CON ÉXITO.")
    print("   Variables listas: train_scaled, val_scaled, test_scaled, scaler")
    print(f"   Features activas: {train_scaled.columns.tolist()[:-1]}") # -1 para excluir 'Fecha'