from fastapi import FastAPI, Depends, Response, Request, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from user_service import UserService, User
from session_layer import validate_session, create_session

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
async def change_weather(request: Request, weather: Annotated[str, Form()]):
    username = request.session.get("username")
    user = us.find_user_by_username(username)
    if weather:
        us.update_user_weather(user.usr_id, weather)
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    return RedirectResponse("/logout", status_code=status.HTTP_303_SEE_OTHER)

@app.get('/login')
async def show_login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@app.post('/login', response_class=RedirectResponse)
async def do_login(username: Annotated[str, Form()], password: Annotated[str, Form()],
                   request: Request):
    found_user = us.find_user_by_username(username)
    if not found_user:
        return templates.TemplateResponse(request=request, name="login.html", context={"username_error": "yes"})
    elif found_user.password != password:
        return templates.TemplateResponse(request=request, name="login.html", context={"password_error": "yes"})

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    create_session((request, response))
    request.session["username"] = username
    print(f"Response headers: {response.raw_headers}")
    return response

@app.get('/register')
async def show_register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html")

@app.post('/register')
async def do_register(username: Annotated[str, Form()], password: Annotated[str, Form()],
                      password2: Annotated[str, Form()], request: Request):
    found_user = us.find_user_by_username(username)
    if found_user:
        return templates.TemplateResponse(request=request, name="register.html", context={"username_error":"yes"})
    if password != password2:
        return templates.TemplateResponse(request=request, name="register.html", context={"password_error":"yes"})

    new_user = User(username=username, password=password, weather="sunny")
    new_user.usr_id = us.add_new_user(new_user)

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    create_session((request, response))
    request.session["username"] = username
    print(f"Response headers: {response.raw_headers}")
    return response


@app.get("/logout")
async def logout(request: Request, response: RedirectResponse):
    request.session.clear()
    response.delete_cookie(key="Authorization")
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)