from django import forms
from .models import Game

class GameForm(forms.ModelForm):

    class Meta:
        model = Game
        fields = ('name', 'platform', 'genre', 'release_date', 'num_of_players', 'publisher', 'box_art')
        