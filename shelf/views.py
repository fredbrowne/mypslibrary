from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from shelf.models import Game, Publisher
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import GameForm
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

def index(request):
    """Main page of the website"""

    # Count all objects
    if request.user.is_authenticated:
        num_games = Game.objects.filter(owner=request.user).count() 
    else: 
        num_games = Game.objects.all().count() 

    num_publishers = Publisher.objects.all().count()
    
    if request.user.is_authenticated:
        # Get last game added by user
        last_game = Game.objects.filter(owner=request.user).last()
    else:
        last_game = 'None'

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_games': num_games,
        'num_publishers': num_publishers,
        'num_visits': num_visits,
        'last_game': last_game,
    }

    # Render the index.html file and render context variable as parameters
    return render(request, 'index.html', context=context)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

class GameListView(generic.ListView):
    model = Game 
    paginate_by = 10

@login_required(login_url='/myaccount/login/')
def GameListUser(request):
    if request.user.is_authenticated:
        game_list = Game.objects.filter(owner=request.user).order_by('name') 
    else:
        game_list = ''
    
    context = {
        'game_list': game_list,
    }

    return render(request, 'game_list.html', context=context)

class GameDetailView(LoginRequiredMixin,generic.DetailView):
    model = Game


class MyGamesUserListView(LoginRequiredMixin,generic.ListView):
    """Class-based view to display only games assigned to current user."""
    model = Game
    template_name ='shelf/my_games.html'
    paginate_by = 10
    
    def get_queryset(self):
        return Game.objects.filter(owner=self.request.user).order_by('name')

@login_required(login_url='/myaccount/login/')
def game_new(request):
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES or None)
        if form.is_valid():
            game = form.save(commit=False)
            game.created_at = timezone.now()
            game.updated_at = timezone.now()
            game.owner = request.user
            game.save()
            return redirect('game-detail', pk=game.pk)
        else: 
            print(form.errors)
    else:
        form = GameForm()
    return render(request, 'game_edit.html', {'form': form})

@login_required(login_url='/myaccount/login/')
def game_edit(request, pk):
     game = get_object_or_404(Game, pk=pk)
     if request.method == "POST":
         form = GameForm(request.POST, request.FILES or None, instance=game)
         if form.is_valid():
             game_image = game.box_art
             game = form.save(commit=False)
             game.owner = request.user
             game.updated_at = timezone.now()
             game.save()
             return redirect('game-detail', pk=game.pk)
     else:
         form = GameForm(instance=game)
     return render(request, 'game_edit.html', {'form': form})