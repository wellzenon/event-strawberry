from django.contrib import admin
from django.urls import path
from strawberry.django.views import GraphQLView, AsyncGraphQLView

from .events.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", AsyncGraphQLView.as_view(schema=schema)),
    path("graphql/sync/", GraphQLView.as_view(schema=schema)),
]
