from django.urls import path, include
from shelf import views



urlpatterns = [
    # Default Page
    path('', views.index, name='index'),
    # Login/Signup
    path('myaccount/', include('django.contrib.auth.urls'), name='account'), 
    path('myaccount/signup/', views.signup, name='signup'),
    # Game Views
    path('games/', views.GameListUser, name= 'games'),
    path('games/<int:pk>', views.GameDetailView.as_view(), name='game-detail'),
    # Add or Edit Games
    path('games/new/', views.game_new, name='game_new'),
    path('games/<int:pk>/edit/', views.game_edit, name='game_edit'),
    path('mygames/', views.MyGamesUserListView.as_view(), name='my_games'),
]
