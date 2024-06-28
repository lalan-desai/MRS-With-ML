from django import forms

from django.core.exceptions import ValidationError

def validate_min_max_choices(value):
    if len(value) < 3 or len(value) > 3:
        raise ValidationError('You must select exactly 3 languages.')

languages = [
    ("English", "English"),
    ("Tamil", "Tamil"),
    ("Italian", "Italian"),
    ("German", "German"),
    ("Hindi", "Hindi"),
    ("Gujarati", "Gujarati"),
]

preferences = [('Adventure', 'Adventure'), ('Drama', 'Drama'), ('Fantasy', 'Fantasy'), ('History', 'History'),
 ('Comedy', 'Comedy'), ('War', 'War'), ('Action', 'Action'), ('Crime', 'Crime'), ('Romance', 'Romance'),
 ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Thriller', 'Thriller'), ('Sci-Fi', 'Sci-Fi'),
 ('Family', 'Family'), ('Documentary', 'Documentary'), ('Western', 'Western'), ('Sport', 'Sport'),
 ('Music', 'Music'), ('Musical', 'Musical'), ('Film-Noir', 'Film-Noir'), ('Biography', 'Biography'),
 ('Short', 'Short'), ('Animation', 'Animation'), ('Adult', 'Adult'), ('News', 'News')]

# creating a form
class InitialSelectionForm(forms.Form):

    languages = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        choices=languages
    )

    genres = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        choices=preferences
    )
