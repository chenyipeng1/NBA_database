from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Player
# Create your views here.


def index(request):
   return HttpResponse("You are going to look through NBA history stats database")


class AboutPageView(generic.TemplateView):
	template_name = 'nba_stats/about.html'


class HomePageView(generic.TemplateView):
	template_name = 'nba_stats/home.html'

class PlayerListView(generic.TemplateView):
	model = Player
	context_object_name = 'players'
	template_name = 'nba_stats/player.html'
	paginate_by = 50	

	def get_queryset(self):
		return Player.objects.all().order_by('player_name')

class PlayerDetailView(generic.TemplateView):
	model = Player
	context_object_name = 'player'
	template_name = 'nba_stats/player_detail.html'