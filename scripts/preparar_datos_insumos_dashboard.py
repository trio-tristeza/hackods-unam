"""
Genera los datos para el mapa interactivo de Insumos (Sección 2) del dashboard.

Produce:
  dashboard/datos/colonias_jerarquia.json        — jerarquía alcaldía → colonias con bboxes y geometrías
  dashboard/datos/insumos_alcaldias/*.geojson     — puntos de insumos por alcaldía (un archivo por alcaldía)

Ejecutar desde la raíz del proyecto:
    uv run python scripts/preparar_datos_insumos_dashboard.py
"""

import geopandas as gpd
import json
import unicodedata
from pathlib import Path

BASE_2     = Path("datos/procesados/procesados_2_etapa/")
BASE_1     = Path("datos/procesados/procesados_1_etapa/")
DASH_DATOS = Path("dashboard/datos/")
OUT_INS    = DASH_DATOS / "insumos_alcaldias"

MAX_WIFI_POR_ALCALDIA = 300  # WiFi tiene 70k puntos; se limita por alcaldía


def normalizar(texto):
    """'Benito Juárez' → 'benito_juarez'"""
    sin_tilde = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode()
    return sin_tilde.lower().replace(" ", "_").replace(".", "").replace("/", "_")


def bounds_a_leaflet(bounds):
    """Convierte (minx, miny, maxx, maxy) a [[minLat, minLng], [maxLat, maxLng]]"""
    minx, miny, maxx, maxy = bounds
    return [[miny, minx], [maxy, maxx]]


def main():
    OUT_INS.mkdir(parents=True, exist_ok=True)

    # ----------------------------------------------------------
    # 1. Colonias y alcaldías
    # ----------------------------------------------------------
    print("Cargando colonias...")
    colonias = gpd.read_file(BASE_1 / "colonias_cdmx.gpkg").to_crs(epsg=4326)
    colonias["geometry"] = colonias.geometry.simplify(tolerance=0.0001, preserve_topology=True)

    alcaldias_gdf = colonias.dissolve(by="alc").reset_index()[["alc", "geometry"]]

    # ----------------------------------------------------------
    # 2. Capas de insumos (puntos)
    # ----------------------------------------------------------
    print("Cargando capas de insumos...")

    denue = gpd.read_file(BASE_2 / "denue.gpkg").to_crs(epsg=4326)
    denue = denue[denue["prioridad"] == "Alta"][["nmbr_st", "activdd", "geometry"]]
    denue = denue.rename(columns={"nmbr_st": "nombre"})
    denue["tipo"] = "denue_alta"

    escuelas = gpd.read_file(BASE_2 / "escuelas_total.gpkg").to_crs(epsg=4326)[["nombre", "tipo", "geometry"]]
    escuelas = escuelas.rename(columns={"tipo": "subtipo"})
    escuelas["tipo"] = "escuela"

    hospitales = gpd.read_file(BASE_2 / "hospitales_cs.gpkg").to_crs(epsg=4326)[["nombre", "geometry"]]
    hospitales["tipo"] = "hospital"

    wifi = gpd.read_file(BASE_2 / "rp_wifiCDMX.gpkg").to_crs(epsg=4326)[["programa", "geometry"]]
    wifi = wifi.rename(columns={"programa": "nombre"})
    wifi["tipo"] = "wifi"

    estaciones = gpd.read_file(BASE_2 / "transporte_estaciones.gpkg").to_crs(epsg=4326)[["NOMBRE", "SISTEMA", "geometry"]]
    estaciones = estaciones.rename(columns={"NOMBRE": "nombre", "SISTEMA": "subtipo"})
    estaciones["tipo"] = "transporte"

    capas = [denue, escuelas, hospitales, wifi, estaciones]

    # ----------------------------------------------------------
    # 3. Jerarquía de colonias → JSON
    # ----------------------------------------------------------
    print("Generando colonias_jerarquia.json...")
    jerarquia = []

    for alc_nombre in sorted(colonias["alc"].unique()):
        cols_alc   = colonias[colonias["alc"] == alc_nombre]
        alc_bounds = cols_alc.geometry.total_bounds

        lista_colonias = []
        for _, row in cols_alc.sort_values("colonia").iterrows():
            lista_colonias.append({
                "nombre":   row["colonia"],
                "bbox":     bounds_a_leaflet(row.geometry.bounds),
                "geometry": row.geometry.__geo_interface__,
            })

        jerarquia.append({
            "nombre":   alc_nombre,
            "archivo":  normalizar(alc_nombre),
            "bbox":     bounds_a_leaflet(alc_bounds),
            "colonias": lista_colonias,
        })

    out_hier = DASH_DATOS / "colonias_jerarquia.json"
    with open(out_hier, "w", encoding="utf-8") as f:
        json.dump(jerarquia, f, ensure_ascii=False, separators=(",", ":"))

    print(f"  colonias_jerarquia.json → {out_hier.stat().st_size / 1024:.0f} KB")

    # ----------------------------------------------------------
    # 4. GeoJSON de insumos por alcaldía
    # ----------------------------------------------------------
    print("Generando GeoJSON de insumos por alcaldía...")
    alc_idx = alcaldias_gdf.set_index("alc")

    for alc_nombre in sorted(colonias["alc"].unique()):
        archivo   = normalizar(alc_nombre)
        alc_mask  = alcaldias_gdf[alcaldias_gdf["alc"] == alc_nombre]
        features  = []

        for gdf in capas:
            try:
                subset = gpd.clip(gdf, alc_mask)
            except Exception:
                continue

            if subset.empty:
                continue

            # Limitar WiFi para no sobrecargar el navegador
            if subset["tipo"].iloc[0] == "wifi" and len(subset) > MAX_WIFI_POR_ALCALDIA:
                subset = subset.sample(MAX_WIFI_POR_ALCALDIA, random_state=42)

            for _, row in subset.iterrows():
                geom = row.geometry
                # Usar centroide si la geometría no es punto (por el buffer previo)
                if geom.geom_type != "Point":
                    geom = geom.centroid

                features.append({
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [round(geom.x, 6), round(geom.y, 6)]},
                    "properties": {
                        "tipo":   row["tipo"],
                        "nombre": str(row.get("nombre", "") or ""),
                    },
                })

        out_path = OUT_INS / f"{archivo}.geojson"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump({"type": "FeatureCollection", "features": features}, f,
                      ensure_ascii=False, separators=(",", ":"))

        print(f"  {alc_nombre}: {len(features):,} puntos → {out_path.stat().st_size / 1024:.0f} KB")

    print("\nListo. Archivos generados en dashboard/datos/")


if __name__ == "__main__":
    main()
