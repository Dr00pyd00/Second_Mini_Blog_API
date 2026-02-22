from fastapi import FastAPI

from app.models.users import User
from app.models.posts import Post

from app.routers.users import router as users_router


app = FastAPI()


#==== ROUTERS ======================#
app.include_router(users_router)

@app.get("/")
def test():
    return {"message":"Hello World!"}


