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
allegroHOST = "http://172.17.0.5"
allegroPORT = "10035"
allegroREPOSITORY = "silabosUC-v2"

#parametros de consulta de similitud al servicio
url = 'http://172.17.0.4:5000/ucuenca/syllabus/similarity/service/fulldetected'

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
               + "         {{ "
               #+ "             { "
               +"                  ?s <http://purl.org/vocab/aiiso/schema#description> ?description . "
               +"    		   ?s <http://purl.org/vocab/aiiso/schema#name> ?title . "
             


               #+ "                  FILTER regex (?title, 'REDES DE COMPUTADORES', 'i') "
               #+ "                   filter (?s = <http://ies.linkeddata.ec/silabo/105>).  "           
               #+ "               } UNION {"
               #+ "                  ?s a <http://ies.linkeddata.ec/vocabulary/Silabo> ."
               #+ "                  ?s <http://purl.org/vocab/aiiso/schema#description> ?description ."
               #+ "                  ?s <http://ies.linkeddata.ec/vocabulary#abarca> ?subject ."
               #+ "  		    ?subject a <http://purl.org/vocab/aiiso/schema#Subject> ."
               #+ "    		    ?subject <http://ies.linkeddata.ec/vocabulary#name> ?title ."
               #+ "                   filter (?s = <http://ies.linkeddata.ec/silabo/102>) .  "          
               #+ " } "
               
               + "          }} order by ?s offset {0} limit {1}")
  
def get_chapters_query():
    return str("PREFIX ies: <http://ies.linkeddata.ec/syllabusOntology/vocabulary#> "
		+ "PREFIX aiiso: <http://purl.org/vocab/aiiso/schema#> "
                +"	SELECT DISTINCT ?chapter ?chapter_name "
               	+ "       WHERE  {{ "
                + "                 {0} ies:has_academic_content ?academic_content ."
                + "                 ?academic_content ies:has_chapter ?chapter ."
                + "                 ?chapter  aiiso:name ?chapter_name .      "      
                + "          }} ")

def get_subchapters_query():  
    return str(" PREFIX ies: <http://ies.linkeddata.ec/syllabusOntology/vocabulary#> "
		+ " PREFIX aiiso: <http://purl.org/vocab/aiiso/schema#> "
                + " SELECT DISTINCT ?subchapter_name"
                + "         {{ "
                + "                 {0} ies:has_subchapter ?subchapters." 
                + "                 ?subchapters aiiso:name ?subchapter_name "             
                + "        }} ")

def get_objectives_query():
    return str(" PREFIX ies: <http://ies.linkeddata.ec/syllabusOntology/vocabulary#> "
	       	+ "	PREFIX aiiso: <http://purl.org/vocab/aiiso/schema#> "
		+ "     SELECT DISTINCT ?objective_name "
              	+ "		WHERE  {{ "
                + " 	        {0} ies:has_objective ?objective ."
                + " 	        ?objective  ies:has_item ?objective_item. "
                + "             ?objective_item aiiso:name ?objective_name .     "
                + " }} ")

def get_count_syllabus():
    return str(" SELECT DISTINCT  (count(distinct ?s) as ?total)"
                + " { " 
                + "               ?s a <http://purl.org/vocab/aiiso/schema#KnowledgeGrouping> "
                + "  } ")


def get_content(idsilabo, silaboData, conn):
    
    contenido = {}
    contenido['id'] = idsilabo
    contenido['title'] = silaboData[1]
    if not silaboData[2] == '" "@es':
        contenido['description'] = silaboData[2]
    #print eachA[0] #URI silabo
    query_get_chapter =  str(get_chapters_query()).format(silaboData[0])    
    chapter_result = executeSparql(query_get_chapter, conn)#capitulos recuperados por cada silabo
    idChapter = 1
    Chapters = []
    if (len(chapter_result['values']) > 0):
        #return {'content': 'null'}
        for eachchapter in chapter_result['values']:
            chapter={}
            chapter['id'] = idChapter
            chapter['title'] = eachchapter[1] 
        
            #print eachchapter[0]#URI capitulo
            query_get_subchapter = str(get_subchapters_query()).format(eachchapter[0])
            subchapter_result = executeSparql(query_get_subchapter, conn)#subcapitulos recuperados por cada capitulo
       	    if (len(subchapter_result['values']) > 0):
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

        contenido['content']= Chapters


    query_get_objectives = str(get_objectives_query()).format(silaboData[0])
    objectives_result = executeSparql(query_get_objectives, conn)#objetivos recuperados
    objectives = [] 
    idobjective = 1
    if (len(objectives_result['values']) > 0):
        for eachobjective in objectives_result['values']:
            if not eachobjective[0] == '" "@es':
                objective={}
                objective['id'] = idobjective
                objective['desc'] = eachobjective[0]
                objectives.append(objective) 
                idobjective = idobjective + 1
        if len(objectives)>0:
            contenido['objectives']= objectives
    
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


def save_similarity(offset, limit, silaboA, silaboB, similitud):
   

    idA = silaboA.split('/')[5] #obtengo el id del silabo A, a partir de la URI del recurso
    idB = silaboB.split('/')[5] #obtengo el id del silabo B, a partir de la URI del recurso
    
    hasSimilarityURI = URIRef("http://ies.linkeddata.ec/syllabusOntology/vocabulary#has_similarity")
    isSimilarityOfURI = URIRef("http://ies.linkeddata.ec/syllabusOntology/vocabulary#is_similarity_of")
    hasSimilarityResourceURI = URIRef("http://ies.linkeddata.ec/syllabusOntology/vocabulary#has_similarity_resource")
    isSimilarityResourceOfURI = URIRef("http://ies.linkeddata.ec/syllabusOntology/vocabulary#is_similarity_resource_of")
    silaboAURI=URIRef(silaboA)
    silaboBURI=URIRef(silaboB)
    similarityClassAURI = URIRef("http://ies.linkeddata.ec/ucuenca/similarity/" +idA)
    similarityClassBURI = URIRef("http://ies.linkeddata.ec/ucuenca/similarity/" +idB)
    similarityResourceURI = URIRef("http://ies.linkeddata.ec/ucuenca/similarity/resource/"+idA+"-"+idB)
    similarityTypeURI = URIRef("http://ies.linkeddata.ec/syllabusOntology/vocabulary#Similarity")
    rdfsTypeURI = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
    
   
    g = Graph()
    g.add( (similarityClassAURI, rdfsTypeURI, similarityTypeURI) )
    g.add( (similarityClassBURI, rdfsTypeURI, similarityTypeURI) )
    
    g.add( (silaboAURI, hasSimilarityURI, similarityClassAURI) )
    g.add( (silaboBURI, hasSimilarityURI, similarityClassBURI) )
    g.add( (similarityClassAURI, isSimilarityOfURI, silaboAURI) )
    g.add( (similarityClassBURI, isSimilarityOfURI, silaboBURI) )

    
    g.add( (similarityClassAURI, hasSimilarityResourceURI, similarityResourceURI) )
    g.add( (similarityClassBURI, hasSimilarityResourceURI, similarityResourceURI) )
    g.add( (similarityResourceURI, isSimilarityResourceOfURI, similarityClassAURI) )
    g.add( (similarityResourceURI, isSimilarityResourceOfURI, similarityClassBURI) )

    for tag in similitud:
        similarityValueURI = URIRef("http://ies.linkeddata.ec/syllabusOntology/vocabulary#" + tag + "_value")
        similarityValue = Literal(str(similitud[tag])) #valor de similitud de cada propiedad
        g.add( (similarityResourceURI, similarityValueURI, similarityValue) )
      

   #print g.serialize(format='nt')
   #g.serialize(destination='similarities.txt', format='nt'))

    f=open("similarRDF-"+str(offset)+"-"+str(limit)+".ttl","a")
    f.write(str(g.serialize(format='nt')) + "\n") 
    f.close()


def save_error(msg):

    hora= time.strftime("%H:%M:%S") 
    fecha = time.strftime("%d/%m/%y")
    fecha= fecha.replace("/", "-")
    f=open("error_"+fecha+".logs","a")
    f.write(str(fecha+"-"+hora+"-"+msg) + "\n") 
    f.close()


def get_data():


    offset = 1586
    limit = 1000
    numero_total_de_silabos = 0
    silabos_procesados = 1586
    with ag_connect(allegroREPOSITORY, host=allegroHOST, create=False, clear=False, port=allegroPORT, user=allegroUSER, password=allegroPASSWORD) as conn:
        get_numero_de_silabos_query = str(get_count_syllabus())
        result_num_syllabus = executeSparql(get_numero_de_silabos_query, conn)
        numero_total_de_silabos = int(result_num_syllabus['values'][0][0].split('"')[1])
        conn.close()
    
    while (limit):
    
        with ag_connect(allegroREPOSITORY, host=allegroHOST, create=False, clear=False, port=allegroPORT, user=allegroUSER, password=allegroPASSWORD) as conn:
            get_syllabus_query = str(get_title_query()).format(offset, limit)
            result = executeSparql(get_syllabus_query, conn)
            num_silabo_por_proceso = 0         
            for silabosA in result['values']:
                print "Silabo procesado: " + str(silabos_procesados)
                json_to_send = [] 
                jsonsilaboA = get_content("0", silabosA, conn)
                json_to_send.append(jsonsilaboA)  
                
                for silabosB in result['values'][num_silabo_por_proceso: len(result['values'])]:
                    if (silabosA[0] != silabosB[0]):#que el silabo (URI) B no sea el mismo que el silabo (URI) A
                        jsonsilaboB = get_content("1", silabosB, conn)
                        json_to_send.append(jsonsilaboB)       #Aqui ya se tiene los dos silabos en JSON
                        #print str(silabosA[1].encode('utf-8').strip() + " -- vs -- " + silabosB[1].encode('utf-8').strip())
                        #print json_to_send
         		try:
                            similarity = json.loads(get_similarity(json_to_send))['value']
                            save_similarity(offset, limit, silabosA[0][1: -1].encode('utf-8').strip(), silabosB[0][1: -1].encode('utf-8').strip(), similarity)  
                        except ValueError:
                            save_error("Error  en consulta de similitud o construccion del JSON. Silabos que se estaban analizando:" + silabosA[0][1: -1].encode('utf-8').strip() + " vs " + silabosB[0][1: -1].encode('utf-8').strip() + " - Silabo procesado: "+ str(silabos_procesados))
                            print "Error  en consulta de similitud o construccion del JSON. Silabos que se estaban analizando:" + silabosA[0][1: -1].encode('utf-8').strip() + " vs " + silabosB[0][1: -1].encode('utf-8').strip() + " - Silabo procesado: "+ str(silabos_procesados)
                                #detectado error cuando un capitulo no tiene subchapters. Se debe controlar eso, detectando la similitud con los titulos de los capitulos.            
 	                json_to_send = [] 
                        json_to_send.append(jsonsilaboA)
                    
                num_silabo_por_proceso = num_silabo_por_proceso + 1 
                silabos_procesados = silabos_procesados + 1
        #print json_to_send 
        conn.close()
        if (offset > numero_total_de_silabos ):
            break
        offset = offset + 1000
        limit = limit + 1000
      
get_data()
#consumeGETRequestSync()
