#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

#-------------------------------------- Importa las librerías --------------------------------------
import psycopg2, sys
import comparingtext.comparingtext.nltk_similarity
from comparingtext.comparingtext.nltk_similarity import *

#--------------------------------- Definición de Variables Globales --------------------------------
conn = psycopg2.connect(database='silabos',user='ucuenca',password='ucuenca2017', host='172.17.0.2')
cur = conn.cursor()
#id_asignatura1 = str(sys.argv[1])
#id_asignatura2 = str(sys.argv[2])
id_asignatura1 = "123"
id_asignatura2 = "124"

capitulos_asignatura1 = {}
capitulos_asignatura2 = {}

#------------------------------------- Definición de Funciones -------------------------------------
def nombre(id_asignatura):
    cur.execute("SELECT DISTINCT nombre_asignatura FROM silabo WHERE id_silabo='"+id_asignatura+"'")
    rows = cur.fetchall()
    desc = rows[0][0]
    return desc

def descripcion(id_asignatura):
    desc = ""
    cur.execute("SELECT DISTINCT descripcion_silabo FROM silabo WHERE id_silabo='"+id_asignatura+"'")
    rows = cur.fetchall()
    desc = rows[0][0]
    return desc

def capitulos(id_asignatura):
    capitulos = {}
    cur.execute("SELECT DISTINCT capitulos FROM contenido WHERE id_silabo='"+id_asignatura+"'")
    for row in cur:
        capitulos[row[0]] = []
    return capitulos

def subcapitulos(id_asignatura, capitulo):
    subcapitulos = []
    cur.execute("SELECT DISTINCT subcapitulos FROM contenido WHERE id_silabo='"+id_asignatura+"' and capitulos='"+capitulo+"'")
    for row in cur:
        subcapitulos.append(row[0])
    return subcapitulos

def preprocesamiento(texto):
    texto_normalize = normalization(texto)
    texto_tokenize = tweet_tokenization(texto_normalize)
    texto_stopping = stopping(texto_tokenize)
    texto_stemming = snowball_stemming(texto_stopping)
    return texto_stemming

def calculo_similitud_capitulos(asignatura1, asignatura2):
    similitud_capitulos = {}
    porcentaje_similitud = 0
    longitud = len(asignatura1)
    for cap_asignatura1 in asignatura1:
        for cap_asignatura2 in asignatura2:
            pro_asignatura1 = preprocesamiento(cap_asignatura1)
            pro_asignatura2 = preprocesamiento(cap_asignatura2)
            similitud = dices_similarity(pro_asignatura1, pro_asignatura2)
            if cap_asignatura1 in similitud_capitulos:
                temp = similitud_capitulos[cap_asignatura1][0]
                if similitud >= temp:
                     similitud_capitulos[cap_asignatura1] = [similitud, cap_asignatura2]
            else:
                similitud_capitulos[cap_asignatura1] = [similitud, cap_asignatura2]
        porcentaje_similitud += similitud_capitulos[cap_asignatura1][0]
    return [porcentaje_similitud/longitud, similitud_capitulos]

def calculo_similitud_subcapitulos(asignatura1, asignatura2):
    similitud_subcapitulos = {}
    porcentaje_similitud = 0
    longitud = len(asignatura1)
    for subcap_asignatura1 in asignatura1:
        for subcap_asignatura2 in asignatura2:
            pro_asignatura1 = preprocesamiento(subcap_asignatura1)
            pro_asignatura2 = preprocesamiento(subcap_asignatura2)
            similitud = dices_similarity(pro_asignatura1, pro_asignatura2)
            if subcap_asignatura1 in similitud_subcapitulos:
                temp = similitud_subcapitulos[subcap_asignatura1]
                if similitud >= temp:
                     similitud_subcapitulos[subcap_asignatura1] = similitud
            else:
                similitud_subcapitulos[subcap_asignatura1] = similitud
        porcentaje_similitud += similitud_subcapitulos[subcap_asignatura1]
    return porcentaje_similitud/longitud

#------------------------------------ Extracción de los Textos ------------------------------------
nombre_asignatura1 = nombre(id_asignatura1)
nombre_asignatura2 = nombre(id_asignatura2)

descripcion_asignatura1 = descripcion(id_asignatura1)
descripcion_asignatura2 = descripcion(id_asignatura2)

capitulos_asignatura1 = capitulos(id_asignatura1)
capitulos_asignatura2 = capitulos(id_asignatura2)

#--------------------------------- Preprocesamiento de los Textos ---------------------------------
texto1_stemming = preprocesamiento(descripcion_asignatura1)
texto2_stemming = preprocesamiento(descripcion_asignatura2)

#---------------------------------- Ejecución de los Algoritmos -----------------------------------



print("\nLa descripción de la Asignatura '"+nombre_asignatura1+"' es: "+descripcion_asignatura1+"\n")
print("La descripción de la Asignatura '"+nombre_asignatura2+"' es: "+descripcion_asignatura2+"\n")
print("La similitud de las asignaturas se presenta a continuación:")

porcentaje_similitud_descripciones = dices_similarity(texto1_stemming, texto2_stemming)
print('El porcentaje similitud de las descripciones es: '+str(round(porcentaje_similitud_descripciones*100,2))+'%')

for key in capitulos_asignatura1:
    capitulos_asignatura1[key] = subcapitulos(id_asignatura1, key)
for key in capitulos_asignatura2:
    capitulos_asignatura2[key] = subcapitulos(id_asignatura2, key)

[porcentaje_similitud_capitulos, similitud_capitulos] = calculo_similitud_capitulos(capitulos_asignatura1.keys(), capitulos_asignatura2.keys())
print('El porcentaje similitud de los capítulos es: '+str(round(porcentaje_similitud_capitulos*100,2))+'%')

similitud = 0
contador = 0
for key in similitud_capitulos:
    if similitud_capitulos[key][0] > 0.0:
        similitud += calculo_similitud_subcapitulos(capitulos_asignatura1[key], capitulos_asignatura2[similitud_capitulos[key][1]])
        contador += 1
if contador > 0:
    porcentaje_similitud_subcapitulos = similitud/contador
else:
    porcentaje_similitud_subcapitulos = 0.0
print('El porcentaje similitud de los temas es: '+str(round(porcentaje_similitud_subcapitulos*100,2))+'%')

porcentaje_similitud_total = (porcentaje_similitud_descripciones)*float(1/5) + (porcentaje_similitud_capitulos + porcentaje_similitud_subcapitulos)*float(2/5)
print('El porcentaje similitud total de las asignaturas es: '+str(round(porcentaje_similitud_total*100,2))+'%\n')

def get_results():
	return (str(round(porcentaje_similitud_total*100,2))+'%\n')


