import strawberry
from strawberry.arguments import UNSET
from typing import List, Optional
from datetime import datetime


@strawberry.type
class User:
    id: strawberry.ID
    first_name: str
    last_name: str
    email: str
    username: str
    birthday: datetime
    bio: str
    slug: str
    picture: str
    is_staff: bool
    is_producer: bool

    @strawberry.field
    def presences(self) -> Optional[List["Presence"]]:
        return self.presence_set.all()

    @strawberry.field
    def comments(self) -> Optional[List["Comment"]]:
        return self.comment_set.all()


@strawberry.type
class Event:
    id: strawberry.ID
    name: str
    start: datetime
    end: datetime
    price: str
    picture: str
    description: str
    created: datetime
    slug: str
    owner: Optional[User]

    @strawberry.field
    def presences(self) -> Optional[List["Presence"]]:
        return self.presence_set.all()

    @strawberry.field
    def comments(self) -> Optional[List["Comment"]]:
        return self.comment_set.all()


@strawberry.type
class Presence:
    id: strawberry.ID
    user: User
    event: Event
    created: datetime
    is_interested: bool
    is_confirmed: bool


@strawberry.type
class Comment:
    id: strawberry.ID
    user: User
    event: Event
    parent: "Comment"
    created: datetime
    body: str


# INPUT Types
@strawberry.input
class UserInput:
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    birthday: datetime
    bio: Optional[str] = UNSET
    picture: Optional[str] = UNSET


@strawberry.input
class EventInput:
    name: str
    description: str
    start: datetime
    end: Optional[datetime] = UNSET
    price: Optional[str] = UNSET
    picture: Optional[str] = UNSET


@strawberry.input
class PresenceInput:
    is_interested: Optional[bool] = False
    is_confirmed: Optional[bool] = False


@strawberry.input
class CommentInput:
    body: str


# UPDATE types


@strawberry.input
class UpdateUserInput:
    email: Optional[str] = UNSET
    username: Optional[str] = UNSET
    password: Optional[str] = UNSET
    first_name: Optional[str] = UNSET
    last_name: Optional[str] = UNSET
    birthday: Optional[datetime] = UNSET
    bio: Optional[str] = UNSET
    picture: Optional[str] = UNSET


@strawberry.input
class UpdateEventInput:
    name: Optional[str] = UNSET
    description: Optional[str] = UNSET
    start: Optional[datetime] = UNSET
    end: Optional[datetime] = UNSET
    price: Optional[str] = UNSET
    picture: Optional[str] = UNSET


@strawberry.input
class UpdatePresenceInput:
    is_interested: Optional[bool] = UNSET
    is_confirmed: Optional[bool] = UNSET


@strawberry.input
class UpdateCommentInput:
    body: Optional[str] = UNSET
