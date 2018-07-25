#import pdb; pdb.set_trace()
import requests
import json
import rdflib
import time
from franz.openrdf.connect import ag_connect
from franz.openrdf.query.query import QueryLanguage
from rdflib import URIRef, BNode, Literal, Graph

#parametros de consulta al repositorio
allegroUSER = "test"
allegroPASSWORD = "xyzzy"
allegroHOST = "http://201.159.223.25"
allegroPORT = "8080"
allegroREPOSITORY = "silabosUC-v2"

#parametros de consulta de similitud al servicio
url = 'http://127.0.17.3:5000/ucuenca/syllabus/full_similarity_detected/service'

def jsonExample():
     return jsonify([
    {
        'id': 1,
        'title': u'INVESTIGACION 2',
        'description': u'La asignacion de Investigacion en la seccion de investigacion cualitativa y cuantitativa tiene como Proposito analizar los conceptos basicos sobre los procesos de investigacion cualitativa', 
        'contenido': [
{ 'id':1, 'title':'Generalidades de la investigacion en Enfermeria', 'subchapter':[
	{'id':1,'title':'Introduccion a la investigacion en enfermeria. Que es la enfermeria basada en evidencias'},

	{'id':2, 'title':'Adquisicion de conocimientos en enfermeria (tradiciones, autoridad, prestamos, ensayo error, experiencia personal, modelos de roles, intuicion, razonamiento)'}, 

	{'id':3,'title':'Por que la investigacion es importante para generar una practica enfermera basada en la evidencia'},

	{'id':4, 'title':'Utilidad del conocimiento: Descripcion, explicacion, prediccion o pronostico, control.'},

	{'id':5, 'title':'La participacion de las enfermeras en la investigacion del pasado al presente. Resena Historica'},

	{'id':6, 'title':'Adquisicion de conocimiento en enfermeria: tradiciones, autoridad, prestamos, ensayo-error, experiencia personal, modelos de roles, intuicion, razonamiento (induccion, deduccion)'} ]}, 

{'id':2, 'title':'Disenos cualitativos', 'subchapter': [{
	'id':1, 'title':'Los tipos de investigacion cualitativa: la investigacion etnografica y etnologica. investigacion participativa e Investigacion accion, la teoria fundamentada, fenomenologia'}] }, 

{'id':3, 'title':'Disenos cuantitativos', 'subchapter': [
	{'id':1 , 'title': 'La Investigacion cuantitativa. Tipos de disenos: casos clinicos, serie de casos, estudios transversales, estudios longitudinales casos y controles y cohortes, estudios experimentales, revisiones sistematicas y metaanalisis'}] }

	]
},  
   {
        'id': 2,
        'title': u'BIOESTADISTICA II',
        'description': u'La Bioestadistica es la rama del metodo estadistico que se dedica a las aplicaciones en el area biologica y particularmente en las ciencias medicas. Es una disciplina en si, y su campo se encuentra en constante evolucion y desarrollo, que permite contestar preguntas claves de la investigacion en salud. ', 
        'contenido': [
{'id':1, 'title': 'Nivelacion, respecto a Bioestadistica I', 'subchapter':[
	{'id':1, 'title':'Analisis V. Cualitativas (Razon, proporcion, porcentajes y tasas)'}] }, 
{'id':2, 'title': 'Panorama General de los metodos de Investigacion utilizados en ciencias de la Salud y calculo muestral en c/u de ellos','subchapter':[
	{'id':1, 'title': 'Metodos descriptivos Metodos Analiticos Metodos experimentales Estudios clinicos controlados'}] }
	]
    }
])

def get_full_query():
    return str("SELECT DISTINCT ?title ?description (group_concat(distinct ?chapter_name;separator=',') as ?chapterstext) (group_concat(distinct ?subchapter_name; separator = ',') as ?subchapterstext) "
               + "         { "
               + "                  ?s a <http://ies.linkeddata.ec/vocabulary/Silabo> ."
               + "                  ?s <http://purl.org/vocab/aiiso/schema#description> ?description ."

               + "                  ?s <http://ies.linkeddata.ec/vocabulary#abarca> ?subject ."
               + "  		    ?subject a <http://purl.org/vocab/aiiso/schema#Subject> ."
               + "    		    ?subject <http://ies.linkeddata.ec/vocabulary#name> ?title ."

                + "                 ?s <http://ies.linkeddata.ec/vocabulary#abarca> ?academic_content ."
                + " 	            ?academic_content a <http://ies.linkeddata.ec/vocabulary/ContenidoAcademico> ."
                + "                 ?academic_content <http://ies.linkeddata.ec/vocabulary#abarca> ?chapters ."
                + "                 ?chapters  <http://ies.linkeddata.ec/vocabulary#name> ?chapter_name .      "      
                 					
                + "                 ?chapters <http://ies.linkeddata.ec/vocabulary#has_subchapter> ?subchapters." 
                + "                 ?subchapters <http://ies.linkeddata.ec/vocabulary#name> ?subchapter_name     "             
                + "          }  group by ?title ?description limit 2 ")

def get_title_query():
    return str("SELECT DISTINCT ?s ?title ?description"
               + "         { "
               #+ "                  { "
               + "                  ?s a <http://ies.linkeddata.ec/vocabulary/Silabo> ."
               + "                  ?s <http://purl.org/vocab/aiiso/schema#description> ?description ."

               + "                  ?s <http://ies.linkeddata.ec/vocabulary#abarca> ?subject ."
               + "  		    ?subject a <http://purl.org/vocab/aiiso/schema#Subject> ."
               + "    		    ?subject <http://ies.linkeddata.ec/vocabulary#name> ?title ."
               ###+ "                  FILTER regex (?title, 'REDES de COMPUTADORES', 'i') "
               #+ "                   filter (?s = <http://ies.linkeddata.ec/silabo/105>).  "           
               #+ "               } UNION {"
               #+ "                  ?s a <http://ies.linkeddata.ec/vocabulary/Silabo> ."
               #+ "                  ?s <http://purl.org/vocab/aiiso/schema#description> ?description ."
               #+ "                  ?s <http://ies.linkeddata.ec/vocabulary#abarca> ?subject ."
               #+ "  		    ?subject a <http://purl.org/vocab/aiiso/schema#Subject> ."
               #+ "    		    ?subject <http://ies.linkeddata.ec/vocabulary#name> ?title ."
               #+ "                   filter (?s = <http://ies.linkeddata.ec/silabo/102>) .  "          
               #+ " } "
               
               + "          } order by ?s")
  
def get_chapters_query():
    return str("SELECT DISTINCT ?chapter ?chapter_name "
               + "       WHERE  {{ "
                + "                 {0} <http://ies.linkeddata.ec/vocabulary#abarca> ?academic_content ."
                + " 	            ?academic_content a <http://ies.linkeddata.ec/vocabulary/ContenidoAcademico> ."
                + "                 ?academic_content <http://ies.linkeddata.ec/vocabulary#abarca> ?chapter ."
                + "                 ?chapter  <http://ies.linkeddata.ec/vocabulary#name> ?chapter_name .      "      
                + "          }} ")

def get_subchapters_query():  
    return str("SELECT DISTINCT ?subchapter_name"
               + "         {{ "
                + "                 {0} <http://ies.linkeddata.ec/vocabulary#has_subchapter> ?subchapters." 
                + "                 ?subchapters <http://ies.linkeddata.ec/vocabulary#name> ?subchapter_name "             
                + "        }} ")

def get_content(idsilabo, silaboData, conn):
    
    contenido = {}
    contenido['id'] = idsilabo
    contenido['title'] = silaboData[1]
    contenido['description'] = silaboData[2]
    #print eachA[0] #URI silabo
    query_get_chapter =  str(get_chapters_query()).format(silaboData[0])    
    chapter_result = executeSparql(query_get_chapter, conn)#capitulos recuperados por cada silabo
    idChapter = 1
    Chapters = []

    for eachchapter in chapter_result['values']:
        chapter={}
        chapter['id'] = idChapter
        chapter['title'] = eachchapter[1] 
        
        #print eachchapter[0]#URI capitulo
        query_get_subchapter = str(get_subchapters_query()).format(eachchapter[0])
        subchapter_result = executeSparql(query_get_subchapter, conn)#subcapitulos recuperados por cada capitulo
	subChapters = [] 
        idsubChapter = 1 

        for eachsubchapter in subchapter_result['values']:
            subchapter={}
            subchapter['id'] = idsubChapter
            subchapter['title'] = eachsubchapter[0]
            subChapters.append(subchapter) 
            idsubChapter = idsubChapter + 1
        
        chapter['subchapter'] = subChapters
        Chapters.append(chapter)
        idChapter=idChapter+1

    contenido['contenido']= Chapters
    return contenido

def executeSparql(query, conn):
    
        tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query)
        return tuple_query.evaluate_generic_query(count=False, accept=None)
        



def get_similarity(silabosData):    
    jsondata = json.dumps(silabosData)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url,data = jsondata)
    #print "code:"+ str(response.status_code)
    #print "headers:"+ str(response.headers)
    #print "content:"+ str(response.text)
    response_similarity = ""
    if (response.status_code == 200):
        response_similarity =  str(response.text)
        response = ""
        #print response_similarity
    return response_similarity


def save_similarity(silaboA, silaboB, similitud):
   

    idA = silaboA.split('/')[4] #obtengo el id del silabo A, a partir de la URI del recurso
    idB = silaboB.split('/')[4] #obtengo el id del silabo B, a partir de la URI del recurso
    
    
    hassimilarityURI = URIRef("http://ies.linkeddata.ec/vocabulary#has_similarity")
    silaboAURI=URIRef(silaboA)
    silaboBURI=URIRef(silaboB)
    similarityResourceURI = URIRef("http://ies.linkeddata.ec/similarity/"+idA+"-"+idB)

    similarityValue = Literal(similitud) # passing a string
    similarityURI = URIRef("http://ies.linkeddata.ec/vocabulary#has_similar_resource")
    similarityValueURI = URIRef("http://ies.linkeddata.ec/vocabulary#value")
    
    g = Graph()
    g.add( (silaboAURI, hassimilarityURI, similarityResourceURI) )
    g.add( (similarityResourceURI, similarityURI, silaboBURI) )
    g.add( (similarityResourceURI, similarityValueURI, similarityValue) )
  

    #print g.serialize(format='nt')
#    g.serialize(destination='similarities.txt', format='nt'))

    f=open("similardd.txt","a")
    f.write(str(g.serialize(format='nt')) + "\n") 
    f.close()



def get_data():
    with ag_connect(allegroREPOSITORY, host=allegroHOST, create=False, clear=False, port=allegroPORT, user=allegroUSER, password=allegroPASSWORD) as conn:
        result = executeSparql(get_title_query(), conn)
   #     print result  
        for silabosA in result['values']:
            json_to_send = [] 
            json_to_send.append(get_content("0", silabosA, conn))       
            for silabosB in result['values']:
                if (silabosA[0] != silabosB[0]):#que el silabo (URI) B no sea el mismo que el silabo (URI) A
                    json_to_send.append(get_content("1", silabosB, conn))       #Aqui ya se tiene los dos silabos en JSON
                    print str(silabosA[1].encode('utf-8').strip() + " -- vs -- " + silabosB[1].encode('utf-8').strip())
                    try:
                        similarity = json.loads(get_similarity(json_to_send))['value']
                        save_similarity(silabosA[0][1: -1].encode('utf-8').strip(), silabosB[0][1: -1].encode('utf-8').strip(), similarity)  
                    except ValueError:
                        print "Error  en construccion del JSON"
                        #detectado error cuando un capitulo no tiene subchapters. Se debe controlar eso, detectando la similitud con los titulos de los capitulos.            
 	            json_to_send = [] 
                    json_to_send.append(get_content("0", silabosA, conn))
                    
               
        #print json_to_send 

get_data()
#consumeGETRequestSync()
