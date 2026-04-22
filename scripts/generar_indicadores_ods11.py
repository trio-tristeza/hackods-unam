"""
Genera datos de indicadores ODS 11 para los 32 estados de México
consultando la API del INEGI (BISE).

Salida: datos/procesados/procesados_2.5_etapa/ods11_final.json

Formato de salida:
[
  {
    "nombre": "11.1.1 Viviendas Precarias (%)",
    "nacional": 4.42,
    "datos": [{"cvegeo": "01", "valor": 4.64}, ...]
  },
  ...
]
"""

import requests
import json
import os
import time

TOKEN = "99ec42c6-f288-2953-2947-f49c55866164"

INDICADORES = {
    "6200240311": "11.1.1 Viviendas Precarias (%)",
    "6200240312": "11.2.1 Acceso Transporte (%)",
    "6200240318": "11.3.1 Relación Expansión Suelo",
    "6200240314": "11.r.2.1a Tiempo Traslado (min)",
    "6200240323": "11.6.1.a Residuos Sólidos (%)",
    "6200240325": "11.6.2.a Partículas PM2.5",
    "6200240326": "11.6.2.b Partículas PM10",
    "6200240320": "11.4.1 Gasto Patrimonio ($)",
    "6200240319": "11.7.1 Espacios Públicos (%)",
    "6200240315": "11.r.2.1b Traslado Indígena (min)",
}

ESTADOS = [str(i).zfill(2) for i in range(1, 33)]
NACIONAL = "00"

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "datos", "procesados", "procesados_2.5_etapa"
)


def consultar_valor(id_ind, cobertura):
    url = (
        f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/"
        f"jsonxml/INDICATOR/{id_ind}/es/{cobertura}/true/BISE/2.0/{TOKEN}?type=json"
    )
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            for serie in data.get("Series", []):
                obs = serie.get("OBSERVATIONS", [])
                if obs:
                    return float(obs[-1]["OBS_VALUE"])
    except Exception as e:
        print(f"    Error {cobertura}/{id_ind}: {e}")
    return None


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    resultado = []

    for id_ind, nombre in INDICADORES.items():
        print(f"\nProcesando: {nombre}")

        val_nacional = consultar_valor(id_ind, NACIONAL)
        print(f"  Nacional: {val_nacional}")
        time.sleep(0.1)

        datos_estados = []
        for cve in ESTADOS:
            val = consultar_valor(id_ind, cve)
            if val is not None:
                datos_estados.append({"cvegeo": cve, "valor": val})
            time.sleep(0.05)

        resultado.append({
            "nombre": nombre,
            "nacional": val_nacional if val_nacional is not None else 0.0,
            "datos": datos_estados,
        })
        print(f"  Estados con datos: {len(datos_estados)}/32")

    out_path = os.path.join(OUTPUT_DIR, "ods11_final.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"\nDatos guardados en {out_path}")


if __name__ == "__main__":
    main()
