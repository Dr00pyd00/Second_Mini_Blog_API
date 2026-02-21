from app.core.databse import LocalSession


# gen for depends database
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()