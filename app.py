"""
Geotechnical Tools - Simple Streamlit App
Aplicación para análisis de datos geotécnicos
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from Tools import save_cache, load_cache
from calculations import (
    get_cache_hash,
    compute_boussinesq_cached,
    create_xz_plot,
    create_yz_plot,
    create_depth_profile_plot,
    generate_pdf_report
)


def boussinesq_interface():
    """Render Boussinesq calculation interface in sidebar and main content"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Boussinesq (Rectángulo)")

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


def main():
    """Main application function"""
    st.set_page_config(
        page_title="Geotechnical Tools",
        page_icon="🏗️",
        layout="wide"
    )

    # Sidebar
    st.sidebar.title("🏗️ Geotechnical Tools")

    # Add mode selector
    mode = st.sidebar.radio(
        "Seleccionar herramienta:",
        ["Análisis CSV", "Boussinesq (Esfuerzos Verticales)"],
        index=0
    )

    if mode == "Boussinesq (Esfuerzos Verticales)":
        # Boussinesq interface
        boussinesq_interface()
    else:
        # Original CSV analysis interface
        st.sidebar.markdown("---")
        st.sidebar.info(
            "Herramientas para el análisis de datos geotécnicos.\n\n"
            "Sube un archivo CSV para comenzar."
        )

        # Main content
        st.title("Análisis de Datos Geotécnicos")
        st.markdown("Sube un archivo CSV para visualizar y analizar tus datos.")

        # File uploader
        uploaded_file = st.file_uploader(
            "Selecciona un archivo CSV",
            type=['csv'],
            help="Sube un archivo CSV con tus datos geotécnicos"
        )

        if uploaded_file is not None:
            try:
                # Read CSV file
                df = pd.read_csv(uploaded_file)

                # Display file info
                st.success(f"Archivo cargado exitosamente: {uploaded_file.name}")
                st.info(f"Dimensiones: {df.shape[0]} filas × {df.shape[1]} columnas")

                # Create tabs for different views
                tab1, tab2, tab3 = st.tabs(["📊 Vista Tabular", "📈 Gráficos", "ℹ️ Información"])

                with tab1:
                    st.subheader("Vista de Datos")
                    st.dataframe(df, use_container_width=True)

                    # Display basic statistics
                    if st.checkbox("Mostrar estadísticas descriptivas"):
                        st.subheader("Estadísticas Descriptivas")
                        st.dataframe(df.describe(), use_container_width=True)

                with tab2:
                    st.subheader("Visualización de Datos")

                    # Get numeric columns
                    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

                    if len(numeric_cols) >= 2:
                        col1, col2 = st.columns(2)

                        with col1:
                            x_axis = st.selectbox("Selecciona eje X", numeric_cols, key="x")
                        with col2:
                            y_axis = st.selectbox(
                                "Selecciona eje Y",
                                numeric_cols,
                                index=1 if len(numeric_cols) > 1 else 0,
                                key="y"
                            )

                        # Plotly scatter plot
                        st.subheader("Gráfico de Dispersión (Plotly)")
                        fig_plotly = px.scatter(
                            df,
                            x=x_axis,
                            y=y_axis,
                            title=f"{y_axis} vs {x_axis}"
                        )
                        st.plotly_chart(fig_plotly, use_container_width=True)

                        # Matplotlib plot
                        st.subheader("Gráfico de Línea (Matplotlib)")
                        fig, ax = plt.subplots(figsize=(10, 6))
                        ax.plot(df[x_axis], df[y_axis], marker='o', linestyle='-', alpha=0.7)
                        ax.set_xlabel(x_axis)
                        ax.set_ylabel(y_axis)
                        ax.set_title(f"{y_axis} vs {x_axis}")
                        ax.grid(True, alpha=0.3)
                        st.pyplot(fig)

                    elif len(numeric_cols) == 1:
                        st.warning("Se necesitan al menos 2 columnas numéricas para generar gráficos de dispersión.")
                        # Show histogram for single numeric column
                        st.subheader(f"Histograma de {numeric_cols[0]}")
                        fig_hist = px.histogram(df, x=numeric_cols[0])
                        st.plotly_chart(fig_hist, use_container_width=True)
                    else:
                        st.warning("No se encontraron columnas numéricas en el archivo.")

                with tab3:
                    st.subheader("Información del Dataset")

                    # Column information
                    st.write("**Columnas:**")
                    col_info = pd.DataFrame({
                        'Columna': df.columns,
                        'Tipo': df.dtypes.astype(str),
                        'Valores No Nulos': df.count(),
                        'Valores Nulos': df.isnull().sum()
                    })
                    st.dataframe(col_info, use_container_width=True)

            except Exception as e:
                st.error(f"Error al procesar el archivo: {str(e)}")
        else:
            st.info("👆 Por favor, sube un archivo CSV para comenzar el análisis.")


if __name__ == "__main__":
    main()
