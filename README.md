# trío tristeza ODS

Este proyecto tiene como objetivo el análisis y la visualización de datos para realizar una evaluación de la accesibilidad en la Ciudad de México. Buscando identificar las zonas de la CDMX en las que vivir, trabajar y descansar pueda suceder en en recorridos de menos de 15 minutos (Moreno, 2021) y a partir de la interpretación de este análisis identificar la asimetría urbana (Ziccardi-Contigiani y Dammert, 2024) relacionada con la movilidad, la inclusividad y la sostenibilidad y con ello visibilizar las relaciones espaciales de inclusividad, seguridad, resiliencia y sostenibilidad; para con ello responder a la pregunta:

> ¿Qué tan cercana está la Ciudad de México de cumplir las metas del ODS 11 para convertirse en un espacio donde la movilidad, la seguridad, la inclusividad, y la sostenibilidad sean un derecho y no un privilegio?

### ODS 11

El ODS 11 nos interesa porque, pensamos que las ciudades como espacios sociales, deberían pensarse, planearse y vivirse como entornos equitativos, de visibilización y de justicia espacial; para lograr que la inclusión, la movilidad, la seguridad, la resiliencia y la sostenibilidad se conviertan en un derecho y no un privilegio.

### ¿Qué queremos visibilizar con los datos?

Buscamos visibilizar procesos de asimetría urbana, relacionados con la movilidad, la seguridad, la inclusividad y la sostenibilidad. Tomando como base la propuesta de Carlos Moreno (2021); donde describe un modelo que busca repensar las ciudades en las que vivir, trabajar y descansar pueda suceder en recorridos de menos de 15 minutos, ya sea a pie o en bicicleta, desde el hogar.

A partir de realizar un cruce espacial de insumos de movilidad, demografía, accesibilidad, distancias del hogar a puntos de recreación y comercio, infraestructura peatonal y ciclista; buscamos identificar las zonas de la CD. MX. que podrían considerarse inclusivas, seguras, resilientes y sostenibles frente a los criterios de proximidad, digitalización, diversidad y densidad propuestos por Carlos Moreno (2021); y, por lo tanto, propensos a cumplir las metas locales del ODS 11.

Tenemos la hipótesis de que el resultado de este análisis permitirá identificar y visibilizar relaciones espaciales de desigualdad estructural con accesos diferenciados, vinculados a dinámicas de exclusión producto de un modelo de desarrollo que busca el beneficio de las clases dominantes.

### Fuentes de datos

Las fuentes de datos consideradas para este análisis articulan información de distintas bases de datos que demuestran la complejidad urbana. Principalmente de la plataforma de datos abiertos de la CDMX y datos del INEGI. Se trabajará en cuatro dimensiones de análisis para identificar que zonas se acercan al ideal de Moreno (2021) y contrastarlo con las metas del ODS:

* **Proximidad**: Infraestructura ciclista, Metro, Metrobús, RTP, transporte eléctrico y vialidades primarias.
* **Diversidad**: Escuelas públicas y privadas, hospitales, centros de salud y áreas verdes, Directorio Estadístico Nacional de Unidades Económicas (INEGI).
* **Densidad**: Grupos poblacionales (Censo de Población y Vivienda 2020, INEGI), densidad de construcción.
* **Digitalización**: Puntos de acceso WiFi gratuito en distintas zonas de la ciudad, módulos de Ecobici, módulo de pago de movilidad integrada. 


## Características principales

Para la implementación utilizamos un enfoque basado en Python para el procesamiento de datos y **Quarto** para la generación de un tablero de control (dashboard) interactivo.

- **Análisis de Datos:** Procesamiento y limpieza de datos mediante `pandas`.
- **Geolocalización:** Visualización de indicadores en mapas interactivos con `folium` y `geopandas`.
- **Dashboard Interactivo:** Generación de un sitio web estático pero dinámico utilizando `Quarto`.
- **Visualización:** Gráficos avanzados con `plotly` y `matplotlib`.

## Estructura del proyecto

```text
.
├── .github/workflows/       # Automatización de despliegue (CI/CD)
├── dashboard/               # Archivos fuente del dashboard Quarto
├── presentacion/            # Diapositivas en Quarto (RevealJS)
├── datos/                   # Gestión de conjuntos de datos
│   ├── crudos/              # Datos originales sin procesar
│   └── procesados/          # Datos limpios para el dashboard
├── notebooks/               # Cuadernos Jupyter para exploración
├── scripts/                 # Scripts Python de automatización
├── main.py                  # Script orquestador del flujo
├── ai-log.md                # Registro de uso de Inteligencia Artificial
├── LICENSE                  # Licencia Creative Commons CC BY-SA 4.0
└── README.md                # Documentación del proyecto
```

## Cómo empezar

Este proyecto utiliza `uv` para la gestión de dependencias. Para configurar el entorno:

1. Instala `uv` si aún no lo tienes.
2. Sincroniza las dependencias:
   ```bash
   uv sync
   ```
3. Para renderizar el dashboard:
   ```bash
   cd dashboard
   quarto render
   ```

## Despliegue

El proyecto se publica automáticamente mediante GitHub Actions en las siguientes rutas:
- **Dashboard**: `https://trio-tristeza.github.io/hackods-unam/`
- **Presentación**: `https://trio-tristeza.github.io/hackods-unam/presentacion/`

## Referencias



## Licencia

Este proyecto está bajo la licencia **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

