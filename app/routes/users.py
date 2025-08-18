import jwt
import datetime
import uuid
import bcrypt
from flask import Blueprint, jsonify, request
from db.models.users import Users

users_bp = Blueprint('users', __name__)

users = []
    
@users_bp.route('/login', methods=['POST'])
def login():
    try:
        body = request.get_json()
        
        if not body:
            return jsonify({"ContentError": "Datos inválidos"}), 406
        
        user_auth = next((user for user in users if user.email == body['email']), None)
        
        if not user_auth:
            return jsonify({"NotFoundError": "Usuario no encontrado"}), 404
  
        if not bcrypt.checkpw(body['password'].encode('utf-8'), user_auth.password):
            return jsonify({"CredentialsError": "Credenciales incorrectas"}), 406
        
        return jsonify({"status": f"Logeado correctamente | Bienvenido {user_auth.name} ({user_auth.role.upper()})",
                        "token": f"{user_auth.token}"}), 200
        
    except:
        return jsonify({"SystemError": "Error de sistema en login"}), 500

@users_bp.route('/users', methods=['POST'])
def create_user():
    try:
        body = request.get_json() # Con get_json() nos traemos el req.body() 
        
        if not body:
            return jsonify({"ContentError": "Datos inválidos"}), 406
        
        payload = {
            "user_id": body["id"],
            "email": body["email"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
            "iat": datetime.datetime.utcnow(),
            "jti": str(uuid.uuid4())
        }
            
        token = jwt.encode(payload, "iberavalejemplo671", algorithm = "HS256")
        user = Users(id= body["id"], name= body["name"], email= body["email"], password= body["password"], role= body["role"], token= token)
            
        for u in users:
            if u.email == user.email:
                return jsonify({"DuplicityError": "El usuario ya existe en la BD"}), 409
            
        users.append(user)
            
        return jsonify({
            "status": "Usuario creado correctamente!",
            "user": user.info()}), 201
    except:
        return jsonify({"SystemError": "Error de sistema en creación de usuarios"}), 500

@users_bp.route('/users', methods=['GET'])
def get_users():
    try:
        if not users:
            return jsonify({"NotFoundError": "No hay usuarios creados en la BD..."}), 404
        
        auth_header = request.headers.get("Authorization")
            
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"TokenError": "No se ha enviado el token en la petición"}), 400
        
        token = auth_header[7:] # Quita los primeros 7 caracteres: "Bearer "
        payload = jwt.decode(token, "iberavalejemplo671", algorithms=["HS256"])
                
        email = payload.get("email")
                
        user_autenticado = next((user for user in users if user.email == email and user.role == 'admin'), None)

        if user_autenticado:
            return jsonify([user.info() for user in users]), 200
        else:
            return jsonify({"AuthorizationError": "Acceso no autorizado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"TokenError": "Token inválido"}), 401
    except Exception as e:
        return jsonify({"SystemError": f"Error de sistema: {str(e)}"}), 500
    
@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    try:
        for user in users:
            if str(user['id']) == user_id:
                return jsonify({
                    "status": "Usuario encontrado correctamente!",
                    "user": user.info()}), 200
                
        return jsonify({"NotFoundError": "Usuario no encontrado"}), 404
    except:
        return jsonify({"SystemError": "Error de sistema"}), 500
    
@users_bp.route('/users/change-password', methods=['PATCH'])
def change_password():
    try:
        body = request.get_json()
        auth_header = request.headers.get("Authorization")
        
        if not body:
            return jsonify({"ContentError": "Datos inválidos"}), 406
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"TokenError": "No se ha enviado el token correctamente en la petición"}), 400
        
        token = auth_header[7:]
        payload = jwt.decode(token, "iberavalejemplo671", algorithms=['HS256'])
        
        email = payload.get("email")
        
        if not users:
            return jsonify({"NotFoundError": "No hay usuarios creados en la BD..."}), 404
        
        user_auth = next((user for user in users if user.email == email or user.role == "admin"), None)
        
        if not user_auth:
            return jsonify({"AuthorizationError": "Usuario no autorizado"}), 401
        
        if not bcrypt.checkpw(body['password'].encode('utf-8'), user_auth.password):
            return jsonify({"CredentialsError": "Credenciales incorrectas"}), 406
        
        user_auth.password = body['new_password']
        
        return jsonify({"status": "Contraseña modificada correctamente!"}), 200
    except jwt.InvalidTokenError:
        return jsonify({"TokenError": "Token inválido"}), 401
    except:
        return jsonify({"SystemError": "Error de sistema en modificación de contraseña"}), 500
    
users_bp.route('/users/<user_id>')
def detele_user(user_id):
    try:
        if not users:
            return jsonify({"NotFoundError": "No hay usuarios creados en la BD..."}), 404
    except:
        return jsonify({"SystemError": "Error de sistema en eliminación de usuarios"}), 500