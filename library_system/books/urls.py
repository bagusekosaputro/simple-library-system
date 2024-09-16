from django.urls import path
from library_system.books import views


urlpatterns = [
    path("books/", views.BookList.as_view())
]