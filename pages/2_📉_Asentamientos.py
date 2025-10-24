import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Asentamientos", page_icon="📉", layout="wide")

st.title("📉 Cálculo de Asentamientos")
st.markdown("---")

st.markdown("""
Esta herramienta calcula asentamientos en suelos cohesivos y granulares.
Incluye asentamiento inmediato y por consolidación.
""")

# Sidebar
with st.sidebar:
    st.header("Tipo de Análisis")
    soil_type = st.radio("Tipo de suelo", ["Cohesivo (Arcilla)", "Granular (Arena)"])
    
    st.markdown("---")
    st.header("Parámetros de Carga")
    
    load = st.number_input("Carga aplicada (q) [kN/m²]", min_value=0.0, value=100.0, step=10.0)
    width = st.number_input("Ancho de cimentación (B) [m]", min_value=0.1, value=2.0, step=0.1)
    
    st.markdown("---")
    st.header("Propiedades del Suelo")

if soil_type == "Cohesivo (Arcilla)":
    with st.sidebar:
        Cc = st.number_input("Índice de compresión (Cc)", min_value=0.0, value=0.3, step=0.01)
        Cr = st.number_input("Índice de recompresión (Cr)", min_value=0.0, value=0.05, step=0.01)
        e0 = st.number_input("Relación de vacíos inicial (e₀)", min_value=0.1, value=0.8, step=0.1)
        H = st.number_input("Espesor de capa compresible (H) [m]", min_value=0.1, value=5.0, step=0.5)
        sigma_p = st.number_input("Presión de preconsolidación (σ'p) [kN/m²]", 
                                  min_value=0.0, value=150.0, step=10.0)
        sigma_0 = st.number_input("Esfuerzo efectivo inicial (σ'₀) [kN/m²]", 
                                  min_value=0.0, value=80.0, step=10.0)
    
    # Cálculo de asentamiento por consolidación
    st.subheader("Resultados - Asentamiento por Consolidación")
    
    delta_sigma = load  # Incremento de esfuerzo
    sigma_f = sigma_0 + delta_sigma
    
    col1, col2 = st.columns(2)
    
    with col1:
        if sigma_f <= sigma_p:
            # Normalmente consolidado
            Sc = (Cr * H / (1 + e0)) * np.log10(sigma_f / sigma_0)
            consolidation_type = "Recompresión"
        else:
            if sigma_0 < sigma_p:
                # Parcialmente sobreconsolidado
                Sc1 = (Cr * H / (1 + e0)) * np.log10(sigma_p / sigma_0)
                Sc2 = (Cc * H / (1 + e0)) * np.log10(sigma_f / sigma_p)
                Sc = Sc1 + Sc2
                consolidation_type = "Sobreconsolidado + Virgen"
            else:
                # Compresión virgen
                Sc = (Cc * H / (1 + e0)) * np.log10(sigma_f / sigma_0)
                consolidation_type = "Compresión Virgen"
        
        st.success(f"**Asentamiento por Consolidación:** {Sc*1000:.2f} mm")
        st.info(f"**Tipo de consolidación:** {consolidation_type}")
        
        # Tabla de parámetros
        params_df = pd.DataFrame({
            'Parámetro': ['σ\'₀', 'Δσ', 'σ\'f', 'σ\'p', 'OCR'],
            'Valor': [
                f"{sigma_0:.1f} kN/m²",
                f"{delta_sigma:.1f} kN/m²",
                f"{sigma_f:.1f} kN/m²",
                f"{sigma_p:.1f} kN/m²",
                f"{sigma_p/sigma_0:.2f}"
            ]
        })
        st.table(params_df)
    
    with col2:
        st.markdown("### Parámetros del suelo")
        soil_params = pd.DataFrame({
            'Propiedad': ['Cc', 'Cr', 'e₀', 'H'],
            'Valor': [f"{Cc:.3f}", f"{Cr:.3f}", f"{e0:.2f}", f"{H:.1f} m"]
        })
        st.table(soil_params)
    
    # Gráfico e-log σ'
    st.markdown("---")
    st.subheader("Curva e - log σ'")
    
    sigma_range = np.logspace(np.log10(max(sigma_0*0.5, 10)), np.log10(sigma_f*2), 100)
    e_range = []
    
    for sigma in sigma_range:
        if sigma <= sigma_p:
            e = e0 - Cr * np.log10(sigma / sigma_0)
        else:
            e_recomp = e0 - Cr * np.log10(sigma_p / sigma_0)
            e = e_recomp - Cc * np.log10(sigma / sigma_p)
        e_range.append(e)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sigma_range, y=e_range, mode='lines', 
                            name='Curva e-log σ\'',
                            line=dict(color='blue', width=2)))
    fig.add_trace(go.Scatter(x=[sigma_0], y=[e0], mode='markers', 
                            name='Estado inicial',
                            marker=dict(color='green', size=10)))
    fig.add_trace(go.Scatter(x=[sigma_f], y=[e0 - (Sc * (1 + e0) / H)], 
                            mode='markers', 
                            name='Estado final',
                            marker=dict(color='red', size=10)))
    
    fig.update_xaxes(type="log", title="Esfuerzo efectivo σ' (kN/m²)")
    fig.update_yaxes(title="Relación de vacíos e")
    fig.update_layout(template='plotly_white', hovermode='x unified')
    
    st.plotly_chart(fig, use_container_width=True)

else:  # Suelo Granular
    with st.sidebar:
        E = st.number_input("Módulo de elasticidad (E) [kN/m²]", 
                           min_value=1000.0, value=30000.0, step=1000.0)
        nu = st.number_input("Relación de Poisson (ν)", 
                            min_value=0.0, max_value=0.5, value=0.3, step=0.05)
        depth = st.number_input("Profundidad influencia (z) [m]", 
                               min_value=0.1, value=3.0, step=0.5)
    
    st.subheader("Resultados - Asentamiento Elástico")
    
    # Asentamiento inmediato (simplificado)
    # Factor de forma para cimentación rectangular
    mu = 1.0  # Factor simplificado
    Si = (load * width * (1 - nu**2) * mu) / E
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success(f"**Asentamiento Inmediato:** {Si*1000:.2f} mm")
        
        params_df = pd.DataFrame({
            'Parámetro': ['Carga q', 'Ancho B', 'E', 'ν'],
            'Valor': [
                f"{load:.1f} kN/m²",
                f"{width:.1f} m",
                f"{E:.0f} kN/m²",
                f"{nu:.2f}"
            ]
        })
        st.table(params_df)
    
    with col2:
        st.info("💡 **Nota:** Cálculo basado en teoría elástica simplificada")
        
        # Variación con módulo E
        st.markdown("### Sensibilidad al Módulo E")
        E_range = np.linspace(E*0.5, E*1.5, 5)
        Si_range = [(load * width * (1 - nu**2) * mu) / Ei for Ei in E_range]
        
        sens_df = pd.DataFrame({
            'E (kN/m²)': E_range,
            'Si (mm)': [s*1000 for s in Si_range]
        })
        st.dataframe(sens_df, hide_index=True)

# Notas
with st.expander("📝 Notas y consideraciones"):
    st.markdown("""
    **Para suelos cohesivos:**
    - Los cálculos están basados en la teoría de consolidación unidimensional de Terzaghi
    - OCR = Grado de sobreconsolidación = σ'p / σ'₀
    - El tiempo de consolidación no está incluido en estos cálculos
    
    **Para suelos granulares:**
    - El asentamiento es principalmente inmediato (elástico)
    - Los cálculos son simplificados y basados en teoría elástica
    - En la práctica, usar correlaciones con SPT o CPT para mejor precisión
    
    **Recomendaciones:**
    - Siempre verificar con ensayos de laboratorio
    - Considerar efectos del nivel freático
    - Para diseño final, consultar con un especialista
    """)
