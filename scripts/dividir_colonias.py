"""
dividir_colonias.py
Divide los archivos mnz_clas_*.geojson por colonia y genera un índice JSON
para consumo en dashboard con selección en cascada: alcaldía → colonia → geometría.

Ejecutar desde la raíz del proyecto:
    uv run python scripts/dividir_colonias.py

Salida:
    datos/procesados/procesados_4_etapa/colonias/
        index.json                          — índice de alcaldías y sus colonias
        {Alcaldia}/
            {colonia_normalizada}.geojson   — manzanas clasificadas de cada colonia

Estructura de index.json:
[
  {
    "nombre": "Azcapotzalco",
    "carpeta": "Azcapotzalco",
    "colonias": [
      { "nombre": "Ex-Hacienda El Rosario", "archivo": "ex-hacienda_el_rosario.geojson" },
      ...
    ]
  },
  ...
]

Cada GeoJSON de colonia contiene únicamente: clavegeo, clasificacion, geometry.
"""

import geopandas as gpd
import json
import shutil
import unicodedata
from pathlib import Path

INPUT_DIR   = Path("datos/procesados/procesados_4_etapa/")
OUTPUT_DIR  = INPUT_DIR / "colonias"
DASH_DIR    = Path("dashboard/datos/colonias")


def normalizar(texto: str) -> str:
    sin_tilde = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode()
    return (
        sin_tilde.lower()
        .replace(" ", "_")
        .replace(".", "")
        .replace("/", "_")
        .replace("(", "")
        .replace(")", "")
        .replace(",", "")
        .replace("'", "")
    )


def main():
    archivos = sorted(INPUT_DIR.glob("mnz_clas_*.geojson"))
    if not archivos:
        print(f"No se encontraron archivos mnz_clas_*.geojson en {INPUT_DIR}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    indice = []

    print(f"Procesando {len(archivos)} alcaldías...\n")

    for ruta in archivos:
        gdf = gpd.read_file(ruta)
        alcaldia = gdf["alcaldia"].iloc[0]
        carpeta_nombre = alcaldia.replace(" ", "_")
        carpeta_alc = OUTPUT_DIR / carpeta_nombre
        carpeta_alc.mkdir(exist_ok=True)

        colonias_lista = []

        for colonia, grupo in gdf.groupby("colonia"):
            nombre_archivo = f"{normalizar(colonia)}.geojson"
            ruta_salida = carpeta_alc / nombre_archivo

            grupo[["clavegeo", "clasificacion", "geometry"]].to_file(
                ruta_salida, driver="GeoJSON"
            )

            colonias_lista.append({
                "nombre": colonia,
                "archivo": nombre_archivo,
            })

        colonias_lista.sort(key=lambda x: x["nombre"])

        indice.append({
            "nombre": alcaldia,
            "carpeta": carpeta_nombre,
            "colonias": colonias_lista,
        })

        print(f"[{alcaldia}] {len(colonias_lista)} colonias exportadas")

    indice.sort(key=lambda x: x["nombre"])

    out_index = OUTPUT_DIR / "index.json"
    with open(out_index, "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=2)

    total_colonias = sum(len(a["colonias"]) for a in indice)
    print(f"\n{total_colonias} colonias en total")
    print(f"Índice → {out_index}")
    print(f"Archivos en: {OUTPUT_DIR.resolve()}")

    if DASH_DIR.exists():
        shutil.rmtree(DASH_DIR)
    shutil.copytree(OUTPUT_DIR, DASH_DIR)
    print(f"Sincronizado → {DASH_DIR.resolve()}")


if __name__ == "__main__":
    main()
