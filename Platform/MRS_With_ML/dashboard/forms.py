from django import forms

languages = [
    ("English", "English"),
    ("Hindi", "Hindi"),
    ("Gujarati", "Gujarati"),
]

preferences = [
    ("Action", "Action"),
    ("Comedy", "Comedy"),
    ("Thriller", "Thriller"),
    ("Adventure", "Adventure"),
    ("Fantasy", "Fantasy"),
    ("Romance", "Romance"),
    ("Drama", "Drama"),
]

# creating a form
class InitialSelectionForm(forms.Form):

    languages = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=languages
    )

    genres = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=preferences
    )
