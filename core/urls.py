from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from books.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("books.urls")),
]
