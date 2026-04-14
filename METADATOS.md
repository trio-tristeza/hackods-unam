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

---
**Nota:** Todos los archivos procesados se encuentran optimizados para su uso en herramientas SIG (QGIS, ArcGIS) y librerías de Python (GeoPandas).
