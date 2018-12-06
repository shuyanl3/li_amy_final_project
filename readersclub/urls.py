from django.urls import path
from django.conf.urls import include, url
from readersclub.views import AuthorDetail, AuthorList, BookList, BookDetail, BookCreate, BookUpdate, \
    BookDelete, AuthorCreate, AuthorUpdate, AuthorDelete
from . import views

urlpatterns = [
    path('book/',
         BookList.as_view(),
         name='readersclub_book_list_urlpattern'),

    path('book/<int:pk>/',
         BookDetail.as_view(),
         name='readersclub_book_detail_urlpattern'),

    path('book/create/',
         BookCreate.as_view(),
         name='readersclub_book_create_urlpattern'),

    path('book/<int:pk>/update/',
         BookUpdate.as_view(),
         name='readersclub_book_update_urlpattern'),

    path('book/<int:pk>/delete/',
         BookDelete.as_view(),
         name='readersclub_book_delete_urlpattern'),

    path('book/<int:pk>/addreview/',
         views.add_review_to_book,
         name='readersclub_review_create_urlpattern'),

    path('author/',
         AuthorList.as_view(),
         name='readersclub_author_list_urlpattern'),

    path('author/<int:pk>/',
         AuthorDetail.as_view(),
         name='readersclub_author_detail_urlpattern'
         ),

    path('author/create/',
         AuthorCreate.as_view(),
         name='readersclub_author_create_urlpattern'),

    path('author/<int:pk>/update/',
         AuthorUpdate.as_view(),
         name='readersclub_author_update_urlpattern'),

    path('author/<int:pk>/delete/',
         AuthorDelete.as_view(),
         name='readersclub_author_delete_urlpattern'),
    ]
