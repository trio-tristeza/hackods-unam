"""
generar_vista_moran.py

Simplifica el GeoJSON de Moran Local (LISA) a dos niveles de detalle:

  vista_moran_alcaldias.geojson   — alcaldía × cluster   (mapa dinámico folium)
  vista_moran_colonias.geojson    — colonia × cluster    (mapa estático PNG)

Entrada:
    datos/procesados/procesados_5_etapa/moran_lisa_cdmx.geojson   (~70 MB)

Salida procesados:
    datos/procesados/procesados_5_etapa/
        vista_moran_alcaldias.geojson
        vista_moran_colonias.geojson

Dashboard (copia sincronizada):
    dashboard/datos/vistas/
        vista_moran_alcaldias.geojson
        vista_moran_colonias.geojson

Ejecutar desde la raíz del proyecto:
    uv run python scripts/generar_vista_moran.py
"""

import shutil
import geopandas as gpd
from pathlib import Path
from shapely import set_precision

INPUT_FILE = Path("datos/procesados/procesados_5_etapa/moran_lisa_cdmx.geojson")
OUTPUT_DIR = Path("datos/procesados/procesados_5_etapa/")
DASH_DIR   = Path("dashboard/datos/vistas/")

TOL_ALC   = 0.003    # ~333 m — vista alcaldías (mapa dinámico)
GRID_ALC  = 0.001    # ~111 m
TOL_COL   = 0.001    # ~111 m — vista colonias (mapa estático)
GRID_COL  = 0.0003   # ~33 m


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


def exportar(gdf: gpd.GeoDataFrame, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    gdf.to_file(out, driver="GeoJSON")
    print(f"→ {out}  ({out.stat().st_size / 1024:.0f} KB, {len(gdf)} features)")


def main():
    print(f"Cargando {INPUT_FILE}  ({INPUT_FILE.stat().st_size / 1e6:.0f} MB)...")
    gdf = gpd.read_file(INPUT_FILE)[["alcaldia", "colonia", "cluster", "geometry"]]
    print(f"  Total manzanas: {len(gdf):,}")
    print(f"  Clústeres: {sorted(gdf['cluster'].unique())}")

    print(f"\n[1/2] vista alcaldías  (simplify={TOL_ALC}°, grid={GRID_ALC}°)")
    vista_alc = disolver(gdf, ["alcaldia", "cluster"], TOL_ALC, GRID_ALC)
    exportar(vista_alc, OUTPUT_DIR / "vista_moran_alcaldias.geojson")

    print(f"\n[2/2] vista colonias  (simplify={TOL_COL}°, grid={GRID_COL}°)")
    vista_col = disolver(gdf, ["alcaldia", "colonia", "cluster"], TOL_COL, GRID_COL)
    exportar(vista_col, OUTPUT_DIR / "vista_moran_colonias.geojson")

    print("\nSincronizando con dashboard/datos/vistas/ ...")
    DASH_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(OUTPUT_DIR / "vista_moran_alcaldias.geojson",
                DASH_DIR / "vista_moran_alcaldias.geojson")
    shutil.copy(OUTPUT_DIR / "vista_moran_colonias.geojson",
                DASH_DIR / "vista_moran_colonias.geojson")
    print(f"→ {DASH_DIR}")

    print("\nListo.")


if __name__ == "__main__":
    main()
