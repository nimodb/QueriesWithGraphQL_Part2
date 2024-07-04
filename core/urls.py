from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("", include("books.urls")),
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),
]
