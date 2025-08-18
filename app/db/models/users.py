import bcrypt

# Clase - Usuarios
class Users():    
    def __init__(self, id, name, email, password, role, token):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.token = token
        
    @property
    def id(self):
       return self._id
   
    @id.setter
    def id(self, id):
       self._id = id
       
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
        
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        self._email = email
        
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self._password = hashed
        
    @property
    def role(self):
        return self._role
    
    @role.setter
    def role(self, role):
        self._role = role  
        
    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, token):
        self._token = token
        
    def info(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role" : self.role,
            "token": self.token
        }
   