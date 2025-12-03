📚 Resumen: Prueba Técnica Dataverse (SIATA)

Autor: Santiago Naranjo Sánchez
Contacto: naranjosanti2@gmail.com | 3128705756

🚀 Enfoque y Diseño General

El proyecto se desarrolló bajo la filosofía de modularidad y transparencia, utilizando Python para todos los scripts.

1. Principios Clave

Estructura por Puntos: Cada requisito de la prueba se aisló en una carpeta independiente (punto1_, punto2_, etc.) para facilitar la revisión y ejecución.

Estructura por Capas: Se implementó un patrón src/, data/, y salida/ para separar claramente la lógica, los insumos y los resultados generados.

Configuración Centralizada: El acceso a Dataverse (BASE_URL, API_TOKEN) se gestionó desde un único archivo (config.py).

Trazabilidad y Errores: Se priorizó el manejo explícito de errores y la generación de reportes detallados (CSV) para identificar qué filas o llamadas a la API fallaron.

⚙️ Estructura del Repositorio

SIATA/
├─ punto1_java_conceptos/     # Conceptos de Java y Diagrama de Arquitectura.
├─ punto2_procesamiento_csv/      # Procesamiento y validación de datos de sensores.
├─ punto3_creacion_datasets/      # Creación masiva de datasets vía API.
├─ punto4_actualizacion_geoespacial/ # Actualización de metadatos geoespaciales (Desafío principal).
├─ punto5_descarga_datasets/      # Descarga de archivos y guía para usuario no técnico.
└─ README_resumen.md              # Este archivo.


📝 Resumen por Puntos

Punto 1: Conceptos de Java y Arquitectura

Propósito: Responder las preguntas teóricas sobre POO, JVM y la arquitectura de la solución implementada, incluyendo el diagrama de la misma.

Documentación: El detalle de las respuestas se encuentra en punto1_java_conceptos/README.md.

Punto 2: Procesamiento y Validación CSV

Propósito: Leer, validar y resumir registros de sensores.

Salidas:

salida/resumen_por_sensor.csv (Conteo, promedio, min/max).

salida/errores.csv (Filas fallidas y motivo).

Archivos JSON con las mediciones válidas por cada sensor_id.

Punto 3: Creación Masiva de Datasets

Propósito: Automatizar la creación de N datasets en Dataverse usando el API REST.

Lógica: Utiliza un JSON base de metadatos y el API_TOKEN para publicar datasets de prueba.

Salidas: Mensajes de confirmación en consola con persistentId de los datasets creados.

Punto 4: Actualización Geoespacial (Limitación)

Propósito: Actualizar masivamente el bloque de metadatos geoespaciales a partir de un CSV.

Lógica: Construye el JSON del bloque geospatial (cobertura y bounding box) e intenta actualizar vía editMetadata.

⚠️ Limitación Crítica: A pesar de que el código construye el payload correctamente y la lógica de validación está completa, la instancia de Dataverse en https://pruebas.siata.gov.co devuelve sistemáticamente un error 500 al intentar la edición de metadatos, impidiendo la publicación final. El código incluye la gestión de este error y la generación del reporte.

Punto 5: Descarga de Archivos

Propósito: Descargar archivos de múltiples datasets automáticamente, y proveer una guía para usuarios no técnicos.

Insumo: data/datasets_a_descargar.csv (lista simple de DOIs).

Salidas: Carpetas ordenadas en salida/<doi_normalizado>/ con todos los archivos descargados.

Documentación: Incluye un README_guia.md con instrucciones "a prueba de errores" para ejecutar el script con un solo comando.

▶️ Ejecución de los Scripts

Cada punto se ejecuta de forma independiente desde su carpeta src/:

# Ejemplo para ejecutar el Punto 2
cd punto2_procesamiento_csv/src
python main.py

# Ejemplo para ejecutar el Punto 4 (actualización geoespacial)
cd punto4_actualizacion_geoespacial/src
python main.py