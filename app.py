"""
Geotechnical Tools - Simple Streamlit App
Aplicación para análisis de datos geotécnicos
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


def main():
    """Main application function"""
    st.set_page_config(
        page_title="Geotechnical Tools",
        page_icon="🏗️",
        layout="wide"
    )

    # Sidebar
    st.sidebar.title("🏗️ Geotechnical Tools")
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
