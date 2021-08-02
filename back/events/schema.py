import typing
import strawberry
import strawberry_django
from typing import List
from strawberry.arguments import is_unset
from strawberry.types import Info
from strawberry_django import auth, auto, mutations
from strawberry_django.mutations.mutations import create

from django.contrib.auth import get_user_model
from . import models
from .permissions import IsAuthenticated

user_model = get_user_model()

@strawberry_django.type(user_model)
class User:
    id: auto
    first_name: auto
    last_name: auto
    email: auto
    username: auto
    birthday: auto
    bio: auto
    slug: str
    picture: auto
    is_staff: auto 
    is_producer: auto
    presences: List["Presence"]
    comments: List["Comment"]

def get_users() -> List[User]:
    return user_model.objects.all()

@strawberry_django.type(models.Event)
class Event:
    id: auto
    name: auto
    start: auto
    end: auto
    price: auto
    picture: auto
    description: auto
    created: auto
    slug: str
    owner: User
    user_presences: List["Presence"]
    user_comments: List["Comment"]

def get_events() -> List[Event]:
    return models.Event.objects.all()

@strawberry_django.input(models.Event)
class AddEventInput:
    name: auto
    start: auto
    end: auto
    price: auto
    picture: auto
    description: auto


@strawberry_django.type(models.Comment)
class Presence:
    user: User
    event: Event
    created: auto
    is_interested: bool
    is_confirmed: bool

@strawberry_django.type(models.Comment)
class Comment:
    user: User
    event: Event
    parent: "Comment"
    created: auto
    body: auto

@strawberry.type
class Query:
    me: User = auth.current_user()
    users: List[User] = strawberry.field(resolver=get_users, permission_classes=[IsAuthenticated])
    events: List[Event] = strawberry.field(resolver=get_events)

@strawberry.type
class Mutation:
    login: User = auth.login()
    logout = auth.logout()
    createEvent: Event = mutations.create(AddEventInput)
    @strawberry.field
    def add_event(self, info: Info, event: AddEventInput) -> Event:
        user = info.context.request.user
        
        if not user.is_authenticated:
            raise Exception("Must be logged in")

        items = event.__dict__.items()
        data = {k:v for (k,v) in items if not is_unset(v) }
        data["owner"] = user_model.objects.get(pk=user.id)
        new_event = models.Event(**data)
        new_event.save()
        
        return new_event

schema = strawberry.Schema(query=Query, mutation=Mutation)