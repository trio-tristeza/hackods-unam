"""
generar_vistas_clasificacion.py
Genera capas GeoJSON simplificadas a distintos niveles de detalle para
soportar una visualización adaptativa por zoom en el dashboard:

  vista_cdmx.geojson
      4 features (uno por clasificación), CDMX completa.
      Uso: capa base visible siempre; zoom ciudad (~10–11).

  vista_alcaldias.geojson
      ~55–64 features (alcaldía × clasificación).
      Uso: al hacer zoom sobre una alcaldía (~12–13); se filtra por alcaldía.

  vistas/colonias/{Alcaldia}.geojson  (un archivo por alcaldía)
      Features por colonia × clasificación, cargados bajo demanda.
      Uso: al seleccionar una colonia específica (~14–15).

Pipeline de simplificación por nivel:
    dissolve(grupo)          — une todas las manzanas del mismo grupo
    buffer(0)                — repara topología del resultado disuelto
    simplify(tolerancia)     — reduce vértices residuales
    set_precision(grid)      — redondea coordenadas para reducir tamaño de archivo

Tolerancias (EPSG:4326; 0.001° ≈ 111 m):
    CDMX y alcaldías : simplify 0.003°, precision grid 0.001°  → ~1 MB c/u
    Colonias         : simplify 0.001°, precision grid 0.0003° → 200–1 300 KB/alcaldía

Ejecutar desde la raíz del proyecto:
    uv run python scripts/generar_vistas_clasificacion.py

Salida procesados:
    datos/procesados/procesados_4_etapa/vistas/
        vista_cdmx.geojson
        vista_alcaldias.geojson
        colonias/
            {Alcaldia}.geojson

Dashboard (copia sincronizada):
    dashboard/datos/vistas/
"""

import geopandas as gpd
import pandas as pd
import shutil
from pathlib import Path
from shapely import set_precision

INPUT_DIR  = Path("datos/procesados/procesados_4_etapa/")
OUTPUT_DIR = INPUT_DIR / "vistas"
DASH_DIR   = Path("dashboard/datos/vistas")

TOL_CIUDAD   = 0.003   # ~333 m — vista CDMX y alcaldías
GRID_CIUDAD  = 0.001   # ~111 m — precisión de coordenadas para vistas ciudad/alcaldía
TOL_COLONIA  = 0.001   # ~111 m — vista colonia
GRID_COLONIA = 0.0003  # ~33 m  — precisión de coordenadas para vistas colonia


def cargar_todo() -> gpd.GeoDataFrame:
    archivos = sorted(INPUT_DIR.glob("mnz_clas_*.geojson"))
    if not archivos:
        raise FileNotFoundError(f"No se encontraron mnz_clas_*.geojson en {INPUT_DIR}")

    gdfs = [
        gpd.read_file(r)[["alcaldia", "colonia", "clasificacion", "geometry"]]
        for r in archivos
    ]
    todo = gpd.GeoDataFrame(
        pd.concat(gdfs, ignore_index=True), crs="EPSG:4326"
    )
    print(f"  Total manzanas: {len(todo):,}")
    return todo


def disolver(
    gdf: gpd.GeoDataFrame,
    agrupar_por: list[str],
    tol: float,
    grid: float,
) -> gpd.GeoDataFrame:
    disuelto = gdf.dissolve(by=agrupar_por, as_index=False)
    disuelto["geometry"] = disuelto.geometry.buffer(0)
    disuelto["geometry"] = disuelto.geometry.simplify(tol, preserve_topology=True)
    disuelto["geometry"] = disuelto.geometry.apply(
        lambda g: set_precision(g, grid_size=grid)
    )
    disuelto = disuelto[disuelto.geometry.is_valid & ~disuelto.geometry.is_empty]
    return disuelto[agrupar_por + ["geometry"]]


def exportar(gdf: gpd.GeoDataFrame, ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(ruta, driver="GeoJSON")
    print(f"    → {ruta}  ({ruta.stat().st_size / 1024:.0f} KB,  {len(gdf)} features)")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Cargando manzanas clasificadas...")
    todo = cargar_todo()

    print(f"\n[1/3] vista_cdmx  (simplify={TOL_CIUDAD}°, grid={GRID_CIUDAD}°)")
    vista_cdmx = disolver(todo, ["clasificacion"], TOL_CIUDAD, GRID_CIUDAD)
    exportar(vista_cdmx, OUTPUT_DIR / "vista_cdmx.geojson")

    print(f"\n[2/3] vista_alcaldias  (simplify={TOL_CIUDAD}°, grid={GRID_CIUDAD}°)")
    vista_alc = disolver(todo, ["alcaldia", "clasificacion"], TOL_CIUDAD, GRID_CIUDAD)
    exportar(vista_alc, OUTPUT_DIR / "vista_alcaldias.geojson")

    print(f"\n[3/3] vistas/colonias por alcaldía  (simplify={TOL_COLONIA}°, grid={GRID_COLONIA}°)")
    vista_col = disolver(
        todo, ["alcaldia", "colonia", "clasificacion"], TOL_COLONIA, GRID_COLONIA
    )
    col_dir = OUTPUT_DIR / "colonias"
    col_dir.mkdir(exist_ok=True)
    for alcaldia, grupo in vista_col.groupby("alcaldia"):
        nombre_archivo = alcaldia.replace(" ", "_") + ".geojson"
        exportar(grupo.reset_index(drop=True), col_dir / nombre_archivo)

    print("\nSincronizando con dashboard/datos/vistas/ ...")
    if DASH_DIR.exists():
        shutil.rmtree(DASH_DIR)
    shutil.copytree(OUTPUT_DIR, DASH_DIR)
    print(f"  → {DASH_DIR.resolve()}")

    print("\nListo.")


if __name__ == "__main__":
    main()
