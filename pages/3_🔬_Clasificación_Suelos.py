import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Clasificación de Suelos", page_icon="🔬", layout="wide")

st.title("🔬 Clasificación de Suelos")
st.markdown("---")

st.markdown("""
Esta herramienta ayuda a clasificar suelos según diferentes sistemas de clasificación:
- Sistema Unificado de Clasificación de Suelos (SUCS/USCS)
- Sistema AASHTO
""")

# Tabs para diferentes sistemas
tab1, tab2 = st.tabs(["SUCS (USCS)", "AASHTO"])

with tab1:
    st.subheader("Sistema Unificado de Clasificación de Suelos (SUCS)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Datos de Granulometría")
        
        # Porcentajes que pasan por tamices
        grava = st.number_input("% Grava (> 4.75 mm)", min_value=0.0, max_value=100.0, value=10.0, step=1.0)
        arena = st.number_input("% Arena (0.075 - 4.75 mm)", min_value=0.0, max_value=100.0, value=60.0, step=1.0)
        finos = st.number_input("% Finos (< 0.075 mm)", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
        
        total = grava + arena + finos
        if abs(total - 100) > 0.1:
            st.warning(f"⚠️ La suma debe ser 100% (actual: {total:.1f}%)")
        
        st.markdown("---")
        st.markdown("### Coeficientes de Uniformidad")
        
        D60 = st.number_input("D₆₀ [mm]", min_value=0.001, value=0.5, step=0.01, format="%.3f")
        D30 = st.number_input("D₃₀ [mm]", min_value=0.001, value=0.2, step=0.01, format="%.3f")
        D10 = st.number_input("D₁₀ [mm]", min_value=0.001, value=0.1, step=0.01, format="%.3f")
        
        Cu = D60 / D10 if D10 > 0 else 0
        Cc = (D30**2) / (D60 * D10) if (D60 * D10) > 0 else 0
        
        st.info(f"**Cu = {Cu:.2f}**")
        st.info(f"**Cc = {Cc:.2f}**")
        
        st.markdown("---")
        st.markdown("### Límites de Atterberg")
        
        LL = st.number_input("Límite Líquido (LL) [%]", min_value=0.0, value=30.0, step=1.0)
        LP = st.number_input("Límite Plástico (LP) [%]", min_value=0.0, value=20.0, step=1.0)
        IP = LL - LP
        
        st.info(f"**IP = {IP:.1f}%**")
    
    with col2:
        st.markdown("### Clasificación SUCS")
        
        # Lógica de clasificación simplificada
        clasificacion = ""
        descripcion = ""
        
        # Determinar si es de grano grueso o fino
        if finos < 50:
            # Suelo de grano grueso
            if grava > arena:
                # Grava predominante
                if finos < 5:
                    if Cu >= 4 and 1 <= Cc <= 3:
                        clasificacion = "GW"
                        descripcion = "Grava bien gradada"
                    else:
                        clasificacion = "GP"
                        descripcion = "Grava pobremente gradada"
                elif 5 <= finos <= 12:
                    clasificacion = "GW-GC o GW-GM"
                    descripcion = "Grava bien gradada con finos"
                else:
                    if IP > 7 and LL < 50:
                        clasificacion = "GC"
                        descripcion = "Grava arcillosa"
                    else:
                        clasificacion = "GM"
                        descripcion = "Grava limosa"
            else:
                # Arena predominante
                if finos < 5:
                    if Cu >= 6 and 1 <= Cc <= 3:
                        clasificacion = "SW"
                        descripcion = "Arena bien gradada"
                    else:
                        clasificacion = "SP"
                        descripcion = "Arena pobremente gradada"
                elif 5 <= finos <= 12:
                    clasificacion = "SW-SC o SW-SM"
                    descripcion = "Arena bien gradada con finos"
                else:
                    if IP > 7 and LL < 50:
                        clasificacion = "SC"
                        descripcion = "Arena arcillosa"
                    else:
                        clasificacion = "SM"
                        descripcion = "Arena limosa"
        else:
            # Suelo de grano fino
            if LL < 50:
                # Baja plasticidad
                if IP > 7:
                    clasificacion = "CL"
                    descripcion = "Arcilla de baja plasticidad"
                elif IP < 4:
                    clasificacion = "ML"
                    descripcion = "Limo de baja plasticidad"
                else:
                    clasificacion = "CL-ML"
                    descripcion = "Limo arcilloso"
            else:
                # Alta plasticidad
                if IP > 0.73 * (LL - 20):
                    clasificacion = "CH"
                    descripcion = "Arcilla de alta plasticidad"
                else:
                    clasificacion = "MH"
                    descripcion = "Limo de alta plasticidad"
        
        # Mostrar resultado
        st.success(f"## Clasificación: **{clasificacion}**")
        st.info(f"### {descripcion}")
        
        # Tabla resumen
        st.markdown("---")
        st.markdown("### Resumen de Datos")
        
        resumen_df = pd.DataFrame({
            'Parámetro': ['% Grava', '% Arena', '% Finos', 'Cu', 'Cc', 'LL', 'LP', 'IP'],
            'Valor': [
                f"{grava:.1f}%",
                f"{arena:.1f}%",
                f"{finos:.1f}%",
                f"{Cu:.2f}",
                f"{Cc:.2f}",
                f"{LL:.1f}%",
                f"{LP:.1f}%",
                f"{IP:.1f}%"
            ]
        })
        st.table(resumen_df)
        
        # Gráfico de distribución granulométrica
        st.markdown("---")
        st.markdown("### Distribución Granulométrica")
        
        fig = go.Figure(data=[
            go.Bar(name='Grava', x=['Distribución'], y=[grava], marker_color='brown'),
            go.Bar(name='Arena', x=['Distribución'], y=[arena], marker_color='yellow'),
            go.Bar(name='Finos', x=['Distribución'], y=[finos], marker_color='gray')
        ])
        
        fig.update_layout(
            barmode='stack',
            yaxis_title="Porcentaje (%)",
            showlegend=True,
            template='plotly_white',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Carta de plasticidad
        st.markdown("### Carta de Plasticidad")
        
        # Línea A y U
        LL_range = np.linspace(0, 100, 100)
        linea_A = 0.73 * (LL_range - 20)
        linea_U = 0.9 * (LL_range - 8)
        
        fig2 = go.Figure()
        
        # Líneas de referencia
        fig2.add_trace(go.Scatter(x=LL_range, y=linea_A, mode='lines', 
                                 name='Línea A', line=dict(color='red', dash='dash')))
        fig2.add_trace(go.Scatter(x=LL_range, y=linea_U, mode='lines', 
                                 name='Línea U', line=dict(color='blue', dash='dash')))
        
        # Punto del suelo
        fig2.add_trace(go.Scatter(x=[LL], y=[IP], mode='markers', 
                                 name='Muestra',
                                 marker=dict(color='green', size=15, symbol='star')))
        
        # Líneas de división
        fig2.add_vline(x=50, line_dash="dot", line_color="gray")
        fig2.add_hline(y=7, line_dash="dot", line_color="gray")
        
        # Anotaciones de zonas
        fig2.add_annotation(x=30, y=25, text="CL", showarrow=False, font=dict(size=12, color="gray"))
        fig2.add_annotation(x=70, y=40, text="CH", showarrow=False, font=dict(size=12, color="gray"))
        fig2.add_annotation(x=30, y=3, text="ML", showarrow=False, font=dict(size=12, color="gray"))
        fig2.add_annotation(x=70, y=15, text="MH", showarrow=False, font=dict(size=12, color="gray"))
        
        fig2.update_layout(
            xaxis_title="Límite Líquido LL (%)",
            yaxis_title="Índice de Plasticidad IP (%)",
            template='plotly_white',
            xaxis_range=[0, 100],
            yaxis_range=[0, 60],
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("Sistema de Clasificación AASHTO")
    st.info("⚙️ Esta funcionalidad estará disponible próximamente")
    
    st.markdown("""
    El sistema AASHTO clasifica los suelos en grupos del A-1 al A-7, 
    basándose en la granulometría y los límites de Atterberg.
    
    **Grupos principales:**
    - A-1, A-2, A-3: Materiales granulares
    - A-4, A-5, A-6, A-7: Materiales limo-arcillosos
    """)

# Información adicional
with st.expander("📚 Guía de Clasificación SUCS"):
    st.markdown("""
    ### Símbolos Principales:
    - **G** = Grava (Gravel)
    - **S** = Arena (Sand)
    - **M** = Limo (Silt)
    - **C** = Arcilla (Clay)
    - **O** = Orgánico
    - **W** = Bien gradado (Well graded)
    - **P** = Pobremente gradado (Poorly graded)
    - **H** = Alta plasticidad
    - **L** = Baja plasticidad
    
    ### Criterios de Clasificación:
    - **Grano grueso:** < 50% pasa tamiz No. 200
    - **Grano fino:** ≥ 50% pasa tamiz No. 200
    - **Grava:** Fracción retenida en tamiz No. 4
    - **Arena:** Fracción que pasa tamiz No. 4 pero retiene No. 200
    
    ### Coeficientes:
    - **Cu (Coeficiente de Uniformidad):** Cu = D₆₀ / D₁₀
    - **Cc (Coeficiente de Curvatura):** Cc = (D₃₀)² / (D₆₀ × D₁₀)
    
    Para arena bien gradada: Cu ≥ 6 y 1 ≤ Cc ≤ 3  
    Para grava bien gradada: Cu ≥ 4 y 1 ≤ Cc ≤ 3
    """)
