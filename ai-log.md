# AI log - Equipo Trío Tristeza

## Herramientas
- **Gemini CLI**: Interfaz de línea de comandos para interactuar con Gemini Pro.

## Filosofía de uso 
Utilizamos herramientas de IA para agilizar la descripción de la arquitectura del proyecto y la consulta sobre el uso de parámetros en distintas librerías para facilitar su uso.

## Registro de uso

### 2026-04-02 | Gemini CLI | Creación de README y Definición de Estructura
- **Tarea**: Crear una descripción del proyecto y estructurar los directorios de datos y análisis.
- **Prompt**: "puedes añadir una descripción al readme que explique brevemente de que trata el proyecto".
- **Resultado**: README.md completo con instrucciones de uso y estructura de directorios optimizada (`datos/crudos`, `datos/procesados`, `notebooks`).
- **Decisión**: Se decidió ajustar la estructura del documento en secciones para facilitar la lectura y explicación breve del proyecto. También se añadió una sección de "Cómo empezar" con `uv`, para describir brevemente como levantar el proyecto.

### 2026-04-02 | Gemini CLI | Estructura de Presentación con Quarto
- **Tarea**: Crear la estructura general de una presentación de diapositivas utilizando Quarto.
- **Prompt**: "puedes usar el directorio presentacion para hacer crear la estrcutura de un proyecto quarto que permita la visualización de una presentación de diapositivas con quarto".
- **Resultado**: Propuesta de construcción de poryecto quarto dentro de `presentacion/` con archivo `index.qmd` estructurado y propuesta de configuración de estilo.
- **Decisión**: Se utilizó la IA para facilitar la creación de la estructura base y posteriormente se realizaron modificaciones manuales sobre el estilo y el contenido específico de las diapositivas para adaptarlo a la narrativa del equipo.

### 2026-04-02 | Gemini CLI | Configuración de CI/CD para GitHub Pages
- **Tarea**: Configurar la integración continua para publicar automáticamente el dashboard y la presentación.
- **Prompt**: "puedes ayudarme a configurar dos sitios github pages uno para el dashboard y otr para la presentacion que funcionen con integracion continua".
- **Resultado**: Archivo `.github/workflows/publish.yml` configurado para renderizar ambos proyectos con Quarto y desplegarlos en `https://trio-tristeza.github.io/hackods-unam/` y `/presentacion/`.
- **Decisión**: Se optó por centralizar el despliegue en un solo flujo de trabajo de GitHub Actions para mayor eficiencia. Se configuró el Dashboard en el root y la presentación en una subcarpeta para mantener la organización.

### 2026-04-06 | Gemini CLI | Generación de Notebook Hello World
- **Tarea**: Generar un notebook de prueba llamado `hello_world.ipynb`.
- **Resultado**: Creación del archivo `notebooks/hello_world.ipynb` con celdas de código base.
- **Decisión**: Modifiqué el archivo generado para realizar la ejecución y pruebas pertinentes.
