from django.urls import path
from readersclub.views import AuthorDetail, AuthorList, BookList, BookDetail

urlpatterns = [
    path('book/',
         BookList.as_view(),
         name='readersclub_book_list_urlpattern'),

    path('book/<int:pk>/',
         BookDetail.as_view(),
         name='readersclub_book_detail_urlpattern'),
    path('author/',
         AuthorList.as_view(),
         name='readersclub_author_list_urlpattern'),
    path('author/<int:pk>/',
         AuthorDetail.as_view(),
         name='readersclub_author_detail_urlpattern'
         ),
    ]
