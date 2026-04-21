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
* **Archivo:** `datos/indicadoresODS11/ods11_final.json`
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

---
**Nota:** Todos los archivos procesados se encuentran documentados en los Notebooks del proyecto, donde se detalla el flujo de trabajo, la limpieza y el análisis de los datos.

[Ver Notebooks del proyecto](./notebooks/)
