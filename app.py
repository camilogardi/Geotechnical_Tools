"""
Geotechnical Tools - Simple Streamlit App
Aplicación para análisis de datos geotécnicos
"""

import streamlit as st
from Tools import save_cache, load_cache, calc_circular_surcharge
from calculations import (
    get_cache_hash,
    compute_boussinesq_cached,
    create_xz_plot,
    create_yz_plot,
    create_depth_profile_plot,
    generate_pdf_report
)
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def boussinesq_interface():
    """Render Boussinesq calculation interface in sidebar and main content"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Parámetros de Cálculo")

    # Initialize session state
    if 'boussinesq_data' not in st.session_state:
        st.session_state.boussinesq_data = None
    if 'plots' not in st.session_state:
        st.session_state.plots = []

    # Input parameters
    with st.sidebar.expander("Parámetros de Carga", expanded=True):
        q = st.number_input("Sobrecarga q (kPa)", min_value=0.0, value=100.0, step=10.0)
        col1, col2 = st.columns(2)
        with col1:
            Lx = st.number_input("Lx (m)", min_value=0.1, value=10.0, step=1.0)
        with col2:
            Ly = st.number_input("Ly (m)", min_value=0.1, value=10.0, step=1.0)

    with st.sidebar.expander("Dominio de Cálculo", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            Xmin = st.number_input("Xmin (m)", value=-20.0, step=1.0)
            Ymin = st.number_input("Ymin (m)", value=-20.0, step=1.0)
        with col2:
            Xmax = st.number_input("Xmax (m)", value=20.0, step=1.0)
            Ymax = st.number_input("Ymax (m)", value=20.0, step=1.0)
        Zmax = st.number_input("Profundidad máx Z (m)", min_value=0.1, value=30.0, step=5.0)

    with st.sidebar.expander("Resolución de Malla", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            Nx = st.number_input("Nx", min_value=2, max_value=200, value=41, step=5)
        with col2:
            Ny = st.number_input("Ny", min_value=2, max_value=200, value=41, step=5)
        with col3:
            Nz = st.number_input("Nz", min_value=2, max_value=200, value=31, step=5)

    # Calculation buttons
    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("🔄 Calcular", use_container_width=True):
            with st.spinner("Calculando esfuerzos..."):
                try:
                    X, Y, Z, sigma = compute_boussinesq_cached(
                        q, Lx, Ly, Xmin, Xmax, Ymin, Ymax, Zmax, Nx, Ny, Nz
                    )
                    st.session_state.boussinesq_data = {
                        'X': X, 'Y': Y, 'Z': Z, 'sigma': sigma,
                        'params': {'q': q, 'Lx': Lx, 'Ly': Ly, 'Xmin': Xmin, 'Xmax': Xmax,
                                   'Ymin': Ymin, 'Ymax': Ymax, 'Zmax': Zmax, 'Nx': Nx, 'Ny': Ny, 'Nz': Nz}
                    }
                    st.sidebar.success("✅ Cálculo completado")
                except Exception as e:
                    st.sidebar.error(f"❌ Error: {str(e)}")

    with col2:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.session_state.boussinesq_data = None
            st.session_state.plots = []
            st.rerun()

    # Cache management
    with st.sidebar.expander("💾 Gestión de Cache", expanded=False):
        cache_name = st.text_input("Nombre de cache",
                                   value=f"boussinesq_{get_cache_hash(q, Lx, Ly, Xmin, Xmax, Ymin, Ymax, Zmax, Nx, Ny, Nz)}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Guardar", use_container_width=True):
                if st.session_state.boussinesq_data is not None:
                    cache_path = f"Tools/cache/{cache_name}.npz"
                    try:
                        save_cache(cache_path, {
                            'X': st.session_state.boussinesq_data['X'],
                            'Y': st.session_state.boussinesq_data['Y'],
                            'Z': st.session_state.boussinesq_data['Z'],
                            'sigma': st.session_state.boussinesq_data['sigma']
                        })
                        st.success(f"💾 Guardado: {cache_path}")
                    except Exception as e:
                        st.error(f"Error al guardar: {str(e)}")
                else:
                    st.warning("No hay datos para guardar")

        with col2:
            if st.button("Cargar", use_container_width=True):
                cache_path = f"Tools/cache/{cache_name}.npz"
                try:
                    data = load_cache(cache_path)
                    st.session_state.boussinesq_data = {
                        'X': data['X'], 'Y': data['Y'], 'Z': data['Z'], 'sigma': data['sigma'],
                        'params': {'q': q, 'Lx': Lx, 'Ly': Ly, 'Xmin': Xmin, 'Xmax': Xmax,
                                   'Ymin': Ymin, 'Ymax': Ymax, 'Zmax': Zmax, 'Nx': Nx, 'Ny': Ny, 'Nz': Nz}
                    }
                    st.success(f"📂 Cargado: {cache_path}")
                    st.rerun()
                except FileNotFoundError:
                    st.error(f"Archivo no encontrado: {cache_path}")
                except Exception as e:
                    st.error(f"Error al cargar: {str(e)}")

    # Main content area
    if st.session_state.boussinesq_data is not None:
        data = st.session_state.boussinesq_data
        X, Y, Z, sigma = data['X'], data['Y'], data['Z'], data['sigma']

        st.header("📊 Resultados de Boussinesq")

        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("σz máximo", f"{sigma.max():.2f} kPa")
        with col2:
            st.metric("σz mínimo", f"{sigma.min():.2f} kPa")
        with col3:
            st.metric("Puntos totales", f"{Nx*Ny*Nz:,}")
        with col4:
            st.metric("Tamaño malla", f"{Nx}×{Ny}×{Nz}")

        st.markdown("---")

        # Plot controls
        st.subheader("📈 Visualización")

        # Add plot controls
        plot_type = st.selectbox("Tipo de gráfica",
                                 ["Corte X-Z", "Corte Y-Z", "Perfil en profundidad"])

        col1, col2, col3 = st.columns(3)

        if plot_type == "Corte X-Z":
            with col1:
                y_val = st.number_input("Valor de Y (m)",
                                        min_value=float(Y.min()),
                                        max_value=float(Y.max()),
                                        value=0.0)
            with col2:
                if st.button("➕ Agregar gráfica"):
                    st.session_state.plots.append({'type': plot_type, 'y_val': y_val})
                    st.rerun()

        elif plot_type == "Corte Y-Z":
            with col1:
                x_val = st.number_input("Valor de X (m)",
                                        min_value=float(X.min()),
                                        max_value=float(X.max()),
                                        value=0.0)
            with col2:
                if st.button("➕ Agregar gráfica"):
                    st.session_state.plots.append({'type': plot_type, 'x_val': x_val})
                    st.rerun()

        elif plot_type == "Perfil en profundidad":
            with col1:
                x_point = st.number_input("X (m)",
                                          min_value=float(X.min()),
                                          max_value=float(X.max()),
                                          value=0.0)
            with col2:
                y_point = st.number_input("Y (m)",
                                          min_value=float(Y.min()),
                                          max_value=float(Y.max()),
                                          value=0.0)
            with col3:
                if st.button("➕ Agregar gráfica"):
                    st.session_state.plots.append({'type': plot_type, 'x_point': x_point, 'y_point': y_point})
                    st.rerun()

        # Plot management buttons
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("🗑️ Eliminar última") and len(st.session_state.plots) > 0:
                st.session_state.plots.pop()
                st.rerun()
        with col2:
            if st.button("🧹 Limpiar todas") and len(st.session_state.plots) > 0:
                st.session_state.plots = []
                st.rerun()

        st.markdown("---")

        # Display all plots
        if st.session_state.plots:
            st.subheader(f"Gráficas ({len(st.session_state.plots)})")

            for i, plot_cfg in enumerate(st.session_state.plots):
                st.markdown(f"**Gráfica {i+1}: {plot_cfg['type']}**")

                if plot_cfg['type'] == "Corte X-Z":
                    fig = create_xz_plot(X, Y, Z, sigma, plot_cfg['y_val'])
                elif plot_cfg['type'] == "Corte Y-Z":
                    fig = create_yz_plot(X, Y, Z, sigma, plot_cfg['x_val'])
                elif plot_cfg['type'] == "Perfil en profundidad":
                    fig = create_depth_profile_plot(X, Y, Z, sigma, plot_cfg['x_point'], plot_cfg['y_point'])

                st.plotly_chart(fig, use_container_width=True)
                st.markdown("---")

            # PDF export
            if st.button("📄 Generar PDF"):
                try:
                    pdf_bytes = generate_pdf_report(data['params'], st.session_state.plots, X, Y, Z, sigma)
                    st.download_button(
                        label="⬇️ Descargar PDF",
                        data=pdf_bytes,
                        file_name="reporte_boussinesq.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error al generar PDF: {str(e)}")
        else:
            st.info("👆 Agregue gráficas usando los controles de arriba")
    else:
        st.info("👈 Configure los parámetros y presione 'Calcular' para comenzar")


def esfuerzo_vertical_continua():
    """Placeholder for Esfuerzo Vertical Continua calculation"""
    st.info("⚠️ En desarrollo — funciones pendientes")


def esfuerzo_vertical_circular():
    """Interface for Esfuerzo Vertical Circular calculation"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Parámetros de Cálculo")

    # Initialize session state
    if 'circular_data' not in st.session_state:
        st.session_state.circular_data = None

    # Input parameters
    with st.sidebar.expander("Parámetros de Carga Circular", expanded=True):
        q = st.number_input("Sobrecarga q (kPa)", min_value=0.0, value=100.0, step=10.0)
        radius = st.number_input("Radio (m)", min_value=0.1, value=5.0, step=0.5)

    with st.sidebar.expander("Punto de Cálculo", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            x_point = st.number_input("X (m)", value=0.0, step=1.0)
        with col2:
            y_point = st.number_input("Y (m)", value=0.0, step=1.0)

    with st.sidebar.expander("Rango de Profundidad", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            z_min = st.number_input("Z mínima (m)", min_value=0.1, value=0.1, step=0.1)
            n_points = st.number_input("Número de puntos", min_value=10, max_value=200, value=50, step=10)
        with col2:
            z_max = st.number_input("Z máxima (m)", min_value=0.1, value=30.0, step=5.0)

    # Calculation buttons
    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("🔄 Calcular", use_container_width=True):
            with st.spinner("Calculando esfuerzos circulares..."):
                try:
                    z_values = np.linspace(z_min, z_max, n_points)
                    z_result, sigma_z = calc_circular_surcharge(q, radius, x_point, y_point, z_values)
                    
                    st.session_state.circular_data = {
                        'z': z_result,
                        'sigma_z': sigma_z,
                        'params': {
                            'q': q,
                            'radius': radius,
                            'x_point': x_point,
                            'y_point': y_point,
                            'z_min': z_min,
                            'z_max': z_max,
                            'n_points': n_points
                        }
                    }
                    st.sidebar.success("✅ Cálculo completado")
                except Exception as e:
                    st.sidebar.error(f"❌ Error: {str(e)}")

    with col2:
        if st.button("🗑️ Limpiar", use_container_width=True):
            st.session_state.circular_data = None
            st.rerun()

    # Main content area
    if st.session_state.circular_data is not None:
        data = st.session_state.circular_data
        z = data['z']
        sigma_z = data['sigma_z']
        params = data['params']

        st.header("📊 Resultados de Esfuerzo Vertical Circular")

        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("σz máximo", f"{sigma_z.max():.2f} kPa")
        with col2:
            st.metric("σz mínimo", f"{sigma_z.min():.2f} kPa")
        with col3:
            r = np.sqrt(params['x_point']**2 + params['y_point']**2)
            st.metric("Distancia radial", f"{r:.2f} m")
        with col4:
            st.metric("Puntos calculados", f"{len(z):,}")

        st.markdown("---")

        # Plot: sigma_z vs z
        st.subheader("📈 Gráfica: Esfuerzo Vertical vs Profundidad")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sigma_z,
            y=z,
            mode='lines+markers',
            name='σz vs z',
            line=dict(color='blue', width=2),
            marker=dict(size=4)
        ))
        
        fig.update_layout(
            title=f'Esfuerzo Vertical a r={r:.2f}m del centro',
            xaxis_title='σz (kPa)',
            yaxis_title='Profundidad z (m)',
            yaxis=dict(autorange='reversed'),  # Depth increases downward
            height=500,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Results table
        st.subheader("📋 Tabla de Resultados")
        
        # Create DataFrame
        df = pd.DataFrame({
            'Profundidad z (m)': z,
            'σz (kPa)': sigma_z
        })
        
        # Format numbers
        df['Profundidad z (m)'] = df['Profundidad z (m)'].map('{:.2f}'.format)
        df['σz (kPa)'] = df['σz (kPa)'].map('{:.2f}'.format)
        
        st.dataframe(df, use_container_width=True, height=400)

        # Download button for CSV
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name="esfuerzo_circular.csv",
            mime="text/csv"
        )
    else:
        st.info("👈 Configure los parámetros y presione 'Calcular' para comenzar")


def esfuerzo_vertical_anular():
    """Placeholder for Esfuerzo Vertical Anular calculation"""
    st.info("⚠️ En desarrollo — funciones pendientes")


def esfuerzo_vertical_terraplen():
    """Placeholder for Esfuerzo Vertical Terraplén calculation"""
    st.info("⚠️ En desarrollo — funciones pendientes")


def main():
    """Main application function"""
    st.set_page_config(
        page_title="Calculo de Esfuerzos",
        page_icon="IMG_2224.jpeg",
        layout="wide"
    )

    # Sidebar
    st.sidebar.title("Calculo de Esfuerzos")

    # Add tab selector for different calculation types
    tab_selection = st.sidebar.radio(
        "Seleccionar tipo de cálculo:",
        [
            "Esfuerzo Vertical Rectangular",
            "Esfuerzo Vertical Continua",
            "Esfuerzo Vertical Circular",
            "Esfuerzo Vertical Anular",
            "Esfuerzo Vertical Terraplén"
        ],
        index=0
    )

    # Display the appropriate interface based on selection
    if tab_selection == "Esfuerzo Vertical Rectangular":
        boussinesq_interface()
    elif tab_selection == "Esfuerzo Vertical Continua":
        esfuerzo_vertical_continua()
    elif tab_selection == "Esfuerzo Vertical Circular":
        esfuerzo_vertical_circular()
    elif tab_selection == "Esfuerzo Vertical Anular":
        esfuerzo_vertical_anular()
    elif tab_selection == "Esfuerzo Vertical Terraplén":
        esfuerzo_vertical_terraplen()


if __name__ == "__main__":
    main()
