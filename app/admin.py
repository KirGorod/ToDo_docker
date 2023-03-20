import os
from app import models
from typing import Optional
from dotenv import load_dotenv

from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

load_dotenv()


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        # Validate username/password credentials
        if username != 'admin' and password != os.getenv('ADMIN_PASSWORD'):
            return False
        # And update session
        request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(
                request.url_for("admin:login"),
                status_code=302
            )

        # Check the token in depth


class ItemAdmin(ModelView, model=models.Item):
    column_list = [models.Item.id, models.Item.title, models.Item.description]
