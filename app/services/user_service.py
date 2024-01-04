import logging
from app.models.db_model import User
from app.util.token_gen import create_refresh_token

class UserService:
    @staticmethod
    def exisiting_user(ID, db):
        '''
            @params : `ID:str`
        '''
        return db.query(User).filter(User.ID == ID).first()
    
    @staticmethod
    def update_password(ID, password, new_password, db):
        user = db.query(User).filter(User.ID == ID).first()

        if user:
            if user.PASSWORD == password:
                user.PASSWORD = new_password
                db.commit()
                return True
            else:
                return False
        else:
            return False