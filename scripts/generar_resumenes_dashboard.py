"""
generar_resumenes_dashboard.py

Genera resúmenes JSON de clasificación de manzanas por alcaldía y colonia
a partir de los GeoJSON de 4ª etapa.

Salida procesados:
    datos/procesados/procesados_4_etapa/
        resumen_alcaldias.json
        resumen_colonias.json

Dashboard (copia sincronizada):
    dashboard/datos/
        resumen_alcaldias.json
        resumen_colonias.json

Ejecutar desde la raíz del proyecto:
    uv run python scripts/generar_resumenes_dashboard.py
"""

import json
import shutil
import pandas as pd
import geopandas as gpd
from pathlib import Path

INPUT_DIR  = Path("datos/procesados/procesados_4_etapa/")
OUTPUT_DIR = INPUT_DIR
DASH_DIR   = Path("dashboard/datos/")


def generate_summaries():
    archivos = sorted(INPUT_DIR.glob("mnz_clas_*.geojson"))
    if not archivos:
        print("No se encontraron archivos GeoJSON.")
        return

    print(f"Cargando {len(archivos)} archivos...")
    df = pd.concat(
        [gpd.read_file(f)[["alcaldia", "colonia", "clasificacion"]] for f in archivos],
        ignore_index=True,
    )
    print(f"  Total manzanas: {len(df):,}")

    # ── Resumen por alcaldía ───────────────────────────────────────────────────
    alc_summary = []
    for alc, group in df.groupby("alcaldia"):
        counts = group["clasificacion"].value_counts(normalize=True) * 100
        alc_summary.append({
            "alcaldia":    alc,
            "pct_alto":    round(float(counts.get("Alto",    0)), 1),
            "pct_medio":   round(float(counts.get("Medio",   0)), 1),
            "pct_bajo":    round(float(counts.get("Bajo",    0)), 1),
            "pct_muy_bajo":round(float(counts.get("Muy bajo",0)), 1),
            "n_manzanas":  int(len(group)),
        })

    # ── Resumen por colonia ────────────────────────────────────────────────────
    col_summary = []
    for (alc, col), group in df.groupby(["alcaldia", "colonia"]):
        counts = group["clasificacion"].value_counts(normalize=True) * 100
        col_summary.append({
            "alcaldia":    alc,
            "colonia":     col,
            "pct_alto":    round(float(counts.get("Alto",    0)), 1),
            "pct_medio":   round(float(counts.get("Medio",   0)), 1),
            "pct_bajo":    round(float(counts.get("Bajo",    0)), 1),
            "pct_muy_bajo":round(float(counts.get("Muy bajo",0)), 1),
            "n_manzanas":  int(len(group)),
        })

    # ── Guardar en procesados_4_etapa/ ─────────────────────────────────────────
    out_alc = OUTPUT_DIR / "resumen_alcaldias.json"
    out_col = OUTPUT_DIR / "resumen_colonias.json"

    with open(out_alc, "w", encoding="utf-8") as f:
        json.dump(alc_summary, f, ensure_ascii=False, indent=2)
    with open(out_col, "w", encoding="utf-8") as f:
        json.dump(col_summary, f, ensure_ascii=False, indent=2)

    print(f"\n→ {out_alc}  ({out_alc.stat().st_size // 1024} KB, {len(alc_summary)} alcaldías)")
    print(f"→ {out_col}  ({out_col.stat().st_size // 1024} KB, {len(col_summary)} colonias)")

    # ── Copiar a dashboard/datos/ ──────────────────────────────────────────────
    DASH_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(out_alc, DASH_DIR / "resumen_alcaldias.json")
    shutil.copy(out_col, DASH_DIR / "resumen_colonias.json")
    print(f"\nSincronizado con {DASH_DIR.resolve()}")


if __name__ == "__main__":
    generate_summaries()
