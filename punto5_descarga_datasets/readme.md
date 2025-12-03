# 📥 GUÍA ULTRA SENCILLA PARA DESCARGAR DATASETS DESDE DATAVERSE

Esta guía está pensada para alguien que **no programa**, pero igual necesita bajar archivos desde Dataverse usando el script. Si sigues los pasos tal cual, lo logras 💪😄

---

## 1️⃣ ¿Qué hace este programa? 💻

Imagina que Dataverse es una estantería con cajas de archivos (datasets) 📦.

Este programa:

* Mira qué cajas (**datasets**) tú le indiques.
* Entra a cada caja.
* Se trae **todos los archivos** y los guarda en tu computador, en carpetas ordenadas 🗂️.

**Tú solo tienes que:**

1.  Decir qué datasets quieres bajar (en un archivito CSV).
2.  Ejecutar **un solo comando**.
3.  Abrir la carpeta donde quedan los archivos descargados.

---

## 2️⃣ ¿Qué cosas ya están listas? ✅

Alguien técnico ya dejó preparado:

* La carpeta del proyecto, por ejemplo:
    `C:\Users\Usuario\Documentos\SIATA\punto5_descarga_datasets\`
* El archivo de configuración `config.py` con:
    * La dirección del servidor Dataverse.
    * El token de API (la “llave” para entrar 🔑).
* El código que habla con Dataverse y descarga los archivos.

> 👉 **Tú NO necesitas tocar el código.**
> Solo vas a editar un archivo de texto y ejecutar un comando.

---

## 3️⃣ Paso 1: decir qué datasets quieres bajar 📋

1.  Ve a la carpeta del proyecto:
    `punto5_descarga_datasets`

2.  Entra a la carpeta:
    `data`

3.  Abre el archivo:
    `datasets_a_descargar.csv`

    Puedes abrirlo con **Excel, LibreOffice o el Bloc de notas**.

---

### 💡 Dentro del archivo CSV

Dentro verás algo parecido a esto:

| id\_dataset |
| :--- |
| doi:10.5072/FK2/EREVDH |
| doi:10.5072/FK2/NWYUQS |

* 🔹 La primera línea (`id_dataset`) **NO se toca**.
* 🔹 Debajo, cada línea es un dataset que quieres descargar (su DOI).

**Si quieres cambiar qué datasets se descargan:**

* **Para quitar uno** → borra esa línea.
* **Para agregar uno** → escribe un DOI nuevo en una línea nueva.

> **Ejemplos válidos (deben tener el prefijo `doi:`):**
>
> `doi:10.5072/FK2/EREVDH`
>
> `doi:10.5072/FK2/NWYUQS`

Cuando termines:

4.  💾 **Guarda** el archivo y ciérralo.

---

## 4️⃣ Paso 2: ejecutar el programa (un solo comando ▶️)

Ahora vamos a “darle play” al programa.

1.  Abre el **Explorador de archivos** y ve a:
    `C:\Users\Usuario\Documentos\SIATA\punto5_descarga_datasets\src`
    (Es la carpeta donde está `main.py`).

2.  En la parte de arriba, donde aparece la ruta (ej: `C:\Users\Usuario\...`):
    * Haz clic allí.
    * Escribe:
        ```text
        cmd
        ```
    * Presiona **Enter**.

> 👉 Se abrirá una **ventana negra (Símbolo del sistema)** ya ubicada en la carpeta `src`. No tienes que navegar nada más.

3.  En esa ventana negra, escribe:
    ```python
    python main.py
    ```
    y presiona **Enter**.

4.  **Monitorea la descarga:**
    Verás mensajes como:
    ```
    [INFO] Se encontraron 2 datasets en el CSV.
    [doi:10.5072/FK2/EREVDH] Descargando archivo ...
    [OK] Descarga finalizada.
    ```
    Cuando veas `[OK] Descarga finalizada.`, significa que el programa terminó de bajar todos los archivos ✅.

---

## 5️⃣ Paso 3: ver los archivos descargados 📂

1.  Vuelve a la carpeta del proyecto:
    `punto5_descarga_datasets`

2.  Entra a la carpeta:
    `salida`

3.  **Resultado:**
    Dentro vas a ver una carpeta por cada dataset, por ejemplo:
    * `doi_10.5072_FK2_EREVDH`
    * `doi_10.5072_FK2_NWYUQS`

4.  **Abre una de esas carpetas 👀:**
    Allí estarán los archivos que Dataverse tenía en ese dataset (`.csv`, `.txt`, `.md`, etc.).

Esos archivos ya están en tu computador, listos para usar.

---

## 6️⃣ Mini explicación de “qué hay detrás” (por si te da curiosidad 🤓)

* **`main.py`**:
    * Lee la lista de datasets desde `data/datasets_a_descargar.csv`.
    * Para cada dataset, llama a funciones que hablan con Dataverse.

* El programa usa una “puerta” llamada **API** (Application Programming Interface):
    * Le pregunta a Dataverse qué archivos tiene el dataset.
    * Descarga cada archivo y lo guarda en la carpeta `salida`.

Pero lo importante para ti es:

1.  ✏️ Editas el CSV (`datasets_a_descargar.csv`) para decir qué datasets quieres.
2.  ▶️ Ejecutas `python main.py`.
3.  📂 Abres `salida/` y ahí tienes los archivos.

**¡Eso es todo!** 💚