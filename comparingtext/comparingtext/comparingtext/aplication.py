#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

#-------------------------------------- Importa las librerías --------------------------------------
import psycopg2, sys
import comparingtext.comparingtext.nltk_similarity
from comparingtext.comparingtext.nltk_similarity import *

#--------------------------------- Definición de Variables Globales --------------------------------
conexion = psycopg2.connect(database='silabos',user='ucuenca',password='ucuenca2017', host='172.17.0.2')
cursor = conexion.cursor()
#id_asignatura1 = str(sys.argv[1])
#id_asignatura2 = str(sys.argv[2])
id_asignatura1 = "118"
id_asignatura2 = "219"

#------------------------------------- Definición de Funciones -------------------------------------
def nombre(id_asignatura):
    cursor.execute("SELECT DISTINCT nombre_asignatura FROM silabo WHERE id_silabo='"+id_asignatura+"'")
    rows = cursor.fetchall()
    desc = rows[0][0]
    return desc

def descripcion(id_asignatura):
    cursor.execute("SELECT DISTINCT descripcion_silabo FROM silabo WHERE id_silabo='"+id_asignatura+"'")
    rows = cursor.fetchall()
    desc = rows[0][0]
    return desc

#------------------------------------ Extracción de los Textos ------------------------------------
nombre_asignatura1 = nombre(id_asignatura1)
nombre_asignatura2 = nombre(id_asignatura2)

texto1 = descripcion(id_asignatura1)
texto2 = descripcion(id_asignatura2)

print("\nLa descripción de la Asignatura '"+nombre_asignatura1+"' es: "+texto1+"\n")
print("La descripción de la Asignatura '"+nombre_asignatura2+"' es: "+texto2+"\n")
print("El porcentaje de similitud de las descripciones según los 4 algoritmos se presenta a continuación:")

#--------------------------------- Preprocesamiento de los Textos ---------------------------------
#texto1_normalize = normalization(texto1)
#texto1_tokenize = tweet_tokenization(texto1_normalize)
texto1_tokenize = tweet_tokenization(texto1)
texto1_stopping = stopping(texto1_tokenize)
texto1_stemming = snowball_stemming(texto1_stopping)

#texto2_normalize = normalization(texto2)
#texto2_tokenize = tweet_tokenization(texto2_normalize)
texto2_tokenize = tweet_tokenization(texto2)
texto2_stopping = stopping(texto2_tokenize)
texto2_stemming = snowball_stemming(texto2_stopping)


def get_value():
    return str(round(jaccard_similarity(texto1_stemming, texto2_stemming)*100,2))

#---------------------------------- Ejecución de los Algoritmos -----------------------------------
print('Índice de Jaccard: '+str(round(jaccard_similarity(texto1_stemming, texto2_stemming)*100,2))+'%')
#print('Similitud Coseno: '+str(round(nltk_similarity.cosine_similarity(texto1_normalize, texto2_normalize)*100,2))+'%')
print("Coeficiente de Sorensen-Dice: "+str(round(dices_similarity(texto1_stemming, texto2_stemming)*100,2))+'%')
print("Coeficiente de Superposición: "+str(round(overlap_similarity(texto1_stemming, texto2_stemming)*100,2))+'%\n')

