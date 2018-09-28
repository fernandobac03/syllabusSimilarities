#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

#-------------------------------------- Importa las librerías --------------------------------------
import sys
import json
import comparingtext.comparingtext.nltk_similarity
from comparingtext.comparingtext.nltk_similarity import *


#------------------------------------- Definición de Funciones -------------------------------------

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


#---------------------------------- Ejecución de los Algoritmos -----------------------------------


def text_similarity(textoA, textoB):
    texto1_stemming = preprocesamiento(textoA)
    texto2_stemming = preprocesamiento(textoB)
    porcentaje_similitud_de_textos = dices_similarity(texto1_stemming, texto2_stemming)
    return round(porcentaje_similitud_de_textos*100,2)


def title_similarity(titleA, titleB):

    return text_similarity(titleA, titleB)


def description_similarity(descA, descB):

    return text_similarity(descA, descB)


def objectives_similarity(objA, objB):

    return text_similarity(objA, objB)


def results_similarity(resultA, resultB):

    return text_similarity(resultA, resultB)


def academic_unit_similarity(unitA, unitB):

    return text_similarity(unitA, unitB)



def chapters_similarity(chaptersA, chaptersB):

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
    porcentaje_similitud_total = description_similarity(descA, descB)*float(1/3) + ((chapters_similarity(chaptersA, chaptersB) + subchapters_similarity(chaptersA, chaptersB))/2)*float(2/3)
    return round(porcentaje_similitud_total,2)


def get_similarity_from_list(listaA, listaB): #para comparar objectives, results y otros que contengan items, exepto capitulo. 
    # se compara todos los items de A vs todos de B (un silabo puede tener 2 objetivos, mientras que el otro puede tener muchos mas.) y se promedia
    suma_similitud = 0;
    similitud_total = 0;
    comparaciones=0;
    for itemA in listaA:
        for itemB in listaB:
            for tag in itemA:
                if tag in itemB:
                    if (not tag=="id") and type(itemA[tag]).__name__ =="str" and type(itemB[tag]).__name__ =="str": #si los dos son strings
                        comparaciones = comparaciones + 1
                        suma_similitud = suma_similitud + text_similarity(itemA[tag], itemB[tag])
                    elif type(itemA[tag]).__name__ =="list" and type(itemB[tag]).__name__ =="list":
                        suma_similitud = suma_similitud + get_similarity_from_list(itemA[tag], itemB[tag]) #recursivo, en caso de contenido es una lista, que contiene capitulos, capitulos contiene otra lista , subcapitulos, entonces se debe entrar a analizar subcapitulos.
    return (suma_similitud/comparaciones) 
    

def get_global_similarity(silaboA, silaboB, pesos):
    similarity_value = 0
    similarities_result = '{'
    similarities_result_JSON = {}
    for tag in silaboA:##obtengo los nombres de los campos del json, ejemplo: title, description, objectives, etc.
        if tag in silaboB:#
            similitud_de_este_tag = 0
            if (not tag=="id") and (type(silaboA[tag]).__name__ =="str") and (type(silaboB[tag]).__name__ =="str"): #si tag no tine items (content, objectives, etc tienen items)
                if pesos[tag]: #existe valor de peso para ese tag, se suma la similitud
                    similitud_de_este_tag = text_similarity(silaboA[tag], silaboB[tag])
                    similarity_value = similarity_value + (similitud_de_este_tag*(int(pesos[tag])/100))
                    similarities_result = similarities_result + '"'+tag+'"' + ':' + str(similitud_de_este_tag) + ','
                    similarities_result_JSON[tag] = str(similitud_de_este_tag)
            elif type(silaboA[tag]).__name__ =="list" and type(silaboB[tag]).__name__ =="list":
                similitud_de_este_tag = get_similarity_from_list(silaboA[tag], silaboB[tag]) 
                similarity_value = similarity_value + (similitud_de_este_tag*(int(pesos[tag])/100))
                similarities_result = similarities_result + '"'+tag+'"' + ':' + str(similitud_de_este_tag) + ','
                similarities_result_JSON[tag] = str(similitud_de_este_tag)

    similarities_result = similarities_result + '"total":'+str(similarity_value)+'}'
    similarities_result_JSON["total"] = str(similarity_value)
    return similarities_result_JSON # return a JSON with similarities by tag
    #return silaboA    


def detecting_similarity(silaboA, silaboB, pesos):
    #return full_similarity(titleA, titleB, descA, descB, capitulos_from_json(chaptersA), capitulos_from_json(chaptersB))
    return get_global_similarity(silaboA, silaboB, pesos)

#def detecting_similarity(titleA, titleB, descA, descB, chaptersA, chaptersB):
#    return full_similarity(titleA, titleB, descA, descB, capitulos_from_json(chaptersA), capitulos_from_json(chaptersB))
 
