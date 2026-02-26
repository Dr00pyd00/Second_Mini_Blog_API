from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, MessageType

from app.models.users import User
from app.models.posts import Post

from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.posts import router as posts_router


app = FastAPI()


#==== ROUTERS ======================#
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(posts_router)

@app.get("/")
def test():
    return {"message":"Hello World!"}



# test send email:
from app.core.mails import mail_conf
from app.schemas.mails import EmailSchema

@app.post("/email_test")
async def simple_send(email: EmailSchema)->JSONResponse:
    
    message = MessageSchema(
        subject="fastapi mail module test",
        recipients=email.model_dump().get("email"),
        subtype=MessageType.html,
        body="""
<p>Thanks for using Fastapi-mail</p> 
"""
    )

    fm = FastMail(mail_conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message":"email sended!"})



