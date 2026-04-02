# trío tristeza ODS

Este proyecto tiene como objetivo el análisis y la visualización de datos relacionados con los **Objetivos de Desarrollo Sostenible (ODS)**. Utiliza un enfoque basado en Python para el procesamiento de datos y **Quarto** para la generación de un tablero de control (dashboard) interactivo.

## Características principales

- **Análisis de Datos:** Procesamiento y limpieza de datos mediante `pandas`.
- **Geolocalización:** Visualización de indicadores en mapas interactivos con `folium` y `geopandas`.
- **Dashboard Interactivo:** Generación de un sitio web estático pero dinámico utilizando `Quarto`.
- **Visualización:** Gráficos avanzados con `plotly` y `matplotlib`.

## Estructura del proyecto

- `dashboard/`: Archivos fuente del sitio web Quarto.
- `datos/`:
  - `crudos/`: Datos originales sin procesar.
  - `procesados/`: Datos limpios y listos para el dashboard.
- `notebooks/`: Espacio para cuadernos Jupyter de exploración y análisis.
- `scripts/`: Scripts de Python para automatización y procesamiento.
- `main.py`: Script orquestador para la ejecución del flujo de datos.

## Cómo empezar

Este proyecto utiliza `uv` para la gestión de dependencias. Para configurar el entorno:

1. Instala `uv` si aún no lo tienes.
2. Sincroniza las dependencias:
   ```bash
   uv sync
   ```
3. Para renderizar el dashboard:
   ```bash
   cd dashboard
   quarto render
   ```

