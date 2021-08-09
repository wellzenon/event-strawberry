from typing import Any
from django.forms import models
from strawberry.types import Info
from strawberry.permission import BasePermission
from . import models


class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        user = info.context.request.user
        print(source)
        if user.is_authenticated:
            return True

        return False


class IsOwner(BasePermission):
    message = "User is not owner"

    def has_permission(self, source: Any, info: Info, **kwargs) -> bool:
        user = info.context.request.user

        model_name = info.return_type._type_definition.name
        model = getattr(models, model_name)
        instance = model.objects.filter(pk=kwargs["id"]).first()
        owner = instance.owner if hasattr(instance, "owner") else instance.user

        if user.id == owner.id:
            return True

        return False
