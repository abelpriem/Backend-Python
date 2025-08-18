import os
import jwt
from flask import Blueprint, request, jsonify
from db.models.documents import Documents
from services.documents_utils import documents
from routes.users import users

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/document', methods=['POST'])
def createDocument():
    try:
        body = request.get_json()
        auth_header = request.headers.get("Authorization")
        
        if not body or not auth_header.startswith("Bearer "):
            return jsonify({"TokenError": "No se ha enviado un token válido"}), 401
        
        token = auth_header[7:]
        payload = jwt.decode(token, "iberavalejemplo671", algorithms=['HS256'])
        
        email = payload.get("email")
        
        # Usuario autenticado
        user_auth = next((user for user in users if user.email == email), None)
        
        if not user_auth:
            return jsonify({"AuthorizationError": "Usuario no autorizado"})
        
        if not body:
            return jsonify({"ContentError": "Datos inválidos"})
    
        file_path = f"files/{body['title']}.pdf"
            
        if os.path.exists(file_path):
            return jsonify({"DuplicityError": "Ya existe ese archivo"}), 409
            
        document = Documents(id= body['id'], user_id= user_auth.id, title= body['title'], body= body['body'])
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(body['body'])
                
        documents.append(document)
 
        return jsonify({
            "status": f"Archivo {body['title']}.pdf creado con éxito",
            "documento": document.info()}), 201
    except jwt.InvalidTokenError:
        return jsonify({"TokenError": "Token inválido"}), 401
    except:
        return jsonify({"SystemError": "Error de sistema en creación de documentos"}), 500
    
@documents_bp.route("/document", methods=['GET'])
def getAllDocuments():
    try:
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"TokenError": "No se ha enviado el token en la petición"}), 400
        
        token = auth_header[7:]
        payload = jwt.decode(token, "iberavalejemplo671", algorithms=['HS256'])
        
        email = payload.get('email')
        
        if not documents:         
            return jsonify({"NotFoundError": "Aún no hay documentos creados..."}), 404    
        
        user_auth = next((user for user in users if user.email == email), None)
            
        if not user_auth:
            return jsonify({"AuthorizationError": "Usuario no autorizado"})
        
        if user_auth.role == "admin":
            list_docs = [doc.info() for doc in documents]
        else:
            list_docs = [doc.info() for doc in documents if doc.user_id == user_auth.id]
        
        return jsonify({
            "total": len(list_docs),
            "documentos": list_docs}), 200
    except jwt.InvalidTokenError:
        return jsonify({"TokenError": "Token inválido"}), 401
    except:
        return jsonify({"SystemError": "Error de sistema en listado de documentos"}), 500
    
@documents_bp.route("/document/<document_id>", methods=['DELETE'])
def deleteDocument(document_id):
    try:
        auth_header = request.headers.get("Authorization")
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"TokenError": "No se ha enviado el token en la petición"}), 400
            
        token = auth_header[7:]
        payload = jwt.decode(token, "iberavalejemplo671", algorithms=["HS256"])
            
        email = payload.get("email")
            
        if not documents:
            return jsonify({"NotFoundError": "Aún no hay documentos registrados"}), 404
                
        user_auth = next((user for user in users if user.email == email), None)
            
        if not user_auth:
            return jsonify({"AuthorizationError": "Usuario no autorizado"})
                
        for document in documents:
            if str(document.id) == str(document_id):  # Asegura comparación correcta
                if document.user_id != user_auth.id and user_auth.role != "admin":
                    return jsonify({"AuthorizationError": "No tienes permiso para eliminar este archivo"}), 401
                
                documents.remove(document) # Lo eliminamos de la lista
                path_file = os.path.join("files", f"{document.title}.pdf")
                            
                if not os.path.exists(path_file):
                    return jsonify({"FileError": "No se ha encontrado la ruta del arcvivo"})
                    
                os.remove(path_file)
                return jsonify({"status": f"Archivo '{document.title}.pdf' eliminado correctamente"}), 200
    except jwt.InvalidTokenError:
            return jsonify({"TokenError": "Token inválido"}), 401
    except:
        return jsonify({"SystemError": "Error de sistema en eliminación de archivos"}), 500