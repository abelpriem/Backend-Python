
class Documents():
    def __init__(self, id, user_id, title, body):    
        self.id = id
        self.user_id = user_id
        self.title = title
        self.body = body
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id
        
    @property
    def user_id(self):
        return self._user_id
    
    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id
        
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        self._title = title
        
    @property
    def body(self):
        return self._body
        
    @body.setter
    def body(self, body):
        self._body = body
        
    def info(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "body": self.body
        }
        