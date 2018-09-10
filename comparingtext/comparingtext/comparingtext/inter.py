
import json
from flask import jsonify
from comparingtext.comparingtext.full_similarity_detected import get_results, get_data_test
#from comparingtext.comparingtext.calculo_similitud_asignatura import get_value


def get_direct_results():
    return jsonify({'similarity': "No hay resultado, bloqueado el código en get_direct_results() en inter.py"})
    #return jsonify({'similarity': get_value()})


def get_test(jsondata):
    return jsonify({'key': 'similarity', 'value': get_data_test(get_title(jsondata, 0), get_title(jsondata, 1), get_description(jsondata, 0), get_description(jsondata, 1), get_chapters(jsondata, 0), get_chapters(jsondata, 1))})

def get_full_similarity(jsondata):
  
  

    titleA = get_title(jsondata, 0) 
    descriptionA = get_description(jsondata, 0)
    chaptersA = get_chapters(jsondata, 0)    

    titleB = get_title(jsondata, 1)
    descriptionB = get_description(jsondata, 1)
    
    return jsonify({'full similarity': get_results(), 'chapters': str(chaptersA), 'test': jsondata[0]['contenido'][0]['title']})

#recuperando capitulos como lista
def get_chapters(jsondata, silabo_id):
    chapters = []  
    for chapter in jsondata[silabo_id]['contenido']:
        #chapters.append(str(chapter['title']))
        chapters.append(chapter) 
    return chapters

#recuperando titulo del silabo
def get_title(jsondata, silabo_id):
    title = str(jsondata[silabo_id]['title'])
    return title 

#recuperando descripcion del titulo
def get_description(jsondata, silabo_id):
    description = str(jsondata[silabo_id]['description'])
    return description
