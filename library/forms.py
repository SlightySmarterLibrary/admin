from django import forms

# User defined forms here


class CreateBookForm(forms.Form):
    name = forms.CharField(max_length=500, required=True)
    year = forms.CharField(
        widget=forms.widgets.DateTimeInput(attrs={"type": "date"}))
    author = forms.CharField(max_length=200)

    def clean(self):
        book = super().clean()
        self.book = book

        return book
