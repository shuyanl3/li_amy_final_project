from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.http.response import HttpResponse
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .utils import PageLinksMixin

from .models import Book, Author, Review
from .forms import ReviewForm, BookForm, AuthorForm


def UserSignup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            group = Group.objects.get(name='rc_user')
            user.groups.add(group)
            return redirect('login_urlpattern')
    else:
        form = UserCreationForm()
    return render(request, 'readersclub/signup.html', {'form': form})


class BookList(PageLinksMixin, ListView):
    template_name = 'readersclub/book_list.html'
    paginate_by = 20
    model = Book

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(Q(title__icontains=query))
        else:
            return Book.objects.all()


# def search_book(request):
#     template_name = 'readersclub/book_list.html'
#     query = request.GET['q']
#     if query:
#         results = Book.objects.filter(Q(title__icontains=query))
#     else:
#         results = Book.objects.all()
#     context = {'results': results}
#
#     return render(request, template_name, context)


class BookDetail(View):
    page_kwarg = 'page'
    paginate_by = 10
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


class BookCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'readersclub.add_book'
    form_class = BookForm
    model = Book


class BookUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'readersclub.change_book'
    form_class = BookForm
    model = Book
    template_name = 'readersclub/book_form_update.html'


class BookDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'readersclub.delete_book'
    model = Book

    def get(self, request, pk):
        book = self.get_object(pk)
        return render(
            request,
            'readersclub/book_confirm_delete.html',
            {'book': book}
        )

    def get_object(self, pk):
        return get_object_or_404(
            Book,
            pk=pk
        )

    def post(self, request, pk):
        book = self.get_object(pk)
        book.delete()
        return redirect('readersclub_book_list_urlpattern')


def add_review_to_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.author = request.user
            review.save()
            return redirect('readersclub_book_detail_urlpattern', pk=book.pk)
    else:
        form = ReviewForm()
    return render(request, 'readersclub/review_form.html', {'form': form})


class ReviewList(LoginRequiredMixin, PermissionRequiredMixin, PageLinksMixin, ListView):
    permission_required = 'readersclub.delete_book'
    template_name = 'readersclub/review_list.html'
    model = Review

    def get_queryset(self):
        query = self.kwargs['pk']
        if query is None:
            return None
        query2 = self.request.GET.get('q')
        reviews = Review.objects.filter(book=query).order_by('-published_date')
        if query2:
            try:
                float(query2)
            except ValueError:
                return reviews.filter(Q(author__username__icontains=query2) |
                                      Q(text__icontains=query2)).order_by('-published_date')
            return reviews.filter(rate__range=(float(query2) - 0.05, float(query2) + 0.05)).order_by('-published_date')
        else:
            return reviews.order_by('-published_date')


class ReviewDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'readersclub.delete_book'
    model = Review

    def get_success_url(self):
        review_list = self.kwargs['pk']
        return reverse_lazy('readersclub_review_list_urlpattern', kwargs={'pk': review_list})


# class ReviewCreate(CreateView):
#     permission_required = 'readersclub.add_review'
#     form_class = ReviewForm
#     model = Review
#     template_name = 'readersclub/review_form.html'
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         form.instance.book_id = self.kwargs.get['pk']
#         return super(ReviewCreate, self).form_valid(form)
#
#     def get_success_url(self):
#         return redirect(reverse('readersclub_book_detail_urlpattern', kwargs={'pk': self.kwargs.get['pk']}))


class AuthorList(PageLinksMixin, ListView):
    paginate_by = 25
    model = Author

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Author.objects.filter(Q(first_name__icontains=query) |
                                         Q(last_name__icontains=query) |
                                         Q(pseudonym__icontains=query))
        else:
            return Author.objects.all()


class AuthorDetail(View):
    page_kwarg = 'page'
    paginate_by = 20
    template_name = 'readersclub/author_detail.html'

    def get(self, request, pk):
        author = get_object_or_404(
            Author,
            pk=pk
        )
        works = author.books.all()

        paginator = Paginator(
            works,
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
            'author': author,
            'works': page,
        }

        return render(
            request,
            self.template_name,
            context
        )


class AuthorCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'readersclub.add_author'
    form_class = AuthorForm
    model = Author


class AuthorUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'readersclub.change_author'
    form_class = AuthorForm
    model = Author
    template_name = 'readersclub/author_form_update.html'


class AuthorDelete(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'readersclub.delete_author'
    model = Author

    def get(self, request, pk):
        author = self.get_object(pk)
        works = author.books.all()
        if works.count() > 0:
            return render(
                request,
                'readersclub/author_refuse_delete.html',
                {'author': author,
                 'works': works,
                 }
            )

        else:
            return render(
                request,
                'readersclub/author_confirm_delete.html',
                {'author': author}
            )

    def get_object(self, pk):
        return get_object_or_404(
            Author,
            pk=pk
        )

    def post(self, request, pk):
        author = self.get_object(pk)
        author.delete()
        return redirect('readersclub_author_list_urlpattern')


