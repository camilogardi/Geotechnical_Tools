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
├── app.py                  # Aplicación principal Streamlit
├── requirements.txt        # Dependencias del proyecto
├── Dockerfile             # Configuración Docker
├── README.md              # Este archivo
├── .gitignore            # Archivos ignorados por Git
├── tests/                # Tests del proyecto
│   ├── __init__.py
│   └── test_app.py
└── .github/
    └── workflows/
        └── ci.yml        # Configuración CI/CD
```

## Tecnologías

- **Streamlit**: Framework para aplicaciones web
- **Pandas**: Manipulación de datos
- **Matplotlib**: Gráficos estáticos
- **Plotly**: Gráficos interactivos
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
