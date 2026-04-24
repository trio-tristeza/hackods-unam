# Trío Tristeza ODS

Análisis geoespacial de accesibilidad urbana en la Ciudad de México bajo el enfoque de la **ciudad de 15 minutos**, con el objetivo de evaluar el cumplimiento del **ODS 11** (ciudades inclusivas, seguras y sostenibles)

Este proyecto tiene como objetivo el análisis y la visualización de datos para realizar una evaluación de la accesibilidad en la Ciudad de México. Buscando identificar las zonas de la CDMX en las que vivir, trabajar y descansar pueda suceder en en recorridos de menos de 15 minutos (Moreno, 2021) y a partir de la interpretación de este análisis identificar la asimetría urbana (Ziccardi y Dammert, 2021) relacionada con la movilidad, la inclusividad y la sostenibilidad y con ello visibilizar las relaciones espaciales de inclusividad, seguridad, resiliencia y sostenibilidad; para con ello responder a la pregunta:

> ¿Qué tan cercana está la Ciudad de México de cumplir las metas del ODS 11 para convertirse en un espacio donde la movilidad, la seguridad, la inclusividad, y la sostenibilidad sean un derecho y no un privilegio?

### ODS 11

El ODS 11 nos interesa porque, pensamos que las ciudades como espacios sociales, deberían pensarse, planearse y vivirse como entornos equitativos, de visibilización y de justicia espacial; para lograr que la inclusión, la movilidad, la seguridad, la resiliencia y la sostenibilidad se conviertan en un derecho y no un privilegio.

### ¿Qué queremos visibilizar con los datos?

Buscamos visibilizar procesos de asimetría urbana, relacionados con la movilidad, la seguridad, la inclusividad y la sostenibilidad. Tomando como base la propuesta de la **ciudad de 15 minutos** ; donde describe un modelo que busca repensar las ciudades en las que vivir, trabajar y descansar pueda suceder en recorridos de menos de 15 minutos, ya sea a pie o en bicicleta, desde el hogar (Moreno, 2021)

A partir de realizar un cruce espacial de insumos de movilidad, demografía, accesibilidad, distancias del hogar a puntos de recreación y comercio, infraestructura peatonal y ciclista; buscamos identificar las zonas de la CD. MX. que podrían considerarse inclusivas, seguras, resilientes y sostenibles frente a los criterios de proximidad, digitalización, diversidad y densidad(Moreno, 2021) ; y, por lo tanto, propensos a cumplir las metas locales del ODS 11.

Tenemos la hipótesis de que el resultado de este análisis permitirá identificar y visibilizar relaciones espaciales de desigualdad estructural con accesos diferenciados, vinculados a dinámicas de exclusión producto de un modelo de desarrollo que busca el beneficio de las clases dominantes.

### Fuentes de datos y su pertinencia con el ODS

Las fuentes de datos consideradas para este análisis articulan información de distintas bases de datos que demuestran la complejidad urbana. 

El análisis se construye a partir de fuentes de datos públicas, oficiales y verificables, con el objetivo de garantizar la consistencia metodológica y la reproducibilidad del proyecto. Se priorizaron datasets provenientes de instituciones como:

* **Instituto Nacional de Estadística y Geografía (INEGI)**
* **Portal de datos abiertos del gobierno de la CDMX**
* **Sistema Nacional de Información de los Objetivos de Desarrollo Sostenible**

La selección de los datos responde a su pertinencia con el ODS 11, en su enfoque gacía ciudades inclusivas, seguras, resilientes y sostenibles. 

A manera de justificación metodológica, las variables fueron organizadas en cuatro dimensiones basadas en el modelo de la **ciudad de los 15 minutos (moreno, 2021)** cada dimensión representa una conjunción de variables claves en la interpretación del ODS 11

* **Proximidad**: Permite evaluar la accesibilidad física a servicios urbanos, elemento central del ODS 11
   Datasets:
   * Infraestructura ciclista 
   * Red de transporte
   * Red vial de la CDMX

* **Diversidad**: Representa la disponibilidad de servicios esenciales que determinan la habitabilidad urbana.
   Datasets:
   * Escuelas públicas y privadas
   * Hospitales y Centros de salud
   * Áreas verdes
   * Directorio Estadistico Nacional de Unidades Economicas (DENUE)

* **Densidad**: Permite identificar zonas de concentración poblacional y su relación con la presión sobre servicios urbanos.
   Datasets
   * Población por manzana (Censo, 2002)
   * Densidad habitacional

* **Digitalización**: Refleja condiciones de inclusión digital y acceso a servicios contemporáneos de movilidad.
   Datasets:
   * Puntis de acceso a WiFi público
   * Infraestructura de movilidad integrada

## Metadatos del proyecto

Accedaa la documentación completa de las fuentes de datos:

**[Presiona aquí para ver los Metadatos](.METADATOS.md)**


## Características principales

El proyecto implementa un flujo de trabajo geoespacial basado en Python para el procesamiento, análisis y visualización de datos urbanos, integrando múltiples fuentes para evaluar la accesibilidad en la Ciudad de México bajo el enfoque de la ciudad de 15 minutos.

El análisis se estructura en distintas etapas:

#### Procesamiento y preparación de datos
* Limpieza, transformación y estandarización de datos con `pandas`y `geopandas`
* Integración de múltiples fuentes (INEGI, datos abiertos CDMX)
* Generación de datasets estructurados para análisis espacial

#### Analisis geoespacial
* Manejo de datos vectoriales con `geopandas`
* Cálculo de proximidad y relaciones espaciales
* Clasificación de variables mediante `mapclassify`
* Cruce espacial de indicadores para identificar patrones territoriales

#### Visualización y análisis exploratorio
* Generación de gráficos estadísticos con `matplotlib` y `plotly`
* Análisis exploratorio de variables urbanas

#### Cartografía interactiva 
* Creación de mapas interactivos con `folium`
* Visualización de indicadores espaciales por estado

#### Dashborad y visualización de resultados
* Desarrollo de un dashboard interactivo con **Quarto**
* Integración de mapas, gráficos y narrativa analítica

## Tecnologias utilizadas
El proyecto utiliza las siguientes librerías principales:

- `pandas`: procesamiento y análisis de datos
- `geopandas`: manejo de datos vectoriales y análisis espacial
- `folium`: mapas interactivos
- `plotly` y `matplotlib`: visualización de datos
- `mapclassify`: clasificación de variables espaciales
- `esda` y `libpysal`: autocorrelación espacial (I de Moran Local — LISA)
- `jupyter` / `notebook`: exploración y desarrollo del análisis

Todo el entorno es gestionado mediante `uv` para garantizar reproducibilidad.

## Estructura del proyecto

```text
.
├── .github/
│   └── workflows/
│       └── publish.yml          # CI/CD: renderizado y despliegue a GitHub Pages
├── dashboard/                   # Fuente del dashboard Quarto
│   ├── _quarto.yml              # Configuración de Quarto (salida → docs/)
│   ├── index.qmd                # Dashboard principal (4 secciones)
│   ├── styles.css               # Estilos del dashboard
│   └── datos/                   # Datos pre-procesados para el dashboard
│       ├── ods11_final.json         # Indicadores ODS 11 por entidad
│       ├── resumen_alcaldias.json   # Accesibilidad agregada por alcaldía
│       ├── resumen_colonias.json    # Accesibilidad agregada por colonia
│       ├── resumen_insumos.json     # Conteo de registros por insumo
│       ├── mapas/                   # Mapas PNG estáticos
│       │   ├── mapa_colonias.png
│       │   └── mapa_moran.png
│       └── vistas/                  # GeoJSONs simplificados para mapas interactivos
│           ├── colonias/            # GeoJSON por alcaldía (clasificación por colonia)
│           ├── vista_alcaldias.geojson
│           ├── vista_moran_alcaldias.geojson
│           └── vista_moran_colonias.geojson
├── docs/                        # Salida del render (publicada en GitHub Pages)
│   ├── index.html               # Dashboard compilado
│   ├── index_files/             # Dependencias JS/CSS generadas por Quarto
│   ├── datos/mapas/             # Imágenes estáticas referenciadas por el dashboard
│   └── styles.css
├── presentacion/                # Diapositivas en Quarto (RevealJS)
│   ├── index.qmd
│   └── _site/                   # Presentación compilada
├── datos/                       # Datos del proyecto
│   ├── crudos/                  # Datos originales sin procesar
│   └── procesados/              # Capas procesadas por etapa
│       ├── procesados_1_etapa/  # Insumos base (catastro, manzanas, DENUE…)
│       ├── procesados_2_etapa/  # Insumos temáticos (transporte, escuelas, WiFi…)
│       ├── procesados_2.5_etapa/# Indicadores ODS 11 (JSON)
│       ├── procesados_3_etapa/  # Cruces de accesibilidad por alcaldía
│       ├── procesados_4_etapa/  # Clasificación de manzanas + división por colonia
│       └── procesados_5_etapa/  # Análisis de autocorrelación (I de Moran LISA)
├── notebooks/                   # Cuadernos Jupyter para exploración
├── scripts/                     # Scripts Python de automatización
│   ├── cruce_accesibilidad.py       # Cálculo de accesibilidad por manzana (Dijkstra)
│   ├── asignar_geometrias.py        # Asignación de geometrías y clasificación
│   ├── dividir_colonias.py          # División de resultados por colonia
│   ├── calcular_moran_lisa.py       # Autocorrelación espacial (I de Moran)
│   ├── generar_indicadores_ods11.py # Consulta a la API BISE de INEGI
│   ├── generar_vistas_clasificacion.py  # GeoJSONs simplificados por alcaldía
│   ├── generar_vista_moran.py       # GeoJSONs del análisis LISA
│   ├── generar_mapas_estaticos.py   # PNG de colonias y Moran para el dashboard
│   ├── generar_resumen_insumos.py   # JSON de conteo de registros por insumo
│   └── generar_resumenes_dashboard.py # JSONs de resumen por alcaldía y colonia
├── main.py                      # Script orquestador del flujo
├── pyproject.toml               # Dependencias del proyecto (gestionadas con uv)
├── ai-log.md                    # Registro de uso de Inteligencia Artificial
├── METADATOS.md                 # Linaje y documentación de cada fuente de datos
├── LICENSE                      # Licencia Creative Commons CC BY-SA 4.0
└── README.md                    # Documentación del proyecto
```

## Cómo empezar

Este proyecto utiliza `uv` para la gestión de dependencias. Para configurar el entorno:

1. Instala `uv` si aún no lo tienes.
2. Sincroniza las dependencias:
   ```bash
   uv sync
   ```
3. Para renderizar el dashboard (la salida se genera en `docs/`):
   ```bash
   cd dashboard
   uv run quarto render index.qmd
   ```

## Despliegue

El proyecto se publica automáticamente mediante GitHub Actions al hacer push a `main`. El workflow renderiza el dashboard (salida en `docs/`) y la presentación, y los despliega en:

- **Dashboard**: `https://trio-tristeza.github.io/hackods-unam/`
- **Presentación**: `https://trio-tristeza.github.io/hackods-unam/presentacion/`

## Referencias
* Moreno, C., Allam, Z., Chabaud, D., Gall, C., & Pratlong, F. (2021). Introducing the “15-Minute City”: Sustainability, Resilience and Place Identity in Future Post-Pandemic Cities. Smart Cities, 4(1), 93-111. https://doi.org/10.3390/smartcities4010006

* Ziccardi, A. y Dammert, M.  (2021). Las desigualdades urbanasy el derecho a la ciudad. Desacatos, (67), pp. 82-91.



## Licencia

Este proyecto está bajo la licencia **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

