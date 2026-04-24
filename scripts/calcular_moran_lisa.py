"""
calcular_moran_lisa.py
Calcula el Índice de Moran Global y Local (LISA) para la accesibilidad urbana en la CDMX.
Utiliza KNN para manejar manzanas separadas por vialidades.

Uso:
    uv run python scripts/calcular_moran_lisa.py
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from libpysal.weights import KNN
from esda.moran import Moran, Moran_Local
from pathlib import Path

INPUT_DIR = Path("datos/procesados/procesados_4_etapa/")
OUTPUT_DIR = Path("datos/procesados/procesados_5_etapa/")
OUTPUT_FILE = OUTPUT_DIR / "moran_lisa_cdmx.geojson"

def main():
    print("Cargando y unificando manzanas clasificadas...")
    archivos = list(INPUT_DIR.glob("mnz_clas_*.geojson"))
    if not archivos:
        print("Error: No se encontraron archivos en la Etapa 4.")
        return

    gdfs = []
    for f in archivos:
        gdf = gpd.read_file(f)[["alcaldia", "colonia", "clasificacion", "geometry"]]
        gdfs.append(gdf)
    
    full_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True), crs="EPSG:4326")
    print(f"  Total de manzanas: {len(full_gdf):,}")

    # 1. Mapeo numérico
    mapping = {"Muy bajo": 0, "Bajo": 1, "Medio": 2, "Alto": 3}
    full_gdf["val_num"] = full_gdf["clasificacion"].map(mapping)
    full_gdf = full_gdf.dropna(subset=["val_num"])

    # 2. Proyectar a UTM 14N (coordenadas métricas) para cálculo de distancias
    print("Reproyectando a EPSG:32614...")
    full_gdf_proj = full_gdf.to_crs(epsg=32614)

    print("Calculando matriz de pesos espaciales (KNN, k=8)...")
    # Usamos KNN porque las manzanas están separadas por calles
    w = KNN.from_dataframe(full_gdf_proj, k=8)
    w.transform = 'r' 

    print("Calculando Moran Global...")
    y = full_gdf["val_num"].values
    moran = Moran(y, w)
    print(f"  Moran's I: {moran.I:.4f}")
    print(f"  p-value: {moran.p_sim:.4f}")

    print("Calculando Moran Local (LISA)...")
    moran_loc = Moran_Local(y, w, permutations=999)
    
    sig = 0.05 
    full_gdf["lisa_p"] = moran_loc.p_sim
    full_gdf["lisa_q"] = moran_loc.q
    
    lisa_labels = {1: "Alto-Alto", 2: "Bajo-Alto", 3: "Bajo-Bajo", 4: "Alto-Bajo"}
    
    def get_cluster_label(row):
        if row["lisa_p"] > sig:
            return "No significativo"
        return lisa_labels.get(row["lisa_q"], "No significativo")

    full_gdf["cluster"] = full_gdf.apply(get_cluster_label, axis=1)

    print(f"Distribución de clusters:\n{full_gdf['cluster'].value_counts()}")

    # 3. Exportar resultado
    print(f"Creando directorio {OUTPUT_DIR}...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    cols_out = ["alcaldia", "colonia", "clasificacion", "cluster", "geometry"]
    print(f"Guardando resultado en {OUTPUT_FILE}...")
    # Regresamos a WGS84 para el GeoJSON final
    full_gdf[cols_out].to_file(OUTPUT_FILE, driver="GeoJSON")
    
    print("\n¡Proceso completado exitosamente!")

if __name__ == "__main__":
    main()
