# Metadatos de Datos Procesados - ODS 11 CDMX

Este documento detalla el linaje de los datos y los pasos de procesamiento aplicados a los insumos crudos para generar las capas finales en formato GeoPackage (GPKG).

**Sistema de Referencia de Coordenadas (CRS) General:** EPSG:32614 (WGS 84 / UTM zone 14N)

---

## 1. Catastro Unificado CDMX
*   **Archivo:** `catastro_unificado_cdmx.gpkg`
*   **Fuente:** [Portal de Datos Abiertos CDMX / SIG CDMX](https://sig.cdmx.gob.mx/datos/descarga#d_datos_cat)
*   **Pasos de Procesamiento:**
    1.  **Unificación:** Se iteró sobre los 16 archivos ZIP correspondientes a cada una de las alcaldías de la Ciudad de México.
    2.  **Limpieza de Atributos:** Eliminación de la columna `fid` para evitar conflictos de exportación.
    3.  **Estandarización de CRS:** Conversión de cada capa individual al CRS de referencia antes de la concatenación.
    4.  **Concatenación:** Unión de los 16 GeoDataFrames en una sola capa continua.
    5.  **Exportación:** Guardado en formato GeoPackage con reproyección final a EPSG:32614.

## 2. Manzanas con Población (INEGI 2020)
*   **Archivo:** `manzanas_cdmx_poblacion.gpkg`
*   **Fuentes:** 
    *   Espacial: [Polígonos de Manzanas CDMX](https://datos.cdmx.gob.mx/dataset/poligonos-de-manzanas-de-la-ciudad-de-mexico)
    *   Tabular: [Censo de Población 2020 nacional por manzanas (INEGI)](https://ri.uaemex.mx/handle/20.500.11799/112105)
*   **Pasos de Procesamiento:**
    1.  **Filtrado Tabular:** Lectura por bloques (chunks) del censo nacional, filtrando solo la Entidad 09 (CDMX).
    2.  **Limpieza de Datos:** Conversión de caracteres especiales (`ï»¿`) y manejo de valores nulos o protegidos (`*` de INEGI) sustituyéndolos por `0` para permitir cálculos numéricos.
    3.  **Normalización de Claves:** Estandarización de la columna `CVEGEO` a 16 dígitos en ambas fuentes (espacial y tabular) para asegurar la coincidencia.
    4.  **Unión Espacial (Join):** Fusión de la geometría de las manzanas con las variables de población (`POBTOT`, `POBFEM`, `POBMAS`) y rangos de edad.
    5.  **Exportación:** Reproyección a EPSG:32614 y guardado en GeoPackage.

## 3. DENUE CDMX (Unidades Económicas)
*   **Archivo:** `denue_cdmx.gpkg`
*   **Fuente:** [INEGI - Directorio Estadístico de Unidades Económicas](https://datos.cdmx.gob.mx/dataset/directorio-estadistico-de-unidades-economicas-ciudad-de-mexico)
*   **Pasos de Procesamiento:**
    1.  **Lectura:** Carga desde archivo comprimido ZIP.
    2.  **Análisis de Atributos:** Identificación de tipos de actividad económica (`activdd`) para indicadores de proximidad y diversidad.
    3.  **Reproyección:** Cambio de coordenadas geográficas a proyectadas UTM 14N (EPSG:32614).
    4.  **Exportación:** Guardado como capa de puntos en GeoPackage.

## 4. Catálogo de Colonias
*   **Archivo:** `colonias_cdmx.gpkg`
*   **Fuente:** [Portal de Datos Abiertos CDMX](https://datos.cdmx.gob.mx/dataset/catalogo-de-colonias-datos-abiertos)
*   **Pasos de Procesamiento:**
    1.  **Limpieza de Columnas:** Selección de atributos clave (`cve_alc`, `alc`, `cve_col`, `colonia`).
    2.  **Validación Geométrica:** Verificación de polígonos para evitar geometrías inválidas.
    3.  **Reproyección:** Conversión a EPSG:32614.
    4.  **Exportación:** Generación del archivo GeoPackage para uso en análisis por zona.

## 5. Infraestructura Vial Ciclista
*   **Archivo:** `infra_vial_ciclista.gpkg`
*   **Fuente:** [Secretaría de Movilidad (SEMOVI)](https://datos.cdmx.gob.mx/dataset/infraestructura-vial-ciclista)
*   **Pasos de Procesamiento:**
    1.  **Lectura Espacial:** Extracción del archivo Shapefile contenido en el ZIP.
    2.  **Categorización:** Mantenimiento de la clasificación de tipo de infraestructura (ciclovía, carril bus-bici, etc.).
    3.  **Reproyección:** Conversión a EPSG:32614.
    4.  **Exportación:** Guardado en formato GeoPackage.

## 6. Vialidades (Primarias y Acceso Controlado)
*   **Archivos:** `vialidades_primarias.gpkg`, `vialidades_acceso_controlado.gpkg`
*   **Fuentes:** [Vialidades de la CDMX](https://datos.cdmx.gob.mx/dataset/vialidades-de-la-ciudad-de-mexico) y [Acceso Controlado](https://datos.cdmx.gob.mx/dataset/vialidades-de-acceso-controlado)
*   **Pasos de Procesamiento:**
    1.  **Limpieza Geométrica:** Manejo de geometrías `LineString Z` convirtiéndolas a `LineString` simple cuando fue necesario.
    2.  **Filtrado:** Separación de redes de acceso controlado de la red vial primaria general.
    3.  **Reproyección:** Conversión a EPSG:32614 para cálculos de distancia lineales.
    4.  **Exportación:** Guardado individual en GeoPackage.

## 7. Red Nacional de Caminos (RNC) - Recorte CDMX
*   **Archivo:** `rnc_vial_cdmx.gpkg`
*   **Fuentes:** 
    *   Vialidades: [Red Nacional de Caminos (RNC)](https://www.gob.mx/imt/acciones-y-programas/red-nacional-de-caminos) - `794551163030_gpk.zip`
    *   Límites: [Marco Geoestadístico (Estados)](https://www.inegi.org.mx/temas/mg/) - `dest25gw_c.zip`
*   **Pasos de Procesamiento:**
    1.  **Extracción de Polígono:** Obtención de la geometría de la Ciudad de México del archivo de estados de México mediante la clave de entidad `09`.
    2.  **Pre-filtrado Espacial:** Uso del *bounding box* de la CDMX para realizar una carga selectiva y eficiente de la capa `red_vial` del GeoPackage nacional.
    3.  **Recorte Espacial (Clip):** Recorte preciso de la red vial nacional utilizando el polígono oficial de la CDMX.
    4.  **Reproyección:** Conversión a EPSG:32614.
    5.  **Exportación:** Guardado en formato GeoPackage optimizado para la región.

## 8. Puntos de acceso gratuito WiFi en la CDMX
*   **Archivo:** `rp_WifiCDMX.gpkg`
*   **Fuentes:**
    1. Puntos de acceso WiFi en la CDMX (https://datos.cdmx.gob.mx/dataset/puntos-de-acceso-wifi-en-la-cdmx) - `00-2025-wifi_gratuito_en_cdmx.xlsx`
    2. WiFi gratuito en Postes Mi Calle (https://datos.cdmx.gob.mx/dataset/wifi-gratuito-en-postes-mi-calle) - `06-2025-wifi_gratuito_en_postes-mi-calle.xlsx`
    3. WiFi gratuito en Colonias Periféricas de la CDMX (https://datos.cdmx.gob.mx/dataset/wifi-gratuito-en-colonias-perifericas-de-la-cdmx) - `03-2025-wifi_gratuito_en_colonias-perifericas-de-la-cdmx.xlsx`
    4. WiFi gratuito en Utopías de la CDMX (https://datos.cdmx.gob.mx/dataset/wifi-gratuito-en-utopias-de-la-cdmx) - `11-2025-wifi_gratuito_en_utopias-de-la-cdmx.xlsx`
    5. WiFi gratuito en Pilares de la CDMX (https://datos.cdmx.gob.mx/dataset/wifi-gratuito-en-pilares-de-la-cdmx) - `05-2025-wifi_gratuito_en_pilares-de-la-cdmx.xlsx`
    6. WiFi gratuito en Unidades Habitacionales de la CDMX (https://datos.cdmx.gob.mx/dataset/wifi-gratuito-en-unidades-habitacionales-de-la-cdmx) - `10-2025-wifi_gratuito_en_unidades-habitacionales-de-la-cdmx.xlsx`
    7. WiFi gratuito en Postes del C5 (https://datos.cdmx.gob.mx/dataset/wifi-gratuito-en-postes-del-c5) - `07-2025-wifi_gratuito_en_postes-del-c5.xlsx`
    8. WiFi gratuito en Escuelas Públicas de la CDMX (https://datos.cdmx.gob.mx/dataset/wifi-gratuito-en-escuelas-publicas-de-la-cdmx) - `04-2025-wifi_gratuito_en_escuelas-publicas-de-la-cdmx.xlsx`
    9. WiFi gratuito en Sitios Públicos de la CDMX (https://datos.cdmx.gob.mx/dataset/wifi-gratuito-en-sitios-publicos-de-la-cdmx-albergues-bibliotecas-etc) - `08-2025-wifi_gratuito_en_sitios-publicos-de-la-cdmx-albergues-bibliotecas-centros-culturales-em.xlsx`
    10.	WiFi gratuito en el Transporte de la CDMX (https://datos.cdmx.gob.mx/dataset/wifi-gratuito-en-el-transporte-de-la-cdmx-metrobus-cablebus-tren-ligero-trolebus-etc) - `09-2025-wifi_gratuito_en_transporte-de-la-cdmx-metrobus-cablebus-tren-ligero-trolebus-etc.xlsx`
    11. WiFi gratuito en Centros de Salud (https://datos.cdmx.gob.mx/dataset/wifi-gratuito-en-centros-de-salud-clinicas-y-hospitales-de-la-cdmx) - `02-2025-wifi_gratuito_en_centros-de-salud-clinicas-y-hospitales-de-la-cdmx.xlsx`
*   **Pasos de procesamiento:**
    1. **Integración:** Se realizó la unión de todos los datos en un solo archivo de Excel y se guardo como ".csv".
    2. **Carga de puntos:** Se realizó la carga del archivo integrador ".csv" como textos separados por coma y considerando los campos de latitud/longitud para georreferenciar.
    3. **Reproyección:** Conversión a EPSG:32614.
    4. **Exportación:** Guardado en formato GeoPackage.

## 9. Categorización de vialidades
*   **Archivo:** `rnc_vial_cdmx_cat.gpkg`
*   **Fuentes:** Vialidades: [Red Nacional de Caminos (RNC) - Recorte CDMX] - `rnc_vial_cdmx.gpkg`
*   **Pasos de procesamiento:**
    1. **Definición**: Establecer las categorias a partir de la información de SEMOVI, CDMX (https://www.semovi.cdmx.gob.mx/storage/app/media/Publicaciones/guia_basica_seguridad_vial.pdf#:~:text=Sabías%20que%2C%20de%20acuerdo%20con%20el%20RTCDMX,total%20para%20permitir%20el%20paso%20de%20peatones).
        - 10 Vías peatonales o estacionamiento (Seguridad peatonal: Alta)
		- 20 Zonas de seguridad(Seguridad peatonal: Idónea) [Idónea debido al rango de velocidad adecuado para bicicletas y tránsito peatonal]
		- 30 Zonas de tránsito(Seguridad peatonal: Moderada)
		- 40 Vías secundarias (Seguridad peatonal: Limitada) [Limitada porque depende de carriles laterales de acceso controlado]
		- 50 Vías primarias (Seguridad peatonal: Baja)
		- 60 - 80 Vías rápidas (Seguridad peatonal: Nula)
    2. **Categorización**: Aplicación de valores categóricos y pseudo-numéricos
        - Se realizó una columna nueva con los valores tipo cadena de texto para colocar el nombre de las categorias establecidas.
        - Se realizó una columna nueva con los valores pseudo-numéricos del 0 al 5, siendo el 0 el valor con mayor inseguridad vial por la alta velocidad estalecidas en las vialidades.
    3. **Exportación:** Guardado en formato GeoPackage.

## 10. Infraestructura Vial Ciclista
* **Archivo:** `infra_ciclista_total.gpkg`
* **Fuente:** [Portal de datos abiertos (SEMOVI)](https://datos.cdmx.gob.mx/dataset/infraestructura-vial-ciclista)

* **Pasos de Procesamiento:**
    1. **Lectura:** Carga de archivos Shapefile desde carpeta descomprimida.
    2. **Filtrado:** Se conservaron únicamente los registros con `ESTADO == "En operacion"`.
    3. **Limpieza de Atributos:** Se seleccionaron las columnas `ALCALDIA`, `TIPO_IC`, `TIPO_VIA`, `TIPO_CONEC`, `LONG_KM` y `geometry`, descartando identificadores internos irre.
    4. **Unificación:** Se unificaron en una sola capa espacial toda la información relacionada a infraestructura ciclista
    5. **Reproyección:** Conversión a EPSG:32614.
    6. **Exportación:** Guardado en formato GeoPackage.

## 11. Líneas y estaciones de Metro
* **Archivo:** `estaciones_metro.gpkg` y `lineas_metro.gpkg`
* **Fuente:** [STC Metro CDMX](https://datos.cdmx.gob.mx/dataset/lineas-y-estaciones-del-metro/resource/288b10dd-4f21-4338-b1ed-239487820512?inner_span=True)
* **Pasos de Procesamiento:**
    1. **Lectura:** Carga de archivos Shapefile de líneas y estaciones.
    2. **Limpieza de Atributos:** Se conservaron `SISTEMA`, `NOMBRE`, `LINEA`, `TIPO` y `ALCALDIAS`, descartando claves internas (`EST`, `CVE_EST`, `CVE_EOD17`) y año.
    3. **Reproyección:** Conversión a EPSG:32614.
    4. **Exportación:** Guardado en formato GeoPackage.

## 12. Líneas y Estaciones del Metrobús
* **Archivo:** `metrobus_estaciones.gpkg` y `metrobus_lineas.gpkg`
* **Fuente:** [Portal de datos abiertos (Metrobús CDMX)](https://datos.cdmx.gob.mx/dataset/geolocalizacion-metrobus)
* **Pasos de Procesamiento:**
    1. **Lectura:** Carga de archivos Shapefile de líneas y estaciones.
    2. **Limpieza de Atributos:** Se conservaron `SISTEMA`, `NOMBRE`, `LINEA`, `TIPO` y `ALCALDIAS`, descartando claves internas 
    3. **Reproyección:** Conversión a EPSG:32614.
    4. **Exportación:** Guardado en formato GeoPackage.

## 13. Rutas de RTP
* **Archivo:** `rtp_lineas.gpkg`, `rtp_paradas.gpkg`
* **Fuente:** [Portal de datos abiertos CDMX: Red de Transporte de Pasajeros](https://datos.cdmx.gob.mx/dataset/e5e67126-8964-4457-a88b-ed0194bb5eb5/resource/391b1ea2-d5e6-4a60-a1fe-114ccb99ee82?activity_id=20c29c35-2c90-4c24-83be-411802c68e3b)
* **Indicador:** Proximidad
* **Pasos de Procesamiento:**
    1. **Lectura Espacial:** Carga de Shapefiles de líneas y paradas.
    2. **Filtrado:** Se conservaron únicamente registros con `ESTATUS == "ACTIVO"`.
    3. **Limpieza de Atributos:** En líneas se conservaron `NOMBRE`, `SISTEMA`, `RUTA`, `ORIGEN`, `DESTINO`. En paradas `RUTA`, `SENTIDO`, `ORIG_DEST`, `SISTEMA`. Se descartaron módulo, corredor e intersección.
    4. **Reproyección:** Conversión a EPSG:32614.
    5. **Exportación:** Guardado en formato GeoPackage.
    
## 14. Servicio de Transportes Eléctricos (Cablebus, Tren Ligero, Trolebús)
* **Archivos:** `cablebus_estaciones.gpkg`, `cablebus_lineas.gpkg`, `tren_ligero_estaciones.gpkg`, `tren_ligero_linea.gpkg`, `trolebus_lineas.gpkg`, `trolebus_paradas.gpkg`
* **Fuente:** [Portal de datos abiertos CDMX: Servicio de Transportes Eléctricos](https://datos.cdmx.gob.mx/dataset/geolocalizacion-de-lineas-y-estaciones-paradas-del-servicio-de-transportes-electricos)
* **Pasos de Procesamiento:**
    1. **Lectura de datos:** Carga de Shapefiles por modo de transporte.
    2. **Limpieza de Atributos:** Se conservaron `SISTEMA`, `NOMBRE`, `LINEA`, `TIPO` y `ALCALDIAS`. Se descartaron claves internas, año, y campos de accesibilidad universal (`Elevadores`, `Guia_tact`, `P_braile`, `Ramp_s_rue`).
    3. **Reproyección:** Conversión a EPSG:32614.
    4. **Exportación:** Guardado en formato GeoPackage por modo de transporte.

## 15. Hospitales y Centros de Salud
* **Archivo:** `hospitales_centros_salud.gpkg`
* **Fuente:** [Portal de datos abiertos CDMX: Secretaría de Salud CDMX](https://datos.cdmx.gob.mx/dataset/hospitales-y-centros-de-salud)

* **Pasos de Procesamiento:**
    1. **Lectura:** Carga de Shapefile de unidades de salud.
    2. **Limpieza de Atributos:** Se conservaron campos de nombre, tipo de unidad y alcaldía.
    3. **Reproyección:** Conversión a EPSG:32614.
    4. **Exportación:** Guardado en formato GeoPackage.

## 16. Escuelas Públicas
* **Archivo:** `escuelas_publicas.gpkg`
* **Fuente:** [Portal de datos abiertos: Secretaría de Educación CDMX](https://datos.cdmx.gob.mx/dataset/escuelas-publicas)
* **Pasos de Procesamiento:**
    1. **Lectura Tabular:** Carga desde archivo CSV ya que no contiene geometría nativa.
    2. **Limpieza de Atributos:** Se conservaron `nombre`, `colonia` y `alcaldia`. Se descartaron `domicilio`, `latitud` y `longitud` por ser redundantes con la geometría generada.
    3. **Eliminación de nulos:** Se eliminaron 141 registros sin coordenadas mediante `dropna`.
    4. **Espacialización:** Construcción de geometría de puntos a partir de columnas `longitud` y `latitud` con `gpd.points_from_xy`.
    5. **Exportación:** Guardado en formato GeoPackage con CRS EPSG:32614.

## 17. Escuelas Privadas
* **Archivo:** `escuelas_privadas.gpkg`
* **Fuente:** [Secretaría de Educación CDMX](https://datos.cdmx.gob.mx/dataset/escuelas-privadas)
* **Pasos de Procesamiento:**
    1. **Lectura Espacial:** Carga desde Shapefile.
    2. **Limpieza de Atributos:** Se conservaron `nombre`, `nivel`, `colonia` y `alcaldi`. Se descartaron `turno`, `sstnmnt`, `domicil` y `ubicacn` por ser redundantes con la geometría.
    3. **Reproyección:** Conversión a EPSG:32614.
    4. **Exportación:** Guardado en formato GeoPackage.

---

## 18. Áreas Verdes de la Ciudad de México
* **Archivo:** `areas_verdes.gpkg`
* **Fuente:** [Secretaría del Medio Ambiente CDMX](ttps://datos.cdmx.gob.mx/dataset/cdmx_areas_verdes_2017)
* **Pasos de Procesamiento:**
    1. **Lectura Tabular:** Carga desde archivo CSV `cdmx_areas_verdes_2017.csv`.
    2. **Limpieza de Atributos:** Se conservaron `categoria`, `subcve_sed`, `superficie` y `zonifica`. Se descartaron metadatos administrativos y campos redundantes con la geometría.
    3. **Eliminación de nulos:** Se eliminaron registros sin geometría mediante `dropna` sobre la columna `geo_shape`.
    4. **Espacialización:** Conversión de la columna `geo_shape` en formato GeoJSON embebido a geometría válida usando `json.loads()` y `shape()` de shapely.
    5. **Exportación:** Guardado en formato GeoPackage con CRS EPSG:32614.

## 19. Indicadores ODS 11 (INEGI API - Nacional y Estatal)
* **Archivo:** `datos/procesados/procesados_2.5_etapa/ods11_final.json`
* **Fuente:** [INEGI - API de Indicadores (Banco de Indicadores BISE)](https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/...)
* **Indicadores Incluidos:**
    * **11.1.1**: Viviendas precarias (%).
    * **11.2.1**: Acceso a transporte público (%).
    * **11.3.1**: Relación de expansión del suelo urbano.
    * **11.r.2.1a/b**: Tiempo de traslado al trabajo (General e Indígena).
    * **11.6.1.a**: Gestión de residuos sólidos (%).
    * **11.6.2.a/b**: Concentración de partículas suspendidas (PM2.5 y PM10).
    * **11.4.1**: Gasto en patrimonio cultural y natural ($).
    * **11.7.1**: Disponibilidad de espacios públicos abiertos (%).
* **Pasos de Procesamiento:**
    1. **Automatización:** Ejecución del script `scripts/generar_indicadores_ods11.py` para realizar consultas masivas a la API del INEGI.
    2. **Alcance Multiescalar:** Extracción sistemática de datos para el nivel Nacional (`00`) y las 32 Entidades Federativas (`01` a `32`).
    3. **Sincronización de Series:** Mapeo de identificadores de series históricas del BISE con las metas globales del ODS 11.
    4. **Consolidación de Datos:** Integración de los valores nacionales como referencia base frente a los datos estatales en una estructura JSON anidada.
    5. **Estructuración para Dashboard:** Formateo de la salida para facilitar la comparativa geográfica y temporal en el tablero de visualización.

## 20. Cruce de Accesibilidad Urbana (Etapa 3)
*   **Archivos:** `cruce_[ALCALDIA].gpkg` (16 archivos en `datos/procesados/procesados_3_etapa/`)
*   **Script de Generación:** `scripts/cruce_accesibilidad.py`
*   **Metodología y Pasos de Procesamiento:**
    1.  **Cálculo Dinámico de Rutas:** Para cada manzana de la CDMX (63,174 registros), el script calcula internamente la red vial alcanzable en un radio de 1,250 metros (aprox. 15-20 min caminando) utilizando el algoritmo de Dijkstra sobre la Red Nacional de Caminos (RNC). No depende de capas de rutas pre-calculadas para asegurar consistencia.
    2.  **Paralelismo:** El proceso utiliza `multiprocessing` para distribuir el cálculo de Dijkstra y los cruces espaciales entre todos los núcleos disponibles del CPU.
    3.  **Cruce de Equipamiento (Puntos):** Se realiza un join espacial con un buffer de 15m para contabilizar el acceso a:
        - Unidades económicas (DENUE) clasificadas por prioridad (Alta, Media, Baja).
        - Escuelas públicas y privadas.
        - Hospitales y centros de salud.
        - Puntos de WiFi gratuito.
        - Estaciones de transporte masivo.
    4.  **Cruce de Infraestructura (Líneas):** Se calcula la longitud en metros de ciclovías, rutas de transporte y vialidades según su nivel de seguridad peatonal (categorías de velocidad).
    5.  **Generación de Indicadores:**
        - **Diversidad:** Conteo de tipos de servicios únicos accesibles.
        - **Nivel de Accesibilidad:** Clasificación cualitativa (**Alta**, **Media**, **Baja**).
    6.  **Exportación Incremental:** Los resultados se guardan por alcaldía para optimizar el uso de memoria y permitir la recuperación del proceso ante interrupciones.

## 21. Clasificación de Accesibilidad Urbana por Manzana (Etapa 4)
*   **Archivos:** `mnz_clas_[ALCALDIA].geojson` (16 archivos en `datos/procesados/procesados_4_etapa/`)
*   **Script de Generación:** `scripts/asignar_geometrias.py`
*   **Metodología y Pasos de Procesamiento:**
    1.  **Carga de geometrías:** Se carga la capa `manzanas_cdmx_poblacion.gpkg` (etapa 2) conservando únicamente el identificador `CVEGEO` y la geometría poligonal de cada manzana (EPSG:4326).
    2.  **Unión con resultados de cruce:** Para cada alcaldía, se une la tabla del archivo `cruce_[ALCALDIA].gpkg` (etapa 3) con los polígonos de manzana mediante un *inner join* sobre `CVEGEO`, asignando así geometría real a cada registro de accesibilidad.
    3.  **Clasificación:** Se genera el campo `clasificacion` a partir del campo `diversidad` (índice de 0 a 8 que cuenta los tipos de equipamiento accesibles), aplicando los siguientes cortes:
        - **Muy bajo:** diversidad 0 – 2
        - **Bajo:** diversidad 3 – 4
        - **Medio:** diversidad 5
        - **Alto:** diversidad ≥ 6
    4.  **Limpieza de campos:** Se descartan todas las columnas de detalle de equipamiento, conservando únicamente `clavegeo`, `alcaldia`, `colonia` y `clasificacion`.
    5.  **Exportación:** Cada alcaldía se exporta como un archivo GeoJSON independiente en `datos/procesados/procesados_4_etapa/`, listo para consumo en el dashboard.

## 22. División por Colonias para Dashboard (Etapa 4 — Colonias)
*   **Archivos:** `index.json` y `[ALCALDIA]/[colonia].geojson` en `datos/procesados/procesados_4_etapa/colonias/`
*   **Script de Generación:** `scripts/dividir_colonias.py`
*   **Metodología y Pasos de Procesamiento:**
    1.  **Lectura por alcaldía:** Se leen los 16 archivos `mnz_clas_[ALCALDIA].geojson` de la etapa 4.
    2.  **División por colonia:** Para cada alcaldía se agrupa el GeoDataFrame por el campo `colonia` y se exporta cada grupo como un GeoJSON independiente, conservando únicamente `clavegeo`, `clasificacion` y `geometry`.
    3.  **Normalización de nombres de archivo:** Los nombres de colonia se normalizan (minúsculas, sin tildes, espacios sustituidos por guiones bajos) para garantizar rutas de archivo compatibles entre sistemas operativos.
    4.  **Organización en directorios:** Cada alcaldía genera su propia carpeta dentro de `colonias/`, agrupando todos los GeoJSON de sus colonias.
    5.  **Generación del índice:** Se produce un archivo `index.json` con la lista de alcaldías y, para cada una, el listado de sus colonias con el nombre legible y el nombre del archivo correspondiente. Este índice permite al dashboard construir la selección en cascada (alcaldía → colonia) sin necesidad de cargar ninguna geometría hasta que el usuario la solicite.

## 23. Autocorrelación Espacial — I de Moran Global y Local LISA (Etapa 5)
*   **Archivo:** `moran_lisa_cdmx.geojson` en `datos/procesados/procesados_5_etapa/`
*   **Script de Generación:** `scripts/calcular_moran_lisa.py`
*   **Fuentes:** Clasificación de accesibilidad por manzana (Etapa 4) — `mnz_clas_[ALCALDIA].geojson`
*   **Dependencias:** `libpysal`, `esda`
*   **Metodología y Pasos de Procesamiento:**
    1.  **Carga y unificación:** Se leen los 16 archivos `mnz_clas_[ALCALDIA].geojson` y se concatenan en un único GeoDataFrame con las columnas `alcaldia`, `colonia`, `clasificacion` y `geometry`.
    2.  **Mapeo numérico:** La variable categórica `clasificacion` se convierte a escala ordinal numérica: Muy bajo = 0, Bajo = 1, Medio = 2, Alto = 3.
    3.  **Reproyección:** El GeoDataFrame se proyecta a EPSG:32614 (UTM 14N) para el cálculo de distancias en metros.
    4.  **Matriz de pesos espaciales (KNN, k=8):** Se utiliza K vecinos más cercanos (KNN) en lugar de contigüidad, ya que las manzanas están separadas físicamente por vialidades y no comparten bordes. Los pesos se estandarizan por fila (`transform='r'`).
    5.  **Moran Global:** Se calcula el índice I de Moran global con 999 permutaciones para obtener el p-valor simulado. Resultado: I = 0.89, p < 0.001.
    6.  **Moran Local (LISA):** Se calculan los valores locales con 999 permutaciones. Para cada manzana se asigna un cuadrante (q): Alto-Alto (1), Bajo-Alto (2), Bajo-Bajo (3), Alto-Bajo (4). Las manzanas con p > 0.05 se clasifican como "No significativo".
    7.  **Exportación:** El resultado se exporta a WGS84 (EPSG:4326) como GeoJSON con las columnas `alcaldia`, `colonia`, `clasificacion`, `cluster` y `geometry`.

## 24. Vistas GeoJSON Simplificadas de Clasificación para el Dashboard (Etapa 4 — Vistas)
*   **Archivos:**
    *   `datos/procesados/procesados_4_etapa/vistas/vista_cdmx.geojson` — 4 features (CDMX × clasificación)
    *   `datos/procesados/procesados_4_etapa/vistas/vista_alcaldias.geojson` — ~64 features (alcaldía × clasificación)
    *   `datos/procesados/procesados_4_etapa/vistas/colonias/[Alcaldia].geojson` — colonia × clasificación (un archivo por alcaldía)
*   **Dashboard (copia sincronizada):** `dashboard/datos/vistas/`
*   **Script de Generación:** `scripts/generar_vistas_clasificacion.py`
*   **Metodología y Pasos de Procesamiento:**
    1.  **Carga:** Se leen los 16 archivos `mnz_clas_[ALCALDIA].geojson` de la Etapa 4.
    2.  **Disolución por nivel:** Se generan tres niveles de agregación mediante `dissolve` sobre los grupos correspondientes (`clasificacion`, `alcaldia × clasificacion`, `alcaldia × colonia × clasificacion`).
    3.  **Pipeline de simplificación:** Para cada nivel se aplica: `buffer(0)` (reparar topología) → `simplify(tol)` (reducir vértices) → `set_precision(grid)` (redondear coordenadas).
    4.  **Tolerancias:** CDMX y alcaldías: simplify = 0.003°, grid = 0.001°. Colonias: simplify = 0.001°, grid = 0.0003°.
    5.  **Exportación:** Cada nivel se guarda como GeoJSON independiente. Las vistas de colonia se organizan en un archivo por alcaldía para permitir carga bajo demanda en el dashboard.
    6.  **Sincronización:** Los archivos generados se copian a `dashboard/datos/vistas/` reemplazando la versión anterior.

## 25. Vistas GeoJSON Simplificadas del Análisis LISA (Etapa 5 — Vistas)
*   **Archivos:**
    *   `datos/procesados/procesados_5_etapa/vista_moran_alcaldias.geojson` — alcaldía × cluster
    *   `datos/procesados/procesados_5_etapa/vista_moran_colonias.geojson` — alcaldía × colonia × cluster
*   **Dashboard (copia sincronizada):** `dashboard/datos/vistas/`
*   **Script de Generación:** `scripts/generar_vista_moran.py`
*   **Fuente:** `datos/procesados/procesados_5_etapa/moran_lisa_cdmx.geojson` (~70 MB)
*   **Metodología y Pasos de Procesamiento:**
    1.  **Carga:** Se lee el GeoJSON completo de LISA conservando `alcaldia`, `colonia`, `cluster` y `geometry`.
    2.  **Vista alcaldías:** `dissolve` por `[alcaldia, cluster]` con simplify = 0.003°, grid = 0.001°. Uso: mapa dinámico Folium en el dashboard.
    3.  **Vista colonias:** `dissolve` por `[alcaldia, colonia, cluster]` con simplify = 0.001°, grid = 0.0003°. Uso: mapa estático PNG.
    4.  **Pipeline de simplificación:** `buffer(0)` → `simplify(tol)` → `set_precision(grid)` → filtrado de geometrías inválidas o vacías.
    5.  **Sincronización:** Ambas vistas se copian a `dashboard/datos/vistas/`.

## 26. Resúmenes JSON de Clasificación por Alcaldía y Colonia
*   **Archivos:**
    *   `datos/procesados/procesados_4_etapa/resumen_alcaldias.json`
    *   `datos/procesados/procesados_4_etapa/resumen_colonias.json`
*   **Dashboard (copia sincronizada):**
    *   `dashboard/datos/resumen_alcaldias.json`
    *   `dashboard/datos/resumen_colonias.json`
*   **Script de Generación:** `scripts/generar_resumenes_dashboard.py`
*   **Fuente:** `datos/procesados/procesados_4_etapa/mnz_clas_[ALCALDIA].geojson`
*   **Metodología y Pasos de Procesamiento:**
    1.  **Carga:** Se leen las columnas `alcaldia`, `colonia` y `clasificacion` de los 16 archivos de la Etapa 4 (sin cargar geometrías para optimizar memoria).
    2.  **Resumen por alcaldía:** Para cada alcaldía se calcula el porcentaje de manzanas en cada nivel de clasificación (`pct_alto`, `pct_medio`, `pct_bajo`, `pct_muy_bajo`) y el total de manzanas (`n_manzanas`).
    3.  **Resumen por colonia:** Mismo cálculo agrupado por `[alcaldia, colonia]`.
    4.  **Exportación:** Ambos resúmenes se guardan como JSON con indentación y codificación UTF-8, y se sincronizan con `dashboard/datos/`.

## 27. Conteo de Registros por Insumo para el Dashboard
*   **Archivo:** `dashboard/datos/resumen_insumos.json`
*   **Script de Generación:** `scripts/generar_resumen_insumos.py`
*   **Fuentes:** Archivos GeoPackage de la Etapa 2 (`datos/procesados/procesados_2_etapa/`)
*   **Metodología y Pasos de Procesamiento:**
    1.  **Carga selectiva:** Se cargan los GeoPackages de los 8 insumos utilizados en el análisis, aplicando filtros donde corresponde (DENUE alta prioridad, DENUE media prioridad).
    2.  **Cálculo de valor:** Para insumos de tipo punto se cuenta el número de registros; para insumos de tipo línea (infraestructura ciclista, rutas de transporte) se calcula la longitud total en kilómetros reproyectando a EPSG:32614.
    3.  **Exportación:** Se genera un JSON con los campos `nombre`, `categoria`, `fuente`, `tipo`, `valor`, `unidad` y `color` (por categoría: Diversidad, Proximidad, Digitalización) para consumo directo en el gráfico de barras del dashboard.

## 28. Mapas PNG Estáticos para el Dashboard
*   **Archivos:**
    *   `dashboard/datos/mapas/mapa_colonias.png` — clasificación de accesibilidad por colonia
    *   `dashboard/datos/mapas/mapa_moran.png` — clústeres LISA del I de Moran Local por colonia
*   **Script de Generación:** `scripts/generar_mapas_estaticos.py`
*   **Fuentes:**
    *   Clasificación: `dashboard/datos/vistas/colonias/[Alcaldia].geojson` (16 archivos)
    *   Moran: `dashboard/datos/vistas/vista_moran_colonias.geojson`
*   **Metodología y Pasos de Procesamiento:**
    1.  **Carga:** Se leen los GeoJSONs simplificados de la vista de colonias (clasificación) y la vista de colonias del análisis LISA.
    2.  **Bordes de alcaldía:** Se genera una capa de alcaldías por disolución del campo `alcaldia`, usada para superponer el límite administrativo como línea gris oscura (linewidth = 0.7).
    3.  **Paletas de color:** Clasificación: Alto (#2ca25f), Medio (#99d8c9), Bajo (#fec44f), Muy bajo (#e34a33). LISA: Alto-Alto (#d7191c), Bajo-Bajo (#2c7bb6), Bajo-Alto (#abd9e9), Alto-Bajo (#fdae61), No significativo (#cccccc).
    4.  **Eliminación de contornos entre polígonos:** Se fija `edgecolor=(0,0,0,0)` y `linewidth=0` en las colecciones de matplotlib. Limitación reconocida: matplotlib mantiene hairlines de antialiasing entre polígonos adyacentes independientemente de estos parámetros.
    5.  **Etiquetas de alcaldía:** Texto en el centroide de cada alcaldía con halo blanco (`path_effects.withStroke`) para legibilidad sobre fondos de color.
    6.  **Exportación:** PNG a 150 DPI con fondo blanco, guardado en `dashboard/datos/mapas/`.

---
**Nota:** Todos los archivos procesados se encuentran documentados en los Notebooks del proyecto, donde se detalla el flujo de trabajo, la limpieza y el análisis de los datos.

[Ver Notebooks del proyecto](./notebooks/)
