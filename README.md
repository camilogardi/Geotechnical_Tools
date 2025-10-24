# Geotechnical_Tools 🏗️

Repositorio con herramientas para el análisis de geotecnia

## Descripción

Esta aplicación web proporciona herramientas interactivas para realizar análisis geotécnicos básicos. Desarrollada con Streamlit, ofrece una interfaz amigable para cálculos relacionados con:

- 📊 **Capacidad Portante**: Cálculo de capacidad portante de cimentaciones superficiales utilizando diferentes teorías (Terzaghi, Meyerhof, Hansen, Vesic)
- 📉 **Asentamientos**: Análisis de asentamientos en suelos cohesivos (consolidación) y granulares (elásticos)
- 🔬 **Clasificación de Suelos**: Clasificación según el Sistema Unificado de Clasificación de Suelos (SUCS/USCS)

## Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/camilogardi/Geotechnical_Tools.git
cd Geotechnical_Tools
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Para ejecutar la aplicación:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador predeterminado en `http://localhost:8501`

## Estructura del Proyecto

```
Geotechnical_Tools/
├── app.py                          # Aplicación principal
├── requirements.txt                # Dependencias del proyecto
├── .gitignore                      # Archivos a ignorar en git
├── README.md                       # Este archivo
├── .streamlit/
│   └── config.toml                 # Configuración de Streamlit
├── pages/
│   ├── 1_📊_Capacidad_Portante.py  # Página de capacidad portante
│   ├── 2_📉_Asentamientos.py       # Página de asentamientos
│   └── 3_🔬_Clasificación_Suelos.py # Página de clasificación de suelos
├── utils/
│   ├── __init__.py
│   └── geotechnical_calcs.py       # Funciones de cálculo geotécnico
└── data/                           # Directorio para datos (vacío por ahora)
```

## Características

### Capacidad Portante
- Cálculo de factores de capacidad portante (Nc, Nq, Nγ)
- Factores de forma para cimentaciones rectangulares
- Visualización interactiva de resultados
- Gráficos de variación con parámetros del suelo

### Asentamientos
- **Suelos Cohesivos**: Análisis de consolidación (primaria) con curvas e-log σ'
- **Suelos Granulares**: Cálculo de asentamiento elástico inmediato
- Consideración de estados de consolidación (NC, OC)
- Visualizaciones interactivas

### Clasificación de Suelos
- Sistema SUCS (USCS) completo
- Carta de plasticidad interactiva
- Análisis granulométrico visual
- Cálculo automático de índices (Cu, Cc, IP)

## Tecnologías Utilizadas

- **Python 3.x**: Lenguaje de programación principal
- **Streamlit**: Framework para la aplicación web
- **Pandas**: Manipulación de datos
- **NumPy**: Cálculos numéricos
- **Plotly**: Visualizaciones interactivas
- **Matplotlib**: Gráficos adicionales
- **SciPy**: Cálculos científicos

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz un fork del proyecto
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## Notas Importantes

⚠️ **Advertencia**: Esta aplicación proporciona herramientas de análisis geotécnico básico con fines educativos y de referencia. Para diseños finales y proyectos de ingeniería real, siempre consulte con un ingeniero geotécnico profesional licenciado.

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Autor

Camilo Gardi

## Contacto

Para preguntas, sugerencias o reportar problemas, por favor abre un issue en este repositorio.
