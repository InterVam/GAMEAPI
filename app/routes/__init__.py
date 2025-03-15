# app/routes/__init__.py

"""
API route definitions for the Game Management API.
"""

from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router
from app.routes.player import router as player_router

# This allows importing all routers from app.routes directly
__all__ = ["auth_router", "admin_router", "player_router"]