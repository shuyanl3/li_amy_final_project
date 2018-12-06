from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    pseudonym = models.CharField(max_length=200)
    introduction = models.CharField(max_length=5000)
    awards = models.CharField(max_length=500)

    def __str__(self):
        return '%s, %s (%s)' % (self.last_name, self.first_name, self.pseudonym)

    def get_absolute_url(self):
        return reverse('readersclub_author_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('readersclub_author_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('readersclub_author_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.PROTECT)
    introduction = models.CharField(max_length=10000)
    rate = models.FloatField()
    publisher = models.CharField(max_length=300)
    genre = models.CharField(max_length=200)

    def __str__(self):
        return '%s' % self.title

    def get_absolute_url(self):
        return reverse('readersclub_book_detail_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_update_url(self):
        return reverse('readersclub_book_update_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    def get_delete_url(self):
        return reverse('readersclub_book_delete_urlpattern',
                       kwargs={'pk': self.pk}
                       )

    class Meta:
        ordering = ['title']


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey('auth.User', related_name='reviews', on_delete=models.CASCADE, blank=True)
    text = models.CharField(max_length=2000)
    rate = models.FloatField()

    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return '%s: %s' % (self.author, self.book)




