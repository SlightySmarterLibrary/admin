from django.urls import path, re_path
from .views.books import browse, index, CreateBook

urlpatterns = (
    path('', index, name='index'),
    re_path(r'^books/$', browse, name='book_index'),
    path('books/create', CreateBook.as_view(), name="create_book")
)
