from back.events.models import Comment
from typing import List
import strawberry
from typing import List

from . import resolvers
from .types import Presence, User, Event
from .permissions import IsAuthenticated, IsOwner


@strawberry.type
class Query:
    csrf: str = strawberry.field(resolver=resolvers.csrf)
    me: User = strawberry.field(
        resolver=resolvers.me, permission_classes=[IsAuthenticated]
    )
    user: User = strawberry.field(resolver=resolvers.user)
    users: List[User] = strawberry.field(resolver=resolvers.users)
    event: Event = strawberry.field(resolver=resolvers.event)
    events: List[Event] = strawberry.field(resolver=resolvers.events)


@strawberry.type
class Mutation:
    login: User = strawberry.mutation(resolver=resolvers.login)
    logout = strawberry.mutation(resolver=resolvers.logout)

    create_user: User = strawberry.mutation(resolver=resolvers.create_user)
    create_event: Event = strawberry.mutation(
        resolver=resolvers.create_event, permission_classes=[IsAuthenticated]
    )
    create_presence: Presence = strawberry.mutation(
        resolver=resolvers.create_presence, permission_classes=[IsAuthenticated]
    )
    create_comment: Comment = strawberry.mutation(
        resolver=resolvers.create_comment, permission_classes=[IsAuthenticated]
    )

    update_me: User = strawberry.mutation(
        resolver=resolvers.update_me, permission_classes=[IsAuthenticated]
    )
    update_event: Event = strawberry.mutation(
        resolver=resolvers.update_event, permission_classes=[IsOwner]
    )
    update_presence: Presence = strawberry.mutation(
        resolver=resolvers.update_presence, permission_classes=[IsOwner]
    )
    update_comment: Comment = strawberry.mutation(
        resolver=resolvers.update_comment, permission_classes=[IsOwner]
    )


schema = strawberry.Schema(query=Query, mutation=Mutation)
