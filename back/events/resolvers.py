from typing import List
from strawberry.types import Info
from strawberry.arguments import is_unset
from django.middleware.csrf import get_token
from django.contrib import auth

from . import models
from .utils import remove_unset
from .types import (
    User,
    UserInput,
    UpdateUserInput,
    Event,
    EventInput,
    UpdateEventInput,
    Presence,
    PresenceInput,
    UpdatePresenceInput,
    Comment,
    CommentInput,
    UpdateCommentInput,
)


# AUTH resolvers


def csrf(self, info: Info) -> str:
    request = info.context.request
    return get_token(request)


def login(self, info: Info, email_or_username: str, password: str) -> User:
    request = info.context.request

    if request.user.is_authenticated:
        auth.logout(request)

    user = auth.authenticate(request, email=email_or_username, password=password)

    if user is None:
        email = models.User.objects.filter(username=email_or_username).first().email
        user = auth.authenticate(request, email=email, password=password)

    if user.is_authenticated:
        auth.login(request, user)
        return user

    auth.logout(request)
    return user


def logout(self, info: Info) -> bool:
    request = info.context.request
    auth.logout(request)
    return True


# RETRIEVE resolvers


def me(self, info: Info) -> User:
    user = info.context.request.user
    return user


def user(self, info: Info, id: int) -> User:
    user = models.User.objects.filter(pk=id).first()
    return user


def users() -> List[User]:
    return models.User.objects.all()


def event(self, info: Info, id: int) -> Event:
    event = models.Event.objects.filter(pk=id).first()
    return event


def events() -> List[Event]:
    return models.Event.objects.all()


# CREATE resolvers


def create_user(self, info: Info, data: UserInput) -> User:
    user_data = remove_unset(data)
    user = models.User(**user_data)
    user.set_password(data.password)
    user.save()
    return user


def create_event(self, info: Info, data: EventInput) -> Event:
    event_data = remove_unset(data)
    event = models.Event(**event_data)
    event.owner = info.context.request.user
    event.save()
    return event


def create_presence(self, info: Info, event_id: int, data: PresenceInput) -> Presence:
    presence_data = remove_unset(data)
    user_id = info.context.request.user.id

    presence = models.Presence.objects.update_or_create(
        user_id=user_id, event_id=event_id, defaults=presence_data
    )[0]

    return presence


def create_comment(self, info: Info, event_id: int, data: CommentInput) -> Comment:
    comment_data = remove_unset(data)
    user_id = info.context.request.user.id

    comment = models.Comment.objects.update_or_create(
        user_id=user_id, event_id=event_id, defaults=comment_data
    )[0]

    return comment


# UPDATE resolvers


def update_me(self, info: Info, data: UpdateUserInput) -> User:
    user_data = remove_unset(data)
    user = info.context.request.user

    for key, value in user_data.items():
        setattr(user, key, value)

    if "password" in user_data:
        user.set_password(user_data["password"])

    user.save(update_fields=user_data.keys())

    return user


def update_event(self, info: Info, id: int, data: UpdateEventInput) -> Event:
    event_data = remove_unset(data)
    event = models.Event.objects.filter(pk=id).first()

    for key, value in event_data.items():
        setattr(event, key, value)

    event.save(update_fields=event_data.keys())

    return event


def update_presence(
    self, info: Info, event_id: int, data: UpdatePresenceInput
) -> Presence:
    presence_data = remove_unset(data)
    user_id = info.context.request.user.id
    presence = models.Presence.objects.filter(
        user_id=user_id, event_id=event_id
    ).first()

    for key, value in presence_data.items():
        setattr(presence, key, value)

    presence.save(update_fields=presence_data.keys())

    return presence


def update_comment(
    self, info: Info, event_id: int, data: UpdateCommentInput
) -> Comment:
    comment_data = remove_unset(data)
    user_id = info.context.request.user.id
    comment = models.Comment.objects.filter(user_id=user_id, event_id=event_id).first()

    for key, value in comment_data.items():
        setattr(comment, key, value)

    comment.save(update_fields=comment_data.keys())

    return comment
