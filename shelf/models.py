from django.db import models
from django.utils.html import mark_safe
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms import ModelForm


class Game(models.Model):
    """ Game model that contains the generic information of the game """
    # Fields
    name = models.CharField(max_length=200)

    platform_choices = [
        ('PS4', 'Playstation 4'),
        ('PS3', 'Playstation 3'),
        ('PS2', 'Playstation 2'),
        ('PSX', 'Playstation'),
        ('PSVITA', 'PS VITA'),
        ('PSVR', 'Playstation VR'),
    ]
    platform = models.CharField(max_length=50, choices=platform_choices, default='PS4')
    
    genre_choices = [
        ('Action', 'Action'), 
        ('Adventure','Adventure'),
        ('Arcade', 'Arcade'), 
        ('Educational', 'Educational'), 
        ('Family', 'Family'), 
        ('Fighting','Fighting'),
        ('First Person Shooter', 'First Person Shooter'), 
        ('Fitness', 'Fitness'), 
        ('Horror', 'Horror'), 
        ('Music and Rhythm', 'Music and Rhythm'),
        ('Party','Party'),
        ('Platformer','Platformer'), 
        ('Puzzle', 'Puzzle'), 
        ('Racing', 'Racing'), 
        ('RPG', 'Role Playing Game (RPG)'), 
        ('Shooter','Shooter'),
        ('Simulation', 'Simulation'), 
        ('Sports', 'Sports'), 
        ('Strategy', 'Strategy'),
    ]
    genre = models.CharField(max_length=50, choices=genre_choices, default='Action')
    release_date = models.DateField()
    
    num_of_players_choice = [
        ('1','1'),
        ('2','1-2'),
        ('3','1-3'),
        ('4','1-4'),
    ]
    num_of_players = models.CharField(max_length=2, choices=num_of_players_choice, default = '1')
    
    # Foreign Key because games only have one publisher, but publishers can release multiple games
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL, null=True)
    box_art = models.ImageField(upload_to='boxart/')
    
    # Current User association
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamp auditory
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Get ID to use as URL to access a detail record of a game."""
        return reverse('game-detail', args=[str(self.id)])


class Publisher(models.Model):
    """Publisher model"""
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
    
    def get_absolute_url(self):
        return reverse('publisher-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name}'