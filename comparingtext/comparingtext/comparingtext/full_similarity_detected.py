#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

#-------------------------------------- Importa las librerías --------------------------------------
import psycopg2, sys
import comparingtext.comparingtext.nltk_similarity
from comparingtext.comparingtext.nltk_similarity import *

#--------------------------------- Definición de Variables Globales --------------------------------
#conn = psycopg2.connect(database='silabos',user='ucuenca',password='ucuenca2017', host='172.17.0.2')
#cur = conn.cursor()
#id_asignatura1 = str(sys.argv[1])
#id_asignatura2 = str(sys.argv[2])
#id_asignatura1 = "123"
#id_asignatura2 = "124"

nameA = ''
nameB = ''
descriptionA = ''
descriptionB = ''
capitulos_asignatura1 = {}
capitulos_asignatura2 = {}

#------------------------------------- Definición de Funciones -------------------------------------

def set_values(titleA, titleB, descA, descB, chaptersA, chaptersB):
    set_nameA(titleA)
    set_nameB(titleB)
    set_descriptionA(descA)
    set_descriptionB(descB)
    set_chaptersA(chaptersA)
    set_chaptersA(chaptersB)

def set_nameA(title):
    nameA = title

def set_nameB(title):
    nameB = title

def set_descriptionA(desc):
    descriptionA = desc

def set_descriptionB(desc):
    descriptionB = desc

def set_chaptersA(chapters):
    capitulos_asignatura1 = capitulos_from_json(chapters)

def set_chaptersB(chapters):
    capitulos_asignatura2 = capitulos_from_json(chapters)


def capitulos_from_json(chapters):
    capitulos = {}
    caps = chapters 
    for row in caps:
        subchapters = []
        for obj in row['subchapter']:
            subchapters.append(obj['title'])
        capitulos[row['title']] = subchapters
    return capitulos
    

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
#nombre_asignatura1 = nombre(id_asignatura1)
#nombre_asignatura2 = nombre(id_asignatura2)

nombre_asignatura1 = nameA
nombre_asignatura2 = nameB


#descripcion_asignatura1 = descriptionA
#descripcion_asignatura2 = descriptionB

#capitulos_asignatura1 = capitulos(id_asignatura1)
#capitulos_asignatura2 = capitulos(id_asignatura2)

#--------------------------------- Preprocesamiento de los Textos ---------------------------------
#texto1_stemming = preprocesamiento(descripcion_asignatura1)
#texto2_stemming = preprocesamiento(descripcion_asignatura2)

#---------------------------------- Ejecución de los Algoritmos -----------------------------------



#print("\nLa descripción de la Asignatura '"+nombre_asignatura1+"' es: "+descripcion_asignatura1+"\n")
#print("La descripción de la Asignatura '"+nombre_asignatura2+"' es: "+descripcion_asignatura2+"\n")
#print("La similitud de las asignaturas se presenta a continuación:")

def description_similarity(descA, descB):

    texto1_stemming = preprocesamiento(descA)
    texto2_stemming = preprocesamiento(descB)


    porcentaje_similitud_descripciones = dices_similarity(texto1_stemming, texto2_stemming)
    return round(porcentaje_similitud_descripciones*100,2)


def chapters_similarity(chaptersA, chaptersB):

    #for key in capitulos_asignatura1:
    #    capitulos_asignatura1[key] = subcapitulos(id_asignatura1, key)
    #for key in capitulos_asignatura2:
    #    capitulos_asignatura2[key] = subcapitulos(id_asignatura2, key)

    [porcentaje_similitud_capitulos, similitud_capitulos] = calculo_similitud_capitulos(chaptersA.keys(), chaptersB.keys())
    return round(porcentaje_similitud_capitulos*100,2)

def subchapters_similarity(chaptersA, chaptersB):
    [porcentaje_similitud_capitulos, similitud_capitulos] = calculo_similitud_capitulos(chaptersA.keys(), chaptersB.keys())
    similitud = 0
    contador = 0
    for key in similitud_capitulos:
        if similitud_capitulos[key][0] > 0.0:
            similitud += calculo_similitud_subcapitulos(chaptersA[key], chaptersB[similitud_capitulos[key][1]])
            contador += 1
    if contador > 0:
        porcentaje_similitud_subcapitulos = similitud/contador
    else:
        porcentaje_similitud_subcapitulos = 0.0
   
    return round(porcentaje_similitud_subcapitulos*100,2)
    

def full_similarity(descA, descB, chaptersA, chaptersB ):
    porcentaje_similitud_total = description_similarity(descA, descB)*float(1/3) + (chapters_similarity(chaptersA, chaptersB) + subchapters_similarity(chaptersA, chaptersB)/2)*float(2/3)
    return round(porcentaje_similitud_total,2)


def get_results():
    return ""
def get_data_test(titleA, titleB, descA, descB, chaptersA, chaptersB):
    return full_similarity(descA, descB, capitulos_from_json(chaptersA), capitulos_from_json(chaptersB))
    #return {'data': titleA + ' --- ' + titleB + '--- ' + id_asignatura1 + '---' , 'chapters':  capitulos_asignatura1 }

