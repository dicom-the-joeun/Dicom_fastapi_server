import logging
from app.models.db_model import User
from app.util.token_gen import create_refresh_token

class UserService:
    @staticmethod
    def create_user(data, db):
        new_user = User(
            ID=data['ID'], 
            PASSWORD=data['PASSWORD'],
            REFRESHTOKEN = create_refresh_token(data['PASSWORD'])
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
    def exisiting_user(ID, db):
        '''
            @params : `ID:str`
        '''
        return db.query(User).filter(User.ID == ID).first()
    

    @staticmethod
    def update_refreshtoken(ID, token, db):
        db.query(User).filter(User.ID == ID).update({'REFRESHTOKEN': token})
        db.commit()
        return 

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