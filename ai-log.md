# AI log - Equipo Trío Tristeza

## Herramientas
- **Gemini CLI**: Interfaz de línea de comandos para interactuar con Gemini Pro.
- **Claude Code (claude-sonnet-4-6)** Interfaz de línea de comandos para interactuar con Claude.

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

### 2026-04-12 | Gemini CLI | Procesamiento Eficiente del Censo por Manzanas (ITER)
- **Tarea**: Realizar una revisión y unificación del Censo de Población 2020 por manzanas con su capa geométrica, optimizando el uso de memoria para variables de sexo y edad.
- **Prompt**: "quiero que me ayudes a analizar el insusmo del censo de población por manzanas, estoy teniendo problemas para integrarlo por medio de la clave manzana con el insumo de geometrías"
- **Resultado**: Implementación de un flujo de procesamiento que lee el archivo tabular nacional de forma fragmentada (chunks) directamente desde el ZIP, filtra por CDMX y limpia valores no numéricos ('*').
- **Decisión**: Ante la solicitud de una integración más adecuada, se propuso e implementó la carga por **chunks** (fragmentos) para manejar el gran volumen de datos del ITER nacional sin saturar la memoria. Se utilizó la inspección previa del archivo para asegurar la unión correcta con la capa de geometrías de manzanas mediante la clave manzanas.

### 2026-04-13 | ChatGPT | Expresión para calcular campos
- **Tarea**: Realizar la revisión y ajuste al código para categorizar las vialidades por cadenas de texto.
- **Prompt**: "¿cómo puedo hacer que el siguiente código funcione?"
- **Resultado**: "Expresión recomendada y alternativa más compacta."
- **Decisión**:  "Debido a la presentación de la propuesta de código, se incorporo esta en un CASE"

### 2026-04-13 | Gemini | Creación de plantilla para metadatos
- **Tarea**: Realizar la plantilla que conforma a los metadatos de los archivos geográficos ".gpkg" en un ".json".
- **Prompt**: "Quiero generar una estructura de metadato en un archivo json"
- **Resultado**: "Estructura recomendada y guía de los campos del metadato."
- **Decisión**: "La estructura principal nos oriento a decidir como estructurar mejor los metadatos de las capas"

### 2026-04-14 | Claude Code (claude-sonnet-4-6) | Estilización de la visualización de indicadores ODS 11
- **Tarea**: Integrar y estilizar la visualización interactiva de los indicadores ODS 11 en el dashboard principal.
- **Prompt**: "¿puedes apoyarme para estilizar la visualización de indicadores?"
- **Resultado**: Propuesta de inclusión de una sección interactiva en el dashboard con gráficas de barras horizontales para cada indicador ODS 11, navegación con botones de flechas, panel de texto descriptivo reactivo y etiquetas de posicionamiento de la CDMX frente al promedio nacional.
- **Decisión**: Se decidió aceptar la propuesta de modificación de estilo, integrando la visualización dentro del flujo de scrollytelling del dashboard de forma que el panel izquierdo alterna entre la gráfica de indicadores y el mapa de accesibilidad según la sección visible.

### 2026-04-14 | Claude Code (claude-sonnet-4-6) | Corrección del flujo de despliegue continuo
- **Tarea**: Corregir el workflow de GitHub Actions tras cambios en la estructura del directorio `dashboard/`.
- **Prompt**: "¿puedes apoyarme a corregir el despliegue continuo, cambié la estructura de dashboard y ahora tiene fallo?"
- **Resultado**: Se actualizaron los archivos correspondientes al flujo de CI/CD: se corrigió la ruta de copia del dashboard de `dashboard/_site/*` a los artefactos renderizados in-place (`index.html`, `index_files/`, `styles.css`, `datos/`), y se añadió la variable de entorno `QUARTO_PYTHON` para que Quarto utilice el entorno virtual de `uv` con las dependencias del proyecto.
- **Decisión**: Se aceptaron los cambios validando que corresponden a la estructura actual del directorio `dashboard/`, donde `format: html` genera archivos en el mismo directorio en lugar de un subdirectorio `_site/`.

### 2026-04-21 | Claude Code (claude-sonnet-4-6) | Generación de metadatos para las etapas 3 y 4
- **Tarea**: Generar una entrada de metadatos que describa el procedimiento de creación de los archivos de cruce de accesibilidad (etapa 3) y de clasificación por manzana (etapa 4).
- **Prompt**: "utilizando como base lo descrito en los scripts `asignar_geometrias.py` y `cruce_accesibilidad.py`, apóyame a generar una propuesta de entrada en el archivo de metadatos que describa el procedimiento de creación de los archivos de las etapas 3 y 4".
- **Resultado**: Se generó una propuesta de entrada en `METADATOS.md` como ítem 21, con la descripción completa del procedimiento, las fuentes, las variables, el índice de diversidad y la metodología de clasificación, siguiendo la estructura del resto del documento.
- **Decisión**: Se adaptó la propuesta ajustando las rutas de los archivos de entrada y salida a las rutas reales del proyecto, conservando la estructura general propuesta por la IA.

### 2026-04-21 | Claude Code (claude-sonnet-4-6) | Generación de metadatos para la división por colonias (Etapa 4 — Colonias)
- **Tarea**: Generar una entrada de metadatos que describa el procedimiento de creación de los archivos de división por colonias y el índice para el dashboard.
- **Prompt**: "puedes darme una propuesta de entrada de metadatos para los datos de `datos/procesados/procesados_4_etapa/colonias` para la generación de metadatos".
- **Resultado**: Se generó un propuesta de entrada en `METADATOS.md` como ítem 22, con la propuesta de descripción de la división por colonia, la normalización de nombres de archivo, la organización en directorios por alcaldía y la generación del `index.json` para selección en cascada en el dashboard.
- **Decisión**: Se aceptó la propuesta sin modificaciones, ya que las rutas y la estructura corresponden directamente a los archivos generados por `scripts/dividir_colonias.py`.

### 2026-04-21 | Claude Code (claude-sonnet-4-6) | Integración del índice de colonias para filtrado en el mapa
- **Tarea**: Integrar el índice generado para la búsqueda de colonias por alcaldía y aplicarlo para una búsqueda eficiente en el mapa del dashboard.
- **Prompt**: "¿puedes ayudarme a integrar el index que he generado para la búsqueda de colonias por alcaldía para hacer una búsqueda eficiente en el mapa?"
- **Resultado**: Propuesta de aplicación del algoritmo de filtrado usando el `index.json` para la selección en cascada alcaldía → colonia, con carga dinámica del GeoJSON correspondiente para la visualización por filtro en el mapa, y texto descriptivo de la funcionalidad de la sección.
- **Decisión**: Se aceptó la propuesta de filtrado y se añadió visualización de categorías por medio de una paleta de colores Color Brewer. El texto descriptivo se dejó por ahora pero se modificará más adelante con una adecuación técnica.

### 2026-04-21 | Claude Code (claude-sonnet-4-6) | Migración del panel de accesibilidad a Observable JS
- **Tarea**: Reemplazar el bloque `{=html}` del panel de accesibilidad (que incluía etiquetas `<script src>` y `<link>` externas) por una celda `{ojs}` equivalente, compatible con el entorno de seguridad de Quarto.
- **Prompt**: "puedes darme la versión más adecuada del quarto que no incluya `{=html}`... tendremos que sacrificar esa funcionalidad de cambio de zoom y solo dejar la máxima resolución por colonia al seleccionar la colonia".
- **Resultado**: Se migró el bloque completo del mapa de accesibilidad a una celda `{ojs}` que carga Leaflet vía `require('leaflet@1.9.4')` e inyecta su CSS en `document.head`. La lógica simplificada muestra: CDMX completa sin selección, colonias simplificadas al seleccionar alcaldía, y manzanas al seleccionar colonia. Se añadió la regla CSS `display: contents` en `styles.css` para que el div envolvente de OJS sea transparente al layout flex del panel.
- **Decisión**: Se sacrificó la funcionalidad de cambio automático de resolución por nivel de zoom, conservando únicamente la resolución máxima (manzanas) al seleccionar una colonia específica. Se mantuvo el script de scrollytelling como `{=html}` ya que no carga recursos externos.

### 2026-04-24 | Claude Code (claude-sonnet-4-6) | Actualización de la estructura del repositorio en el README
- **Tarea**: Actualizar el archivo `README.md` para reflejar la estructura real y actualizada del repositorio tras los cambios recientes.
- **Prompt**: "puedes actualizar la estructura del repositorio con todos los nuevos cambios desde la última versión".
- **Resultado**: Se entregó una propuesta de estructura de árbol de directorios con descripción de cada componente, incluyendo la nueva carpeta `docs/` como salida del render de Quarto, el archivo `_quarto.yml` en `dashboard/`, el desglose de las etapas de procesamiento de datos, los scripts de generación de vistas e insumos para el dashboard, y las dependencias actualizadas (`esda`, `libpysal`). Se actualizaron además las instrucciones de "Cómo empezar" y la sección de despliegue.
- **Decisión**: Se revisó, verificó y aprobó la propuesta de estructura sin modificaciones, ya que corresponde fielmente al estado actual del repositorio.

### 2026-04-24 | Claude Code (claude-sonnet-4-6) | Actualización de metadatos para las etapas 5 y preparación del dashboard
- **Tarea**: Actualizar el archivo `METADATOS.md` con las entradas faltantes correspondientes a la etapa 5 (autocorrelación espacial) y los scripts de preparación de datos para el dashboard.
- **Prompt**: "puedes actualizar el archivo de metadatos con los cambios realizados en las fases 4 y 5 que no estén registrados usando los scripts como base de los procedimientos".
- **Resultado**: Se inspeccionaron los scripts `calcular_moran_lisa.py`, `generar_vistas_clasificacion.py`, `generar_vista_moran.py`, `generar_resumenes_dashboard.py`, `generar_resumen_insumos.py` y `generar_mapas_estaticos.py` para detallar con precisión cada procedimiento. Se generaron 6 nuevas entradas (items 23–28) en `METADATOS.md` que documentan: el análisis LISA con KNN k=8 y clasificación de cuadrantes, las vistas GeoJSON simplificadas en tres niveles, los resúmenes JSON por alcaldía y colonia, el conteo de insumos y los mapas PNG estáticos.
- **Decisión**: Se aprobó la propuesta al validar la concordancia con los procedimientos empleados en cada script, sin necesidad de modificaciones.

### 2026-04-24 | Claude Code (claude-sonnet-4-6) | Generación de mapas estáticos con simbología equivalente a los mapas dinámicos
- **Tarea**: Generar mapas estáticos a nivel colonia con la misma simbología de los mapas interactivos para incluirlos como alternativa de visualización en el dashboard.
- **Prompt**: "puedes apoyarme a generar una propuesta de script que genere mapas estáticos a nivel manzana con la misma simbología de los mapas dinámicos pero con mayor detalle y líneas de contorno transparentes".
- **Resultado**: Propuesta del script `generar_mapas_estaticos.py` que genera imágenes PNG para los mapas de colonias clasificadas y de I de Moran Local (LISA), con paletas de color equivalentes a las de los mapas dinámicos, bordes de alcaldía con línea gris oscura delgada, etiquetas de alcaldía con halo blanco en el centroide y leyenda. Se generó además `generar_vista_moran.py` para simplificar el GeoJSON de Moran a nivel colonia, insumo del mapa estático.
- **Decisión**: Se adoptó la propuesta integrando los mapas estáticos como pestaña adicional junto a los mapas dinámicos en la sección "Nuestra propuesta" del dashboard. Se añadió un título flotante a los mapas interactivos y un título de figura a los estáticos para mantener consistencia visual. El intento de eliminar los contornos entre polígonos de manzana no fue resuelto completamente, ya que matplotlib mantiene hairlines de antialiasing entre polígonos adyacentes independientemente de los parámetros `edgecolor`, `linewidth` y `set_antialiased` aplicados a las colecciones.
