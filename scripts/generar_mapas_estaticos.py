"""
generar_mapas_estaticos.py

Genera mapas PNG estáticos para el dashboard con las mismas paletas de colores
que los mapas dinámicos:

  dashboard/datos/mapas/mapa_colonias.png   — colonias clasificadas por accesibilidad
  dashboard/datos/mapas/mapa_moran.png      — clústeres LISA del I de Moran

Ambos mapas incluyen:
  - División por alcaldía con línea gris oscura delgada
  - Etiqueta pequeña en el centroide de cada alcaldía

Ejecutar desde la raíz del proyecto:
    uv run python scripts/generar_mapas_estaticos.py
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from pathlib import Path

COLONIAS_DIR = Path("dashboard/datos/vistas/colonias/")  # clasificación a nivel colonia
VISTAS_DIR   = Path("dashboard/datos/vistas/")            # Moran colonia y alcaldías
OUT_DIR      = Path("dashboard/datos/mapas/")

COLORS_CLAS = {
    "Alto":     "#2ca25f",
    "Medio":    "#99d8c9",
    "Bajo":     "#fec44f",
    "Muy bajo": "#e34a33",
}

COLORS_MORAN = {
    "Alto-Alto":        "#d7191c",
    "Bajo-Bajo":        "#2c7bb6",
    "Bajo-Alto":        "#abd9e9",
    "Alto-Bajo":        "#fdae61",
    "No significativo": "#cccccc",
}

BORDER_COLOR = "#444444"
LABEL_COLOR  = "#222222"


def abreviar(nombre: str, max_chars: int = 15) -> str:
    """Inserta salto de línea en nombres largos cerca de la mitad."""
    if len(nombre) <= max_chars:
        return nombre
    palabras = nombre.split()
    mitad = len(palabras) // 2
    return " ".join(palabras[:mitad]) + "\n" + " ".join(palabras[mitad:])


def make_map(
    gdf: gpd.GeoDataFrame,
    color_col: str,
    color_map: dict,
    out_path: Path,
    title: str = "",
) -> None:
    alc = gdf.dissolve(by="alcaldia").reset_index()

    fig, ax = plt.subplots(figsize=(8, 9), dpi=150)
    ax.set_aspect("equal")

    # Capas de clasificación / clúster — sin contorno entre polígonos
    for label, color in color_map.items():
        sub = gdf[gdf[color_col] == label]
        if not sub.empty:
            sub.plot(ax=ax, facecolor=color, edgecolor=(0, 0, 0, 0), linewidth=0)

    # Triple garantía: limpiar edge en todas las colecciones ya renderizadas
    for coll in ax.collections:
        coll.set_edgecolor((0, 0, 0, 0))
        coll.set_linewidths(0)
        coll.set_antialiased(False)

    # Bordes de alcaldía
    alc.boundary.plot(ax=ax, color=BORDER_COLOR, linewidth=0.7)

    # Etiquetas en centroides con halo blanco
    for _, row in alc.iterrows():
        c = row.geometry.centroid
        ax.annotate(
            abreviar(row["alcaldia"]),
            xy=(c.x, c.y),
            fontsize=5.5,
            ha="center",
            va="center",
            color=LABEL_COLOR,
            fontweight="semibold",
            linespacing=1.3,
            path_effects=[
                pe.withStroke(linewidth=2.5, foreground="white"),
            ],
        )

    # Leyenda
    patches = [mpatches.Patch(color=c, label=l) for l, c in color_map.items()]
    ax.legend(
        handles=patches,
        loc="lower left",
        fontsize=7,
        framealpha=0.85,
        edgecolor="#cccccc",
    )

    if title:
        ax.set_title(title, fontsize=10, fontweight="semibold", color="#222222", pad=8)

    ax.set_axis_off()
    fig.tight_layout(pad=0.3)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"→ {out_path}  ({out_path.stat().st_size // 1024} KB)")


def main():
    print("[1/2] Mapa colonias clasificadas (detalle colonia)...")
    archivos_col = sorted(COLONIAS_DIR.glob("*.geojson"))
    if not archivos_col:
        raise FileNotFoundError(f"No se encontraron GeoJSONs en {COLONIAS_DIR}")
    import pandas as pd
    gdf_clas = gpd.GeoDataFrame(
        pd.concat([gpd.read_file(f) for f in archivos_col], ignore_index=True),
        crs="EPSG:4326",
    )
    print(f"  {len(gdf_clas):,} features de {len(archivos_col)} alcaldías")
    make_map(
        gdf_clas,
        color_col="clasificacion",
        color_map=COLORS_CLAS,
        out_path=OUT_DIR / "mapa_colonias.png",
        title="Accesibilidad urbana por colonia — Ciudad de México",
    )

    print("[2/2] Mapa I de Moran (detalle colonia)...")
    make_map(
        gpd.read_file(VISTAS_DIR / "vista_moran_colonias.geojson"),
        color_col="cluster",
        color_map=COLORS_MORAN,
        out_path=OUT_DIR / "mapa_moran.png",
        title="Autocorrelación espacial (I de Moran Local — LISA)",
    )

    print("\nListo.")


if __name__ == "__main__":
    main()
