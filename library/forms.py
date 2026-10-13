from django.forms import ModelForm
from .models import Book,Reviews

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title','author','description','category']

class ReviewsForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ['body','rating']