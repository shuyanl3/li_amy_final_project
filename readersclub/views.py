from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http.response import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .utils import PageLinksMixin

from .models import Book, Author, Review, CustomUser


class BookList(PageLinksMixin, ListView):
    paginate_by = 25
    model = Book


class BookDetail(View):
    page_kwarg = 'page'
    paginate_by = 1
    template_name = 'readersclub/book_detail.html'

    def get(self, request, pk):
        book = get_object_or_404(
            Book,
            pk=pk
        )
        review_list = book.reviews.all()

        paginator = Paginator(
            review_list,
            self.paginate_by
        )
        page_number = request.GET.get(
            self.page_kwarg
        )
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(
                paginator.num_pages()
            )
        first_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=1
            )
        last_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=paginator.num_pages
            )
        if page.has_previous():
            prev_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=page.previous_page_number()
            )
        else:
            prev_url = None
        if page.has_next():
            next_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=page.next_page_number()
            )
        else:
            next_url = None
        context = {
            'is_paginated':
                page.has_other_pages(),
            'first_page_url': first_url,
            'last_page_url': last_url,
            'next_page_url': next_url,
            'paginator': paginator,
            'previous_page_url': prev_url,
            'book': book,
            'review_list': page,
        }

        return render(
            request,
            self.template_name,
            context
        )


class AuthorList(PageLinksMixin, ListView):
    paginate_by = 25
    model = Author


class AuthorDetail(View):

    def get(self, request, pk):
        author = get_object_or_404(
            Author,
            pk=pk
        )
        works = author.books.all()
        return render(
            request,
            'readersclub/author_detail.html',
            {'author': author,
             'works': works}
        )



