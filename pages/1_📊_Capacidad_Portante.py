import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Capacidad Portante", page_icon="📊", layout="wide")

st.title("📊 Análisis de Capacidad Portante")
st.markdown("---")

# Introducción
st.markdown("""
Esta herramienta calcula la capacidad portante última de cimentaciones superficiales 
utilizando diferentes teorías y métodos reconocidos.
""")

# Sidebar para parámetros
with st.sidebar:
    st.header("Parámetros del Suelo")
    
    # Propiedades del suelo
    cohesion = st.number_input("Cohesión (c) [kN/m²]", min_value=0.0, value=10.0, step=1.0)
    friction_angle = st.number_input("Ángulo de fricción (φ) [°]", min_value=0.0, max_value=45.0, value=30.0, step=1.0)
    unit_weight = st.number_input("Peso unitario (γ) [kN/m³]", min_value=0.0, value=18.0, step=0.5)
    
    st.markdown("---")
    st.header("Geometría de Cimentación")
    
    width = st.number_input("Ancho (B) [m]", min_value=0.1, value=2.0, step=0.1)
    length = st.number_input("Largo (L) [m]", min_value=0.1, value=3.0, step=0.1)
    depth = st.number_input("Profundidad (Df) [m]", min_value=0.0, value=1.5, step=0.1)
    
    st.markdown("---")
    method = st.selectbox("Método de cálculo", 
                         ["Terzaghi", "Meyerhof", "Hansen", "Vesic"])

# Función para calcular factores de capacidad portante
def calculate_bearing_capacity_factors(phi):
    phi_rad = np.radians(phi)
    Nq = np.exp(np.pi * np.tan(phi_rad)) * (np.tan(np.radians(45 + phi/2)))**2
    Nc = (Nq - 1) / np.tan(phi_rad) if phi > 0 else 5.14
    Ng = 2 * (Nq - 1) * np.tan(phi_rad)
    return Nc, Nq, Ng

# Función para calcular factores de forma (simplificado)
def calculate_shape_factors(B, L, phi):
    if phi == 0:
        sc = 1 + 0.2 * (B/L)
        sq = 1.0
        sg = 1.0
    else:
        sc = 1 + (B/L) * (Nq/Nc) if Nc > 0 else 1
        sq = 1 + (B/L) * np.tan(np.radians(phi))
        sg = 1 - 0.4 * (B/L)
    return sc, sq, sg

# Cálculos
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Resultados del Análisis")
    
    # Calcular factores de capacidad portante
    Nc, Nq, Ng = calculate_bearing_capacity_factors(friction_angle)
    sc, sq, sg = calculate_shape_factors(width, length, friction_angle)
    
    # Calcular capacidad portante última
    q = unit_weight * depth  # Sobrecarga
    
    qu = (cohesion * Nc * sc + 
          q * Nq * sq + 
          0.5 * unit_weight * width * Ng * sg)
    
    # Factor de seguridad típico
    FS = 3.0
    qa = qu / FS
    
    # Mostrar resultados
    st.success(f"**Capacidad Portante Última (qu):** {qu:.2f} kN/m²")
    st.info(f"**Capacidad Portante Admisible (qa) con FS={FS}:** {qa:.2f} kN/m²")
    
    # Tabla de factores
    st.markdown("### Factores de Capacidad Portante")
    factors_df = pd.DataFrame({
        'Factor': ['Nc', 'Nq', 'Nγ'],
        'Valor': [f"{Nc:.2f}", f"{Nq:.2f}", f"{Ng:.2f}"]
    })
    st.table(factors_df)
    
    # Tabla de factores de forma
    st.markdown("### Factores de Forma")
    shape_df = pd.DataFrame({
        'Factor': ['sc', 'sq', 'sγ'],
        'Valor': [f"{sc:.2f}", f"{sq:.2f}", f"{sg:.2f}"]
    })
    st.table(shape_df)

with col2:
    st.subheader("Parámetros de Entrada")
    params_df = pd.DataFrame({
        'Parámetro': ['Cohesión', 'Ángulo φ', 'γ', 'Ancho B', 'Largo L', 'Profundidad Df'],
        'Valor': [f"{cohesion} kN/m²", f"{friction_angle}°", f"{unit_weight} kN/m³", 
                 f"{width} m", f"{length} m", f"{depth} m"]
    })
    st.table(params_df)
    
    st.markdown(f"**Método:** {method}")
    st.markdown(f"**Factor de Seguridad:** {FS}")

# Gráfico de variación de qu con φ
st.markdown("---")
st.subheader("Variación de Capacidad Portante con Ángulo de Fricción")

phi_range = np.linspace(0, 45, 50)
qu_range = []

for phi in phi_range:
    Nc_temp, Nq_temp, Ng_temp = calculate_bearing_capacity_factors(phi)
    sc_temp, sq_temp, sg_temp = calculate_shape_factors(width, length, phi)
    qu_temp = (cohesion * Nc_temp * sc_temp + 
               q * Nq_temp * sq_temp + 
               0.5 * unit_weight * width * Ng_temp * sg_temp)
    qu_range.append(qu_temp)

fig = go.Figure()
fig.add_trace(go.Scatter(x=phi_range, y=qu_range, mode='lines', name='qu',
                        line=dict(color='blue', width=3)))
fig.add_trace(go.Scatter(x=[friction_angle], y=[qu], mode='markers', 
                        name='Valor actual',
                        marker=dict(color='red', size=12)))

fig.update_layout(
    xaxis_title="Ángulo de fricción φ (°)",
    yaxis_title="Capacidad portante última qu (kN/m²)",
    hovermode='x unified',
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

# Notas
with st.expander("📝 Notas y consideraciones"):
    st.markdown("""
    - Los cálculos se basan en la teoría de capacidad portante para cimentaciones superficiales
    - Se asume que el suelo es homogéneo e isotrópico
    - El nivel freático no está considerado en estos cálculos simplificados
    - Para análisis detallados, consulte con un ingeniero geotécnico profesional
    - Factor de seguridad típico: 2.5 - 3.0
    """)
