from django import forms
from .models import Review, Book, Author


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'rate')

    def clean_text(self):
        return self.cleaned_data['text'].strip()


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

    def clean_title(self):
        return self.cleaned_data['title'].strip()

    def clean_publisher(self):
        return self.cleaned_data['publisher'].strip()


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

    def clean_last_name(self):
        return self.cleaned_data['last_name'].strip()

    def clean_first_name(self):
        return self.cleaned_data['first_name'].strip()

    def clean_pseudonym(self):
        return self.cleaned_data['pseudonym'].strip()
