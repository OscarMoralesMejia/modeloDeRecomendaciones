from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import numpy as np
import json
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from typing import List

app = FastAPI()
#uvicorn main:app --reload
@app.get("/")
def read_root():
    return {"message": "Bienvenido, a mi api sobre peliculas"}

def consulta_datos():
    data_movies=pd.read_csv('datasets/movies_limpio.csv',encoding='UTF-8',sep=',')
    return data_movies

def consulta_datos_actores():
    data_actores=pd.read_csv('datasets/actores_limpio.csv',encoding='UTF-8',sep=',')
    return data_actores

def consulta_datos_directores():
    data_directores=pd.read_csv('datasets/directores_limpio.csv',encoding='UTF-8',sep=',')
    return data_directores

@app.get("/peliculas_por_mes")
def cantidad_filmaciones_por_mes(mes:str):
    """_summary_
        Consulta el total de las peliculas de un determinado mes
    Args:
        mes (str, optional): Indica un mes en idioma español. Defaults to ''.

    Returns:
        str: Un mensaje con el número de observaciones de peliculas del mes solicitado
    """
    respuesta=''
    try:
        #Validar que no este vacio el parametro mes
        if mes=='':
            return "Debe proporcionar un mes en idioma Español"
        meses = {'enero': 1,'febrero': 2,'marzo': 3,'abril': 4,'mayo': 5,'junio': 6,'julio': 7,'agosto': 8,'septiembre': 9,'octubre': 10,'noviembre': 11,'diciembre': 12}
        #Valido el mes pasandolo a minusculas
        mes_numero = meses[mes.lower()]
        
        #consulta los datos de las peliculas
        data_movies=consulta_datos()
        
        #Extraer el mes de la columna
        data_movies['release_date'] = pd.to_datetime(data_movies['release_date'], errors='coerce')

        data_movies['mes'] = data_movies['release_date'].dt.month
        # Filtrar los registros que correspondan al mes indicado
        registros_filtrados = data_movies[data_movies['mes'] == mes_numero]
        # Contar los registros filtrados
        num_observaciones = registros_filtrados.shape[0]
        #Genero el mensaje de respuesta
        parte1="La cantidad de peliculas en el mes de"
        partes = [parte1, str(mes), "son",str(num_observaciones)]
        respuesta = " ".join(partes)
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        
    return respuesta

@app.get("/peliculas_por_dia/{dia}")
def cantidad_filmaciones_dia(dia:str=''):
    """Método que consulta las paliculas por dia

    Args:
        dia (str, optional): _description_. Defaults to ''.

    Returns:
        _type_: _description_
    """
    respuesta=''
    try:
        if dia=='':
            return "Proporciones un dia de la semana en Español"
        dias_semana={'lunes':0,'martes':1,'miercoles':2,'jueves':3,'viernes':4,'sabado':5,'domingo':6}
        dia_numero = dias_semana[dia.lower()]
        
        #consulta los datos de las peliculas
        data_movies=consulta_datos()
        #Extraer el mes de la columna
        data_movies['release_date'] = pd.to_datetime(data_movies['release_date'], errors='coerce')
        data_movies['dia_semana_num'] = data_movies['release_date'].dt.weekday
        
        # Filtrar los registros que correspondan al mes indicado
        registros_filtrados = data_movies[data_movies['dia_semana_num'] == dia_numero]
        # Contar los registros filtrados
        num_observaciones = registros_filtrados.shape[0]
        #Armado de respuesta
        respuesta="La cantidad de peliculas estrenadas en el dia"
        partes = [respuesta, dia.lower(), "son",str(num_observaciones)]
        respuesta = " ".join(partes)
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        
    return respuesta

@app.get("/score_por_titulo/{titulo}")
def score_titulo(titulo:str=''):
    """_summary_
        Esta función busca el año de estreno de la pelicula y su score
    Args:
        titulo (str, optional): Nombre de la Pelicula a buscar en español

    Returns:
        Regresa una cadena con el titulo de la pelicula su año de estreno y su score
    """
    respuesta=''
    try:
        if titulo=='':
            return "Proporciona un titulo de una pelicula"
        data_movies=consulta_datos()
        #resultado = df[df['titulo'].str.lower() == titulo]
        pelicula = data_movies[data_movies['original_title'].str.lower() == titulo.lower()]
        
        parte1="La pelicula"
        parte2="fue estrenada en el año"
        parte3="con un score de"
        partes = [parte1, titulo,parte2,str(pelicula['año'].values[0]) ,parte3,str(pelicula['popularity'].values[0])]
        respuesta = " ".join(partes)
        #cambiar por popularity
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        
    return respuesta

@app.get("/votos_por_titulo/{titulo}")
def votos_titulo( titulo:str='' ):
    """_summary_
        Esta función busca la cantidad de votos y el valor promedio de las votaciones.
        
    Args:
        titulo (str, optional): Nombre de la Pelicula a buscar en español

    Returns:
        Si la pelicula no cuenta con una puntuación mayor a 2000 puntos se regresa un mensaje de que 
        la pelicula no cuenta con al menos 2000 valoraciones de lo contrario regresa una cadena con el nombre de la pelicula 
        las valoraciones y el promedio
    """
    respuesta=''
    cantidad_votos=0
    promedio_votaciones=0
    try:
        if titulo=='':
            return "Proporciona un titulo de una pelicula"
        data_movies=consulta_datos()

        pelicula = data_movies[data_movies['original_title'].str.lower()==titulo.lower()]
         
        if pelicula.empty:
             return "pelicula no encontrada"
         
        if not pelicula.empty:
            cantidad_votos = pelicula['vote_count'].values[0]
            promedio_votaciones = str(pelicula['vote_average'].values[0])
        
        if cantidad_votos < 2000:
           return "La pelicula no cuenta con al menos 2000 valoraciones"
        
        parte1="La pelicula"
        parte2="fue estrenada en el año"
        parte3="La misma cuenta con un total de"
        parte4="valoraciones, con un promedio de"
        partes = [parte1, titulo,parte2,str(pelicula['año'].values[0]) ,parte3,str(cantidad_votos),parte4,promedio_votaciones]
        respuesta = " ".join(partes)
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")

    return respuesta

@app.get("/actor/{nombre}")
def get_actor(nombre:str=''):
    """_summary_
    Esta función busca la cantidad de peliculas en las que ha participado el actor y el promedio de retorno

    Args:
        nombre (str, optional): Nombre del actor

    Returns:
        Regresa una cadena con el nombre del actor, el número de peliculas en las que ha participado, y el retorno
        y promedio de retorno que ha generado
    """
    conteo=0
    respuesta=''
    try:       
        data_movies=consulta_datos()
        data_actores=consulta_datos_actores()
        df_join_interno = pd.merge(data_movies, data_actores, left_on='id_orig',right_on='id', how='inner')
        
        conteo_peliculas = df_join_interno.groupby('cast_name')['original_title'].count().reset_index()
        conteo= conteo_peliculas.loc[conteo_peliculas['cast_name']==nombre]
        if not conteo.empty :
            num_conteo=conteo['original_title'].values[0]
            
            num_retorno=0
            df_join_interno['return'] = df_join_interno['return'].replace([np.inf, -np.inf], 0)
            df_join_interno['return']=df_join_interno['return'].fillna(0)
            suma_retorno = df_join_interno.groupby('cast_name')['return'].sum().reset_index()
            retorno=suma_retorno.loc[suma_retorno['cast_name']==nombre]
            num_retorno=retorno['return'].values[0]
                        
            num_promedio =0
            promedio_retorno = df_join_interno.groupby('cast_name')['return'].mean().reset_index()
            
            promedio=promedio_retorno.loc[promedio_retorno['cast_name']==nombre]
            num_promedio=promedio['return'].values[0]
            
            parte1="El actor"
            parte2="ha participado de"
            parte3="cantidad de filmaciones, el mismo ha conseguido un retorno de"
            parte4="con un promedio de"
            parte5="por filmacion"
            partes=[parte1,nombre,parte2,str(num_conteo),parte3,str(round(num_retorno,2)),parte4,str(round(num_promedio,2)),parte5]
            respuesta = " ".join(partes)
        else:
            return "El actor no esta en mi base de datos"
    except Exception as e:
        print(f"Ocurrió un error: {e}")
      
    return respuesta    
    
@app.get("/director/{nombre}")
def get_director(nombre:str=''):
    """_summary_
        Busca el retorno que ha tenido como director y las peliculas en las que ha dirigido 
    Args:
        nombre (str, optional): Nombre del director

    Returns:
        Una lista de peliculas con el año de estreno retorno individual, costo y ganancia de la misma
    """
    conteo=0
    respuesta=''
    try:       
        data_movies=consulta_datos()
        data_directores=consulta_datos_directores()
        df_join_interno = pd.merge(data_movies, data_directores, left_on='id_orig',right_on='id', how='inner')
        
        df_directores = df_join_interno[df_join_interno['crew_job'].str.lower() == 'director']
        
        conteo_peliculas = df_directores.groupby('crew_name')['original_title'].count().reset_index()
        conteo= conteo_peliculas.loc[conteo_peliculas['crew_name']==nombre]
        
        if not conteo.empty :
            num_conteo=conteo['original_title'].values[0]
            
            num_promedio =0
            promedio_retorno = df_directores.groupby('crew_name')['return'].mean().reset_index()
            
            promedio=promedio_retorno.loc[promedio_retorno['crew_name']==nombre]
            if not promedio.empty:
                num_promedio=promedio['return'].values[0]
                if pd.isna(num_promedio):
                    num_promedio = 0
                
                pelis=df_directores.loc[df_directores['crew_name']==nombre]
                peliculas=pelis.loc[:,['original_title','release_date','return','budget','revenue']]
                peliculas['return'].replace([np.nan], 0, inplace=True)
                peliculas['budget'].replace([np.nan], 0, inplace=True)
                peliculas['revenue'].replace([np.nan], 0, inplace=True)
                
                respuesta={'Exito como director':num_promedio,'peliculas':peliculas}
            
            else:
                 return "El actor no esta en mi base de datos"
    except Exception as e:
         print(f"Ocurrió un error: {e}")
      
    return respuesta
    
@app.get("/recomendaciones")
def get_recomendacion(titulo:str):

    movies=pd.read_csv("datasets/movies_limpio.csv",sep=',',encoding='UTF-8')
    
    titulos=movies['original_title']
    
    df_titulos=pd.DataFrame(titulos)
    df_titulos
        
    X = movies.drop(columns=['original_title','original_language','release_date'])
    
    X['return']=X['return'].fillna(0)
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X['return']=X['return'].fillna(0)

    model = NearestNeighbors(metric='cosine', algorithm='auto')
    model.fit(X)

    movie_index = movies.loc[movies['original_title'].apply(lambda x: x.lower()) == titulo.lower()]
       
    if movie_index.empty:
        indice=-1
    else :
        indice=movie_index['id_orig'].index[0]
    
    distances, indices = model.kneighbors(X.iloc[indice, :].values.reshape(1, -1), n_neighbors=6)
      
    recomendaciones =[]
    for i in range(1, len(distances.flatten())):
        recomendacion = {
        "Recomendación": i,
        "Título": df_titulos.iloc[indices.flatten()[i]]['original_title'],
        "Distancia": distances.flatten()[i]
        }
        recomendaciones.append(recomendacion)

    mensaje_json = recomendaciones
        
    return mensaje_json
