1. **¿Qué es la JVM y por qué es importante para correr aplicaciones como Dataverse?**
   
La JVM (Java Virtual Machine) es básicamente el motor de traducción. Su trabajo es coger el código Java y traducirlo al lenguaje de máquina específico del servidor donde estemos (ya sea Linux, Windows o Mac).

Importancia para Dataverse: La clave aquí es la portabilidad. Gracias a la JVM, podemos desarrollar Dataverse una sola vez y desplegarlo en cualquier servidor con diferente sistema operativo sin tener que reescribir ni una línea de codigo. .

2. **¿Qué diferencias hay entre el JDK y el JRE?**

JRE (Java Runtime Environment): Es el entorno para ejecutar (correr) las aplicaciones. es lo que necesita el servidor para que el programa funcione.

JDK (Java Development Kit): Es el kit completo para desarrollar. Incluye todo lo que trae el JRE más las herramientas para compilar y depurar código.

3. **¿Qué es un WAR y cómo se relaciona con aplicaciones como Dataverse?**
Un WAR (Web Application Archive) es un archivo comprimido (como un .ZIP) que contiene toda la aplicación web lista para produccion.

Relación con Dataverse: Dataverse es una aplicación Jakarta EE y su entregable principal es justamente un archivo .war. El proceso es simple: nosotros "cargamos" este archivo en un servidor de aplicaciones el servidor se encarga de descomprimirlo, leer las configs y poner la aplicación en línea para los usuarios.

4. **¿Qué son las dependencias en JAVA?**
   
Son simplemente librerías externas o módulos de código que no escribimos nosotros.

6. **¿Explique cómo interpretar una excepción Java Básica?**
Una excepción es la forma en que Java grita que algo salió mal. Para entender qué pasó sin perderse, hay que mirar el Stack Trace (la lista de pasos del error) siguiendo este orden lógico:

Mira la primera línea (El "Qué"): Ahí te dice el tipo de error (ej. NullPointerException = algo estaba vacío).

Busca el "Caused by" (La Raíz): Si el error es largo, baja hasta encontrar esto. Generalmente aquí está el problema real (ej. conexión rechazada).

Identifica tu código (El "Dónde"): Busca en la lista la línea que empiece con el nombre de nuestro paquete (ej. edu.harvard.iq.dataverse...). Esa línea te dice exactamente en qué parte del código explotó.
