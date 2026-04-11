# AI log - Equipo Trío Tristeza

## Herramientas
- **Gemini CLI**: Interfaz de línea de comandos para interactuar con Gemini Pro.

## Filosofía de uso 
Utilizamos herramientas de IA para agilizar la descripción de la arquitectura del proyecto y la consulta sobre el uso de parámetros en distintas librerías para facilitar su uso.

## Registro de uso

### 2026-04-02 | Gemini CLI | Creación de README y Definición de Estructura
- **Tarea**: Crear una descripción del proyecto y estructurar los directorios de datos y análisis.
- **Prompt**: "puedes añadir una descripción al readme que explique brevemente de que trata el proyecto".
- **Resultado**: README.md completo con instrucciones de uso y estructura de directorios optimizada (`datos/crudos`, `datos/procesados`, `notebooks`).
- **Decisión**: Se decidió ajustar la estructura del documento en secciones para facilitar la lectura y explicación breve del proyecto. También se añadió una sección de "Cómo empezar" con `uv`, para describir brevemente como levantar el proyecto.

### 2026-04-02 | Gemini CLI | Estructura de Presentación con Quarto
- **Tarea**: Crear la estructura general de una presentación de diapositivas utilizando Quarto.
- **Prompt**: "puedes usar el directorio presentacion para hacer crear la estrcutura de un proyecto quarto que permita la visualización de una presentación de diapositivas con quarto".
- **Resultado**: Propuesta de construcción de poryecto quarto dentro de `presentacion/` con archivo `index.qmd` estructurado y propuesta de configuración de estilo.
- **Decisión**: Se utilizó la IA para facilitar la creación de la estructura base y posteriormente se realizaron modificaciones manuales sobre el estilo y el contenido específico de las diapositivas para adaptarlo a la narrativa del equipo.

### 2026-04-02 | Gemini CLI | Configuración de CI/CD para GitHub Pages
- **Tarea**: Configurar la integración continua para publicar automáticamente el dashboard y la presentación.
- **Prompt**: "puedes ayudarme a configurar dos sitios github pages uno para el dashboard y otr para la presentacion que funcionen con integracion continua".
- **Resultado**: Archivo `.github/workflows/publish.yml` configurado para renderizar ambos proyectos con Quarto y desplegarlos en `https://trio-tristeza.github.io/hackods-unam/` y `/presentacion/`.
- **Decisión**: Se optó por centralizar el despliegue en un solo flujo de trabajo de GitHub Actions para mayor eficiencia. Se configuró el Dashboard en el root y la presentación en una subcarpeta para mantener la organización.

### 2026-04-10 | Gemini CLI | Función Robusta de Carga de Capas Espaciales
- **Tarea**: Implementar la carga de insumos espaciales directamente de carpetas comprimidas.
- **Prompt**: "ayudarme a crear un funcion para buscar archivos shp en capas comprimidas donde no pueda utilizar directamente la carga zip con pandas o geopandas por el metodo de compresion original del archivo".
- **Resultado**: Creación e integración de la función `cargarCapaComprimida` en `notebooks/carga_insumos.ipynb`, la cual resuelve dinámicamente rutas internas en archivos ZIP (incluyendo subcarpetas y metadatos de macOS).
- **Decisión**: Se decidió utilizar esta función para todos los insumos espaciales, ajustando los parámetros de entrada según las rutas de los archivos definidas en el proyecto ante diferentes estructuras de compresión.

### 2026-04-10 | Gemini CLI | Unificación del Catastro CDMX
- **Tarea**: Consolidar la información fragmentada del Catastro por alcaldías.
- **Prompt**: "como podría general la unificación de los disntintos archivos de catastro de la cdmx, dividos por alcaldia, que al tener tanta información dificulta su análsis, podrías darme el flujo base para generar una búsqueda recursiva en la ruta especificada para cada zip".
- **Resultado**: Propuesta de ciclo de carga que localiza y concatena los 16 archivos ZIP de catastro.
- **Decisión**: Se decidió usar la base del ciclo resultante y se ajustó para procesar, limpiar y unir todo en un solo archivo `catastro_unificado_cdmx.gpkg` en la carpeta de procesados para optimizar futuros análisis.

### 2026-04-11 | Gemini CLI | Corrección de Codificación en Nombres de Hospitales
- **Tarea**: Encontrar caracteres raros o inválidos en nombres de hospitales.
- **Prompt**: "tengo una lista de nombres de hospitales con errores de codificación, ayudame a crear una función en python para que los detecte y corrija".
- **Resultado**: Una función en Python que detecta y corrige errores de codificación en cadenas de texto.
- **Decisión**: Se decidió modificar el campo "nombre" que contiene los caracteres y se aplicó la función con los errores encontrados para limpiar los datos.

### 2026-04-11 | Gemini CLI | Espacialización de CSV con GeoJSON
- **Tarea**: Espacializar un archivo CSV que contiene una columna geo_shape con geometrías válidas en formato GeoJSON para exportarlo como GeoPackage.
- **Prompt**: "tengo un csv de áreas verdes con una columna geo_shape en formato geojson, como lo convierto a geodataframe y lo exporto como gpkg".
- **Resultado**: Se usó json.loads() con shape() de shapely para parsear la columna geo_shape y construir un GeoDataFrame con crs EPSG:4326.
- **Decisión**: Se decidió hacer uso de shapely ya que se intentó usar geopandas con gpd.read_file() pero no soportaba la geometría a través de un csv.
