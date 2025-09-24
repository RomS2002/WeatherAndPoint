import secrets

from fastapi import Request, Response
from datetime import datetime, timedelta

def create_random_session_string():
    return secrets.token_urlsafe(32)

def validate_session(request: Request):
    session_auth = request.cookies.get("Authorization")
    session_id = request.session.get("session_id")
    session_access_token = request.session.get("access_token")
    token_exp = request.session.get("token_expiry")
    print(f"Session check: {session_auth}, {session_id}, {session_access_token}, {token_exp}")

    if not session_auth and not session_access_token:
        return False
    if session_auth != session_id:
        return False
    if is_token_expired(token_exp):
        return False
    return True

def is_token_expired(unix_timestamp: int) -> bool:
    if unix_timestamp:
        datetime_from_unix = datetime.fromtimestamp(unix_timestamp)
        current_datetime = datetime.now()
        diff_in_min = (datetime_from_unix - current_datetime).total_seconds() / 60
        return diff_in_min <= 0
    return True

def create_session(args: tuple):
    request, response = args
    session_id = request.session["session_id"] = create_random_session_string()
    request.session["token_expiry"] = (datetime.now() + timedelta(days=3)).timestamp()
    response.set_cookie(key="Authorization", value=session_id)
