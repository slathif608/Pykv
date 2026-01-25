from fastapi import Request
from security.errros import AuthError


class SessionManager:
    SESSION_KEY = "user"

    @staticmethod
    def login(request: Request, email: str, remember_me: bool = False):
        request.session[SessionManager.SESSION_KEY] = email

        if remember_me:
            request.session["remember"] = True
            request.session["max_age"] = 60 * 60 * 24 * 7  # 7 days
        else:
            request.session["remember"] = False

    @staticmethod
    def logout(request: Request):
        request.session.clear()

    @staticmethod
    def get_current_user(request: Request) -> str:
        user = request.session.get(SessionManager.SESSION_KEY)
        if not user:
            raise AuthError("Login required")
        return user

    @staticmethod
    def is_authenticated(request: Request) -> bool:
        return SessionManager.SESSION_KEY in request.session

    @staticmethod
    def is_remembered(request: Request) -> bool:
        return request.session.get("remember", False)