# Sistema de recomendación

## Contenido
1. [Introducción](#introducción)
2. [Objetivo](#objetivo)
3. [ETL](#etl)
4. [EDA](#eda)
5. [Modelo de recomendación](#modelo-de-recomendaciones)
6. [Conclusiones](#conclusiones)






# Introducción
En este proyecto podras encontrar como se construyó un sistema de recomendaciones, desde la extracción , transformación y carga de datos pasando por el análisis exploratorio y llegando a la generación del modelo de recomendaciones basado en items.

Utilice el algoritmo de NearestNeighbors con la metrica de coseno, que sin duda se puede mejorar pero para presentar 


# Objetivo
El objetivo es crear un producto mínimo viable en menos de 10 dias, que consiste en generar una api que este disponible en alguna plataforma publica y se tenga disponible un modelo de recomendaciones de peliculas.

## Estructura del Proyecto

- `datasets/`: Contiene los conjuntos de datos utilizados para entrenar y probar el modelo.
- `src/`: Código fuente del modelo de recomendaciones y scripts auxiliares.
- `main.py`: Script principal para ejecutar el sistema de recomendaciones.
- `requirements.txt`: Lista de dependencias necesarias para ejecutar el proyecto.

## Instalación

1. Clona este repositorio:
    ```bash
    git clone https://github.com/OscarMoralesMejia/modeloDeRecomendaciones.git
    cd modeloDeRecomendaciones
    ```

2. Crea un entorno virtual y actívalo:
    ```bash
    python -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```


# ETL
El archivo etl.py es responsable de las operaciones de Extracción, Transformación y Carga (ETL) en el proyecto. Aquí se detalla el flujo de trabajo para preparar los datos antes de utilizarlos en el modelo de recomendaciones.

Extracción de Datos:
Se cargaron datos de un archivo csv con de 45 000 observaciones el cual se utilizó la libreria pandas para su manipulación
Se checaron las columnas se limpiaron los datos, se checó el formato de fecha logrando un set de datos para las peliculas, uno para directores y otro para actores los cuales se pueden unir en determinado caso por medio del id de pelicula

Se puede ver mas detalle en el archivo etl.ipynb de todas las partes del etl.

# EDA
En este etapa del proyecto se analizaron los datos de tal manera que pudiesemos tener visivilidad de cuantas variables númericas y cuántas variables cualitativas teniamos para tomar un set de datos para una primer versión del modelo

Los valores atipicos en este set de datos no necesariamente se pueden ver como outlayers ya que no nos estamos tomando medidas estadisticas como el promedio para ver el comportamiento sino que se analizan los datos desde un enfoque de similaridad asi que no quitamos outlayers.

Podemos ver mediante las palabras mas usadas que las peliculas en su gran mayoria son de drama y comedia casi el 50%.


# Modelo de recomendaciones
El modelo de recomendación generado se baso en similaridad de coseno y los vecinos mas cercanos como primer acercamiento se utilizaron las columnas 'budget','revenue','popularity','vote_average','vote_count','año','return'como primer versión para tener un punto de partida. Otro modelo que podemos usar es vectorización de texto y similitud de coseno.


# Conclusiones
Al realizar el proyecto pude darme cuenta de que:
La calidad y cantidad de datos son fundamentales para el éxito de un sistema de recomendaciones. Datos insuficientes o de baja calidad pueden llevar a un modelo poco preciso y a recomendaciones irrelevantes.

La normalización, eliminación de valores atípicos y el manejo de datos faltantes son pasos esenciales para preparar los datos antes de entrenar el modelo.

Elegir el algoritmo adecuado (como NearestNeighbors, filtrado colaborativo, o modelos basados en contenido) y ajustar los parámetros (como el número de vecinos k) son cruciales para obtener buenos resultados.
Métricas como Precision y Recall son útiles para evaluar el rendimiento del modelo.

Lecciones aprendidas: 
El formato parquet no es dificil de manejar y ayuda mucho a usar los recursos de manera eficiente.
El Deployar un MVP puede ser muy rapido si se tiene el proyecto armado en github.
La limpieza de nulos es fundamental

### Autor
Oscar Morales Mejía 
oscar.moralesm@hotmail.com
