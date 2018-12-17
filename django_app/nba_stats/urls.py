from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('players/', views.PlayerListView.as_view(), name='players'),    
    path('players/<int:pk>', views.PlayerDetailView.as_view(), name='player_detail'),
]