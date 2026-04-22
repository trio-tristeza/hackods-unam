"""
asignar_geometrias.py
Une los resultados de cruce_accesibilidad.py con las geometrías de manzana
y genera un GeoJSON limpio por alcaldía con clasificación de accesibilidad.

Ejecutar desde la raíz del proyecto:
    uv run python scripts/asignar_geometrias.py

Salida: datos/procesados/procesados_4_etapa/mnz_clas_{alcaldia}.geojson
Campos en cada capa:
    clavegeo      — clave geoestadística de la manzana
    alcaldia      — nombre de la alcaldía
    colonia       — nombre de la colonia
    clasificacion — Muy bajo (0-2) | Bajo (3-4) | Medio (5) | Alto (6+)
"""

import geopandas as gpd
import pandas as pd
from pathlib import Path

INPUT_DIR  = Path("datos/procesados/procesados_3_etapa/")
MANZANAS   = Path("datos/procesados/procesados_2_etapa/manzanas_cdmx_poblacion.gpkg")
OUTPUT_DIR = Path("datos/procesados/procesados_4_etapa/")


def clasificar_diversidad(serie: pd.Series) -> pd.Categorical:
    return pd.cut(
        serie,
        bins=[-1, 2, 4, 5, 100],
        labels=["Muy bajo", "Bajo", "Medio", "Alto"],
    )


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Cargando geometrías de manzanas...")
    manzanas = gpd.read_file(MANZANAS, engine="pyogrio")[["CVEGEO", "geometry"]]
    print(f"  {len(manzanas):,} manzanas cargadas | CRS: {manzanas.crs}")

    archivos = sorted(INPUT_DIR.glob("cruce_*.gpkg"))
    if not archivos:
        print(f"No se encontraron archivos en {INPUT_DIR}")
        return

    print(f"\nProcesando {len(archivos)} alcaldías...\n")

    for ruta in archivos:
        nombre = ruta.stem.replace("cruce_", "")
        salida = OUTPUT_DIR / f"mnz_clas_{nombre}.geojson"

        print(f"[{nombre}]", end=" ", flush=True)

        cruce = gpd.read_file(ruta, engine="pyogrio")

        resultado = manzanas.merge(
            cruce[["CVEGEO", "colonia", "alcaldia", "diversidad"]],
            on="CVEGEO",
            how="inner",
        )

        resultado["clasificacion"] = clasificar_diversidad(resultado["diversidad"])

        resultado = resultado.rename(columns={"CVEGEO": "clavegeo"})[
            ["clavegeo", "alcaldia", "colonia", "clasificacion", "geometry"]
        ]

        resultado.to_file(salida, driver="GeoJSON")
        print(f"{len(resultado):,} manzanas → {salida.name}")

    print(f"\nListo. Archivos en: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
