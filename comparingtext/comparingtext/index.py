#!flask/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from comparingtext.comparingtext.inter import get_full_similarity, get_test, get_direct_results

app = Flask(__name__)


@app.route('/ucuenca/syllabus/full_similarity_detected/service', methods=['POST'])
def get_similarity():
    varjson = request.get_json(force=True)
    
    return get_test(varjson)
    #return get_full_similarity(varjson)



@app.route('/ucuenca/syllabus/full_similarity_detected/direct', methods=['GET'])
def get_data():
    
    return get_direct_results()
   



if __name__ == '__main__':
    app.run()




#from Docker: In docker file copy this file, build, run and call sw : http://127.0.17.2:5000/ucuenca/syllabus/full_similarity_detected/service





