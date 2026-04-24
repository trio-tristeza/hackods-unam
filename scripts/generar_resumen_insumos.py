"""
generar_resumen_insumos.py

Genera un resumen JSON con el conteo de registros de cada uno de los 8 insumos
utilizados en el análisis de la ciudad de 15 minutos.

Salida:
    dashboard/datos/resumen_insumos.json

Ejecutar desde la raíz del proyecto:
    uv run python scripts/generar_resumen_insumos.py
"""

import json
import geopandas as gpd
from pathlib import Path

BASE    = Path("datos/procesados/procesados_2_etapa/")
OUT     = Path("dashboard/datos/resumen_insumos.json")

INSUMOS = [
    {
        "nombre":     "Comercios alta densidad",
        "archivo":    "denue.gpkg",
        "categoria":  "Diversidad",
        "fuente":     "DENUE, INEGI",
        "tipo":       "Puntos",
        "filtro":     lambda gdf: gdf[gdf["prioridad"] == "Alta"],
    },
    {
        "nombre":     "Comercios media densidad",
        "archivo":    "denue.gpkg",
        "categoria":  "Diversidad",
        "fuente":     "DENUE, INEGI",
        "tipo":       "Puntos",
        "filtro":     lambda gdf: gdf[gdf["prioridad"] == "Media"],
    },
    {
        "nombre":     "Escuelas",
        "archivo":    "escuelas_total.gpkg",
        "categoria":  "Diversidad",
        "fuente":     "Equipamiento INEGI",
        "tipo":       "Puntos",
        "filtro":     None,
    },
    {
        "nombre":     "Hospitales y centros de salud",
        "archivo":    "hospitales_cs.gpkg",
        "categoria":  "Diversidad",
        "fuente":     "Equipamiento INEGI",
        "tipo":       "Puntos",
        "filtro":     None,
    },
    {
        "nombre":     "Puntos WiFi gratuito",
        "archivo":    "rp_wifiCDMX.gpkg",
        "categoria":  "Digitalización",
        "fuente":     "CDMX Abierta",
        "tipo":       "Puntos",
        "filtro":     None,
    },
    {
        "nombre":     "Estaciones de transporte",
        "archivo":    "transporte_estaciones.gpkg",
        "categoria":  "Proximidad",
        "fuente":     "RNC",
        "tipo":       "Puntos",
        "filtro":     None,
    },
    {
        "nombre":     "Infraestructura ciclista",
        "archivo":    "infra_ciclista_total.gpkg",
        "categoria":  "Proximidad",
        "fuente":     "RNC",
        "tipo":       "Líneas",
        "filtro":     None,
    },
    {
        "nombre":     "Rutas de transporte público",
        "archivo":    "transporte_rutas.gpkg",
        "categoria":  "Proximidad",
        "fuente":     "RNC",
        "tipo":       "Líneas",
        "filtro":     None,
    },
]

CATEGORIA_COLOR = {
    "Diversidad":    "#80b1d3",
    "Digitalización":"#b3de69",
    "Proximidad":    "#fdb462",
}


def main():
    resultado = []
    archivos_cargados = {}

    for ins in INSUMOS:
        archivo = ins["archivo"]
        ruta = BASE / archivo

        if archivo not in archivos_cargados:
            print(f"  Cargando {archivo}...")
            archivos_cargados[archivo] = gpd.read_file(ruta)

        gdf = archivos_cargados[archivo]
        if ins["filtro"]:
            gdf = ins["filtro"](gdf)

        if ins["tipo"] == "Líneas":
            gdf_m = gdf.to_crs(epsg=32614)
            valor = round(gdf_m.geometry.length.sum() / 1000, 1)
            unidad = "km"
        else:
            valor = len(gdf)
            unidad = "registros"

        resultado.append({
            "nombre":    ins["nombre"],
            "categoria": ins["categoria"],
            "fuente":    ins["fuente"],
            "tipo":      ins["tipo"],
            "valor":     valor,
            "unidad":    unidad,
            "color":     CATEGORIA_COLOR[ins["categoria"]],
        })
        print(f"  → {ins['nombre']}: {valor:,} {unidad}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    print(f"\n→ {OUT}")


if __name__ == "__main__":
    main()
