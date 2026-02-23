
from app.models.users import RoleEnum, User
from app.core.databse import LocalSession
from app.security.password_users import hash_user_pw
from app.models.posts import Post

def create_admin_user(name:str,password:str):

    db = LocalSession()
    try:
        hashed_pw = hash_user_pw(password) 
        admin_user = User(
            username=name,
            password=hashed_pw,
            role=RoleEnum.ADMIN,
        )
        db.add(admin_user)
        db.commit()
        print(f"Admin User <{name}> created!")
    except Exception as e:
        db.rollback()
        print(f"Error to admin_creation: {e}")
    finally:
        db.close()
    

if __name__=="__main__":
    create_admin_user("King", "password123")
