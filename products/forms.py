from django import forms
from .models import Product, ProductComment


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['comment', 'rating']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating', None)
        if any([rating > 5, rating < 0, not isinstance(rating, int)]):
            raise forms.ValidationError('مقدار وارد شده معتبر نمیباشد')
        return rating

    def clean_comment(self):
        comment = self.cleaned_data.get('comment', None)
        if not comment:
            raise forms.ValidationError('باید دیدگاهی وارد کنید')
        return comment