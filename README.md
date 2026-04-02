# trío tristeza ODS

Este proyecto tiene como objetivo el análisis y la visualización de datos relacionados con los **Objetivos de Desarrollo Sostenible (ODS)**. Utiliza un enfoque basado en Python para el procesamiento de datos y **Quarto** para la generación de un tablero de control (dashboard) interactivo.

## Características principales

- **Análisis de Datos:** Procesamiento y limpieza de datos mediante `pandas`.
- **Geolocalización:** Visualización de indicadores en mapas interactivos con `folium` y `geopandas`.
- **Dashboard Interactivo:** Generación de un sitio web estático pero dinámico utilizando `Quarto`.
- **Visualización:** Gráficos avanzados con `plotly` y `matplotlib`.

## Estructura del proyecto

```text
.
├── .github/workflows/       # Automatización de despliegue (CI/CD)
├── dashboard/               # Archivos fuente del dashboard Quarto
├── presentacion/            # Diapositivas en Quarto (RevealJS)
├── datos/                   # Gestión de conjuntos de datos
│   ├── crudos/              # Datos originales sin procesar
│   └── procesados/          # Datos limpios para el dashboard
├── notebooks/               # Cuadernos Jupyter para exploración
├── scripts/                 # Scripts Python de automatización
├── main.py                  # Script orquestador del flujo
├── ai-log.md                # Registro de uso de Inteligencia Artificial
├── LICENSE                  # Licencia Creative Commons CC BY-SA 4.0
└── README.md                # Documentación del proyecto
```

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

## Despliegue

El proyecto se publica automáticamente mediante GitHub Actions en las siguientes rutas:
- **Dashboard**: `https://trio-tristeza.github.io/hackods-unam/`
- **Presentación**: `https://trio-tristeza.github.io/hackods-unam/presentacion/`

## Licencia

Este proyecto está bajo la licencia **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
Proyecto en desarrollo para el seguimiento de indicadores ODS.
