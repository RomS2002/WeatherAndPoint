from fastapi import FastAPI, Depends, Response, Request, Form, status
from fastapi.responses import RedirectResponse, FileResponse, PlainTextResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from user_service import UserService
from session_layer import validate_session, create_session

user = None

us = UserService()
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-very-secret-key")
app.mount("/public", StaticFiles(directory="public"), name="public")

templates = Jinja2Templates(directory="public/templates")

@app.get('/')
async def root(request: Request, is_valid_session = Depends(validate_session)):
    print(f"Request_headers: {request.headers}")
    if not is_valid_session:
        return RedirectResponse("/logout", status_code=status.HTTP_303_SEE_OTHER)

    username = request.session.get("username")
    user = us.find_user_by_username(username)
    weather = user.weather
    context = {"username":username, "body_class":weather}
    return templates.TemplateResponse(request=request, name="index.html", context=context)

@app.post('/')
async def changeWeather(weather: Annotated[str, Form()]):
    if weather:
        us.update_user_weather()
    return RedirectResponse("/logout", status_code=status.HTTP_303_SEE_OTHER)

@app.get('/login')
async def show_login_page():
    return FileResponse("public/login.html")

@app.post('/login', response_class=RedirectResponse)
async def do_login(username: Annotated[str, Form()], password: Annotated[str, Form()],
                   request: Request):
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    create_session((request, response))
    request.session["username"] = username
    print(f"Response headers: {response.raw_headers}")
    return response

@app.get('/register')
async def show_register_page():
    return FileResponse("public/register.html")

@app.get("/logout")
async def logout(request: Request, response: RedirectResponse):
    request.session.clear()
    response.delete_cookie(key="Authorization")
    global user
    user = None
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)