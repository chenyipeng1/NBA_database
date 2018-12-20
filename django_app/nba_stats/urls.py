from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('players/', views.PlayerListView.as_view(), name='players'),    
    path('players/<int:pk>', views.PlayerDetailView.as_view(), name='player_detail'),
    path('teams/', views.TeamListView.as_view(), name='teams'),    
    path('teams/<int:pk>', views.TeamDetailView.as_view(), name='team_detail'),
	path('players/new/', views.PlayerCreateView.as_view(), name='player_new'),
	path('players/<int:pk>/delete/', views.PlayerDeleteView.as_view(), name='player_delete'),
	path('players/<int:pk>/update/', views.PlayerUpdateView.as_view(), name='player_update'),
	path('players/filter', views.PlayerFilterView.as_view(), name='filter'),
]