# Geotechnical Tools 🏗️

Repositorio con herramientas para el análisis de datos geotécnicos.

## Descripción

Aplicación web desarrollada con Streamlit para el análisis y visualización de datos geotécnicos. Permite cargar archivos CSV, visualizar datos en formato tabular y generar gráficos interactivos.

## Características

- 📤 Carga de archivos CSV
- 📊 Vista tabular de datos
- 📈 Gráficos interactivos con Plotly y Matplotlib
- 📋 Estadísticas descriptivas
- ℹ️ Información detallada del dataset
- 🧮 Cálculo de esfuerzos verticales con metodología de Boussinesq
  - Sobrecarga rectangular con superposición de cargas puntuales
  - Visualización interactiva (cortes X-Z, Y-Z, perfiles de profundidad)
  - Gestión de cache en disco y memoria
  - Exportación de resultados a PDF

## Instalación

### Requisitos Previos

- Python 3.11 o superior
- pip

### Instalación Local

1. Clona el repositorio:
```bash
git clone https://github.com/camilogardi/Geotechnical_Tools.git
cd Geotechnical_Tools
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
streamlit run app.py
```

4. Abre tu navegador en `http://localhost:8501`

## Uso con Docker

1. Construye la imagen:
```bash
docker build -t geotechnical-tools .
```

2. Ejecuta el contenedor:
```bash
docker run -p 8501:8501 geotechnical-tools
```

3. Abre tu navegador en `http://localhost:8501`

## Desarrollo

### Ejecutar Tests

```bash
pytest tests/ -v
```

### Ejecutar Linter

```bash
flake8 . --max-line-length=127
```

## Estructura del Proyecto

```
Geotechnical_Tools/
├── app.py                  # Aplicación principal Streamlit (interfaz UI)
├── calculations.py         # Funciones de cálculo y visualización
├── requirements.txt        # Dependencias del proyecto
├── Dockerfile             # Configuración Docker
├── README.md              # Este archivo
├── .gitignore            # Archivos ignorados por Git
├── Tools/                # Módulo de cálculos geotécnicos
│   ├── __init__.py
│   ├── Tools.py          # Funciones de Boussinesq
│   └── cache/            # Cache de resultados
├── tests/                # Tests del proyecto
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_calculations.py
│   ├── test_import.py
│   └── test_tools.py
└── .github/
    └── workflows/
        └── ci.yml        # Configuración CI/CD
```

## Organización del Código

El proyecto sigue una arquitectura de separación de responsabilidades:

### `app.py` - Interfaz de Usuario
Contiene exclusivamente el código de la interfaz Streamlit:
- Configuración de la página
- Widgets de entrada (sliders, botones, etc.)
- Orquestación de la UI
- Manejo de estado de la sesión
- Renderizado de resultados

### `calculations.py` - Lógica de Cálculo
Módulo de funciones puras para cálculos y visualizaciones:
- Generación de hashes de caché
- Cálculos de Boussinesq (wrapper con caché)
- Interpolación de valores
- Creación de gráficos (X-Z, Y-Z, perfiles)
- Generación de reportes PDF

Esta separación mejora:
- ✅ **Testabilidad**: funciones de cálculo independientes
- ✅ **Mantenibilidad**: lógica clara y organizada
- ✅ **Reutilización**: funciones pueden usarse en otros contextos

## Tecnologías

- **Streamlit**: Framework para aplicaciones web
- **Pandas**: Manipulación de datos
- **Matplotlib**: Gráficos estáticos
- **Plotly**: Gráficos interactivos
- **NumPy**: Cálculos numéricos
- **SciPy**: Interpolación y análisis científico
- **FPDF2**: Generación de reportes PDF
- **Pytest**: Framework de testing
- **Flake8**: Linter de código

## CI/CD

El proyecto incluye un pipeline de CI/CD con GitHub Actions que:
- Instala dependencias
- Ejecuta tests con pytest
- Ejecuta linter con flake8

## Licencia

Este proyecto es de código abierto.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Uso de la Herramienta de Boussinesq

### Metodología

La herramienta de Boussinesq calcula esfuerzos verticales (σz) generados por una sobrecarga rectangular sobre un medio elástico semi-infinito. Utiliza la solución de Boussinesq para cargas puntuales con superposición de subelementos.

### Parámetros de Entrada

- **q**: Sobrecarga superficial (kPa)
- **Lx, Ly**: Dimensiones de la carga rectangular (m)
- **Xmin, Xmax, Ymin, Ymax**: Límites del dominio de cálculo (m)
- **Zmax**: Profundidad máxima de análisis (m)
- **Nx, Ny, Nz**: Resolución de la malla de cálculo

### Visualizaciones Disponibles

1. **Corte X-Z**: Contorno de esfuerzos en un plano vertical paralelo al eje X
2. **Corte Y-Z**: Contorno de esfuerzos en un plano vertical paralelo al eje Y
3. **Perfil en profundidad**: Variación de σz con la profundidad en un punto (x,y)

### Gestión de Cache

Los resultados pueden guardarse en disco (formato .npz comprimido) para reutilización posterior:
- **Guardar cache**: Almacena X, Y, Z, sigma en `Tools/cache/`
- **Cargar cache**: Recupera resultados previamente calculados

### Exportación PDF

Genera un reporte PDF que incluye:
- Resumen de parámetros de entrada
- Lista de gráficas generadas
- Información sobre las visualizaciones creadas

### Notas de Rendimiento

- Costo computacional: O(Nx × Ny × Nz × mx × my)
- Para mallas grandes (>100,000 puntos), considerar reducir resolución
- Los cálculos se cachean automáticamente en memoria con `@st.cache_data`
- Discretización adaptativa de subelementos: mx = my = min(40, max(4, Nx/2))
