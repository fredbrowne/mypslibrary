from django.contrib import admin
from .models import Game, Publisher

admin.site.register(Publisher)

fields = ( 'image_tag' )
readonly_fields = ('image_tag')


@admin.register(Game)
class GamesAdmin(admin.ModelAdmin):
    list_display = ('name','genre', 'owner', 'publisher','num_of_players', 'release_date')
    list_filter = ('genre', 'release_date')