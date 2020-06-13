from django import forms

# User defined forms here


class CreateBookForm(forms.Form):
    name = forms.CharField(max_length=500, required=True)
    year = forms.CharField(
        widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
    author = forms.CharField(max_length=200, required=True)
    genre = forms.CharField(max_length=100, required=True)
    isbn = forms.CharField(max_length=25, required=True)

    def clean(self):
        book = super().clean()
        self.book = book

        return book
