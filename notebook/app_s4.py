# =============================================================================
# APP STREAMLIT - PRONÓSTICO DE CENTELLEO IONOSFÉRICO S4
# =============================================================================

import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow.keras.models import load_model
from sklearn.metrics import mean_squared_error, mean_absolute_error

# =============================================================================
# 1. CONFIGURACIÓN GLOBAL
# =============================================================================

st.set_page_config(page_title="Pronóstico de Centelleo S4", page_icon="📡", layout="wide")

MODEL_PATH = "modelo_lstm_experimento_S4_1808.keras"
SCALER_PATH = "SCALER_S4.pkl"

LOOKBACK = 70
HORIZON = 10
SAMPLING_MINUTES = 1

TARGET_COLUMN = "S4"
THRESHOLD = 0.6

ALPHA = 1.5
BETA = 10.0
UNDERESTIMATION_PENALTY = 2.0

# =============================================================================
# FEATURES UTILIZADAS POR EL MODELO
# =============================================================================

FEATURES_COLS = ["TEC","ROTEC","ROTI","Kp_Index","Dst_Index","AE_Index","f10.7_Index","daily_sin","daily_cos","day_of_year_sin","day_of_year_cos","S4"]

# =============================================================================
# COLUMNAS ORIGINALES ESPERADAS EN EL DATASET
# =============================================================================

REQUIRED_COLUMNS = ["Tiempo","ID_Satelite","Azimuth","Elevacion","Estacion","TEC","ROTEC","ROTI","Kp_Index","Dst_Index","AE_Index","f10.7_Index","S4"]

# =============================================================================
# 2. FUNCIÓN DE PÉRDIDA PERSONALIZADA
# =============================================================================

def focal_mse_s4(threshold_norm, alpha=1.5, beta=10.0, underestimation_penalty=2.0):

    def loss(y_true, y_pred):

        error = y_pred - y_true
        abs_error = tf.abs(error)
        squared_error = tf.square(error)

        event_mask = tf.cast(y_true >= threshold_norm, tf.float32)
        event_weights = 1.0 + event_mask * (beta - 1.0)

        focal_weights = tf.pow(abs_error + 1e-7, alpha)

        underestimation_mask = tf.cast(
            tf.logical_and(y_true >= threshold_norm, y_pred < y_true),
            tf.float32
        )

        underestimation_weights = 1.0 + underestimation_mask * (underestimation_penalty - 1.0)

        total_loss = squared_error * event_weights * focal_weights * underestimation_weights

        return tf.reduce_mean(total_loss)

    return loss

# =============================================================================
# 3. CARGA EN CACHE DE MODELO Y SCALER
# =============================================================================

@st.cache_resource
def load_model_and_scaler():

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"No se encontró el modelo: {MODEL_PATH}")

    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(f"No se encontró el scaler: {SCALER_PATH}")

    scaler = joblib.load(SCALER_PATH)

    model = load_model(MODEL_PATH, compile=False)

    return model, scaler


# =============================================================================
# 4. FEATURES TEMPORALES
# =============================================================================

def add_temporal_features(df):

    out = df.copy()
    idx = pd.DatetimeIndex(out.index)

    minute_of_day = idx.hour * 60 + idx.minute
    daily_period = 24 * 60

    out["daily_sin"] = np.sin(2 * np.pi * minute_of_day / daily_period)
    out["daily_cos"] = np.cos(2 * np.pi * minute_of_day / daily_period)

    day_of_year = idx.dayofyear
    days_in_year = np.where(idx.is_leap_year, 366, 365)

    out["day_of_year_sin"] = np.sin(2 * np.pi * (day_of_year - 1) / days_in_year)
    out["day_of_year_cos"] = np.cos(2 * np.pi * (day_of_year - 1) / days_in_year)

    return out


# =============================================================================
# 5. VALIDACIÓN DEL DATASET
# =============================================================================

def validate_dataset(df):

    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing_columns:
        return False, f"Faltan columnas: {', '.join(missing_columns)}"

    if len(df) < LOOKBACK:
        return False, f"El dataset debe contener al menos {LOOKBACK} observaciones."

    return True, "Dataset válido."

# =============================================================================
# 6. PREPARACIÓN DEL DATASET
# =============================================================================

def prepare_input_data(df):

    df = df.copy()

    df["Tiempo"] = pd.to_datetime(df["Tiempo"], errors="coerce")

    if df["Tiempo"].isna().any():
        raise ValueError("Existen valores inválidos en la columna Tiempo.")

    df = df.sort_values("Tiempo")
    df = df.set_index("Tiempo")

    if df.index.has_duplicates:
        df = df[~df.index.duplicated(keep="last")]

    df = add_temporal_features(df)

    return df

# =============================================================================
# 7. VALIDACIÓN DE CONTINUIDAD TEMPORAL
# =============================================================================

def validate_temporal_continuity(df):

    differences = df.index.to_series().diff()
    expected_interval = pd.Timedelta(minutes=SAMPLING_MINUTES)

    gaps = differences[differences != expected_interval].dropna()

    return gaps


# =============================================================================
# 8. ESCALAMIENTO
# =============================================================================

def scale_input_data(df, scaler):

    values = df[FEATURES_COLS].astype(float)

    scaled_values = scaler.transform(values)

    scaled_df = pd.DataFrame(
        scaled_values,
        index=df.index,
        columns=FEATURES_COLS
    )

    return scaled_df


# =============================================================================
# 9. DESNORMALIZACIÓN DE S4
# =============================================================================

def desnormalize_s4(values_scaled, scaler):

    idx_s4 = FEATURES_COLS.index("S4")

    min_s4 = scaler.data_min_[idx_s4]
    max_s4 = scaler.data_max_[idx_s4]

    return values_scaled * (max_s4 - min_s4) + min_s4


# =============================================================================
# 10. CREACIÓN DE VENTANA LSTM
# =============================================================================

def create_prediction_window(scaled_df):

    if len(scaled_df) < LOOKBACK:
        raise ValueError(f"Se necesitan al menos {LOOKBACK} observaciones.")

    last_window = scaled_df[FEATURES_COLS].iloc[-LOOKBACK:].to_numpy(dtype=np.float32)

    X = np.expand_dims(last_window, axis=0)

    return X


# =============================================================================
# 11. PREDICCIÓN
# =============================================================================

def predict_s4(model, scaler, X):

    prediction_scaled = model.predict(X, verbose=0)

    prediction_real = desnormalize_s4(prediction_scaled, scaler)

    return np.asarray(prediction_real).reshape(-1)


# =============================================================================
# 12. CREAR RESULTADOS DEL PRONÓSTICO
# =============================================================================

def create_prediction_results(prediction, last_timestamp):

    future_times = pd.date_range(
        start=last_timestamp + pd.Timedelta(minutes=SAMPLING_MINUTES),
        periods=HORIZON,
        freq=f"{SAMPLING_MINUTES}min"
    )

    results = pd.DataFrame({
        "Tiempo": future_times,
        "S4_Predicho": prediction,
        "Evento": np.where(prediction >= THRESHOLD, "SI", "NO")
    })

    return results

# =============================================================================
# 13. PRUEBA: 70 MINUTOS INPUT + 10 MINUTOS REALES
# =============================================================================

def create_test_prediction(df, model, scaler):

    required_rows = LOOKBACK + HORIZON

    if len(df) < required_rows:
        raise ValueError(f"Para esta prueba se necesitan al menos {required_rows} observaciones.")

    test_df = df.iloc[:required_rows].copy()

    scaled_df = scale_input_data(test_df, scaler)

    input_scaled = scaled_df[FEATURES_COLS].iloc[:LOOKBACK].to_numpy(dtype=np.float32)

    X = np.expand_dims(input_scaled, axis=0)

    prediction_scaled = model.predict(X, verbose=0)

    prediction_real = desnormalize_s4(prediction_scaled, scaler).reshape(-1)

    real_values = test_df["S4"].iloc[LOOKBACK:LOOKBACK + HORIZON].to_numpy(dtype=float)

    prediction_times = test_df.index[LOOKBACK:LOOKBACK + HORIZON]

    rmse = np.sqrt(mean_squared_error(real_values, prediction_real))
    mae = mean_absolute_error(real_values, prediction_real)

    comparison = pd.DataFrame({
        "Tiempo": prediction_times,
        "S4_Real": real_values,
        "S4_Predicho": prediction_real,
        "Error": prediction_real - real_values,
        "Evento_Real": np.where(real_values >= THRESHOLD, "SI", "NO"),
        "Evento_Predicho": np.where(prediction_real >= THRESHOLD, "SI", "NO")
    })

    return test_df, prediction_times, prediction_real, real_values, comparison, rmse, mae

# =============================================================================
# 14. GRÁFICO DE VALIDACIÓN
# =============================================================================

def plot_validation(test_df, prediction_times, prediction_real):
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(test_df.index, test_df["S4"], linewidth=2, label="S4 Real")
    ax.plot(prediction_times, prediction_real, linewidth=3, linestyle="--", label="S4 Predicho")
    ax.axhline(THRESHOLD, linestyle=":", linewidth=2, label=f"Umbral S4 = {THRESHOLD}")

    boundary_time = test_df.index[LOOKBACK - 1]
    ax.axvline(boundary_time, linestyle="--", linewidth=1.5, label="Fin entrada LSTM")

    ax.set_title("S4 Real vs Predicción LSTM")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("S4")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()
    return fig


# =============================================================================
# 15. INTERFAZ DE USUARIO
# =============================================================================

st.title("📡 Pronóstico de Centelleo Ionosférico S4")

st.markdown("""
### Modelo LSTM Multistep

El sistema utiliza **70 minutos de información histórica** para
pronosticar los siguientes **10 minutos de S4**.
""")


# =============================================================================
# SIDEBAR - CONFIGURACIÓN
# =============================================================================

with st.sidebar:
    st.header("Configuración global")

    st.write(f"**Lookback:** {LOOKBACK} minutos")
    st.write(f"**Horizonte:** {HORIZON} minutos")
    st.write(f"**Frecuencia:** {SAMPLING_MINUTES} minuto")
    st.write(f"**Umbral S4:** {THRESHOLD}")
    st.write("**LSTM:** 64 unidades")

    st.divider()
    st.write("**Variables utilizadas:**")

    for feature in FEATURES_COLS:
        st.write(f"- {feature}")


# =============================================================================
# CARGA DE MODELO
# =============================================================================

try:
    model, scaler = load_model_and_scaler()
    st.success("Modelo y scaler cargados correctamente.")
except Exception as e:
    st.error(f"Error cargando modelo/scaler: {e}")
    st.stop()


# =============================================================================
# INFORMACIÓN DEL MODELO
# =============================================================================

with st.expander("Información del modelo"):
    st.write(f"**Modelo:** {MODEL_PATH}")
    st.write(f"**Scaler:** {SCALER_PATH}")
    st.write(f"**Lookback:** {LOOKBACK}")
    st.write(f"**Horizonte:** {HORIZON}")
    st.write(f"**Features:** {len(FEATURES_COLS)}")
    st.write(f"**Target:** {TARGET_COLUMN}")
    st.write(f"**Umbral:** {THRESHOLD}")
    st.write(f"**Alpha:** {ALPHA}")
    st.write(f"**Beta:** {BETA}")
    st.write(f"**Penalización subestimación:** {UNDERESTIMATION_PENALTY}")


# =============================================================================
# CARGA DEL DATASET
# =============================================================================

st.header("1. Cargar dataset")
uploaded_file = st.file_uploader("Seleccione un archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # ---------------------------------------------------------------------
        # LEER DATASET
        # ---------------------------------------------------------------------
        df_raw = pd.read_csv(uploaded_file)
        st.subheader("Vista previa del dataset")
        st.dataframe(df_raw.head(10), use_container_width=True)
        
        # ---------------------------------------------------------------------
        # VALIDACIÓN
        # ---------------------------------------------------------------------
        valid, message = validate_dataset(df_raw)
        if not valid:
            st.error(message)
            st.stop()
        st.success(message)

        # ---------------------------------------------------------------------
        # PREPARAR DATASET
        # ---------------------------------------------------------------------
        df = prepare_input_data(df_raw)
        st.write(f"**Observaciones disponibles:** {len(df):,}")
        st.write(f"**Inicio:** {df.index.min()}")
        st.write(f"**Fin:** {df.index.max()}")

        # ---------------------------------------------------------------------
        # CONTINUIDAD TEMPORAL
        # ---------------------------------------------------------------------
        gaps = validate_temporal_continuity(df)
        if len(gaps) > 0:
            st.warning(f"Se detectaron {len(gaps)} intervalos temporales no consecutivos.")
            st.dataframe(gaps.head(10))
        else:
            st.success("La serie temporal tiene una cadencia continua de 1 minuto.")

        # =========================================================================
        # 16. MODO DE OPERACIÓN
        # =========================================================================
        st.header("2. Modo de operación")
        mode = st.radio("Seleccione una opción:", ["Pronóstico", "Prueba: 70 + 10 minutos"], horizontal=True)

        # =========================================================================
        # MODO 1: PRONÓSTICO
        # =========================================================================
        if mode == "Pronóstico":
            st.subheader("Pronóstico de los próximos 10 minutos")

            if len(df) < LOOKBACK:
                st.warning(f"Se necesitan al menos {LOOKBACK} observaciones.")
                st.stop()

            if st.button("🚀 Generar pronóstico", type="primary"):
                # -------------------------------------------------------------
                # ESCALAMIENTO Y VENTANA
                # -------------------------------------------------------------
                scaled_df = scale_input_data(df, scaler)
                X = create_prediction_window(scaled_df)
                st.info(f"Entrada LSTM: {X.shape}")

                # -------------------------------------------------------------
                # PREDICCIÓN
                # -------------------------------------------------------------
                prediction = predict_s4(model, scaler, X)
                last_timestamp = df.index[-1]
                results = create_prediction_results(prediction, last_timestamp)

                # -------------------------------------------------------------
                # RESULTADOS
                # -------------------------------------------------------------
                st.subheader("Pronóstico")
                st.dataframe(results, use_container_width=True)

                # -------------------------------------------------------------
                # MÉTRICAS
                # -------------------------------------------------------------
                max_s4 = results["S4_Predicho"].max()
                event_count = results["Evento"].eq("SI").sum()

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("S4 máximo", f"{max_s4:.4f}")
                with col2:
                    st.metric("Umbral", f"{THRESHOLD:.2f}")
                with col3:
                    st.metric("Eventos pronosticados", int(event_count))

                # -------------------------------------------------------------
                # GRÁFICO Y ESTADO
                # -------------------------------------------------------------
                st.subheader("Pronóstico temporal")
                chart_df = results.set_index("Tiempo")[["S4_Predicho"]]
                st.line_chart(chart_df)

                if event_count > 0:
                    st.warning("⚠️ Se pronostican valores de S4 por encima del umbral.")
                else:
                    st.success("✓ No se pronostican eventos por encima del umbral.")

        # =========================================================================
        # MODO 2: PRUEBA 70 + 10
        # =========================================================================
        else:
            st.subheader("Validación: 70 minutos de entrada + 10 minutos de predicción")
            st.markdown("""
            En esta prueba:
            **Primeros 70 minutos → entrada del LSTM**
            **Siguientes 10 minutos → comparación Real vs Predicción**
            """)

            required_rows = LOOKBACK + HORIZON
            if len(df) < required_rows:
                st.warning(f"Esta prueba necesita al menos {required_rows} observaciones.")
                st.stop()

            st.info(f"El dataset contiene {len(df)} observaciones. Se utilizarán las primeras {required_rows} para la prueba.")

            if st.button("🔬 Ejecutar prueba 70 + 10", type="primary"):
                (
                    test_df, prediction_times, prediction_real,
                    real_values, comparison, rmse_test, mae_test
                ) = create_test_prediction(df, model, scaler)

                # -------------------------------------------------------------
                # MÉTRICAS
                # -------------------------------------------------------------
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("RMSE +10 min", f"{rmse_test:.4f}")
                with col2:
                    st.metric("MAE +10 min", f"{mae_test:.4f}")
                with col3:
                    st.metric("Observaciones evaluadas", HORIZON)

                # -------------------------------------------------------------
                # TABLA Y GRÁFICO
                # -------------------------------------------------------------
                st.subheader("Comparación Real vs Predicción")
                st.dataframe(comparison, use_container_width=True)

                st.subheader("Visualización: 70 minutos + 10 minutos")
                fig = plot_validation(test_df, prediction_times, prediction_real)
                st.pyplot(fig)

                # -------------------------------------------------------------
                # INTERPRETACIÓN Y EVENTOS
                # -------------------------------------------------------------
                st.subheader("Interpretación")
                st.write(
                    f"El modelo recibió los primeros **{LOOKBACK} minutos** como entrada y "
                    f"generó un pronóstico de los siguientes **{HORIZON} minutos**.\n\n"
                    f"El RMSE obtenido para estos 10 minutos fue **{rmse_test:.4f}** y el MAE fue **{mae_test:.4f}**."
                )

                real_events = int(np.sum(real_values >= THRESHOLD))
                predicted_events = int(np.sum(prediction_real >= THRESHOLD))

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Eventos reales", real_events)
                with col2:
                    st.metric("Eventos predichos", predicted_events)

    except Exception as e:
        st.error(f"Error procesando el dataset: {e}")

# =============================================================================
# PIE DE APLICACIÓN
# =============================================================================
st.divider()
st.caption("Sistema experimental de pronóstico de centelleo ionosférico S4 mediante LSTM.")