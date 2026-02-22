from passlib.context import CryptContext

# the context
pw_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# hash pw for db
def hash_user_pw(plain_pw:str)->str:
    return pw_context.hash(plain_pw)

# verify plain pw to db pw
def verify_user_pw(plain_pw:str, db_pw:str)->bool:
    return pw_context.verify(secret=plain_pw, hash=db_pw)

