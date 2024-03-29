from django.urls import path, re_path
from .views.books import browse, index, CreateBook, EditBook
from .views.pages import home

urlpatterns = (
    path('', home, name='index'),
    re_path(r'^books/$', index, name='book_index'),
    path('books/<slug:id>/edit', EditBook.as_view(), name="edit_book"),
    path('books/create', CreateBook.as_view(), name="create_book")
)
