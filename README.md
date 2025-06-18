# 🌌 Centelleo Ionosférico -PERU

Detección y Análisis usando Machine Learning(DAML)
Este repositorio contiene el desarrollo de un sistema para la **detección, caracterización y pronóstico del centelleo ionosférico** utilizando técnicas de **procesamiento de señales, machine learning y análisis de datos satelitales**. El proyecto está enfocado en mejorar la comprensión y mitigación de los efectos del centelleo sobre las señales GNSS (como GPS), especialmente en regiones ecuatoriales como Perú.

## 🎯 Objetivo General

Desarrollar herramientas computacionales que permitan:
- Detectar eventos de centelleo ionosférico en datos reales.
- Caracterizar su intensidad y duración.
- Realizar pronósticos a corto plazo utilizando modelos predictivos.

## 📦 Contenido del Repositorio

```
centelleo-ionosferico/
│
├── data/                 # Scripts y enlaces para acceso a datos (GNSS, TEC, S4)
├── preprocessing/        # Funciones para limpieza, normalización y extracción de features
├── models/               # Entrenamiento y evaluación de modelos ML (clasificación/regresión)
├── notebooks/            # Exploración de datos, visualizaciones y pruebas interactivas
├── src/                  # Módulos principales del sistema
├── plots/                # Gráficos de resultados y mapas
├── README.md             # Descripción general del proyecto
└── requirements.txt      # Librerías necesarias
└── bitacora              # Notas y apuntes de las tareas
```

## 📊 Tecnologías y Herramientas

- 🛰️ **Datos**: GNSS S4 Index, TEC maps, datos ionosféricos locales (IGP, LISN)
- 🧠 **Modelos**: Random Forest, XGBoost, LSTM, SVM
- 📈 **Análisis**: Python (NumPy, Pandas, Scikit-learn, Matplotlib, Seaborn)
- 🌐 **Visualización Geoespacial**: Cartopy, Folium
- ☁️ **Infraestructura**: Google Colab / Jupyter / Docker

## 🛰️ Contexto Científico

El centelleo ionosférico es una fluctuación rápida de la fase y amplitud de las señales GNSS, causada por **irregularidades del plasma ionosférico**. Estas perturbaciones pueden afectar la navegación aérea, terrestre y marítima, así como los sistemas de sincronización crítica.

## 🚀 Estado del Proyecto

- ✅ Extracción y limpieza de datos
- ✅ Visualización de eventos de centelleo
- ✅ Modelos de clasificación para detección automática
- 🔄 En progreso: predicción de eventos con modelos secuenciales
- 🔜 Futuro: integración en una plataforma web de monitoreo

## 🧠 Autor

**Alexander Valdez Portocarrero**  }
Especialista en Radar e Ingeniería Electrónica 
Instituto Geofísico del Perú (IGP)  

💡 Apasionado por la inteligencia artificial aplicada a la geociencia, espacio y sociedad.
