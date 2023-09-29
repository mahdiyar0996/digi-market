from django import forms
from .models import Product, ProductComment


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['comment', 'rating']

    def clean_rating(self):
        rating = self.cleaned_data.get(['rating'], None)
        if any([rating > 5, rating < 0, isinstance(rating, int)]):
            raise forms.ValidationError
        return rating
