import strawberry
from typing import Any
from strawberry.types import Info
from strawberry.permission import BasePermission

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        user = info.context.request.user
        
        if not user.is_authenticated:
            return False
        
        return True