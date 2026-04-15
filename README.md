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
- `geopandas`: Visualización de archivos espaciales
- `folium`: Mapas interactivos
- `plotly` y `matplotlib`: Visualización de datos
- `mapclassify`: Clasificación de variables espaciales
- `jupyter` / `notebook`: Exploración y desarrollo del análisis

Todo el entorno es gestionado mediante `uv` para garantizar reproducibilidad.

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

## Referencias
* Moreno, C., Allam, Z., Chabaud, D., Gall, C., & Pratlong, F. (2021). Introducing the “15-Minute City”: Sustainability, Resilience and Place Identity in Future Post-Pandemic Cities. Smart Cities, 4(1), 93-111. https://doi.org/10.3390/smartcities4010006

* Ziccardi, A. y Dammert, M.  (2021). Las desigualdades urbanasy el derecho a la ciudad. Desacatos, (67), pp. 82-91.



## Licencia

Este proyecto está bajo la licencia **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

