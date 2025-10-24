import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Herramientas Geotécnicas",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("🏗️ Herramientas Geotécnicas")
st.markdown("---")

# Barra lateral
with st.sidebar:
    st.header("Navegación")
    st.markdown("""
    Bienvenido a la aplicación de herramientas geotécnicas.
    
    **Herramientas disponibles:**
    - Análisis de capacidad portante
    - Cálculos de asentamiento
    - Análisis de estabilidad de taludes
    - Clasificación de suelos
    """)
    
    st.markdown("---")
    st.info("💡 Selecciona una herramienta del menú principal para comenzar")

# Contenido principal
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 Capacidad Portante")
    st.markdown("""
    Herramienta para calcular la capacidad portante de suelos basándose en diferentes teorías:
    - Terzaghi
    - Meyerhof
    - Hansen
    - Vesic
    """)
    if st.button("Ir a Capacidad Portante", key="bearing"):
        st.info("Esta herramienta estará disponible próximamente")

with col2:
    st.subheader("📉 Asentamientos")
    st.markdown("""
    Calcula asentamientos en suelos cohesivos y granulares:
    - Asentamiento inmediato
    - Consolidación primaria
    - Consolidación secundaria
    """)
    if st.button("Ir a Asentamientos", key="settlement"):
        st.info("Esta herramienta estará disponible próximamente")

with col3:
    st.subheader("⛰️ Estabilidad de Taludes")
    st.markdown("""
    Análisis de estabilidad de taludes utilizando:
    - Método de Bishop
    - Método de Fellenius
    - Método de Spencer
    """)
    if st.button("Ir a Estabilidad", key="stability"):
        st.info("Esta herramienta estará disponible próximamente")

# Sección de información
st.markdown("---")
st.header("📖 Acerca de esta aplicación")

with st.expander("ℹ️ Información general"):
    st.markdown("""
    Esta aplicación web proporciona herramientas para análisis geotécnico básico.
    
    **Características:**
    - Interfaz interactiva y fácil de usar
    - Visualizaciones dinámicas de resultados
    - Cálculos basados en estándares internacionales
    - Exportación de resultados
    
    **Desarrollado con:**
    - Python
    - Streamlit
    - NumPy/Pandas
    - Plotly/Matplotlib
    """)

with st.expander("🚀 Cómo usar"):
    st.markdown("""
    1. Selecciona la herramienta que deseas utilizar
    2. Ingresa los parámetros requeridos
    3. Visualiza los resultados
    4. Exporta los datos si es necesario
    """)

# Footer
st.markdown("---")
st.caption("Herramientas Geotécnicas v1.0 - Desarrollado con Streamlit")
