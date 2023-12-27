import logging
from app.models.db_model import User
from app.util.token_gen import create_refresh_token

class UserService:
    @staticmethod
    def create_user(data, db):
        new_user = User(
            ID=data['id'], 
            PASSWORD=data['password'],
            REFRESHTOKEN = create_refresh_token(data['password'])
        )
        db.add(new_user)
        try:
            db.commit()
            return new_user
        except Exception as e:
            logging.error(f"Failed to insert record: {e}")
            db.rollback()
            raise
    
    @staticmethod
    def exisiting_user(id, db):
        '''
            @params : `ID:str`
        '''
        return db.query(User).filter(User.ID == id).first()
    

    @staticmethod
    def update_refreshtoken(id, token, db):
        db.query(User).filter(User.ID == id).update({'REFRESHTOKEN': token})
        db.commit()
        return 

    @staticmethod
    def update_password(id, password, new_password, db):
        user = db.query(User).filter(User.ID == id).first()

        if user:
            if user.PASSWORD == password:
                user.PASSWORD = new_password
                db.commit()
                return True
            else:
                return False
        else:
            return False