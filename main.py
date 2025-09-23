from fastapi import FastAPI, Response, Form, status
from fastapi.params import Cookie
from fastapi.responses import RedirectResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated

app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get('/')
def root(username = Cookie(default=None)):
    if not username:
        return RedirectResponse("/login")
    else:
        return PlainTextResponse(username)

@app.get('/login')
def show_login_page():
    return FileResponse("public/login.html")

@app.post('/login')
def do_login(username: Annotated[str, Form()], password: Annotated[str, Form()], response:Response):
    response.set_cookie(key="username", value=username)
    #return RedirectResponse("/",  status_code=status.HTTP_302_FOUND)
    return {"message":"OK"}

@app.get('/register')
def show_register_page():
    return FileResponse("public/register.html")