#!flask/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)




#from Docker: In docker file copy this file, build, run and call sw : http://127.17.0.2:5000

