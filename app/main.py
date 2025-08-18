# Importaciones
#  Nos permite interactuar con el interprete y con el SO, para leer rutas, carpetas, etc.
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from services.documents_utils import cargar_documento
from routes.users import users_bp
from routes.documents import documents_bp

# Creamos la instancia del servicio
server = Flask(__name__)

# Usamos Blueprint para llamar a las rutas
server.register_blueprint(users_bp)
server.register_blueprint(documents_bp)

# Para recargar automáticamente el servicio si se cambia código
if __name__ == '__main__':
    cargar_documento()
    server.run(debug=True)