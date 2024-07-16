from django import forms
from .models import Content
from django.core.exceptions import ValidationError

def validate_min_max_choices(value):
    if len(value) < 3 or len(value) > 3:
        raise ValidationError('You must select exactly 3 languages.')

languages = [
    ("English", "English"),
    ("Hindi", "Hindi"),
    ("Gujarati", "Gujarati"),
    ("Tamil", "Tamil"),
    ("Italian", "Italian"),
    ("German", "German"),
]

preferences = [
('Comedy', 'Comedy'),('Action', 'Action'), ('Crime', 'Crime'), ('Romance', 'Romance'), ('Adventure', 'Adventure'), ('Drama', 'Drama'), 
('Fantasy', 'Fantasy'), ('History', 'History'),('War', 'War'), ('Horror', 'Horror'), ('Mystery', 'Mystery'), ('Thriller', 'Thriller'), 
('Sci-Fi', 'Sci-Fi'), ('Family', 'Family'), ('Documentary', 'Documentary'), ('Western', 'Western'), ('Sport', 'Sport'),
('Biography', 'Biography'),('Animation', 'Animation')]

# creating a form
class InitialSelectionForm(forms.Form):

    languages = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox' }),
        choices=languages
    )

    genres = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        choices=preferences
    )



class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = '__all__'