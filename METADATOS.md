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
*   **Fuentes:** 
    *   Vialidades: [Red Nacional de Caminos (RNC) - Recorte CDMX] - `rnc_vial_cdmx.gpkg`
*   **Pasos de procesamiento:**
    1. **Definición**: Establecer las categorias a partir de la información de SEMOVI, CDMX (https://www.semovi.cdmx.gob.mx/storage/app/media/Publicaciones/guia_basica_seguridad_vial.pdf#:~:text=Sabías%20que%2C%20de%20acuerdo%20con%20el%20RTCDMX,total%20para%20permitir%20el%20paso%20de%20peatones).
        - 10 km/h Vías peatonales o estacionamiento (Seguridad peatonal: Alta)
		- 20 km/h Zonas de seguridad(Seguridad peatonal: Idónea) [Idónea debido al rango de velocidad adecuado para bicicletas y tránsito peatonal]
		- 30 km/h Zonas de tránsito(Seguridad peatonal: Moderada)
		- 40 km/h Vías secundarias (Seguridad peatonal: Limitada) [Limitada porque depende de carriles laterales de acceso controlado]
		- 50 km/h Vías primarias (Seguridad peatonal: Baja)
		- 60 - 80 km/h Vías rápidas (Seguridad peatonal: Nula)
    2. **Categorización**: Aplicación de valores categóricos y pseudo-numéricos
        - Se realizó una columna nueva con los valores tipo cadena de texto para colocar el nombre de las categorias establecidas.
        - Se realizó una columna nueva con los valores pseudo-numéricos del 0 al 5, siendo el 0 el valor con mayor inseguridad vial por la alta velocidad estalecidas en las vialidades.
    3. **Exportación:** Guardado en formato GeoPackage.

---
**Nota:** Todos los archivos procesados se encuentran optimizados para su uso en herramientas SIG (QGIS, ArcGIS) y librerías de Python (GeoPandas).
