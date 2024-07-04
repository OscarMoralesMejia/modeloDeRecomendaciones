from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import numpy as np


appi = FastAPI()

@appi.get("/")
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

@appi.get("peliculas_por_mes/{mes}")
def cantidad_filmaciones_por_mes(mes:str):
    """_summary_
        Consulta las paliculas de un determinado mes
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

@appi.get("/peliculas_por_dia/{dia}")
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
        print(dia_numero)
        #consulta los datos de las peliculas
        data_movies=consulta_datos()
        #Extraer el mes de la columna
        data_movies['release_date'] = pd.to_datetime(data_movies['release_date'], errors='coerce')
        
        data_movies['dia_semana_num'] = data_movies['release_date'].dt.weekday
        
        # Filtrar los registros que correspondan al mes indicado
        registros_filtrados = data_movies[data_movies['dia_semana_num'] == dia_numero]
        # Contar los registros filtrados
        num_observaciones = registros_filtrados.shape[0]
        
        respuesta="La cantidad de peliculas estrenadas en el dia"
        partes = [respuesta, dia.lower(), "son",str(num_observaciones)]
        respuesta = " ".join(partes)
    except Exception as e:
        print(f"Ocurrió un error: {e}")
        
    return respuesta

@appi.get("/score_por_titulo/{titulo}")
def score_titulo(titulo:str=''):
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

@appi.get("/votos_por_titulo/{titulo}")
def votos_titulo( titulo:str='' ):
    respuesta=''
    cantidad_votos=0
    promedio_votaciones=0
    try:
        if titulo=='':
            return "Proporciona un titulo de una pelicula"
        data_movies=consulta_datos()

        pelicula = data_movies[data_movies['original_title'].str.lower()==titulo.lower()]
        #print(type(pelicula)) 
        if pelicula.empty:
             return "pelicula no encontrada"
         
        if not pelicula.empty:
        # Obtener el valor de la columna 'vote_count' de la primera (y única) fila resultante
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

@appi.get("/actor/{nombre}")
def get_actor(nombre:str=''):
# Consulta de agregación
    conteo=0
    respuesta=''
    try:       
        data_movies=consulta_datos()
        #print(data_movies)
        data_actores=consulta_datos_actores()
        #print(data_actores)
        df_join_interno = pd.merge(data_movies, data_actores, left_on='id_orig',right_on='id', how='inner')
        #print(df_join_interno.columns)
        #print(df_join_interno.columns)
        
        conteo_peliculas = df_join_interno.groupby('cast_name')['original_title'].count().reset_index()
        conteo= conteo_peliculas.loc[conteo_peliculas['cast_name']==nombre]
        if not conteo.empty :
            num_conteo=conteo['original_title'].values[0]
            
            num_retorno=0
            suma_retorno = df_join_interno.groupby('cast_name')['return'].sum().reset_index()
            retorno=suma_retorno.loc[suma_retorno['cast_name']==nombre]
            num_retorno=retorno['return'].values[0]
            #print("suma:",str(suma_retorno))
            
            num_promedio =0
            promedio_retorno = df_join_interno.groupby('cast_name')['return'].mean().reset_index()
            #print("retorno:",promedio_retorno)
            promedio=promedio_retorno.loc[promedio_retorno['cast_name']==nombre]
            num_promedio=promedio['return'].values[0]
            
            #conteo_peliculas.columns = ['cast_name', 'conteo_peliculas','suma_retorno']
            parte1="El actor"
            parte2="ha participado de"
            parte3="cantidad de filmaciones, el mismo ha conseguido un retorno de"
            parte4="con un promedio de"
            parte5="por filmacion"
            partes=[parte1,nombre,parte2,str(num_conteo),parte3,str(num_retorno),parte4,str(num_promedio),parte5]
            #El actor X ha participado de X cantidad de filmaciones, el mismo ha conseguido un retorno de X con un promedio de X por filmación
            respuesta = " ".join(partes)
        else:
            return "El actor no esta en mi base de datos"
    except Exception as e:
        print(f"Ocurrió un error: {e}")
      
    return respuesta    
    
@appi.get("/director/{nombre}")
def get_director(nombre:str=''):
# Consulta de agregación
    conteo=0
    respuesta=''
    try:       
        data_movies=consulta_datos()
        #print(data_movies)
        data_directores=consulta_datos_directores()
        #print(data_actores)
        df_join_interno = pd.merge(data_movies, data_directores, left_on='id_orig',right_on='id', how='inner')
        #print(df_join_interno.columns)
        df_directores = df_join_interno[df_join_interno['crew_job'].str.lower() == 'director']
        #print(df_directores)
        conteo_peliculas = df_directores.groupby('crew_name')['original_title'].count().reset_index()
        conteo= conteo_peliculas.loc[conteo_peliculas['crew_name']==nombre]
        #print(conteo)
        
        if not conteo.empty :
            num_conteo=conteo['original_title'].values[0]
            print(num_conteo)
            
            # num_retorno=0
            # suma_retorno = df_join_interno.groupby('crew_name')['return'].sum().reset_index()
            # retorno=suma_retorno.loc[suma_retorno['crew_name']==nombre]
            # num_retorno=retorno['return'].values[0]
            #print("suma:",str(suma_retorno))
            
            num_promedio =0
            promedio_retorno = df_directores.groupby('crew_name')['return'].mean().reset_index()
            print("retorno:",promedio_retorno)
            promedio=promedio_retorno.loc[promedio_retorno['crew_name']==nombre]
            if not promedio.empty:
                num_promedio=promedio['return'].values[0]
                if pd.isna(num_promedio):
                    num_promedio = 0
                
                print("numero promedio",num_promedio)
                pelis=df_directores.loc[df_directores['crew_name']==nombre]
                print("pelis",pelis)
                peliculas=pelis.loc[:,['original_title','release_date','return','budget','revenue']]
                #df_directores_final=df_directores.loc[:,['id','crew_department','crew_id','crew_job','crew_name','budget','revenue']]
                print(peliculas) #, np.inf, -np.inf
                print(type(peliculas['return']))
                peliculas['return'].replace([np.nan], 0, inplace=True)
                peliculas['budget'].replace([np.nan], 0, inplace=True)
                peliculas['revenue'].replace([np.nan], 0, inplace=True)
                
                respuesta={'Exito como director':num_promedio,'peliculas':peliculas}
            
            else:
                 return "El actor no esta en mi base de datos"
    except Exception as e:
         print(f"Ocurrió un error: {e}")
      
    return respuesta
    
