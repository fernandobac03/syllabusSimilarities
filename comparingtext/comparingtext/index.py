#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_cors import CORS
from comparingtext.comparingtext.inter import get_full_similarity, get_direct_results

app = Flask(__name__)
CORS(app)

@app.route('/ucuenca/syllabus/similarities/service/full', methods=['POST'])
def get_similarity():
    varjson = request.get_json(force=True)
    
    return get_full_similarity(varjson)




@app.route('/ucuenca/syllabus/full_similarity_detected/direct', methods=['GET'])
def get_data():
    
    #return get_direct_results()
    return jsonify({'test': 'ok'})

   
@app.route('/ucuenca/syllabus/similarities/service/jsonexample', methods=['GET'])
def get_example2():
    
    return jsonExample();


@app.route('/ucuenca/syllabus/full_similarity_detected/jsonexample', methods=['GET'])
def get_example():
    
    return jsonExample();


def jsonExample():
     return jsonify([
    {
        'id': 1,
        'title': 'INVESTIGACION 2',
        'description': 'La asignacion de Investigacion en la seccion de investigacion cualitativa y cuantitativa tiene como Proposito analizar los conceptos basicos sobre los procesos de investigacion cualitativa', 
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
        'title': 'BIOESTADISTICA II',
        'description': 'La Bioestadistica es la rama del metodo estadistico que se dedica a las aplicaciones en el area biologica y particularmente en las ciencias medicas. Es una disciplina en si, y su campo se encuentra en constante evolucion y desarrollo, que permite contestar preguntas claves de la investigacion en salud. ', 
        'contenido': [
{'id':1, 'title': 'Nivelacion, respecto a Bioestadistica I', 'subchapter':[
	{'id':1, 'title':'Analisis V. Cualitativas (Razon, proporcion, porcentajes y tasas)'}] }, 
{'id':2, 'title': 'Panorama General de los metodos de Investigacion utilizados en ciencias de la Salud y calculo muestral en c/u de ellos','subchapter':[
	{'id':1, 'title': 'Metodos descriptivos Metodos Analiticos Metodos experimentales Estudios clinicos controlados'}] }
	]
    }
])




if __name__ == '__main__':
    app.run()




#from Docker: In docker file copy this file, build, run and call sw : http://127.0.17.2:5000/ucuenca/syllabus/full_similarity_detected/service





