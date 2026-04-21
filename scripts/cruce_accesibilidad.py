"""
cruce_accesibilidad.py
Cruce espacial de accesibilidad urbana ODS 11 - CDMX

Ejecutar desde la raíz del proyecto:
    uv run python scripts/cruce_accesibilidad.py

Mejoras respecto al notebook original:
  - Dijkstra paralelizado con multiprocessing (el grafo se envía una sola vez por worker)
  - Exportación incremental por alcaldía (puedes revisar resultados mientras corre)
  - union_all() pre-calculado una sola vez fuera del loop
  - Retoma automáticamente desde donde se quedó si se interrumpe
"""

import geopandas as gpd
import pandas as pd
import networkx as nx
from shapely.geometry import MultiLineString, LineString
import numpy as np
from scipy.spatial import KDTree
import multiprocessing as mp
from pathlib import Path
import time
from tqdm.auto import tqdm

# ============================================================
# CONFIGURACIÓN — ajusta aquí antes de correr
# ============================================================
N_WORKERS  = -1     # -1 = todos los núcleos disponibles, 1 = sin paralelismo
MAX_DIST   = 1250   # metros (equivale a ~15 min caminando)
CHUNKSIZE  = 50     # manzanas por tarea enviada al pool (balance velocidad/memoria)

# Rutas (relativas a la raíz del proyecto)
BASE_2     = Path("datos/procesados/procesados_2_etapa/")
BASE_1     = Path("datos/procesados/procesados_1_etapa/")
OUTPUT_DIR = Path("datos/procesados/procesados_3_etapa/")

# Capas de puntos → se les aplica un buffer de 15m para la intersección
CAPAS_PUNTOS = {
    "denue":            BASE_2 / "denue.gpkg",
    "escuelas":         BASE_2 / "escuelas_total.gpkg",
    "hospitales":       BASE_2 / "hospitales_cs.gpkg",
    "wifi":             BASE_2 / "rp_wifiCDMX.gpkg",
    "estaciones_transp": BASE_2 / "transporte_estaciones.gpkg",
}

# Capas de líneas → se miden metros intersectados con cada ruta
CAPAS_LINEAS = {
    "ciclovia":   BASE_2 / "infra_ciclista_total.gpkg",
    "transporte": BASE_2 / "transporte_rutas.gpkg",
    "rnc":        BASE_2 / "rnc_vial_cdmx_cat.gpkg",
}

# Categorías de seguridad peatonal presentes en rnc.cat_Vel
CATS_RNC = ["Alta", "Idónea", "Moderada", "Nula", "Limitada", "Baja"]


# ============================================================
# VARIABLES GLOBALES DEL WORKER
# Se inicializan una sola vez por proceso (no se repicklan en cada tarea)
# ============================================================
_graph = None
_tree  = None
_nodes = None


def _init_worker(graph, tree, nodes):
    global _graph, _tree, _nodes
    _graph = graph
    _tree  = tree
    _nodes = nodes


def _compute_ruta(tarea):
    """
    Calcula la red vial alcanzable en MAX_DIST desde el centroide de una manzana.
    Recibe una tupla (cvegeo, colonia, alcaldia, x, y).
    Devuelve (cvegeo, colonia, alcaldia, MultiLineString) o None si no hay red.
    """
    cvegeo, colonia, alcaldia, cx, cy = tarea

    _, idx = _tree.query([cx, cy])
    start_node = _nodes[idx]

    try:
        alcance = nx.single_source_dijkstra_path_length(
            _graph, start_node, cutoff=MAX_DIST, weight="weight"
        )
        subgrafo = _graph.subgraph(alcance.keys())
        geoms = [data["geometry"] for _, _, data in subgrafo.edges(data=True)]
        if not geoms:
            return None
        return (cvegeo, colonia, alcaldia, MultiLineString(geoms))
    except Exception:
        return None


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def construir_grafo(rnc_gdf):
    """Construye grafo de red NetworkX a partir de la capa vial."""
    G = nx.Graph()
    for _, row in tqdm(rnc_gdf.iterrows(), total=len(rnc_gdf), desc="  Construyendo grafo"):
        geom = row.geometry
        segmentos = [geom] if isinstance(geom, LineString) else list(geom.geoms)
        for seg in segmentos:
            coords = list(seg.coords)
            G.add_edge(coords[0], coords[-1], weight=seg.length, geometry=seg)
    return G


def cruzar_capas(routes_gdf, pts_data, lns_data, lns_unions):
    """
    Cruza las rutas de una alcaldía con todas las capas de equipamiento.
    Devuelve un GeoDataFrame con conteos y longitudes por manzana.
    """
    # Índice temporal para los joins
    rdf = routes_gdf.rename_axis("_rid").reset_index()
    stats = rdf[["_rid", "CVEGEO", "colonia", "alcaldia", "geometry"]].copy()

    # --- Puntos: sjoin + conteo ---
    for nombre, pts_gdf in pts_data.items():
        joined = gpd.sjoin(pts_gdf, rdf[["_rid", "geometry"]], predicate="intersects")

        if nombre == "denue":
            conteos = (
                joined.groupby(["_rid", "prioridad"])
                .size()
                .unstack(fill_value=0)
            )
            for prio in ["Alta", "Media", "Baja"]:
                col = f"denue_{prio.lower()}"
                stats[col] = (
                    stats["_rid"]
                    .map(conteos[prio] if prio in conteos.columns else pd.Series(dtype=int))
                    .fillna(0)
                    .astype(int)
                )
        else:
            conteos = joined.groupby("_rid").size()
            stats[nombre] = stats["_rid"].map(conteos).fillna(0).astype(int)

    # --- Líneas: overlay + suma de longitudes ---
    for nombre, lns_gdf in lns_data.items():
        # Filtrado rápido con union pre-calculada (evita overlay sobre toda la capa)
        mascara = rdf.intersects(lns_unions[nombre])
        rdf_subset = rdf[mascara]

        if rdf_subset.empty:
            if nombre == "rnc":
                for cat in CATS_RNC:
                    stats[f"rnc_{_norm(cat)}"] = 0.0
            else:
                stats[f"long_{nombre}"] = 0.0
            continue

        intersecciones = gpd.overlay(
            lns_gdf,
            rdf_subset[["_rid", "geometry"]],
            how="intersection",
            keep_geom_type=False,
        )
        intersecciones["length"] = intersecciones.geometry.length

        if nombre == "rnc":
            longitudes = (
                intersecciones.groupby(["_rid", "cat_Vel"])["length"]
                .sum()
                .unstack(fill_value=0)
            )
            for cat in CATS_RNC:
                col = f"rnc_{_norm(cat)}"
                stats[col] = (
                    stats["_rid"]
                    .map(longitudes[cat] if cat in longitudes.columns else pd.Series(dtype=float))
                    .fillna(0.0)
                )
        else:
            longitudes = intersecciones.groupby("_rid")["length"].sum()
            stats[f"long_{nombre}"] = stats["_rid"].map(longitudes).fillna(0.0)

    # --- Índice de diversidad y nivel ---
    cols_pt = ["denue_alta", "denue_media", "escuelas", "hospitales", "wifi", "estaciones_transp"]
    cols_ln = ["long_ciclovia", "long_transporte"]
    stats["diversidad"] = (stats[cols_pt + cols_ln] > 0).sum(axis=1)
    stats["nivel"] = stats["diversidad"].apply(
        lambda d: "Alta" if d >= 6 else ("Media" if d >= 3 else "Baja")
    )

    return stats.drop(columns=["_rid"])


def _norm(texto):
    """Normaliza nombre de categoría para usarlo como nombre de columna."""
    return texto.lower().replace("ó", "o").replace(" ", "_")


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":
    t_inicio = time.time()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # ----------------------------------------------------------
    # 1. Carga de datos
    # ----------------------------------------------------------
    print("\n=== CARGA DE DATOS ===")
    print("Cargando manzanas y colonias...")
    manzanas = gpd.read_file(BASE_2 / "manzanas_cdmx_poblacion.gpkg").to_crs(epsg=32614)
    colonias = gpd.read_file(BASE_1 / "colonias_cdmx.gpkg").to_crs(epsg=32614)

    # Asignar colonia y alcaldía a cada manzana por centroide
    mzas_c = manzanas.copy()
    mzas_c["geometry"] = manzanas.geometry.centroid
    mza_info = gpd.sjoin(
        mzas_c,
        colonias[["colonia", "alc", "geometry"]],
        how="left",
        predicate="within",
    ).drop_duplicates(subset=["CVEGEO"])
    manzanas = manzanas.merge(
        mza_info[["CVEGEO", "colonia", "alc"]], on="CVEGEO", how="left"
    ).rename(columns={"alc": "alcaldia"})

    print(f"  {len(manzanas):,} manzanas | {manzanas['alcaldia'].nunique()} alcaldías")

    print("Cargando capas de equipamiento...")
    pts_data = {}
    for nombre, ruta in CAPAS_PUNTOS.items():
        gdf = gpd.read_file(ruta, engine="pyogrio")
        gdf["geometry"] = gdf.buffer(15)     # buffer de 15m para intersección
        pts_data[nombre] = gdf
        print(f"  {nombre}: {len(gdf):,} registros")

    lns_data = {}
    for nombre, ruta in CAPAS_LINEAS.items():
        gdf = gpd.read_file(ruta, engine="pyogrio")
        lns_data[nombre] = gdf
        print(f"  {nombre}: {len(gdf):,} segmentos")

    # Pre-calcular union geométrica de capas lineales (una sola vez para todo el proceso)
    print("Pre-calculando uniones geométricas de capas lineales (esto tarda un momento)...")
    lns_unions = {nombre: gdf.union_all() for nombre, gdf in lns_data.items()}
    print("  Uniones listas.")

    # ----------------------------------------------------------
    # 2. Construcción del grafo vial
    # ----------------------------------------------------------
    print("\n=== GRAFO VIAL ===")
    rnc = gpd.read_file(BASE_2 / "rnc_vial_cdmx_cat.gpkg").to_crs(epsg=32614)
    grafo = construir_grafo(rnc)
    nodos = list(grafo.nodes)
    nodos_arr = np.array([(n[0], n[1]) for n in nodos])
    arbol = KDTree(nodos_arr)
    print(f"  Grafo listo: {len(grafo.nodes):,} nodos | {len(grafo.edges):,} aristas")

    # ----------------------------------------------------------
    # 3. Procesamiento por alcaldía
    # ----------------------------------------------------------
    n_workers = mp.cpu_count() if N_WORKERS == -1 else max(1, N_WORKERS)
    alcaldias = sorted(manzanas["alcaldia"].dropna().unique())

    print(f"\n=== PROCESANDO {len(alcaldias)} ALCALDÍAS con {n_workers} workers ===\n")

    for alcaldia in alcaldias:
        nombre_archivo = alcaldia.replace(" ", "_").replace("/", "-")
        archivo_salida = OUTPUT_DIR / f"cruce_{nombre_archivo}.gpkg"

        if archivo_salida.exists():
            print(f"[SKIP] {alcaldia} — archivo ya existe, omitiendo")
            continue

        t0 = time.time()
        mzas_alc = manzanas[manzanas["alcaldia"] == alcaldia].copy()
        print(f"[START] {alcaldia} ({len(mzas_alc):,} manzanas)...")

        # Preparar tareas: solo los datos escalares necesarios (evita picklear geometrías)
        tareas = [
            (
                row["CVEGEO"],
                row["colonia"],
                row["alcaldia"],
                row.geometry.centroid.x,
                row.geometry.centroid.y,
            )
            for _, row in mzas_alc.iterrows()
        ]

        # Dijkstra paralelo — el grafo se envía una sola vez al inicializar cada worker
        with mp.Pool(
            processes=n_workers,
            initializer=_init_worker,
            initargs=(grafo, arbol, nodos),
        ) as pool:
            resultados_raw = list(
                tqdm(
                    pool.imap(_compute_ruta, tareas, chunksize=CHUNKSIZE),
                    total=len(tareas),
                    desc=f"  Rutas",
                )
            )

        # Filtrar manzanas sin red alcanzable
        validos = [r for r in resultados_raw if r is not None]
        omitidos = len(tareas) - len(validos)
        if omitidos:
            print(f"  ⚠ {omitidos} manzanas sin red vial alcanzable (omitidas)")

        if not validos:
            print(f"  Sin resultados para {alcaldia}, continuando...\n")
            continue

        routes_gdf = gpd.GeoDataFrame(
            [
                {"CVEGEO": r[0], "colonia": r[1], "alcaldia": r[2], "geometry": r[3]}
                for r in validos
            ],
            crs="EPSG:32614",
        )

        # Cruce espacial con equipamiento
        print(f"  Cruzando {len(routes_gdf):,} rutas con capas de equipamiento...")
        resultado_gdf = cruzar_capas(routes_gdf, pts_data, lns_data, lns_unions)

        # Exportar
        resultado_gdf.to_file(archivo_salida, driver="GPKG", engine="pyogrio")
        t_alc = time.time() - t0
        print(f"  [OK] → {archivo_salida.name} | {len(resultado_gdf):,} manzanas | {t_alc:.1f}s\n")

    t_total = time.time() - t_inicio
    print(f"=== PROCESO COMPLETADO en {t_total/60:.1f} min ===")
    print(f"Resultados en: {OUTPUT_DIR.resolve()}")
