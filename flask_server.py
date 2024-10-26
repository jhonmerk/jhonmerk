from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Verifica que 'index.html' está en la carpeta 'templates'

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    return f"Datos recibidos: {username}, Contraseña: {password}"

if __name__ == '__main__':
    app.run(port=5001)  # Habilita el modo de depuración
